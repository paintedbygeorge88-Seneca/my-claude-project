# Clipping — Standalone Reference

*Everything about clipping, pulled out of the main faceless-channel research so it can live in the clipping project. Compiled 2026-08-03.*

---

## What a clipping account is
You **cut short clips out of long content that already exists** (Twitch/YouTube streamers, big podcasts) and post them. You don't generate anything — you find the best 30–60 seconds of someone else's video and repackage it vertical with captions. The whole skill is **spotting the moment that will go viral before anyone else.**

---

## The two clipping approaches (from research videos)

### 1. Clip live streamers (@fatheryashk)
- Watch big streamers, clip the moments you think will do best, post them. Creator says it's "super easy to get views" and is making a 3-part series on building a clipping page.
- Tool he named: **cliptai.com** ⚠️ — but it's a site *he started*, so treat it as self-promotion, not a neutral recommendation.
- Hashtags: #clipt #clipping
- Key idea from comments: the real skill is *being early on what people will want to watch*.

### 2. Clip podcasts with an AI "selection layer" (@oliver.merrick) — the smart one ⭐
His whole point: **editing was never the hard part — choosing the right 47 seconds is.** AI can already cut, caption and format. So you build a system that knows *which* moment to pick:

1. **Study what already works.** Scrape the latest ~100 clips from big podcast short-form accounts (Steven Bartlett, Chris Williamson, Alex Hormozi). Capture views, post date, duration, transcript, text overlay, format.
2. **Get the source.** Scrape their original long episodes and pull full transcripts **with timestamps** (timestamps let Claude match each clip back to the exact moment).
3. **Reverse-engineer the decision.** Why those seconds? Where does the clip start? What context was cut? What hook/overlay/format? How did it perform vs the account's normal clips?
4. **Turn the patterns into a Claude skill** that understands how top teams select + package clips.
5. **Use it:** hand it any new timestamped transcript → it returns the strongest moments, exact timestamps, hook options, text overlays, formats and editing instructions. A separate editing skill does the easy cutting part.

His kicker: *"None of this needs new software. The tools exist. The clipping skills exist. The data is public. Nobody is assembling it into an intelligence layer."*

---

## ⚠️ The legal reality (important — read before clipping anything)
- Clipping someone's stream/podcast and posting it **for profit without permission is copyright infringement.** The owner can issue DMCA takedowns; **3 strikes = channel termination.**
- "I edited it / added captions" is **not** automatic fair use. Fair use needs genuine commentary/critique + directing people back to the source, and even then it's a legal defence, not a guarantee.
- **The safe, legit path:** clip for creators who *give you permission and pay you* → this is exactly what **Whop / clipping campaigns** are. The creator funds it, wants the clips, and hands you the rights. No copyright risk, no follower minimum, you get paid per view.
- Clipping any random streamer yourself carries real DMCA risk unless they allow it.

---

## The money: clipping campaigns (Whop)
- **No follower minimum.** A creator funds a campaign, sets a rate per 1,000 views + content rules, and opens it to clippers. You join, post qualifying clips, submit the links, they verify views and pay.
- **Pay:** ~$0.20–$6 per 1,000 views, averaging ~$1, and only while the campaign budget lasts.
- Payment models: pay-per-view, affiliate commission (a % of sales your clips drive), or flat per accepted clip.
- ⚠️ Never pay a joining fee — legit campaigns don't charge you to join.

---

## Clipping tools (verified, mid-2026)
| Job | Tool | Cost | Notes |
|---|---|---|---|
| Find paid campaigns | **Whop** (whop.com) | Free to join | Search "clipping" / "content rewards" |
| Cut / caption (free) | **CapCut** | Free | Manual but powerful; best on a budget |
| Cut / caption (faster, volume) | **Ssemble** | ~£12–15/mo | Cheaper than Opus; 1 credit per video not per minute |
| All-in-one alt | **quso.ai** | Free tier / ~$19/mo | Clipping + virality scoring + scheduler |
| Opus alt | **Vugola AI** | ~$14/mo | Clip + captions + scheduling |
| Podcast-specific | **Choppity** | Paid | Best hook detection for conversations |
| Industry standard | **Opus Clip** | ~$29/mo | Charges per minute of source (pricier) |
| Manual cutter | **LosslessCut** | Free | Simple lossless trimming |

**Don't reinvent the editing.** Off-the-shelf tools already auto-cut/caption/format well and cheaply. The bit worth building yourself is the **selection layer** (which moment to pick) from @oliver.merrick's method, on top of a cheap cutter.

---

## Clip format basics (every clip needs)
- Vertical **9:16** (1080×1920).
- **Captions on** — most people watch on mute.
- **Strong first 1–2 seconds** — start on the most interesting moment, not a slow intro. Put the best line as a text hook.
- 15–60 seconds is the sweet spot for most campaigns.

---

## Where clipping fits for earning ASAP
Clipping *campaigns* are the fastest legal way to earn with **no audience**: permission + payment are built in, and you get paid per view. It also teaches you what goes viral (instant feedback = money), which is the exact skill any channel needs later.

**Note on direct platform payouts:** TikTok's Creator Rewards will NOT pay for reposts/clips — only original 60s+ videos, and you need 10k followers + 100k views/30 days. So clipping income comes from **campaigns (Whop)**, not from TikTok paying you directly for the clips.

---

## Worth re-watching / building
- @oliver.merrick — the exact free GitHub "clipping skills" he links (spoken, not written).
- @sina.growthtech — "The AI Agent That Clips Videos" (shows building a custom clipping agent).
- The "100 TikToks/Hour" video (bulk-posting method).

### Sources
- Clipping legality / DMCA — [ClipAffiliates](https://www.clipaffiliates.com/blog/is-clipping-legal), [Lumina Clippers](https://luminaclippers.com/blog/is-clipping-legal)
- Whop clipping — [Ssemble](https://www.ssemble.com/blog/best-clipping-platforms-2026), [Vyroclips](https://vyroclips.com/whop-clipping-platform-how-it-works-and-what-it-pays)
- Clipping tools & pricing — [Ssemble](https://www.ssemble.com/blog/best-ai-clipping-tools-2026), [quso.ai](https://quso.ai/alternatives/opus-clip-alternative), [Choppity](https://www.choppity.com/blog/best-ai-podcast-clip-makers-generators/)
