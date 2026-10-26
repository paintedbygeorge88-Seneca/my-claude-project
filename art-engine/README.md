# Art Engine

A free system that gets your abstract art in front of people who buy art prints, and
keeps doing it without you.

## What it does, in plain English

1. **You add a painting** by dropping a photo into `artworks/` or sending it to Claude.
2. **It builds your shop website** for free on GitHub Pages. Every painting gets its own
   page, written so Google can find and understand it. Each page has a room mockup,
   prices and buy buttons.
3. **It turns every painting into a stream of Pinterest pins.** These are a styled
   poster, framed room mockups and close-up texture shots, all with different titles
   written around what people search for ("navy abstract art for the bedroom"). After
   90 days each painting gets a fresh set of new images, so old work keeps working.
4. **It drips those pins out a few per day, every day, forever.** A GitHub robot
   rebuilds the site each morning. Pinterest reads the feed and pins the new ones to
   your account automatically.
5. **Once a month you have one short chat with Claude.** It finds interior designers,
   boutique hotels and art consultants who match your style. It writes them personal
   emails and leaves them in your Gmail drafts. You read them and press send.

**Why Pinterest:** people go there to *plan their homes*, and "abstract wall art"
is one of its biggest searches. A pin keeps sending visitors for months or years. An
Instagram post is dead in two days, and an ad stops the moment you stop paying.
Pinterest is the closest thing to free advertising for art prints.

**Cost: €0.** GitHub hosting, GitHub Actions, Pinterest business account, Google Search
Console and Merchant Center are all free. You only pay per sale, through the
print/payment service you choose (see step 4 below).

---

## One-time setup (about 1–2 hours, once)

### 1. Turn on the website (5 min)
1. On GitHub, open this repository, then **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Edit `art-engine/config.yml`: fill in your name, email and bio (the lines marked TODO).
4. Once this is merged into `main`, your site is live at
   https://paintedbygeorge88-seneca.github.io/my-claude-project/

### 2. Pinterest business account + auto-pinning (20 min)
1. Create a free **Pinterest Business** account (or convert your personal one) at
   business.pinterest.com. Use your artist name.
2. **Claim your website:** Settings → Claimed accounts → Websites → Claim. Choose
   "Add HTML tag", copy the long code inside `content="..."` and put it in
   `config.yml` as `pinterest_verify`. Push, wait ~2 min for the site to rebuild, then
   click Verify.
3. Create one board, e.g. "Abstract Wall Art Prints". You can add more later, like
   "Blue Abstract Art" or "Art for the Living Room".
4. **Turn on auto-publishing:** Settings → Bulk create Pins → *Auto-publish* → connect RSS
   feed: `https://paintedbygeorge88-seneca.github.io/my-claude-project/feeds/pinterest.xml`
   and choose your board. Pinterest checks the feed every day and pins anything new.

### 3. Google (15 min)
1. **Search Console** (search.google.com/search-console): add the site URL, choose
   "HTML tag", put the code in `config.yml` as `google_verify`, push, verify. Then submit
   the sitemap: `sitemap.xml`.
2. **Merchant Center** (optional, once you have prices + a buy button): add the feed
   `https://paintedbygeorge88-seneca.github.io/my-claude-project/feeds/google-products.xml`.
   This puts your prints in the free Google Shopping listings. Google wants a
   shipping and returns policy, so add them to the About page first.

### 4. Choose how people pay and how prints get made
The site doesn't hold stock. Each painting's `buy_links` sends buyers to wherever the
sale happens. Pick one; you can change it later:

| Option | Upfront cost | You do | Good for |
|---|---|---|---|
| **Etsy + Gelato/Prodigi** (print-on-demand) | ~€0.20 per listing | Nothing; they print & ship worldwide | Easiest, and Etsy brings its own buyers |
| **Stripe Payment Link + Gelato/Prodigi** | €0 | Place the print order when a sale arrives | Higher margin, buy button straight on your site |
| **INPRNT / Society6 / Redbubble** | €0 | Nothing | Zero effort, lower margin, extra marketplace traffic |
| **Saatchi Art / Artfinder** (originals) | €0 | Ship the original when it sells | Selling original canvases to collectors |

Recommendation: start with **Etsy + Gelato** for prints and **Saatchi Art** for originals.
Point `buy_links` at those listings. You get buyers from Pinterest *and* from
Etsy and Saatchi searches.

### 5. Add your paintings
Send Claude photos and say **"add these paintings"**. Or drag the images into
`art-engine/artworks/` on the GitHub website. The site rebuilds within a few minutes.

---

## Day to day

| Who | What | How often |
|---|---|---|
| Robot | Rebuild site, release 3 new pins, Pinterest auto-pins them | Daily, automatic |
| You + Claude | "Add this painting" | Whenever you finish something |
| You + Claude | "Run outreach": Claude drafts ~10 emails, you press send | Monthly, ~15 min |
| You + Claude | "How's it going?": Claude checks the pin log and you share Pinterest numbers | Monthly, ~5 min |

## Files
- `config.yml`: your settings
- `artworks/`: one image (or folder) per painting
- `scripts/build.py`: the engine (site, pin images, feeds)
- `knowledge/strategy.md`: why each channel, who buys, keyword guide
- `outreach/`: target list and log for designer/hotel outreach
- `logs/pins-released.csv`: every pin the engine has released (written by the robot)

Preview a build locally: `pip install pillow pyyaml && python art-engine/scripts/build.py`,
then open `art-engine/_site/index.html`.
