# The machine: how it runs itself

Design principles:
1. **Robots do repetition, AI does judgment, George does the human moments.**
   Daily tasks are plain code (free, zero tokens). Claude runs weekly or monthly, in
   batches (cheap on tokens). George only steps in when a real person has raised their hand.
2. **Pull, don't push.** Automating *outbound* rapport (bot DMs, bot comments) gets the
   account banned and, in a men's-support space, would fake the trust the work is about.
   So all the automation goes into *inbound*: making it effortless for the right people to
   come to George, then warming them up automatically until they're ready to talk.
3. **Everything free.** GitHub Actions, Pages, Pinterest, Meta's official Instagram API,
   MailerLite/Kit and ManyChat free tiers, Claude scheduled tasks on the existing plan.

## The agents

| Agent | Runs | Built with | Tokens |
|---|---|---|---|
| **Publisher** | Daily, 24/7 | GitHub Actions | 0 |
| **Poster** | Posts approved Reels at the best times | GitHub Actions + Instagram API | 0 |
| **Door** | 24/7, replies the moment someone comments a keyword | ManyChat free | 0 |
| **Nurture** | 24/7, email sequence for every new subscriber | MailerLite/Kit free | 0 |
| **Scout** | Weekly (Mon) | Claude scheduled task | Low |
| **Content** | Weekly, when footage arrives | Claude | Low |
| **Analyst** | Monthly | Claude scheduled task | Low |

### Scout: weekly
Finds the right people and hands George a **"warm 10"** list every Monday:
- **Hubs:** men's-work, breathwork, cold-exposure and men's mental-health accounts,
  podcasts, retreat centres, coaches, therapists who post about masking. Their audiences
  are George's audience.
- For each: why they fit, the exact post to reply to, a drafted comment or DM in George's
  voice that refers to *their* work, and the collab idea that suits them.
- George taps send on the ones he likes (~10 min/day max). Replies go into `outreach/log.csv`.
- Keeps a growing map of the community in `outreach/hubs.csv`.

### Door: 24/7 inbound automation
Every Reel ends with a keyword prompt: *"Comment MASK and I'll send you the painting
that matches what you're hiding."* ManyChat instantly DMs them the quiz link. Quiz → email
→ Nurture sequence → prints and commissions. Anyone who replies with something real gets
flagged for George to answer personally. **That conversation is George's only job.**

### Creative reach plays (Scout pitches them, George says yes or no)
- **"Paint your mask":** followers DM one feeling they never say out loud. George paints
  a small anonymous face from one of them each week. It's content, community and
  connection in one, and the people who submitted share it.
- **Gift the hubs:** send a print to 3 men's-work podcasters or retreat leaders a month.
  Costs a print, not ad money, and they often show it on camera or hang it.
- **Ice bath + art:** sessions end with a postcard of a face piece and a QR code to the quiz.
- **Retreat walls:** pitch retreats and studios to hang work with a QR code, with sales split or commission.
- **Guest on podcasts:** "the painter who coaches men to take off the mask." Scout drafts the pitches.

## Weekly rhythm
- **Mon** (auto): Scout delivers the warm 10 and the week's reach plays
- **George** (~15 min): film a talking clip, send footage
- **Content** (auto): clips + hooks + captions → George approves → Poster schedules them
- **Every day** (George, ~10 min): send a few Scout drafts, answer flagged DMs
- **Monthly** (auto): Analyst report → adjusts Scout targets and Content hooks
