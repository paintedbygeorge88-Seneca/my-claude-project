# Playbook — How to evaluate a clipping campaign

The reusable method, separated from the findings. Follow this order — it is cheapest-first
on purpose, so bad campaigns get killed before any real work goes into them.

Derived from the 2026-08-03 session where this process killed the top-ranked candidate
in about thirty seconds.

---

## Step 1 — Viability (do this FIRST, it is nearly free)

Before caring about money at all, check the campaign is actually joinable.

- Follow **every external link** in the campaign description — signup forms, briefs,
  Discord invites, contact emails.
- If a mandatory form is closed, the campaign is dead **no matter what the listing says**.
- A campaign can be featured, prominently placed, and advertising a huge budget while
  being completely shut. Whop's discover carousel carries stale listings.

*Evidence: Dreamina AI — $10/1K, $60,000 budget, top of the featured carousel. Its
mandatory PandaDoc onboarding form returned "no longer accepting responses."*

## Step 2 — Remaining budget, not total

The advertised budget is what the campaign STARTED with. Pools are first-come-first-served
and views verifying after a pool empties pay nothing.

- On Whop, the campaign grid shows `$paid / $total`. **Remaining = total − paid.**
- The featured carousel does NOT show this. The grid inside a joined community does.
- Rank by **CPM × remaining budget**, never CPM alone.
- Also compute **burn rate**: paid ÷ days live. That gives runway in days.
  - Fast burn = content converts, but the pool dies soon.
  - Slow burn on a big pool = long runway, possibly less competition, possibly content
    nobody can make work. Ambiguous — don't read it as purely good.

*Evidence: Trailblazers Podcast burned 39% of a $6,000 pool in 6 days — about two weeks
of life left. Boxabl burned 6% of $85,000 in 14 days — roughly six months of runway.*

## Step 3 — Account risk

High CPM is often compensation for risk, not generosity.

- Gambling, sweepstakes and crypto campaigns pay well **because fewer clippers will take
  the ban risk** on their accounts.
- On a new account with no trust history, a ban costs more than the campaign pays.
- Check what the brand actually is before being impressed by the rate.

## Step 4 — Read the brief for ENGINEERING constraints

Most people read a brief for the rules. Read it for what it breaks in the pipeline.

Look specifically for:
- **Hook window** — campaigns specify their own (Boxabl says 2s; our default was 3s).
- **Spelling / branding requirements** that auto-captions will get wrong. Whisper
  mis-transcribes brand names, and a misspelling can be an automatic rejection.
- **Visual requirements** the transcript cannot detect. If the rule is about what's on
  screen, our transcript-only scoring is blind to it and a human must check.
- **Payout caps per clip** — changes strategy from chasing one hit to consistent volume.
- **Audience geography requirements** — affects posting times and hashtags.

## Step 5 — Only now, decide

Compare surviving campaigns on: remaining budget × CPM, runway in days, risk, and how
much pipeline work the brief demands.

Prefer a long-runway campaign for the first 30 clips even at a lower CPM. Early clips
exist to calibrate the scoring rules, and mistakes are cheaper where the pool isn't
about to vanish.

---

## Anti-patterns caught in practice

- **Trusting a featured listing.** Featured ≠ open. See step 1.
- **Trusting an advertised budget.** It is the starting figure, not what's left.
- **Being seduced by CPM.** $6/1K on a $13k crypto pool is worse than $1.10/1K on a
  fresh $75k pool, before even counting ban risk.
- **Writing a rule from intuition without checking the platform.** Claude asserted that
  obvious clip-farm handles underperform, then found all ten top "podcast clips"
  accounts use exactly that pattern. Search first, assert second.
