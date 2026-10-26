#!/usr/bin/env python3
"""
ART ENGINE — build.py

Turns art-engine/artworks/ into:
  - a static portfolio + shop site (SEO pages, structured data, sitemap)
  - feeds/pinterest.xml  -> RSS feed Pinterest auto-pins from (drip released, a few per day)
  - feeds/google-products.xml -> Google Merchant Center free-listings feed
  - logs/pins-released.csv -> record of every pin released so far

Usage:
  python art-engine/scripts/build.py                 # build into art-engine/_site
  python art-engine/scripts/build.py --today 2026-12-01   # preview a future day
"""
import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import random
import re
import shutil
import subprocess
from email.utils import format_datetime
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = 250_000_000

ENGINE = Path(__file__).resolve().parent.parent
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
PIN_W, PIN_H = 1000, 1500
VARIANTS = ["poster", "wall", "detail", "poster_dark", "wall_alt", "detail_alt"]
VARIANT_OFFSET_DAYS = [0, 2, 5, 9, 14, 20]
WALLS = [(236, 231, 223), (214, 207, 196), (196, 204, 188), (222, 203, 186),
         (205, 212, 216), (229, 222, 210), (70, 72, 74)]

# Named colours used to turn pixels into search keywords ("ochre abstract art")
COLOUR_NAMES = {
    "black": (20, 20, 20), "charcoal": (60, 60, 64), "grey": (128, 128, 128),
    "white": (245, 245, 242), "cream": (238, 228, 205), "beige": (215, 195, 165),
    "terracotta": (190, 95, 65), "rust": (160, 70, 40), "red": (200, 35, 40),
    "burgundy": (115, 25, 40), "pink": (235, 160, 175), "blush": (230, 195, 185),
    "orange": (235, 130, 40), "ochre": (200, 150, 50), "mustard": (215, 175, 45),
    "yellow": (245, 215, 60), "olive": (120, 120, 50), "sage": (160, 175, 145),
    "green": (60, 140, 70), "emerald": (20, 110, 80), "teal": (30, 120, 125),
    "turquoise": (60, 190, 190), "sky blue": (135, 190, 230), "blue": (40, 80, 175),
    "navy": (25, 35, 80), "indigo": (60, 50, 120), "lilac": (190, 165, 210),
    "purple": (110, 50, 130), "brown": (110, 75, 45), "gold": (195, 160, 80),
}


# ---------------------------------------------------------------- helpers

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "artwork"


def esc(text):
    return html.escape(str(text or ""), quote=True)


def seeded(*parts):
    return random.Random(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest())


def to_date(value):
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value))


def font(size, serif=False):
    names = ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"] if serif else \
            ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    for root in ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation",
                 "/usr/share/fonts/dejavu", "/Library/Fonts", "/System/Library/Fonts/Supplemental"]:
        for name in names:
            path = Path(root) / name
            if path.exists():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


def fit_text(draw, text, max_width, size, serif=False, min_size=22):
    while size > min_size:
        f = font(size, serif)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(min_size, serif)


def git_added_date(path):
    """Date the file first entered git; falls back to file mtime."""
    try:
        out = subprocess.run(["git", "log", "--diff-filter=A", "--follow", "--format=%as", "--", str(path)],
                             cwd=ENGINE, capture_output=True, text=True, timeout=20).stdout.split()
        if out:
            return dt.date.fromisoformat(out[-1])
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    return dt.date.fromtimestamp(path.stat().st_mtime)


def dominant_colour_names(img, count=3):
    small = img.copy()
    small.thumbnail((200, 200))
    pal = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    rgb = pal.getpalette()[:24]
    counts = sorted(pal.getcolors(), reverse=True)
    names = []
    for _, idx in counts:
        c = rgb[idx * 3: idx * 3 + 3]
        name = min(COLOUR_NAMES, key=lambda n: sum((a - b) ** 2 for a, b in zip(c, COLOUR_NAMES[n])))
        if name not in names:
            names.append(name)
        if len(names) == count:
            break
    return names


def save_jpg(img, path, quality=85):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)


# ---------------------------------------------------------------- artworks

