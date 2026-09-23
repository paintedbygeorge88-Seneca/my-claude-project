# Faceless YouTube / TikTok — Research Reference

**Source:** Research videos saved in your TikTok favourites (@saunadiaries1).
**Goal of the project:** faceless YouTube + TikTok accounts that get views by reusing other viral videos in top niches.
**Compiled:** 2026-07-23 · **Updated:** 2026-07-31 (added clipping research, split into two account types, + **my own independent research — see Section 9, read it before you build**)

> **The big picture:** There are **two different business models** in your saved videos, and they need different tools and skills. Don't mix them up. Section 1 explains the difference. Section 2 = the **Viral/Repurposing** playbook. Section 3 = the **Clipping** playbook. Then shared strategy, monetisation, and sources.
>
> Links marked ✅ are confirmed from a video's caption; 🗣️ were spoken/on-screen and worth re-watching to confirm spelling.

---

## 1. The two account types (read this first)

| | **A. Viral / Repurposing account** | **B. Clipping account** |
|---|---|---|
| **What you make** | Brand-new faceless videos (AI voiceover + AI visuals) *based on* a viral topic | Short clips cut straight out of someone else's existing long video |
| **Where the content comes from** | You take the *idea/script* from a viral YouTube video, then generate a fresh video | You take the *actual footage* from live streams or podcasts and trim the best 30–60s |
| **Main skill** | Picking topics + AI generation + light editing | Spotting the *moment* that will go viral before anyone else |
| **Main tools** | ShadowScript → Hypernatural → CapCut | Scraping/transcript tools + Claude "skills" + a clipping cutter |
| **Your face on camera?** | No | No |
| **Best for** | Building an original-feeling channel in a niche | Fast volume, riding big creators' existing audiences |

You can run **both**, but start with one. My recommendation is at the very bottom.

---

## 2. Playbook A — Viral / Repurposing accounts

The exact process from the most on-topic video (@dombavaro, "Illegal Websites"). Everything here supports this loop:

1. **Find a viral video** in your niche (a YouTube video already getting big views = topic is proven).
2. **Turn it into an original script** → paste the YouTube link into **ShadowScript** (`getshadowscript.com`). Original, optimised script + description in seconds.
3. **Turn the script into a finished video** → paste it into **Hypernatural** (`hypernatural.ai`). Auto-builds the full video: AI voiceover + visuals. No face, no filming.
4. **Polish/edit** → **CapCut** for captions, hooks, final tweaks.
5. **Batch it** → steps 2–4 take minutes, so you can make a week of videos in one sitting.
6. **Post at volume** across TikTok + YouTube Shorts, leaning into already-trending topics.

### Toolbox for Playbook A
| Job | Tool | What it does | Link | Confirmed |
|---|---|---|---|---|
| Idea/niche research | **vidIQ + Claude** (MCP connector) | Ask Claude for ideas/titles powered by vidIQ's YouTube data | vidiq.com | ✅ |
| Idea/niche research | **Claude** (Sonnet) | The "brain" — ideas, titles, scripts, descriptions | claude.ai | ✅ |
| Script writing | **ShadowScript** | Viral YouTube link → original optimised script | getshadowscript.com | ✅ |
| Video generation | **Hypernatural AI** | Script in → full video out (voiceover + visuals) | hypernatural.ai | ✅ |
| Video generation | **Imagine Explainers** | AI explainer videos (no camera) | imagineexplainers.com | ✅ |
| Video generation | **NoteGPT** | Free alternative for explainer content | notegpt.io | ✅ |
| Video generation (free) | **WAN 2.1** | Open-source: text/image → video | open source | ✅ |
| Video generation (free) | **Tencent Hunyuan** | Open-source: photo → video | open source | ✅ |
| Video generation (free) | **CogVideo** | Open-source: cinema-grade video from text | open source | ✅ |
| Editing | **CapCut** | Editing, captions, hooks | capcut.com | ✅ |

---

## 3. Playbook B — Clipping accounts (NEW)

Instead of generating videos, you **cut short clips out of long content that already exists** (Twitch/YouTube streamers, big podcasts) and post them. Two flavours in your saves:

### B1. Clip live streamers (@fatheryashk)
- Watch big streamers, **clip the moments you think will do best online**, post the clips.
- His words: "super easy to get views." He's making a **3-part series on how to build a clipping page**.
- Tool he named: **CLIPTAI.COM** ⚠️ — but he says it's a site *he started*, so treat it as **self-promotion**, not an independent recommendation. Try it, but don't assume it's the best option.
- Hashtags: #clipt #clipping
- Comment worth remembering: *the real skill is being early on what people will want to watch* — same instinct whether you clip streamers or spot TikTok trends.

