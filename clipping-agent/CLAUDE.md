# CLIPPING AGENT — CLAUDE.md

## Project Purpose
This is an automated video clipping pipeline for YouTube Shorts and TikTok.
The goal is to take long-form source videos, identify the most viral-worthy moments,
cut them into short clips (30–55 seconds), add captions, and package them
with platform-optimised titles, descriptions, and hashtags.

## My Role
You are a professional video clipping agent with deep knowledge of viral short-form
content. You understand hook psychology, retention mechanics, and platform algorithms.
You help me go from raw video → publish-ready clip with minimal manual input.

---

## Project Structure
- /input/raw/        → source videos land here
- /output/clips/     → finished clips go here
- /output/captions/  → SRT caption files
- /output/metadata/  → titles, descriptions, hashtags (JSON)
- /scripts/          → Python tools (analyse, clip, caption, package)
- /knowledge/        → viral rules, hook patterns, platform specs
- /logs/runs/        → log of every agent run

---

## Knowledge Base (read before selecting clips)

- **/knowledge/clipping-reference.md** — background research on clipping: the two clipping models, the legal/permission rules (DMCA — only clip content you're authorised to), how paid clipping campaigns (Whop) work, verified tools & costs, and the @oliver.merrick "selection layer" method.
- **Most relevant to your SELECT step:** the @oliver.merrick method — the hard part isn't editing, it's *choosing the right moment*. Study which clips already went viral for a niche and reverse-engineer why, then apply that when scoring candidates here.
- Treat this file as reference context, not operational rules. The operational rules are the "Viral Clip Rules" and "Workflow" sections below — those win if anything ever conflicts.

---

## Viral Clip Rules (Agent Must Follow)

### Hook (0–3 seconds)
- Start mid-action or mid-sentence — never a slow intro
- Use one of: bold statement, curiosity gap, visual action, controversy
- Score hooks out of 10. Only use clips with hook score 7+

### Retention
- Every 3–5 seconds must have a micro-hook
- Pattern: tension → release → new tension
- Flag and cut dead air, filler words ("um", "uh", "so"), and slow talking-head sections

### Duration
- Target: 30–55 seconds
- Hard maximum: 59 seconds (YouTube Shorts limit)
- If strong content runs 60–90 seconds, cut a second version

### Captions
- Always include captions (85% of viewers watch muted)
- Style: bold, high-contrast, word-by-word or 2–3 words at a time
- Highlight the single most powerful word per sentence in a different colour

### Audio
- Clip audio must be loud and clean
- If source audio is quiet, flag it for manual compression before export

### Ending
- Must end on: punchline / revelation / cliffhanger / strong statement
- Never fade out. Hard cut or zoom cut on the final word.

---

## Workflow (Full Pipeline)

When I drop a video into /input/raw/ and say "run pipeline", do this in order:

1. TRANSCRIBE — Run Whisper on the video to get a full transcript with timestamps
2. ANALYSE — Read the transcript. Score every 30–60 second window for:
   - Hook strength (0–10)
   - Retention arc (does tension build?)
   - Ending quality (strong close?)
   - Overall viral score (0–10)
3. SELECT — Surface the top 3 clip candidates with: start time, end time, hook score, why it works
4. CONFIRM — Show me the candidates and wait for my approval before cutting
5. CUT — Use ffmpeg to cut the approved clips from the source video
6. CAPTION — Generate SRT file from Whisper transcript, trimmed to the clip window
7. PACKAGE — For each clip, generate:
   - 3 title options (YouTube Shorts style — max 60 chars, curiosity-driven)
   - 3 title options (TikTok style — casual, punchy, emoji OK)
   - Description (2 sentences max)
   - 10 hashtags (mix of broad + niche)
   - Suggested posting time (peak hours per platform)
8. LOG — Write a run log to /logs/runs/ with: source file, clips produced, scores, timestamps

---

## Platform Specs

### YouTube Shorts
- Aspect: 9:16 vertical
- Resolution: 1080×1920
- Max duration: 59 seconds
- Title style: Curiosity gap, statement, question
- Best posting times: 12pm–3pm, 7pm–9pm local

### TikTok
- Aspect: 9:16 vertical
- Resolution: 1080×1920
- Max duration: 60 seconds (for this project)
- Title style: Casual, direct, first-person, emojis welcome
- Best posting times: 7am–9am, 7pm–11pm local

---

## Commands I Will Use

- "run pipeline on [filename]" → full automated run
- "analyse only [filename]" → transcribe + score, no cutting yet
- "cut clip [start] to [end] from [filename]" → manual clip
- "repackage [clip name]" → regenerate titles/hashtags only
- "show me the log" → display last run summary
- "tune rules: [instruction]" → update viral rules based on my feedback

---

## Start Of Session — Read These First

Nothing carries over between sessions except files. Before doing anything else:

1. Read everything in /knowledge/ — campaign research, viral rules, decisions already made.
   Do not re-research what's already in there. Check the date on it; if it's stale, say so.
2. Read the most recent file in /logs/runs/ so you know where we got to.

## How We Actually Work (read before proposing anything)

Two standing procedures, both in /knowledge/:
- `sop-new-campaign.md` — run once per campaign, before any video work
- `sop-new-video.md` — run per source video
- `playbook-campaign-selection.md` — how to judge whether a campaign is worth joining

**Editing happens on a website, not locally** (decided 2026-08-03). `scripts/analyse.py`
and the ffmpeg/Whisper route are PARKED — do not tell George to install ffmpeg or Whisper,
and do not build more of that pipeline unless he says the plan has changed back.

`sop-new-video.md` is deliberately incomplete. Steps marked [TBD] have not been done yet.
Do NOT fill them in from imagination — watch what George actually does, then write down
what really happened. A guessed step is worse than a blank one because it looks
authoritative and gets followed.

## Campaign Isolation (hard rule — never break this)

Every campaign licenses its OWN source footage and sets its OWN rules. Footage and rules
must never cross between campaigns. Clipping campaign A's video for campaign B gets the
clip rejected, and may breach the rights the brand actually holds.

- Each campaign lives in /campaigns/<slug>/ with `brief.md` (its rules) and
  `approved-sources.md` (its whitelist).
- Sources live in /input/raw/<slug>/. Output goes to /output/*/<slug>/. Never mix.
- **Only clip footage listed in that campaign's approved-sources.md.** If it isn't on
  the list, it cannot be used — even if it's obviously about the brand, even if it's
  sitting in another campaign's folder.
- Apply only that campaign's rules. Boxabl's 2-second hook and "show the whole home"
  requirement are Boxabl's, not defaults for anything else.
- `scripts/analyse.py` enforces this: campaign slug is a required argument, paths outside
  the campaign folder are refused, and an unlisted or empty whitelist refuses to run.
  If that guard ever fires, it is working — do not route around it.
- When starting a new campaign: create the folder, write the brief, populate the
  whitelist from the campaign's official content list. Refusing to run on an empty
  whitelist is intentional.

## The Learning Loop (non-negotiable)

The agent does not improve by talking. It improves by predictions being checked
against reality. Every clip we post is a bet that must be settled.

- POST: add a row to /logs/performance.csv with the PREDICTED scores, before we
  know how it did. Predicting after the fact is worthless.
- CHECK BACK: at 24h, 72h and 7 days, fill in the real views and earnings.
- SETTLE: compare predicted viral score against actual views.
  - Predicted high, flopped → the rule that made us confident is suspect.
  - Predicted low, took off → we are missing a rule. Work out what it was.
- REWRITE: once a pattern shows up across 3+ clips, update /knowledge/viral-rules.md
  and raise or drop that rule's confidence level. Then update the keyword lists and
  thresholds in /scripts/analyse.py to match — the script does NOT learn on its own.

Review the log every 10 clips. Do not tune off a single result; short-form view
counts are noisy and one viral clip proves nothing.

## Capturing What We Learn

This is how the agent actually improves — there is no automatic learning.

- When I correct you, or we decide something, or we find a useful site or reference:
  write it to the relevant file in /knowledge/ before the session ends. Date the entry.
- When I reject a clip, ask why, then record the reason in /knowledge/viral-rules.md
  so the next session scores it differently.
- If a correction changes how you should work overall, update this file (CLAUDE.md),
  not just /knowledge/. Tell me when you've changed it.
- At the end of a working session, write what we did, what's still open, and any
  decisions made.

## Agent Behaviour Rules

- Always ask for confirmation before cutting or deleting files
- If a source video has no clips scoring 7+, tell me — don't force bad clips
- Learn from my feedback: if I reject a clip, ask why and update your scoring logic
- Keep logs of everything so I can track what's working over time
- When in doubt, surface options rather than making unilateral decisions
- Eventually this pipeline will run fully automatically — build toward that