def load_artworks(folder):
    artworks = []
    entries = sorted(p for p in folder.iterdir() if not p.name.startswith((".", "_")))
    for entry in entries:
        if entry.is_dir():
            images = sorted(p for p in entry.iterdir() if p.suffix.lower() in IMAGE_EXTS)
            preferred = [p for p in images if p.stem.lower() in ("artwork", "image", "main")]
            if not images:
                continue
            image = (preferred or images)[0]
            info_file = entry / "info.yml"
            info = yaml.safe_load(info_file.read_text()) if info_file.exists() else {}
            slug = slugify(entry.name)
            fallback_title = entry.name
        elif entry.suffix.lower() in IMAGE_EXTS:
            image, info, slug, fallback_title = entry, {}, slugify(entry.stem), entry.stem
        else:
            continue

        info = info or {}
        img = ImageOps.exif_transpose(Image.open(image)).convert("RGB")
        title = info.get("title") or re.sub(r"[-_]+", " ", fallback_title).strip().title()
        artworks.append({
            "slug": slug,
            "image_path": image,
            "img": img,
            "title": title,
            "added": to_date(info["added"]) if info.get("added") else git_added_date(image),
            "year": info.get("year", ""),
            "medium": info.get("medium", ""),
            "original_size": info.get("original_size", ""),
            "description": (info.get("description") or "").strip(),
            "colours": info.get("colours") or dominant_colour_names(img),
            "mood": info.get("mood") or [],
            "rooms": info.get("rooms") or ["living room", "bedroom", "home office"],
            "keywords": info.get("keywords") or [],
            "prices": info.get("prices") or [],
            "buy_links": info.get("buy_links"),
            "original_available": bool(info.get("original_available", False)),
            "sold": bool(info.get("sold", False)),
        })
    artworks.sort(key=lambda a: (a["added"], a["slug"]), reverse=True)
    return artworks


# ---------------------------------------------------------------- pin images

def with_shadow(canvas, art, x, y, radius=18, offset=(10, 16), alpha=95):
    shadow = Image.new("L", (art.width + radius * 4, art.height + radius * 4), 0)
    ImageDraw.Draw(shadow).rectangle([radius * 2, radius * 2, radius * 2 + art.width, radius * 2 + art.height],
                                     fill=alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius))
    canvas.paste((0, 0, 0), (x - radius * 2 + offset[0], y - radius * 2 + offset[1]), shadow)
    canvas.paste(art, (x, y))