### B2. Clip podcasts with an AI "selection layer" (@oliver.merrick) — the smart one
His whole point: **editing was never the hard part — choosing the right 47 seconds is.** AI can already cut, caption and format. So you build a system that knows *which* moment to pick:

1. **Study what already works.** Scrape the latest ~100 clips from big podcast short-form accounts (Steven Bartlett, Chris Williamson, Alex Hormozi). Capture views, post date, duration, transcript, text overlay, format.
2. **Get the source.** Scrape their original long episodes and pull full transcripts **with timestamps** (timestamps are essential — they let Claude match each clip back to the exact moment).
3. **Reverse-engineer the decision.** Why those seconds? Where does the clip start? What context was cut? What hook/overlay/format? How did it perform vs the account's normal clips?
4. **Turn the patterns into a Claude skill** that understands how top teams select + package clips.
5. **Use it:** hand it any new timestamped transcript → it returns the strongest moments, exact timestamps, hook options, text overlays, formats and editing instructions. A separate editing skill does the easy cutting part.

His kicker: *"None of this needs new software. The tools exist. The clipping skills exist. The data is public. Nobody is assembling it into an intelligence layer."*

### Toolbox for Playbook B
| Job | Tool | What it does | Link | Confirmed |
|---|---|---|---|---|
| Cut/caption/format clips | **Claude "skills"** (free, from GitHub) | Teach Claude to do the mechanical editing in minutes | github.com (search "claude clipping skills") | ✅ |
| Pick the best moment | **Custom Claude skill** you build (the selection layer) | Reads a transcript, returns the clips worth making | build-your-own | ✅ |
| Clip streamers | **CLIPTAI.COM** | Web tool for making streamer clips | cliptai.com | 🗣️ (creator's own site) |
| Clip long videos | **Custom "AI clipping agent"** (@sina.growthtech) | Auto-cut long videos into 1080×1920 vertical clips | build-your-own | 🗣️ |
| Cutting | **LosslessCut** | Free manual video cutter | losslesscut app | ✅ |
| Named in comments | **Workbeaver** | Clipping/automation tool | — | 🗣️ |
| Marketplace (comments) | **Whop** | Where people hire clippers / sell clipping services | whop.com | 🗣️ |

---

## 4. Build / automation tools (used by both)
| Tool | What it does | Link | Confirmed |
|---|---|---|---|
| **Claude Code** | Build agents/automations, "team of AI agents" | — | ✅ |
| **aitmpl.com/agents** | Library of prebuilt Claude Code agents — copy the code | aitmpl.com/agents | ✅ |

---

## 5. Content strategy notes (apply to both types)
- **Repurpose what's already viral / already watched.** The algorithm already knows people want it. This is the whole edge — true for both remixing and clipping.
- **Volume, but not spam.** GaryVee says 100–500 clips/week; ⚠️ but a top comment warns TikTok *throttles* accounts that post too much per day. Saner target: **~3 posts/day**, consistently.
- **Own a niche.** "Own your niche and get rich" — pick one lane so the algorithm can categorise you.
- **Quality can beat quantity once the format works.** Case-study channel "easy actually" hit 1.09M subs with only **23 videos** ("few words + more pictures").
- **Post to both platforms** — YouTube Shorts + TikTok from the same clips.
- **Be early (clipping).** The clipping edge is spotting what's about to pop *before* others do.

## 6. Monetisation angles seen
- **TikTok Shop Affiliate** — rebrand a faceless account into a TikTok Shop affiliate account (@dave_preneur). Newer saves also show "Reviving an Inactive Affiliate Account" and "Featured Shop Creator" angles.
- **Get paid to clip** — brands/creators hire clippers (see Whop). Clipping can be a paid service, not just your own channel.
- **Ad / Shorts monetisation** at scale.
- **Selling the workflow itself** — many of these creators funnel to a paid "free guide." (Also why income claims below are marketing, not proof.)

> ⚠️ **Reality check:** the "$10k/month", "$20,648 in 7 days", "1M views" hooks are how these creators sell their own guides. The *workflows* are real and worth trying. The *numbers* are bait — ignore them.

## 7. Gaps / worth re-watching yourself
Tools named out loud or on fast screens that I couldn't fully capture:
- @seancannellofficial "Best AI Tools for Content Creators" (full tool list is spoken)
- @sina.growthtech "The AI Agent That Clips Videos" (shows building a custom clipping agent)
- The "100 TikToks/Hour" video (bulk-posting method)
- @oliver.merrick — the exact GitHub "clipping skills" he links (spoken, not written in caption)

## 8. Sources
**Playbook A (viral/repurposing):**
1. @dombavaro — "Illegal Websites" (the core workflow) — the anchor
2. @vidiq.tiktok — vidIQ + Claude MCP for idea research
3. @sebintel — "Build Your Faceless Channel With AI" (imagineexplainers / NoteGPT)
4. @nicksadler.io — "Best Free AI Video Tools" (WAN 2.1 / Hunyuan / CogVideo)
5. @seancannellofficial — "Best AI Tools for Content Creators"

**Playbook B (clipping):**
6. @fatheryashk — "Started clipping last weekend" (clip streamers; cliptai.com)
7. @oliver.merrick — "Ultimate AI Clipping System" (the Claude selection-layer method) ⭐
8. @sina.growthtech — "The AI Agent That Clips Videos"

**Monetisation / build:**
9. @dave_preneur — "Rebrand a Faceless Account for TikTok Shop"
10. @theaiimpact — "Build a team of AI Agents in Claude" (aitmpl.com/agents)
11. @garyvee — posting cadence / volume

---

## 9. My independent research — the 2026 reality (READ THIS FIRST)

I went beyond the TikTok videos and checked the actual platform rules, tool costs and legal side, because the creators selling these methods leave out the parts that get you demonetised or unpaid. This section is the honest picture.

### 9a. ⚠️ The single most important thing: YouTube changed the rules in 2026
In **July 2026** YouTube renamed its "Inauthentic Content" rule to **"Generic or Repetitive Content"** and started actively cracking down on exactly the low-effort AI/repurposing style these videos teach.
- **Mass-produced or recycled AI videos** (AI voiceover + stock/slideshow visuals, recycled clips, low-effort compilations) now face a **3-strike system**: warning → 90-day suspension → permanent removal from the Partner Program.
- **AI disclosure is mandatory** since Jan 2026 for AI-generated/altered media that could look real. Not disclosing = demonetisation or channel termination.
- **Faceless is NOT banned.** What matters is that *each video is materially different and adds real value* (commentary, analysis, a genuinely new angle). Disclosed, higher-effort AI content earns the same RPM as non-AI in the same niche.
- **Translation for you:** Playbook A still works, **but only if you add a real original layer** (your own take, script, structure) — not if you just run ShadowScript → Hypernatural and post the raw output. The "spray 100 identical AI videos" advice is now a demonetisation trap.

### 9b. What you actually need to earn (thresholds)
| Platform | To get paid | Pay rate (rough) |
|---|---|---|
| **YouTube Shorts** (main tier) | 1,000 subs **+** 10M Shorts views in 90 days (or 4,000 watch hrs on long-form) | Varies by niche |
| **YouTube Shorts** (intro tier) | 500 subs **+** 3M Shorts views in 90 days | Lower |
| **TikTok Creator Rewards** | **10,000 followers + 100k views/30 days**, 18+, videos **must be original AND 60+ seconds** | ~$0.40–$1.00 per 1,000 views |
| **Whop clipping campaigns** | **No follower minimum.** Just join a campaign and post | ~$0.20–$6 per 1,000 views, avg ~$1 |

⚠️ **TikTok won't pay you for reposts.** Duets, stitches, watermarked reposts and slideshows are **ineligible** for Creator Rewards — only original 60s+ videos count. So "just repost viral clips" earns you *nothing directly from TikTok*; the money there comes from TikTok Shop affiliate or driving traffic elsewhere.

### 9c. The legal reality of clipping (important)
- Clipping someone's stream/podcast and posting it **for profit without permission is copyright infringement.** The owner can issue DMCA takedowns; **3 strikes = channel termination.**
- "I edited it / added captions" is **not** automatic fair use. Fair use needs genuine commentary/critique + directing people back to the source, and even then it's a legal defence, not a guarantee.
- **The safe, legit path:** clip for creators who *give you permission and pay you* → this is exactly what **Whop / clipping campaigns** are. The creator funds it, wants the clips, and hands you the rights. No copyright risk, no follower minimum, you get paid per view.
- @fatheryashk's "clip any streamer" approach carries real DMCA risk unless the streamer allows it. @oliver.merrick's podcast approach is safer *if* you're clipping for the podcast's own team / an approved campaign.

### 9d. Verified tool costs (as of mid-2026)
| Tool | Real? | Cost |
|---|---|---|
| **ShadowScript** | ✅ Real, operational (US company, Yardley PA) | Pricing hidden behind signup |
| **Hypernatural** | ✅ Real | Free = 10 watermarked 30s clips; **$22/mo** (1,500 credits) or **$99/mo** unlimited/no watermark |
| **Opus Clip** (podcast/clipping) | ✅ Industry standard | ~$29/mo |
| **Ssemble** (Opus alt, volume) | ✅ | ~$15/mo |
| **Vugola AI** (Opus alt) | ✅ | ~$14/mo |
| **quso.ai** (all-in-one Opus alt) | ✅ | Free tier; paid from ~$19/mo |
| **Choppity** | ✅ Podcast-focused, best hook detection | Paid |
| **CapCut** | ✅ | Free (paid Pro optional) |

**Note on clipping tools:** the TikTok videos push building your *own* Claude clipping agent, but off-the-shelf tools (**Opus Clip, Ssemble, quso.ai, Choppity**) already do the auto-cut/caption/format part well and cheaply. @oliver.merrick's real insight — the *selection* layer (which moment to pick) — is the bit worth building yourself on top of a cheap cutter. Don't reinvent the editing.

---

### 10. Suggested build path (revised after the research)

**If your goal is money ASAP with the least risk → start with clipping *campaigns*, not a channel.**

1. **Week 1 — Whop clipping campaigns.** No follower minimum, permission + payment built in, no copyright risk. Join a campaign in a niche you like, use a cheap cutter (Opus Clip / Ssemble ~$15/mo), post clips, get paid per 1,000 views. This teaches you what goes viral *while earning*, with zero audience needed. Fastest path to a first payout.
2. **Week 2–4 — build the "selection" edge.** Apply @oliver.merrick's method: study which clips win, turn the pattern into a Claude skill that picks the best moments. This makes your campaign clips outperform everyone else's.
3. **Month 2+ — launch your own faceless channel (Playbook A), done properly.** Pick one niche → ShadowScript for the script → Hypernatural for video → **add your own original angle/commentary** (this is what keeps you monetisable under the 2026 rules) → **disclose AI** → CapCut → post ~2–3/day to TikTok (60s+ originals) + YouTube Shorts. Aim for 20–30 genuinely-distinct videos before judging it.
4. **Money on top:** TikTok Shop affiliate + Shorts/Creator Rewards once you hit thresholds, plus ongoing Whop clipping income throughout.

**Why this order:** clipping campaigns pay from day one with no audience and no legal/monetisation risk, so you earn and learn what's viral *before* you sink weeks into a channel that the 2026 rules could demonetise if it's low-effort. Prove one thing at a time.

---

### Sources (my independent research)
- YouTube 2026 monetisation & reused/inauthentic-content rules — [vidIQ](https://vidiq.com/blog/post/youtube-reused-content-policy-guide/), [peggyktc](https://www.peggyktc.com/2026/07/youtube-clarifies-inauthentic-content.html), [invideo](https://invideo.io/blog/youtube-kills-ai-faceless-channels/), [vexub](https://vexub.com/blog/ai-generated-video-monetization-policies)
- YouTube Shorts monetisation thresholds — [unkoa](https://www.unkoa.com/youtube-shorts-monetization-requirements/), [Conbersa](https://www.conbersa.ai/learn/youtube-shorts-monetization-requirements-2026)
- TikTok Creator Rewards eligibility/payouts — [Multilogin](https://multilogin.com/blog/mobile/tiktok-creator-rewards-program/), [postlink](https://postlinkapp.com/blog/tiktok-creator-rewards-program)
- Clipping legality / DMCA — [ClipAffiliates](https://www.clipaffiliates.com/blog/is-clipping-legal), [Lumina Clippers](https://luminaclippers.com/blog/is-clipping-legal), [clipspeed](https://www.clipspeed.ai/blog/make-money-clipping-other-peoples-videos.html)
- Whop clipping — [Ssemble](https://www.ssemble.com/blog/best-clipping-platforms-2026), [Vyroclips](https://vyroclips.com/whop-clipping-platform-how-it-works-and-what-it-pays)
- Clipping tools & pricing — [Ssemble](https://www.ssemble.com/blog/best-ai-clipping-tools-2026), [quso.ai](https://quso.ai/alternatives/opus-clip-alternative), [Choppity](https://www.choppity.com/blog/best-ai-podcast-clip-makers-generators/)
- Hypernatural pricing — [Tekpon](https://tekpon.com/software/hypernatural/reviews/), [heyorai](https://heyorai.com/tool/hypernatural/)
- ShadowScript — [getshadowscript.com](https://getshadowscript.com)
