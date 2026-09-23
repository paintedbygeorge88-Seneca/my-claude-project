# SOP — Producing Clips From One Source Video

**STATUS: SKELETON. Being filled in as George walks each step for the first time.**

Steps marked `[TBD]` have not been done yet — do not invent them. Ask, watch what
actually happens, then write down what was really done. A guessed step is worse than a
blank one, because it looks authoritative.

Workflow decision (2026-08-03): **editing happens on a website, not locally.** The local
ffmpeg/Whisper route in `scripts/analyse.py` is PARKED and not part of this SOP.

Editing site: `[TBD — not yet chosen/named]`

---

## 1. Pick the source video
- Choose from `campaigns/<slug>/approved-sources.md` ONLY.
- Record which video and why it was picked (celebrity present? factory tour? big view
  count on the original?). The "why" is what we learn from later.

## 2. Get the video
- Boxabl's campaign recommends: `turboscribe.ai/downloader/youtube/mp4`
- `[TBD]` — where the file goes when editing happens in a browser. Local download first,
  or straight into the editing site by URL?

## 3. Find the clip moments
`[TBD]` — how candidate moments get identified in the web tool.
Whatever the method, capture per candidate: **start time, end time, and why it's good.**

Campaign rules that constrain the choice (Boxabl):
- Hook must land in **2 seconds** — strong visual or a recognisable face, no setup
- The clip must show **the whole home**, not just one feature
- "BOXABL" must be said or on screen while the home is visible
- No Kanye footage — automatic rejection

## 4. Score it BEFORE editing
Write the predicted scores into `logs/performance.csv` — hook, retention, ending, overall
— **before** you know how the clip performs. Predicting afterwards is worthless; the
whole point is catching where the rules are wrong.

## 5. Edit
`[TBD]` — the actual steps in the web tool.

Requirements that must survive editing (Boxabl):
- **"BOXABL" spelled correctly in captions** — auto-captions will produce "boxable" or
  "box able" and that is an automatic rejection. Check every single time.
- Bold captions, big text, story readable on mute
- Jump cuts and a real edit — raw rips get rejected
- No other brand watermarks, nothing political, positive framing only

## 6. Export
`[TBD]` — format, resolution, where it lands. Target 1080×1920, 9:16.

## 7. Write the post
- Caption mentioning Boxabl specifically (the Casita, foldable homes, the factory)
- `@boxabl` tag in the caption — on X, the tracking URL instead
- Hashtags `[TBD]`
- Posting time — Boxabl needs 40% Tier 1 audience (US/CAN/AUS/UK), so UK evening
  overlaps UK + US afternoon

## 8. Post
`[TBD]` — manual on each platform, or scheduled.

## 9. Submit to the campaign
`[TBD]` — how the clip gets submitted to Clip Farm for review. Review takes ~3 days.

## 10. Check back and settle the bet
Fill in real views at **24h, 72h and 7 days**, plus earnings.
Compare against the predicted score:
- Predicted high, flopped → the rule that made us confident is suspect
- Predicted low, took off → we're missing a rule; work out what it was

Review every 10 clips. Never tune off a single result.

---

## Per-video checklist
- [ ] Source is on the approved list
- [ ] Reason for picking it recorded
- [ ] Candidate moments logged with timestamps + why
- [ ] Predicted scores written to performance.csv BEFORE posting
- [ ] Hook lands within the campaign's window
- [ ] Whole-home rule satisfied (human eye — no tool checks this)
- [ ] Brand name spelled correctly in captions
- [ ] Attribution tag in caption
- [ ] Posted, submitted
- [ ] 24h / 72h / 7d numbers filled in