def poster_pin(a, artist, dark=False):
    bg, fg, muted = ((28, 28, 30), (240, 238, 234), (165, 162, 158)) if dark else \
                    ((244, 241, 236), (30, 30, 30), (110, 108, 104))
    canvas = Image.new("RGB", (PIN_W, PIN_H), bg)
    art = a["img"].copy()
    art.thumbnail((PIN_W - 180, PIN_H - 440), Image.LANCZOS)
    x = (PIN_W - art.width) // 2
    y = (PIN_H - art.height - 250) // 2  # centre the artwork + caption block
    with_shadow(canvas, art, x, y)
    d = ImageDraw.Draw(canvas)
    ty = y + art.height + 100
    title_font = fit_text(d, a["title"], PIN_W - 140, 60, serif=True)
    d.text((PIN_W // 2, ty), a["title"], font=title_font, fill=fg, anchor="mm")
    sub = f"Abstract art print  ·  {artist}"
    d.text((PIN_W // 2, ty + 72), sub, font=fit_text(d, sub, PIN_W - 140, 30), fill=muted, anchor="mm")
    d.text((PIN_W // 2, ty + 122), "Painted in Barcelona  ·  Ships worldwide", font=font(24), fill=muted,
           anchor="mm")
    return canvas


def wall_pin(a, wall):
    canvas = Image.new("RGB", (PIN_W, PIN_H), wall)
    floor_y = int(PIN_H * 0.82)
    # soft light falloff on the wall
    light = Image.linear_gradient("L").resize((PIN_W, floor_y)).point(lambda v: int(v * 0.10))
    canvas.paste((0, 0, 0), (0, 0), light)
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, floor_y, PIN_W, PIN_H], fill=(150, 116, 86))
    for i in range(0, PIN_H - floor_y, 22):
        d.line([0, floor_y + i, PIN_W, floor_y + i], fill=(138, 106, 78), width=1)
    d.rectangle([0, floor_y - 16, PIN_W, floor_y], fill=tuple(min(255, c + 12) for c in wall))

    # bench under the art
    bench_top = floor_y - 175
    bench = (200, 158, 120) if sum(wall) > 300 else (120, 92, 70)
    d.rectangle([170, bench_top, PIN_W - 170, bench_top + 26], fill=bench)
    for lx in (205, PIN_W - 225):
        d.rectangle([lx, bench_top + 26, lx + 20, floor_y - 4], fill=tuple(c - 25 for c in bench))

    art = a["img"].copy()
    art.thumbnail((560, 660), Image.LANCZOS)
    mat = max(18, int(min(art.size) * 0.07))
    frame = 12
    framed = Image.new("RGB", (art.width + 2 * (mat + frame), art.height + 2 * (mat + frame)), (25, 25, 25))
    framed.paste((250, 249, 246), (frame, frame, framed.width - frame, framed.height - frame))
    framed.paste(art, (frame + mat, frame + mat))
    x = (PIN_W - framed.width) // 2
    y = max(80, bench_top - 110 - framed.height)
    with_shadow(canvas, framed, x, y, radius=16, offset=(8, 18), alpha=110)
    return canvas


def detail_pin(a, rng, title):
    img = a["img"]
    w, h = img.size
    # a 2:3 crop showing roughly a third of the painting, at a seeded position
    ch = int(min(h, w * 1.5) * rng.uniform(0.42, 0.6))
    cw = int(ch / 1.5)
    x = rng.randint(0, max(0, w - cw))
    y = rng.randint(0, max(0, h - ch))
    crop = img.crop((x, y, x + cw, y + ch)).resize((PIN_W, PIN_H), Image.LANCZOS)
    band = Image.linear_gradient("L").resize((PIN_W, 360))
    crop.paste((0, 0, 0), (0, PIN_H - 360), band.point(lambda v: int(v * 0.75)))
    d = ImageDraw.Draw(crop)
    d.text((70, PIN_H - 150), "Detail", font=font(28), fill=(225, 222, 218), anchor="ls")
    d.text((70, PIN_H - 85), title, font=fit_text(d, title, PIN_W - 140, 56, serif=True), fill=(255, 255, 255),
           anchor="ls")
    return crop


def render_pin(a, variant, cycle, artist):
    rng = seeded(a["slug"], variant, cycle)
    if variant == "poster":
        return poster_pin(a, artist, dark=cycle % 2 == 1)
    if variant == "poster_dark":
        return poster_pin(a, artist, dark=cycle % 2 == 0)
    if variant in ("wall", "wall_alt"):
        light_walls = [w for w in WALLS if sum(w) > 300]
        return wall_pin(a, rng.choice(WALLS if variant == "wall_alt" else light_walls))
    return detail_pin(a, rng, a["title"])


def pin_copy(a, variant, cycle, artist):
    """Pinterest is a search engine: titles and descriptions are written around what buyers type."""
    rng = seeded("copy", a["slug"], variant, cycle)
    colours = a["colours"] or ["colourful"]
    c1 = colours[0]
    palette = " and ".join(colours[:2])
    room = rng.choice(a["rooms"])
    mood = rng.choice(a["mood"]) if a["mood"] else rng.choice(["modern", "contemporary", "minimal"])
    t = a["title"]
    titles = {
        "poster": [f"{t} — {c1} abstract wall art print", f"{palette.capitalize()} abstract art print: {t}"],
        "poster_dark": [f"{mood.capitalize()} abstract painting print — {t}", f"{t} | modern abstract art"],
        "wall": [f"{c1.capitalize()} abstract art for the {room}", f"{t} styled in a {room}"],
        "wall_alt": [f"{mood.capitalize()} wall art idea for your {room}", f"Abstract art above a bench: {t}"],
        "detail": [f"Texture close-up — {t}", f"Painterly texture detail in {palette}"],
        "detail_alt": [f"Up close: {t}, abstract painting", f"{c1.capitalize()} brushwork detail — {t}"],
    }
    title = rng.choice(titles[variant])[:100]
    intro = a["description"] or f"{t} is an original abstract painting by {artist} in {palette}."
    tags = [f"{c1} abstract art", f"{room} wall art", "abstract art print", "modern art print",
            f"{mood} wall decor", "contemporary painting"] + list(a["keywords"])
    desc = (f"{intro} Fine art print by {artist}, painted in Barcelona and shipped worldwide. "
            f"Perfect for a {room}. " + " · ".join(dict.fromkeys(tags)))
    return title, desc[:500]


# ---------------------------------------------------------------- pin schedule

def schedule_pins(artworks, cfg, today):
    """Greedy drip: every pin has an earliest date; each day releases at most pins_per_day."""
    per_day = int(cfg.get("pins_per_day", 3))
    recycle = int(cfg.get("recycle_after_days", 90))
    cycles = int(cfg.get("max_cycles", 6))
    start = to_date(cfg.get("pin_start_date", today))
    candidates = []
    for a in artworks:
        for cycle in range(cycles):
            for v, variant in enumerate(VARIANTS):
                earliest = max(start, a["added"] + dt.timedelta(days=cycle * recycle + VARIANT_OFFSET_DAYS[v]))
                if earliest <= today:
                    candidates.append((earliest, a["slug"], cycle, v, a, variant))
    candidates.sort(key=lambda c: c[:4])

    released, used = [], {}
    day = start
    for earliest, _, cycle, _, a, variant in candidates:
        day = max(day, earliest)
        while used.get(day, 0) >= per_day:
            day += dt.timedelta(days=1)
        if day > today:
            break
        used[day] = used.get(day, 0) + 1
        released.append({"date": day, "artwork": a, "variant": variant, "cycle": cycle,
                         "id": f"{a['slug']}-{variant}-{cycle}"})
    return released


# ---------------------------------------------------------------- site

CSS = """
:root{--bg:#f6f4f0;--fg:#1d1d1f;--muted:#6d6a66;--line:#e2ded7;--accent:#1d1d1f}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 Georgia,'Times New Roman',serif}
a{color:inherit}img{max-width:100%;height:auto;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{display:flex;justify-content:space-between;align-items:center;padding:26px 0;gap:16px;flex-wrap:wrap}
header .name{font-size:22px;text-decoration:none;letter-spacing:.02em}
nav a{margin-left:20px;text-decoration:none;font:14px/1 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
nav a:first-child{margin-left:0}
.hero{padding:40px 0 30px;max-width:720px}
.hero h1{font-weight:400;font-size:clamp(30px,5vw,48px);line-height:1.15;margin:0 0 12px}
.hero p{color:var(--muted);margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:36px 28px;padding:20px 0 60px}
.card{text-decoration:none}.card img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#e9e5df}
.card h3{font-weight:400;font-size:18px;margin:12px 0 2px}.card p{margin:0;color:var(--muted);font:14px system-ui,sans-serif}
.art{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:48px;padding:20px 0 50px}
.art h1{font-weight:400;font-size:clamp(28px,4vw,40px);margin:0 0 6px;line-height:1.2}
.meta{color:var(--muted);font:15px system-ui,sans-serif;margin-bottom:22px}
.prices{width:100%;border-collapse:collapse;font:15px system-ui,sans-serif;margin:20px 0}
.prices td{padding:10px 0;border-bottom:1px solid var(--line)}.prices td:last-child{text-align:right}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:14px 22px;margin:6px 8px 0 0;font:15px system-ui,sans-serif;letter-spacing:.03em}
.btn.ghost{background:transparent;color:var(--fg);border:1px solid var(--fg)}
.note{font:14px system-ui,sans-serif;color:var(--muted);margin-top:18px}
.mock{margin-top:28px}
h2{font-weight:400;font-size:24px;margin:10px 0 0}
footer{border-top:1px solid var(--line);padding:30px 0 50px;color:var(--muted);font:14px system-ui,sans-serif}
footer a{margin-right:16px}
.prose{max-width:680px;padding:20px 0 60px}
@media (max-width:820px){.art{grid-template-columns:1fr;gap:26px}nav a{margin-left:14px}}
"""


def page(cfg, title, description, body, root, canonical, image=None, jsonld=None):
    head_extra = ""
    if cfg.get("pinterest_verify"):
        head_extra += f'<meta name="p:domain_verify" content="{esc(cfg["pinterest_verify"])}">\n'
    if cfg.get("google_verify"):
        head_extra += f'<meta name="google-site-verification" content="{esc(cfg["google_verify"])}">\n'
    if image:
        head_extra += f'<meta property="og:image" content="{esc(image)}">\n'
    if jsonld:
        head_extra += f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
    links = [f'<a href="{root}">Work</a>', f'<a href="{root}about/">About</a>']
    footer_links = ""
    if cfg.get("instagram"):
        footer_links += f'<a href="https://instagram.com/{esc(cfg["instagram"])}">Instagram</a>'
    if cfg.get("contact_email"):
        footer_links += f'<a href="mailto:{esc(cfg["contact_email"])}">{esc(cfg["contact_email"])}</a>'
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}"><meta property="og:type" content="website">
<link rel="alternate" type="application/rss+xml" title="New work" href="{root}feeds/pinterest.xml">
<link rel="stylesheet" href="{root}style.css">
{head_extra}</head><body><div class="wrap">
<header><a class="name" href="{root}">{esc(cfg['artist_name'])}</a><nav>{''.join(links)}</nav></header>
{body}
<footer>{footer_links}<p>© {dt.date.today().year} {esc(cfg['artist_name'])} · {esc(cfg.get('location', ''))}</p></footer>
</div></body></html>"""


def money(value, currency):
    return f"{float(value):,.2f} {currency}".replace(".00 ", " ")


def build_site(artworks, cfg, out, released):
    base = cfg["site_url"].rstrip("/") + "/"
    currency = cfg.get("currency", "EUR")
    artist = cfg["artist_name"]
    (out / "style.css").write_text(CSS)
    (out / ".nojekyll").write_text("")

    for a in artworks:
        d = out / "art" / a["slug"]
        web = a["img"].copy()
        web.thumbnail((1800, 1800), Image.LANCZOS)
        save_jpg(web, d / "artwork.jpg", 86)
        thumb = ImageOps.fit(a["img"], (640, 800), Image.LANCZOS)
        save_jpg(thumb, d / "thumb.jpg", 82)
        save_jpg(wall_pin(a, WALLS[0]), d / "in-room.jpg", 84)

    # index
    cards = "".join(
        f'<a class="card" href="art/{a["slug"]}/"><img src="art/{a["slug"]}/thumb.jpg" loading="lazy" '
        f'alt="{esc(a["title"])} — abstract painting in {esc(", ".join(a["colours"]))} by {esc(artist)}">'
        f'<h3>{esc(a["title"])}</h3><p>{esc(", ".join(str(x) for x in [a["year"], a["medium"]] if x))}</p></a>'
        for a in artworks) or "<p>New work coming soon.</p>"
    body = (f'<section class="hero"><h1>{esc(cfg.get("tagline", ""))}</h1>'
            f'<p>Original paintings and fine art prints by {esc(artist)}. Shipping worldwide.</p></section>'
            f'<section class="grid">{cards}</section>')
    first_image = f"{base}art/{artworks[0]['slug']}/artwork.jpg" if artworks else None
    site_ld = {"@context": "https://schema.org", "@type": "Person", "name": artist, "jobTitle": "Abstract artist",
               "url": base, "address": cfg.get("location", "")}
    (out / "index.html").write_text(page(cfg, cfg["site_title"], cfg.get("tagline", ""), body, "./", base,
                                         first_image, site_ld))

    # about
    bio_text = "\n".join(l for l in cfg.get("bio", "").splitlines() if not l.strip().startswith("#"))
    bio = "".join(f"<p>{esc(p)}</p>" for p in bio_text.split("\n\n") if p.strip())
    contact = (f'<p>Commissions, trade and interior design enquiries: '
               f'<a href="mailto:{esc(cfg["contact_email"])}">{esc(cfg["contact_email"])}</a></p>'
               if cfg.get("contact_email") else "")
    about = f'<section class="prose"><h1 style="font-weight:400">About</h1>{bio}{contact}</section>'
    (out / "about").mkdir(exist_ok=True)
    (out / "about" / "index.html").write_text(
        page(cfg, f"About {artist}", f"About {artist}, abstract artist in {cfg.get('location', '')}", about,
             "../", base + "about/"))

    # artwork pages
    for i, a in enumerate(artworks):
        url = f"{base}art/{a['slug']}/"
        img_url = url + "artwork.jpg"
        palette = ", ".join(a["colours"])
        desc = a["description"] or (f"{a['title']} — an original abstract painting by {artist} in {palette}. "
                                    f"Available as a fine art print, shipped worldwide.")
        meta = " · ".join(str(x) for x in [a["year"], a["medium"], a["original_size"]] if x)
        prices = ""
        if a["prices"]:
            rows = "".join(f'<tr><td>{esc(p.get("size", ""))}</td><td>{money(p["price"], currency)}</td></tr>'
                           for p in a["prices"] if "price" in p)
            prices = f'<table class="prices">{rows}</table>'
        links = a["buy_links"] if a["buy_links"] is not None else cfg.get("default_buy_links") or []
        buttons = "".join(f'<a class="btn" href="{esc(l["url"])}">{esc(l.get("label", "Buy print"))}</a>'
                          for l in links if l.get("url"))
        if cfg.get("contact_email"):
            subject = f"Enquiry: {a['title']}"
            buttons += (f'<a class="btn ghost" href="mailto:{esc(cfg["contact_email"])}?subject='
                        f'{esc(subject.replace(" ", "%20"))}">Enquire</a>')
        status = ""
        if a["sold"]:
            status = '<p class="note">Original: sold. Prints available.</p>'
        elif a["original_available"]:
            status = '<p class="note">The original painting is available — enquire for price and shipping.</p>'
        others = [o for o in artworks if o is not a][:3]
        more = "".join(f'<a class="card" href="../{o["slug"]}/"><img src="../{o["slug"]}/thumb.jpg" loading="lazy" '
                       f'alt="{esc(o["title"])} by {esc(artist)}"><h3>{esc(o["title"])}</h3></a>' for o in others)
        body = f"""<article class="art">
<div><img src="artwork.jpg" alt="{esc(a['title'])} — abstract painting in {esc(palette)} by {esc(artist)}">
<img class="mock" src="in-room.jpg" loading="lazy" alt="{esc(a['title'])} framed above a bench in a {esc(a['rooms'][0])}"></div>
<div><h1>{esc(a['title'])}</h1><div class="meta">{esc(meta)}</div>
<p>{esc(desc)}</p>{prices}{buttons}{status}
<p class="note">Colours: {esc(palette)}. Suits a {esc(' or '.join(a['rooms'][:2]))}.</p></div>
</article>{'<h2>More work</h2><section class="grid">' + more + '</section>' if more else ''}"""
        offers = [{"@type": "Offer", "price": str(p["price"]), "priceCurrency": currency,
                   "availability": "https://schema.org/InStock", "name": p.get("size", ""), "url": url}
                  for p in a["prices"] if "price" in p]
        ld = {"@context": "https://schema.org", "@type": ["VisualArtwork", "Product"], "name": a["title"],
              "image": img_url, "url": url, "description": desc, "artform": "Painting",
              "artMedium": a["medium"] or None, "creator": {"@type": "Person", "name": artist},
              "brand": {"@type": "Brand", "name": artist}, "keywords": ", ".join(a["colours"] + a["mood"])}
        if offers:
            ld["offers"] = offers
        ld = {k: v for k, v in ld.items() if v}
        (out / "art" / a["slug"] / "index.html").write_text(
            page(cfg, f"{a['title']} — abstract art print by {artist}", desc[:160], body, "../../", url,
                 img_url, ld))

    # sitemap + robots
    urls = [base, base + "about/"] + [f"{base}art/{a['slug']}/" for a in artworks]
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{esc(u)}</loc></url>" for u in urls) + "</urlset>\n")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")


def build_feeds(artworks, cfg, out, released):
    base = cfg["site_url"].rstrip("/") + "/"
    artist = cfg["artist_name"]
    feeds = out / "feeds"
    pins_dir = out / "pins"
    feeds.mkdir(parents=True, exist_ok=True)

    # Pinterest RSS: newest 100 released pins (Pinterest only reads recent items)
    items = []
    for pin in sorted(released, key=lambda p: (p["date"], p["id"]), reverse=True)[:100]:
        a = pin["artwork"]
        path = pins_dir / f"{pin['id']}.jpg"
        save_jpg(render_pin(a, pin["variant"], pin["cycle"], artist), path, 86)
        title, desc = pin_copy(a, pin["variant"], pin["cycle"], artist)
        link = (f"{base}art/{a['slug']}/?utm_source=pinterest&utm_medium=pin"
                f"&utm_campaign={pin['variant']}-{pin['cycle']}")
        when = dt.datetime.combine(pin["date"], dt.time(9, 0), dt.timezone.utc)
        img_url = f"{base}pins/{pin['id']}.jpg"
        items.append(f"""<item><title>{esc(title)}</title><link>{esc(link)}</link>
<description>{esc(desc)}</description><pubDate>{format_datetime(when)}</pubDate>
<guid isPermaLink="false">{esc(pin['id'])}</guid>
<enclosure url="{esc(img_url)}" length="{path.stat().st_size}" type="image/jpeg"/>
<media:content url="{esc(img_url)}" medium="image" type="image/jpeg"/></item>""")
    (feeds / "pinterest.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>
<title>{esc(cfg['site_title'])}</title><link>{esc(base)}</link>
<description>{esc(cfg.get('tagline', ''))}</description><language>en</language>
{''.join(items)}
</channel></rss>
""")

    # Google Merchant Center free listings (artworks with a price only)
    currency = cfg.get("currency", "EUR")
    products = []
    for a in artworks:
        priced = [p for p in a["prices"] if "price" in p]
        if not priced:
            continue
        cheapest = min(priced, key=lambda p: float(p["price"]))
        desc = a["description"] or f"Abstract art print in {', '.join(a['colours'])} by {artist}."
        products.append(f"""<item><g:id>{esc(a['slug'])}</g:id>
<title>{esc(a['title'])} — abstract art print by {esc(artist)}</title>
<description>{esc(desc)}</description><link>{esc(base)}art/{esc(a['slug'])}/</link>
<g:image_link>{esc(base)}art/{esc(a['slug'])}/artwork.jpg</g:image_link>
<g:additional_image_link>{esc(base)}art/{esc(a['slug'])}/in-room.jpg</g:additional_image_link>
<g:price>{float(cheapest['price']):.2f} {currency}</g:price><g:availability>in_stock</g:availability>
<g:condition>new</g:condition><g:brand>{esc(artist)}</g:brand><g:identifier_exists>no</g:identifier_exists>
<g:google_product_category>500044</g:google_product_category><g:color>{esc('/'.join(a['colours'][:3]))}</g:color></item>""")
    (feeds / "google-products.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0"><channel>
<title>{esc(cfg['site_title'])}</title><link>{esc(base)}</link><description>Art prints</description>
{''.join(products)}
</channel></rss>
""")


def write_pin_log(released, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "pin_id", "artwork", "variant", "cycle"])
        for p in sorted(released, key=lambda p: (p["date"], p["id"])):
            w.writerow([p["date"].isoformat(), p["id"], p["artwork"]["title"], p["variant"], p["cycle"]])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artworks", type=Path, default=ENGINE / "artworks")
    ap.add_argument("--config", type=Path, default=ENGINE / "config.yml")
    ap.add_argument("--out", type=Path, default=ENGINE / "_site")
    ap.add_argument("--log", type=Path, default=ENGINE / "logs" / "pins-released.csv")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    artworks = load_artworks(args.artworks)
    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)

    released = schedule_pins(artworks, cfg, args.today)
    build_site(artworks, cfg, args.out, released)
    build_feeds(artworks, cfg, args.out, released)
    write_pin_log(released, args.log)

    todays = [p for p in released if p["date"] == args.today]
    print(f"Built {len(artworks)} artworks -> {args.out}")
    print(f"Pins released so far: {len(released)} ({len(todays)} today)")


if __name__ == "__main__":
    main()
