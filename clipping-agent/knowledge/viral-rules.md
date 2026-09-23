# Viral Rules — Living Rulebook

This is the agent's actual scoring brain. CLAUDE.md holds the fixed process;
this file holds the rules that CHANGE as we learn.

**How to use this file**
- Every rule has a confidence level. Start honest: most of v1 is UNPROVEN.
- Never delete a rule. Move it to "Retired rules" with the reason it died.
- A rule only gets promoted to PROVEN with evidence from logs/performance.csv.
- Date every change.

Confidence levels:
- `UNPROVEN` — copied from general short-form advice. We have no data of our own.
- `WEAK` — 3+ of our own clips point this way.
- `PROVEN` — 10+ of our own clips, and it held when we tried the opposite.

---

## v1 — 2026-08-03 (starting position, all unproven)

### Hooks
| Rule | Confidence | Evidence |
|---|---|---|
| Start mid-action or mid-sentence, never a slow intro | UNPROVEN | general advice |
| Hook must be one of: bold statement, curiosity gap, visual action, controversy | UNPROVEN | general advice |
| Only use clips scoring hook 7+ | UNPROVEN | our own threshold, arbitrary so far |
| Opening on filler ("um", "so") kills the clip | UNPROVEN | general advice |
| Numbers/specifics in the first 3s help | UNPROVEN | general advice |

### Retention
| Rule | Confidence | Evidence |
|---|---|---|
| Micro-hook every 3–5 seconds | UNPROVEN | general advice |
| Pattern: tension → release → new tension | UNPROVEN | general advice |
| Dead air over 2.5s is fatal | UNPROVEN | guess baked into analyse.py |
| Sweet spot 2.3–3.6 words/sec | UNPROVEN | guess baked into analyse.py |

### Duration
| Rule | Confidence | Evidence |
|---|---|---|
| Target 30–55s, hard max 59s | UNPROVEN | 59s is a real YouTube Shorts limit; 30–55 is a guess |

### Endings
| Rule | Confidence | Evidence |
|---|---|---|
| End on punchline / revelation / cliffhanger / strong statement | UNPROVEN | general advice |
| Never fade out — hard cut or zoom cut on the final word | UNPROVEN | general advice |

### Captions
| Rule | Confidence | Evidence |
|---|---|---|
| Always include captions (85% watch muted) | UNPROVEN | widely repeated stat, unverified |
| Word-by-word or 2–3 words at a time, bold high contrast | UNPROVEN | general advice |
| Highlight one power word per sentence in another colour | UNPROVEN | general advice |

### Campaign selection
| Rule | Confidence | Evidence |
|---|---|---|
| Rank by CPM × REMAINING budget, never CPM alone | UNPROVEN | logic is sound; untested by us |
| Avoid gambling/crypto campaigns on a new account (ban risk) | UNPROVEN | high CPM is compensation for risk |

---

## Account naming — added 2026-08-03

| Rule | Confidence | Evidence |
|---|---|---|
| Put the niche keyword in the DISPLAY NAME — that's what search matches | WEAK | 10/10 top "podcast clips" accounts do this |
| The @username barely matters | WEAK | biggest account in the set is @quiz_game32 (393.7K followers) — username is unrelated nonsense |
| Judge peer accounts on likes-per-follower, not followers | UNPROVEN | clipping pays on views, and views come from FYP not followers |

## Retired rules

**"Avoid obvious clip-farm names like @dailyXclips; sound like a real brand instead."**
Killed 2026-08-03, same day it was written. Claude asserted this from general
branding intuition, then checked TikTok search for "podcast clips": all ten of the
top accounts use exactly the pattern the rule warned against — "Podcast Clips 101",
"Top Podcast Clips", "Joe Rogan Podcast Clips" — at 21K–393K followers.

The earlier supporting evidence (dead accounts named @thecutroom, @thedailycut) was
survivorship bias read backwards: those accounts are dead because their owners quit,
and the naming pattern had nothing to do with it.

Lesson for the agent: an intuition that sounds sophisticated is still unproven until
checked. Search the platform before writing a rule about the platform.

---

## Open contradictions
_(when two rules conflict in practice, log it here rather than silently picking one)_
