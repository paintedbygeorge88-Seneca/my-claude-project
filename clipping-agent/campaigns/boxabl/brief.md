# ACTIVE CAMPAIGN — Boxabl Official Clipping (Clip Farm)

Joined 2026-08-03. This is the campaign we are learning on. Read before every run.

Source: Boxabl x ClipFarm Clipper Brief (Google Doc)
https://docs.google.com/document/d/1DP7iD-sndoSnaihYhwppziogPXi5ZT3OkTHiOQI__X0/edit

## Money

- **CPM: $0.50 per 1,000 views** (lowest tier — 1M views = $500)
- **Max payout per clip: $500** — a clip is capped at 1M views of value
- Budget $85,000, ~$5.5k paid out, **~$79.5k remaining (93.5% left)**
- Avg review time: **3 days**
- Platforms: YouTube, TikTok, Instagram, X

Optional affiliate on top (boxabl.com/affiliate): $1 per form fill, 3% of unit price on
sales, 0.5% recruit override. Not required.

## What Boxabl is

Foldable, factory-made homes. Flagship product is the **Casita** — a 20x20ft home that
ships flat and unfolds on-site. The angle is: cool product, cool factory, cool
transformation.

## Where the footage is

Pre-approved list only — "BOXABL Content To Clip" Google Doc, linked from the brief.
Includes Boxabl factory tours and walkthroughs from Enes Yilmazer (15M views), Orkun
Isitmak (16.3M views), Elon Musk, Airrack, Faze Rug.
Download tool they recommend: turboscribe.ai/downloader/youtube/mp4

## HARD REJECTS — any one of these and the clip is not billable

- **Kanye clips.** Explicitly called out: "NO MORE CLIPS OF KANYE, YOU WILL BE REJECTED"
- **Auto-captions that misspell "BOXABL".** Called out twice. See engineering note below.
- **Raw rips.** Lifted footage with no edit. Must have captions, jump cuts, hooks.
- **Low-effort slop or engagement bait.** "RANDOM CLIPS THAT ADD NO VALUE COUNT AS SLOP"
- **Story boosting / view botting / paying for boosts.**
- **Other brand watermarks.**
- **Political or controversial content.**
- **Trashing the product or the talent.** Positive vibes only — celebrity guests
  (Post Malone, Elon etc.) get treated well in every clip.

## EVERY CLIP MUST HAVE

1. **Attribution** — `@boxabl` tag in the caption on TikTok / Reels / Shorts.
   On **X** it's the tracking URL instead. Caption tag is the minimum; a pinned
   comment does not replace it.
2. **A caption that mentions Boxabl** — must be relevant (the Casita, foldable homes,
   the factory, the product). Not blank, not unrelated.
3. **Boxabl's own footage** from the approved content doc.
4. **Positive framing.**

## THE CONTENT RULE (most important, and easiest to fail)

> "Clips must show the whole Boxabl home, not just one feature. At the end of the day
> Boxabl is paying you to promote their HOME."

Their analogy: a good car review shows the whole car first, not just the cup holder.

- Show the whole home, how it looks, with a clear mention of "BOXABL" while the home is
  on screen — spoken or on-screen text.
- *Then* you can show the small feature, the funny moment, the engaging bit.
- The clip cannot be unrelated engagement bait. Elon talking about Boxabl with no b-roll
  of the house = rejected.

## DO

- **Hook in 2 SECONDS.** First frame matters more than anything. Strong visual or a
  strong celebrity face. No slow intros, no logos, no setup.
- **Bold captions** — big text overlays that tell the story with sound off.
- **Mention Boxabl in the caption.**
- **Vary the clips** — don't post the same moment 10 times. Variety wins the algorithm.

## Audience requirement

**40% Tier 1 audience (US / CAN / AUS / UK).** Affects posting times and hashtag choice —
posting on UK evening hits UK + US afternoon, which is the useful overlap.

---

## Engineering notes — how this changes our pipeline

1. **Hook window is 2s, not 3s.** `scripts/analyse.py` scores the first 3.0 seconds.
   This campaign says 2. Use `--hook-window 2.0` on every Boxabl run.

2. **"Boxabl" WILL be mis-transcribed.** Whisper will almost certainly produce
   "boxable", "box able", "boxabel". The brief says a misspelling in auto-captions is a
   straight rejection. Whatever generates the SRT must force-correct every variant to
   `BOXABL` before the caption file is written. This is a hard requirement, not a polish
   item.

3. **Our scoring is blind to the thing that matters most.** `analyse.py` reads the
   transcript only. It cannot see whether the whole house is on screen — which is the
   campaign's single biggest rejection criterion. The script can shortlist candidate
   moments; a human must confirm the house is actually shown. Do not let the pipeline
   pick clips unsupervised on this campaign.

4. **Cap awareness.** Max $500/clip means a mega-viral clip stops earning at 1M views.
   Ten clips at 100k views each are worth the same as one at 1M, and are far more likely.
   Favour consistent volume over swinging for one hit.
