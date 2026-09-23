# SOP — Onboarding a New Campaign

Run this once per campaign, before any video work. Written from actually doing it for
Boxabl on 2026-08-03, so the steps are real rather than guessed.

For *choosing* which campaign to join, see `playbook-campaign-selection.md` first.

---

## 1. Evaluate before joining
Follow `playbook-campaign-selection.md`. Cheapest checks first: is intake actually open,
how much budget REMAINS, what's the account risk.

## 2. Join, and record the joining
Note the date, the operator (e.g. Clip Farm), and the direct URL to the campaign page.
George clicks Join — Claude never accepts terms on his behalf.

## 3. Create the campaign folder
```
campaigns/<slug>/          brief.md + approved-sources.md
input/raw/<slug>/          source footage, this campaign only
output/clips/<slug>/
output/captions/<slug>/
output/metadata/<slug>/
```
Slug is lowercase, no spaces (e.g. `boxabl`).

## 4. Capture the brief into campaigns/<slug>/brief.md
Get the campaign's own rules doc and pull out, explicitly:

- **Money** — CPM, total budget, remaining, max payout per clip, review time
- **Platforms** allowed
- **HARD REJECTS** — everything that makes a clip unbillable. List them all, quoted.
- **MUST INCLUDE** — attribution tag/URL, caption requirements, footage source
- **The content rule** — what the brand is actually paying to promote
- **Hook window** — campaigns specify their own (Boxabl says 2s, not the usual 3)
- **Audience requirements** — geography quotas affect posting time and hashtags

## 5. Populate approved-sources.md
From the campaign's official content list ONLY. One line per video:
```
filename.mp4 | source URL | note
```
Nothing gets clipped for this campaign that isn't on this list. An empty list means
nothing may be clipped yet — that is intentional, not a blocker to route around.

## 6. Write down what the brief breaks
Every campaign has requirements that trip up the standard workflow. Note them where
they'll be seen at edit time, not buried. Examples from Boxabl:
- Brand name that auto-captions will misspell → automatic rejection
- A visual requirement no transcript can detect → needs a human eye on every clip
- A per-clip payout cap → changes strategy from one big hit to consistent volume

## 7. Log it
Write the decision, the numbers, and what was rejected into `logs/runs/`.
Update the memory file so the next session knows which campaign is active.

---

## Checklist
- [ ] Evaluated via playbook (viability → remaining budget → risk)
- [ ] Joined, date and URL recorded
- [ ] Folders created
- [ ] brief.md written with hard rejects quoted
- [ ] approved-sources.md populated
- [ ] Tooling constraints noted
- [ ] Session logged, memory updated
