#!/usr/bin/env python3
"""
analyse.py — step 1 and 2 of the clipping pipeline.

Takes a source video from input/raw/, transcribes it with Whisper, then scores
every plausible 30-59 second window for hook strength, retention and ending
quality. Writes a transcript + analysis JSON to output/metadata/ and a run log
to logs/runs/. Cuts nothing — selection and confirmation stay with the agent.

Usage:
    python3 scripts/analyse.py my-video.mp4
    python3 scripts/analyse.py my-video.mp4 --model small --top 5
    python3 scripts/analyse.py my-video.mp4 --transcript output/metadata/my-video.transcript.json
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAIGN_DIR = os.path.join(ROOT, "campaigns")
LOG_DIR = os.path.join(ROOT, "logs", "runs")

# Duration rules from CLAUDE.md
MIN_DURATION = 30.0
TARGET_MAX = 55.0
HARD_MAX = 59.0

# Windows this close together are treated as the same moment.
OVERLAP_TOLERANCE = 0.5

FILLER_WORDS = {
    "um", "uh", "erm", "ah", "eh", "hmm", "mmm", "like", "so", "basically",
    "actually", "literally", "obviously", "anyway", "kinda", "sorta",
    "yknow", "y'know", "right", "okay", "ok", "well", "just", "really",
}

# Words that signal a bold claim, curiosity gap or controversy in a hook.
HOOK_WORDS = {
    "never", "nobody", "everyone", "everybody", "always", "secret", "truth",
    "wrong", "mistake", "stop", "worst", "best", "biggest", "insane", "crazy",
    "shocking", "hate", "love", "lie", "lied", "scam", "hack", "reason",
    "why", "how", "what", "actually", "problem", "danger", "warning",
    "million", "billion", "thousand", "percent", "first", "only", "real",
    "here's", "listen", "look", "imagine", "forget", "myth", "banned",
}

# Words that signal a payoff, revelation or punchline at the end of a clip.
PAYOFF_WORDS = {
    "because", "so", "result", "point", "answer", "truth", "that's", "thats",
    "simple", "done", "over", "forever", "changed", "never", "everything",
    "difference", "matters", "works", "why", "lesson", "remember", "finally",
}

STRONG_ENDINGS = (".", "!", "?")


class AnalyseError(Exception):
    """Anything that should stop the run with a readable message."""


# ---------------------------------------------------------------------------
# External tools
# ---------------------------------------------------------------------------

def require_tool(name):
    path = shutil.which(name)
    if not path:
        raise AnalyseError(
            "%s not found on PATH. Install it with: brew install ffmpeg" % name
        )
    return path


def run(cmd):
    """Run a command, return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return proc.returncode, proc.stdout, proc.stderr


def probe_duration(video_path):
    require_tool("ffprobe")
    code, out, err = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path,
    ])
    if code != 0:
        raise AnalyseError("ffprobe failed on %s:\n%s" % (video_path, err.strip()))
    try:
        return float(out.strip())
    except ValueError:
        raise AnalyseError("Could not read duration from ffprobe output: %r" % out)


def extract_audio(video_path, wav_path):
    """16kHz mono WAV — what Whisper wants anyway."""
    require_tool("ffmpeg")
    code, _, err = run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le",
        wav_path,
    ])
    if code != 0:
        raise AnalyseError("ffmpeg audio extraction failed:\n%s" % err.strip()[-2000:])
    return wav_path


