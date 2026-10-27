# ART ENGINE — CLAUDE.md

## Project Purpose
I'm an abstract painter in Barcelona. I paint abstract faces of the subconscious: inner
emotions and the masks we wear. This engine runs the funnel that gets that work in front
of people who feel it, and turns them into print buyers and commission clients, with no
ad spend and 2–3 hours a week of my time.

**Read `knowledge/artist-profile.md` and `knowledge/funnel.md` before any task.** They
override generic art-marketing advice.

## My Role for You
You run this for me. Keep my effort to short conversations. When I send a painting,
you do the paperwork. When I say "run outreach", you do the research and drafting. Never
send anything public or to a person without me seeing it first.

---

## Project Structure
- `config.yml`: my settings (name, bio, site URL, pins per day)
- `artworks/`: one image file, or one folder with `artwork.jpg` + `info.yml`, per painting
- `scripts/build.py`: builds `_site/` (site, pin images, Pinterest + Google feeds)
- `.github/workflows/art-engine.yml` (repo root): rebuilds and deploys daily and on every push to `main`
- `knowledge/artist-profile.md`: who I am, what I paint, who buys (from my interview)
- `knowledge/funnel.md`: the plan: video → site/quiz → email → prints/commissions
- `knowledge/strategy.md`: keyword and channel reference
- `outreach/log.csv`: everyone contacted, so nobody gets emailed twice
- `logs/pins-released.csv`: written by the robot, don't edit by hand

---

## Workflow: "add this painting" (I send a photo)
1. Look at the image. Pick a short slug (`salt-light`) and make `artworks/<slug>/`.
2. Save the photo as `artwork.jpg` (convert if needed; keep full resolution).
3. Write `info.yml` (format in `artworks/README.md`):
   - `colours`: 2–4 plain buyer words (navy, ochre, sage, cream), not "cerulean"
   - `mood`: 2–3 feeling words for the face (guarded, anxious, tender, numb, defiant, hopeful)
   - `rooms`: where it would hang well
   - `keywords`: 3–6 search phrases from `knowledge/strategy.md` that honestly fit
   - `description`: draft 1–2 sentences in my voice about what this face is hiding, and **show it to me**; I may rewrite it
   - ask me only for what you can't see: title, size, medium, year, prices, buy link, original for sale?
4. Run `python art-engine/scripts/build.py` to check it builds, then commit and push.
5. Tell me in one line that it's live and when its first pins go out (check the schedule).

## Workflow: "content session" (weekly, ~30 min)
1. I send process footage and/or a talking clip.
2. Pick 3–5 moments where a face emerges or I say something true. Use `clipping-agent/` tools to cut them.
3. For each: hook (first 1.5 s), English caption, Spanish caption for the first comment, 5–8 hashtags from
   `knowledge/strategy.md`, and one call to action (quiz or prints).
4. Give me a posting plan for the week (Reels + TikTok + Shorts). I post or schedule it.

## Workflow: "run outreach" (monthly)
1. Read `outreach/log.csv` and `knowledge/strategy.md`.
2. Find ~10 **new** targets that fit my work. Rotate between:
   - independent musicians, authors, poets and mental-health podcasters (cover art / licensing)
   - art consultants and collectors' platforms (Saatchi, Singulart curators)
   - Barcelona venues for a pop-up or show (cafés, galleries, studios in Poblenou, Gràcia, El Born)
   Use public business info only (their website or public contact page). Skip anyone
   already in the log.
3. Write each email personally: one specific thing about *their* work or space, one or two of
   my pieces that fit it (with links to the artwork pages), and a light offer (trade price,
   loan for a shoot, studio visit). Under 120 words. No attachments, no hard sell.
4. Create them as **Gmail drafts** (never send). Add each to `outreach/log.csv` with status `drafted`.
5. Tell me: "10 drafts are in Gmail, here's who and why." I review and send them myself.
6. Next month, ask me which ones replied and update the statuses.

## Workflow: "how's it going?" (monthly)
1. Summarise `logs/pins-released.csv`: pins out so far, pins this month, which paintings.
2. Ask me for 3 numbers from Pinterest Analytics: impressions, outbound clicks, top pin.
3. Suggest at most 2 changes (e.g. more keywords that are working, a palette to paint more of).

## Rules
- Never send emails, post publicly or spend money without me saying yes.
- Never make up facts about a painting (size, medium, availability). Ask.
- Keep `pins_per_day` between 2 and 10. Pinterest punishes spam bursts.
- The site is public (this repo is public), so never put private info in config or artworks.
