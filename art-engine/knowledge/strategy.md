# Strategy: getting abstract art in front of the right buyers for €0

## Who actually buys abstract art prints
1. **Home decorators (largest group).** Mostly 25–45, furnishing or redecorating a room.
   They search by *colour, room and mood*, not by artist name: "sage green abstract art",
   "large art for living room", "neutral bedroom wall art". → **Pinterest + Google.**
2. **Interior designers & stylists.** They buy for client projects, often several pieces
   at once, and come back for more. → **Direct outreach.**
3. **Hospitality & commercial spaces.** Boutique hotels, holiday rentals, restaurants,
   co-working spaces, clinics. Barcelona is full of them. → **Direct outreach.**
4. **Art collectors (originals).** Fewer, higher value. → **Saatchi Art / Artfinder** listings.

## Channels, ranked by return on zero money
| Channel | Why | Effort after setup |
|---|---|---|
| Pinterest (auto RSS) | Search engine for home decor, and a pin keeps working for months or years | None (automated) |
| Google (site SEO + free Shopping listings) | Buyers with intent, slow to build, compounds | None (automated) |
| Marketplaces (Etsy, Saatchi, Society6) | They already have the buyers | Listing once per painting |
| Designer / hotel outreach | One yes can mean 5–20 pieces | 15 min a month (Claude drafts) |
| Instagram | Good for collectors and credibility, but needs daily posting | Optional, manual |

## How the pins are written
Pinterest ranks pins by keywords in the title and description and by fresh images.
The engine combines:
- **colour** (detected or from `info.yml`): "ochre abstract art"
- **room** (`rooms`): "for the living room"
- **mood** (`mood`): "calm", "coastal", "moody"
- **your own keywords** (`keywords`): "mediterranean art", "large canvas"

So when adding a painting, the most valuable fields are `colours`, `rooms`, `mood` and
`keywords`. Use the words a buyer would type, not art-school words.

Strong search phrases for abstract prints (use in `keywords`):
neutral abstract art, large abstract wall art, modern abstract painting, boho abstract
art, minimalist wall art, textured abstract art, mid century modern art, mediterranean
wall art, coastal abstract art, earthy tones wall art, abstract art for bedroom,
living room wall decor, gallery wall art, original abstract painting, Barcelona art.

## What to measure (monthly check)
- Pinterest Analytics: impressions, outbound clicks, top pins
- Search Console: clicks and which searches show your pages
- Sales and enquiries by source (the pin links carry `utm_source=pinterest`)

Typical timeline: Pinterest usually takes 2–4 months of steady pinning to build
momentum. Don't judge it in week 3. The engine keeps pinning anyway.

## What to do when something works
- If a painting's pins get the most clicks, paint related work in that palette or
  series and add it.
- If a room or colour word wins, add more of it to `keywords` on other pieces.
- If a designer says yes, ask what else they're working on and offer trade pricing
  (typically 15–20% off).