def measure_loudness(wav_path):
    """
    Mean/max volume via ffmpeg volumedetect.

    CLAUDE.md wants quiet source audio flagged for manual compression rather
    than silently exported, so this returns the numbers and a flag.
    """
    code, _, err = run([
        "ffmpeg", "-i", wav_path, "-af", "volumedetect", "-f", "null", "-",
    ])
    if code != 0:
        return {"mean_db": None, "max_db": None, "quiet": False,
                "note": "volumedetect failed; check audio manually"}

    mean = re.search(r"mean_volume:\s*(-?\d+(?:\.\d+)?) dB", err)
    peak = re.search(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", err)
    mean_db = float(mean.group(1)) if mean else None
    max_db = float(peak.group(1)) if peak else None

    # Broadcast-ish speech sits around -16 to -20 dB mean. Below -26 is thin.
    quiet = mean_db is not None and mean_db < -26.0
    note = ""
    if quiet:
        note = "Source audio is quiet (mean %.1f dB). Compress/normalise before export." % mean_db
    elif max_db is not None and max_db > -0.5:
        note = "Peaks near 0 dB (%.1f) — check for clipping." % max_db

    return {"mean_db": mean_db, "max_db": max_db, "quiet": quiet, "note": note}


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------

def transcribe(wav_path, model_name, language=None):
    """
    Try faster-whisper first (much quicker on CPU), fall back to openai-whisper.
    Returns a list of {start, end, text} segments.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        pass
    else:
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        segments, _info = model.transcribe(
            wav_path, language=language, vad_filter=True, word_timestamps=False
        )
        return [
            {"start": float(s.start), "end": float(s.end), "text": s.text.strip()}
            for s in segments
            if s.text and s.text.strip()
        ]

    try:
        import whisper
    except ImportError:
        raise AnalyseError(
            "No Whisper install found. Install one of:\n"
            "  pip3 install faster-whisper      (recommended, faster on CPU)\n"
            "  pip3 install openai-whisper"
        )

    model = whisper.load_model(model_name)
    result = model.transcribe(wav_path, language=language, verbose=False)
    return [
        {"start": float(s["start"]), "end": float(s["end"]), "text": s["text"].strip()}
        for s in result.get("segments", [])
        if s.get("text", "").strip()
    ]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def words_of(text):
    return re.findall(r"[a-z']+", text.lower())


def clamp(value, low=0.0, high=10.0):
    return max(low, min(high, value))


def score_hook(segments, window_start, hook_window=3.0):
    """
    Hook quality for the opening seconds, per CLAUDE.md.
    Rewards questions, numbers, second person, bold/controversial words and
    starting mid-sentence. Penalises filler openings and slow intros.

    Campaigns set their own hook window — Boxabl demands 2s, not 3 — so this is
    a parameter rather than a constant. See knowledge/campaign-boxabl.md.
    """
    cutoff = window_start + hook_window
    opening = " ".join(
        s["text"] for s in segments
        if s["start"] < cutoff and s["end"] > window_start
    ).strip()

    if not opening:
        return 0.0, ["No speech in the first %.0f seconds — dead-air opening" % hook_window]

    words = words_of(opening)
    reasons = []
    score = 4.0  # neutral talking-head opener

    hits = [w for w in words if w in HOOK_WORDS]
    if hits:
        score += min(2.5, 0.7 * len(set(hits)))
        reasons.append("Bold/curiosity words: %s" % ", ".join(sorted(set(hits))[:4]))

    if "?" in opening:
        score += 1.2
        reasons.append("Opens on a question (curiosity gap)")

    if re.search(r"\d", opening):
        score += 0.8
        reasons.append("Contains a number/specific")

    if any(w in ("you", "your", "you're", "youre") for w in words):
        score += 0.8
        reasons.append("Speaks directly to the viewer")

    # Mid-sentence starts are good: lowercase first word, or a conjunction.
    first = words[0] if words else ""
    if first in ("and", "but", "so", "because", "then", "which", "that"):
        score += 0.5
        reasons.append("Starts mid-thought")
    elif opening[0].islower():
        score += 0.3
        reasons.append("Starts mid-sentence")

    lead_filler = 0
    for w in words[:4]:
        if w in FILLER_WORDS:
            lead_filler += 1
        else:
            break
    if lead_filler:
        score -= 1.0 * lead_filler
        reasons.append("Opens on filler (%d words) — trim the start" % lead_filler)

    # A slow opener says very little in the hook window.
    if len(words) < max(3, int(2 * hook_window)):
        score -= 1.0
        reasons.append("Only %d words in the first %.0fs — slow intro"
                       % (len(words), hook_window))

    return clamp(score), reasons


def score_retention(segments, start, end):
    """
    Retention arc: pace, dead air and filler density across the window.
    CLAUDE.md wants a micro-hook every 3-5 seconds, so long silent stretches
    and filler-heavy talking are the things to punish.
    """
    duration = end - start
    inside = [s for s in segments if s["end"] > start and s["start"] < end]
    text = " ".join(s["text"] for s in inside)
    words = words_of(text)
    reasons = []

    if not words:
        return 0.0, ["No speech in window"], {"wps": 0.0, "filler_ratio": 0.0,
                                              "longest_gap": duration}

    wps = len(words) / duration
    score = 5.0

    # Engaging short-form speech runs roughly 2.3-3.5 words/sec.
    if 2.3 <= wps <= 3.6:
        score += 1.8
        reasons.append("Good pace (%.1f words/sec)" % wps)
    elif wps < 1.7:
        score -= 2.0
        reasons.append("Slow delivery (%.1f words/sec) — likely drags" % wps)
    elif wps < 2.3:
        score -= 0.6
        reasons.append("Slightly slow (%.1f words/sec)" % wps)
    else:
        score += 0.6
        reasons.append("Fast delivery (%.1f words/sec)" % wps)

    # Dead air: gaps between consecutive segments inside the window.
    gaps = []
    cursor = start
    for s in sorted(inside, key=lambda x: x["start"]):
        gap = s["start"] - cursor
        if gap > 0:
            gaps.append(gap)
        cursor = max(cursor, s["end"])
    if end - cursor > 0:
        gaps.append(end - cursor)

    longest_gap = max(gaps) if gaps else 0.0
    total_silence = sum(gaps)
    if longest_gap > 2.5:
        score -= 2.0
        reasons.append("Dead air of %.1fs — cut it or skip this window" % longest_gap)
    elif longest_gap > 1.5:
        score -= 0.8
        reasons.append("Pause of %.1fs" % longest_gap)
    if total_silence / duration > 0.25:
        score -= 1.0
        reasons.append("%.0f%% of the window is silence" % (100 * total_silence / duration))

    filler_count = sum(1 for w in words if w in FILLER_WORDS)
    filler_ratio = filler_count / len(words)
    if filler_ratio > 0.12:
        score -= 2.0
        reasons.append("Heavy filler (%.0f%% of words) — needs tightening" % (100 * filler_ratio))
    elif filler_ratio > 0.07:
        score -= 0.8
        reasons.append("Some filler (%.0f%%)" % (100 * filler_ratio))

    # Tension -> release -> new tension: proxy on how evenly sentences land.
    sentence_ends = len(re.findall(r"[.!?]", text))
    if sentence_ends >= duration / 8.0:
        score += 0.8
        reasons.append("Multiple beats (%d sentences)" % sentence_ends)
    elif sentence_ends <= 1:
        score -= 0.8
        reasons.append("One long unbroken thought — few micro-hooks")

    stats = {"wps": round(wps, 2), "filler_ratio": round(filler_ratio, 3),
             "longest_gap": round(longest_gap, 2)}
    return clamp(score), reasons, stats


def score_ending(segments, end):
    """
    Ending quality. CLAUDE.md: must land on a punchline, revelation,
    cliffhanger or strong statement — never trail off.
    """
    window_from = end - 6.0
    tail = " ".join(
        s["text"] for s in segments
        if s["end"] > window_from and s["start"] < end
    ).strip()

    if not tail:
        return 0.0, ["Nothing said in the last 6 seconds"]

    reasons = []
    score = 4.0
    words = words_of(tail)

    if tail.endswith(STRONG_ENDINGS):
        score += 2.0
        reasons.append("Lands on a complete sentence")
    elif tail.endswith(","):
        score -= 1.5
        reasons.append("Cuts mid-clause — move the out point")
    else:
        score -= 1.0
        reasons.append("Trails off without closing the thought")

    if tail.endswith("?"):
        score += 0.8
        reasons.append("Ends on a question (cliffhanger)")
    if tail.endswith("!"):
        score += 0.5
        reasons.append("Ends emphatically")

    payoff = [w for w in words[-14:] if w in PAYOFF_WORDS]
    if payoff:
        score += min(1.5, 0.6 * len(set(payoff)))
        reasons.append("Payoff language: %s" % ", ".join(sorted(set(payoff))[:3]))

    if words and words[-1] in FILLER_WORDS:
        score -= 1.5
        reasons.append("Final word is filler (%r)" % words[-1])

    return clamp(score), reasons


def build_windows(segments, source_duration):
    """
    Candidate windows anchored on natural sentence starts. Each start extends
    to the segment boundary that gets closest to the 30-55s target without
    breaking the 59s hard cap.
    """
    windows = []
    ordered = sorted(segments, key=lambda s: s["start"])

    for i, seg in enumerate(ordered):
        start = seg["start"]
        if source_duration - start < MIN_DURATION:
            break

        best = None
        for j in range(i, len(ordered)):
            end = ordered[j]["end"]
            duration = end - start
            if duration < MIN_DURATION:
                continue
            if duration > HARD_MAX:
                break
            # Prefer landing inside the 30-55s target band.
            penalty = 0.0 if duration <= TARGET_MAX else (duration - TARGET_MAX)
            if best is None or penalty < best[0]:
                best = (penalty, end, j)

        if best is not None:
            windows.append({"start": round(start, 2), "end": round(best[1], 2)})

    return windows


def score_window(segments, window, hook_window=3.0):
    start, end = window["start"], window["end"]
    hook, hook_reasons = score_hook(segments, start, hook_window)
    retention, retention_reasons, stats = score_retention(segments, start, end)
    ending, ending_reasons = score_ending(segments, end)

    # Hook carries short-form hardest, then the close, then the middle.
    overall = clamp(0.45 * hook + 0.30 * ending + 0.25 * retention)

    inside = [s for s in segments if s["end"] > start and s["start"] < end]
    transcript = " ".join(s["text"] for s in inside).strip()

    return {
        "start": start,
        "end": end,
        "duration": round(end - start, 2),
        "hook_score": round(hook, 1),
        "retention_score": round(retention, 1),
        "ending_score": round(ending, 1),
        "viral_score": round(overall, 1),
        "stats": stats,
        "why": {
            "hook": hook_reasons,
            "retention": retention_reasons,
            "ending": ending_reasons,
        },
        "transcript": transcript,
    }


def dedupe(scored, top_n):
    """Keep the best window per moment — no near-identical overlapping picks."""
    picked = []
    for cand in sorted(scored, key=lambda c: -c["viral_score"]):
        if all(
            cand["end"] <= p["start"] + OVERLAP_TOLERANCE
            or cand["start"] >= p["end"] - OVERLAP_TOLERANCE
            for p in picked
        ):
            picked.append(cand)
        if len(picked) >= top_n:
            break
    return sorted(picked, key=lambda c: c["start"])


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def timecode(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    frac = int(round((seconds - int(seconds)) * 100))
    if h:
        return "%d:%02d:%02d.%02d" % (h, m, s, frac)
    return "%02d:%02d.%02d" % (m, s, frac)


def print_report(result):
    src = result["source"]
    print()
    print("=" * 72)
    print("ANALYSIS — %s" % src["file"])
    print("Duration %s | %d transcript segments | model %s"
          % (timecode(src["duration"]), result["segment_count"], src["whisper_model"]))
    audio = result["audio"]
    if audio.get("note"):
        print("AUDIO: %s" % audio["note"])
    print("=" * 72)

    candidates = result["candidates"]
    if not candidates:
        print("\nNo windows scored 7+. Per CLAUDE.md, not forcing weak clips.")
        best = result.get("best_rejected")
        if best:
            print("Best available was %.1f/10 at %s-%s."
                  % (best["viral_score"], timecode(best["start"]), timecode(best["end"])))
        return

    for n, c in enumerate(candidates, 1):
        print("\n--- CANDIDATE %d — viral %.1f/10 ---" % (n, c["viral_score"]))
        print("  %s → %s  (%.1fs)" % (timecode(c["start"]), timecode(c["end"]), c["duration"]))
        print("  hook %.1f | retention %.1f | ending %.1f"
              % (c["hook_score"], c["retention_score"], c["ending_score"]))
        for label in ("hook", "retention", "ending"):
            for reason in c["why"][label]:
                print("    [%s] %s" % (label, reason))
        preview = c["transcript"]
        if len(preview) > 320:
            preview = preview[:317] + "..."
        print("  transcript: %s" % preview)

    print("\n" + "=" * 72)
    print("Nothing has been cut. Approve candidates before the CUT step.")


def write_json(path, payload):
    with open(path, "w") as fh:
        json.dump(payload, fh, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_approved_sources(campaign):
    """
    Read the campaign's whitelist. Returns the set of approved filenames.

    Campaigns must never share footage — each one licenses its own source list, and
    clipping campaign A's video for campaign B gets the clip rejected at best. This
    reads campaigns/<campaign>/approved-sources.md and pulls the filename from each
    'name.mp4 | url | note' line outside comment blocks.
    """
    path = os.path.join(CAMPAIGN_DIR, campaign, "approved-sources.md")
    if not os.path.isfile(path):
        raise AnalyseError(
            "No approved-sources.md for campaign %r.\nExpected: %s\n"
            "Every campaign needs a whitelist before anything can be clipped for it."
            % (campaign, path)
        )

    approved = set()
    in_comment = False
    with open(path) as fh:
        for line in fh:
            stripped = line.strip()
            if "<!--" in stripped:
                in_comment = True
            if in_comment:
                if "-->" in stripped:
                    in_comment = False
                continue
            if not stripped or stripped.startswith(("#", "-", "*", "<")):
                continue
            if "|" not in stripped:
                continue
            candidate = stripped.split("|")[0].strip()
            # Must actually look like a media file, otherwise prose in the doc
            # (e.g. the "one entry per line, as filename.mp4 | url" example) gets
            # parsed as an approved source.
            if re.match(r"^[\w.\-]+\.(mp4|mov|mkv|webm|m4v|avi)$", candidate, re.I):
                approved.add(candidate)
    return approved


def resolve_video(name, campaign):
    """
    Resolve a source video INSIDE the campaign's own input folder only.

    Deliberately does not accept arbitrary paths — that is the whole point. A path
    outside input/raw/<campaign>/ is refused so footage cannot be crossed between
    campaigns by accident.
    """
    raw_dir = os.path.join(ROOT, "input", "raw", campaign)
    basename = os.path.basename(name)

    if basename != name:
        raise AnalyseError(
            "Pass a filename, not a path. Sources must live in input/raw/%s/ so footage "
            "cannot cross between campaigns.\nGot: %s" % (campaign, name)
        )

    candidate = os.path.join(raw_dir, basename)
    if not os.path.isfile(candidate):
        raise AnalyseError(
            "Video not found for campaign %r: %s\nExpected at: %s"
            % (campaign, basename, candidate)
        )

    approved = load_approved_sources(campaign)
    if not approved:
        raise AnalyseError(
            "The approved-sources list for %r is empty, so nothing may be clipped yet.\n"
            "Populate campaigns/%s/approved-sources.md from the campaign's official "
            "content list first.\nRefusing by default is intentional." % (campaign, campaign)
        )
    if basename not in approved:
        raise AnalyseError(
            "%s is NOT on the approved source list for campaign %r.\n"
            "Approved (%d): %s\n"
            "Only footage the campaign has licensed may be clipped for it."
            % (basename, campaign, len(approved), ", ".join(sorted(approved)[:8]))
        )

    return candidate


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Transcribe a source video and score 30-59s clip windows."
    )
    parser.add_argument("campaign",
                        help="Campaign slug, e.g. boxabl. Scopes sources and outputs.")
    parser.add_argument("video", help="Filename inside input/raw/<campaign>/")
    parser.add_argument("--model", default="base",
                        help="Whisper model: tiny, base, small, medium, large (default: base)")
    parser.add_argument("--language", default=None,
                        help="Force a language code (e.g. en) instead of auto-detect")
    parser.add_argument("--top", type=int, default=3,
                        help="How many candidates to surface (default: 3)")
    parser.add_argument("--min-score", type=float, default=7.0,
                        help="Minimum viral score to surface (default: 7.0, per CLAUDE.md)")
    parser.add_argument("--hook-window", type=float, default=3.0,
                        help="Seconds the hook is scored over (default: 3.0; Boxabl wants 2.0)")
    parser.add_argument("--transcript", default=None,
                        help="Reuse an existing transcript JSON instead of re-running Whisper")
    args = parser.parse_args(argv)

    video_path = resolve_video(args.video, args.campaign)
    stem = os.path.splitext(os.path.basename(video_path))[0]
    meta_dir = os.path.join(ROOT, "output", "metadata", args.campaign)
    os.makedirs(meta_dir, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    transcript_path = os.path.join(meta_dir, "%s.transcript.json" % stem)
    duration = None

    if args.transcript:
        with open(args.transcript) as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            segments = data["segments"]
            duration = data.get("duration")
        else:
            segments = data
        audio = {"mean_db": None, "max_db": None, "quiet": False,
                 "note": "Skipped audio check (reused transcript)"}
        print("Reusing transcript: %s" % args.transcript)
        # Only reach for ffprobe if the transcript didn't record the duration.
        if duration is None:
            duration = probe_duration(video_path)
    else:
        duration = probe_duration(video_path)
        tmp_dir = tempfile.mkdtemp(prefix="clipping-agent-")
        try:
            wav_path = os.path.join(tmp_dir, "%s.wav" % stem)
            print("Extracting audio from %s ..." % os.path.basename(video_path))
            extract_audio(video_path, wav_path)
            audio = measure_loudness(wav_path)
            print("Transcribing with Whisper (%s) — this can take a while ..." % args.model)
            segments = transcribe(wav_path, args.model, args.language)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        write_json(transcript_path, {
            "source": os.path.basename(video_path),
            "duration": round(duration, 2),
            "model": args.model,
            "segments": segments,
        })
        print("Transcript saved: %s" % os.path.relpath(transcript_path, ROOT))

    if not segments:
        raise AnalyseError("Whisper returned no speech segments — is there audio on this video?")

    if duration < MIN_DURATION:
        raise AnalyseError(
            "Source is %.1fs — shorter than the %.0fs minimum clip length."
            % (duration, MIN_DURATION)
        )

    windows = build_windows(segments, duration)
    scored = [score_window(segments, w, args.hook_window) for w in windows]
    qualifying = [c for c in scored if c["viral_score"] >= args.min_score]
    candidates = dedupe(qualifying, args.top)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "file": os.path.basename(video_path),
            "path": video_path,
            "duration": round(duration, 2),
            "whisper_model": args.model,
        },
        "audio": audio,
        "segment_count": len(segments),
        "windows_evaluated": len(scored),
        "min_score": args.min_score,
        "candidates": candidates,
    }
    if not candidates and scored:
        result["best_rejected"] = max(scored, key=lambda c: c["viral_score"])

    analysis_path = os.path.join(meta_dir, "%s.analysis.json" % stem)
    write_json(analysis_path, result)

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, "%s_%s_%s.analyse.json" % (stamp, args.campaign, stem))
    write_json(log_path, {
        "step": "analyse",
        "campaign": args.campaign,
        "source": os.path.basename(video_path),
        "generated_at": result["generated_at"],
        "windows_evaluated": len(scored),
        "candidates": [
            {k: c[k] for k in ("start", "end", "duration", "hook_score",
                               "retention_score", "ending_score", "viral_score")}
            for c in candidates
        ],
        "audio_flag": audio.get("note") or None,
        "cut": False,
    })

    print_report(result)
    print("\nAnalysis: %s" % os.path.relpath(analysis_path, ROOT))
    print("Run log:  %s" % os.path.relpath(log_path, ROOT))
    return 0 if candidates else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AnalyseError as exc:
        print("Error: %s" % exc, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
