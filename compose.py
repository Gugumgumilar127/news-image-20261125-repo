# compose.py - renders the one-page world-news image.
# Flat vector style: cream paper, navy ink, red accents, a giant
# serif masthead, a proportional region bar, 16 illustrated lead
# stories, a dot-grid world map with numbered pins, a DATE CHECK
# box, a 34-story numbered digest and a dated footer.
# Rendering is fully deterministic: same input, same bytes.
# NOTE: compose.py is a build-time tool only. The shipped main.py
# does not import it; it copies the pre-rendered entry.png asset.

import math
import sys

from PIL import Image, ImageColor, ImageDraw, ImageFont

import mapdata
import stories

W = 1024
H = 1024
MARGIN = 24
CW = W - 2 * MARGIN  # content width = 976

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
CREAM = "#F7F1E3"
PAPER = "#FFFDF6"
INK = "#1B2A4A"
RED = "#C0392B"
GRAY = "#6B6252"
LINE = "#D8CFBB"
AMBER = "#E8A33D"
GREEN = "#2E7D4F"

_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _cache[key]


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def reg(size):
    return font("DejaVuSans.ttf", size)


def rgb(hexcolor):
    return ImageColor.getrgb(hexcolor)


def tint(hexcolor, frac=0.82):
    """Blend a colour towards the cream background."""
    r, g, b = rgb(hexcolor)
    cr, cg, cb = rgb(CREAM)
    return (int(r + (cr - r) * frac), int(g + (cg - g) * frac),
            int(b + (cb - b) * frac))


def wrap(d, text, fnt, maxw):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


# -----------------------------------------------------------------
# Flat vector icon glyphs. Each draws inside a square box of side s
# at (x, y) using navy ink plus one accent colour.
# -----------------------------------------------------------------

def _p(d, pts, fill=None, outline=None, width=1):
    d.polygon([(pts[i], pts[i + 1]) for i in range(0, len(pts), 2)],
              fill=fill, outline=outline, width=width)


def icon_summit(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 4 * u, y + 42 * u, x + 19 * u, y + 16 * u,
           x + 34 * u, y + 42 * u], fill=ink)
    _p(d, [x + 20 * u, y + 42 * u, x + 36 * u, y + 12 * u,
           x + 50 * u, y + 42 * u], fill=ink)
    _p(d, [x + 36 * u, y + 12 * u, x + 32 * u, y + 19 * u,
           x + 40 * u, y + 19 * u], fill=rgb(CREAM))
    d.line([x + 36 * u, y + 12 * u, x + 36 * u, y + 5 * u],
           fill=acc, width=max(2, int(2 * u)))
    _p(d, [x + 36 * u, y + 5 * u, x + 44 * u, y + 7.5 * u,
           x + 36 * u, y + 10 * u], fill=acc)


def icon_gavel(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 10 * u, y + 14 * u, x + 26 * u, y + 6 * u,
           x + 32 * u, y + 14 * u, x + 16 * u, y + 22 * u], fill=ink)
    _p(d, [x + 14 * u, y + 26 * u, x + 30 * u, y + 18 * u,
           x + 36 * u, y + 26 * u, x + 20 * u, y + 34 * u], fill=ink)
    d.line([x + 24 * u, y + 24 * u, x + 40 * u, y + 40 * u],
           fill=acc, width=max(2, int(4 * u)))
    d.line([x + 8 * u, y + 47 * u, x + 46 * u, y + 47 * u],
           fill=ink, width=max(2, int(3 * u)))


def icon_tank(d, x, y, s, ink, acc):
    u = s / 54.0
    d.rounded_rectangle([x + 4 * u, y + 31 * u, x + 50 * u, y + 43 * u],
                        radius=6 * u, outline=ink, width=max(2, int(3 * u)))
    _p(d, [x + 10 * u, y + 31 * u, x + 16 * u, y + 22 * u,
           x + 40 * u, y + 22 * u, x + 46 * u, y + 31 * u], fill=ink)
    d.rectangle([x + 21 * u, y + 14 * u, x + 35 * u, y + 23 * u], fill=ink)
    d.line([x + 35 * u, y + 17 * u, x + 51 * u, y + 17 * u],
           fill=ink, width=max(2, int(3 * u)))
    for cx in (13, 22, 31, 40):
        d.ellipse([x + (cx - 3) * u, y + 34 * u, x + (cx + 3) * u,
                   y + 40 * u], fill=acc)


def icon_burst(d, x, y, s, ink, acc):
    cx, cy = x + s / 2, y + s / 2
    pts = []
    for i in range(24):
        ang = math.pi * i / 12.0
        r = (21 if i % 2 == 0 else 9) * s / 54.0
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=acc)
    d.ellipse([cx - 5 * s / 54.0, cy - 5 * s / 54.0,
               cx + 5 * s / 54.0, cy + 5 * s / 54.0], fill=rgb(CREAM))


def icon_bridge(d, x, y, s, ink, acc):
    u = s / 54.0
    d.rectangle([x + 13 * u, y + 12 * u, x + 18 * u, y + 38 * u], fill=ink)
    d.rectangle([x + 36 * u, y + 12 * u, x + 41 * u, y + 38 * u], fill=ink)
    d.line([x + 4 * u, y + 20 * u, x + 15 * u, y + 12 * u,
            x + 27 * u, y + 19 * u, x + 39 * u, y + 12 * u,
            x + 50 * u, y + 20 * u], fill=acc, width=max(2, int(2 * u)))
    d.line([x + 3 * u, y + 38 * u, x + 51 * u, y + 38 * u],
           fill=ink, width=max(2, int(4 * u)))
    for vx in (21, 27, 33):
        d.line([x + vx * u, y + 24 * u, x + vx * u, y + 38 * u],
               fill=ink, width=max(1, int(1.6 * u)))
    d.line([x + 6 * u, y + 45 * u, x + 48 * u, y + 45 * u],
           fill=acc, width=max(2, int(2 * u)))


def icon_virus(d, x, y, s, ink, acc):
    u = s / 54.0
    cx, cy = x + 27 * u, y + 27 * u
    for i in range(8):
        ang = math.pi * i / 4.0
        x1 = cx + 10 * u * math.cos(ang)
        y1 = cy + 10 * u * math.sin(ang)
        x2 = cx + 19 * u * math.cos(ang)
        y2 = cy + 19 * u * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=ink, width=max(2, int(3 * u)))
        d.ellipse([x2 - 3.4 * u, y2 - 3.4 * u, x2 + 3.4 * u,
                   y2 + 3.4 * u], fill=acc)
    d.ellipse([cx - 11 * u, cy - 11 * u, cx + 11 * u, cy + 11 * u],
              fill=ink)
    for dx, dy in ((-4, -3), (4, 1), (-1, 5)):
        d.ellipse([cx + (dx - 1.8) * u, cy + (dy - 1.8) * u,
                   cx + (dx + 1.8) * u, cy + (dy + 1.8) * u],
                  fill=rgb(CREAM))


def icon_shield(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 27 * u, y + 5 * u, x + 45 * u, y + 11 * u,
           x + 45 * u, y + 27 * u, x + 27 * u, y + 49 * u,
           x + 9 * u, y + 27 * u, x + 9 * u, y + 11 * u], fill=ink)
    d.line([x + 18 * u, y + 27 * u, x + 25 * u, y + 34 * u,
            x + 37 * u, y + 19 * u], fill=rgb(CREAM),
           width=max(2, int(4 * u)), joint="curve")


def icon_swirl(d, x, y, s, ink, acc):
    u = s / 54.0
    d.arc([x + 10 * u, y + 8 * u, x + 44 * u, y + 42 * u],
          start=300, end=200, fill=ink, width=max(2, int(4 * u)))
    d.arc([x + 16 * u, y + 15 * u, x + 39 * u, y + 40 * u],
          start=120, end=30, fill=acc, width=max(2, int(4 * u)))
    d.ellipse([x + 24 * u, y + 24 * u, x + 30 * u, y + 30 * u], fill=ink)
    d.line([x + 12 * u, y + 47 * u, x + 42 * u, y + 47 * u],
           fill=acc, width=max(2, int(2.4 * u)))


def icon_chart(d, x, y, s, ink, acc):
    u = s / 54.0
    d.line([x + 9 * u, y + 7 * u, x + 9 * u, y + 45 * u,
            x + 47 * u, y + 45 * u], fill=ink, width=max(2, int(2.4 * u)))
    for bx, bh in ((15, 11), (25, 18), (35, 26)):
        d.rectangle([x + bx * u, y + (45 - bh) * u, x + (bx + 6) * u,
                     y + 45 * u], fill=tint(stories.REGION_COLORS["AMERICAS"], 0.35))
    d.line([x + 13 * u, y + 36 * u, x + 23 * u, y + 29 * u,
            x + 33 * u, y + 20 * u, x + 45 * u, y + 11 * u],
           fill=acc, width=max(2, int(3 * u)), joint="curve")
    d.ellipse([x + 42.5 * u, y + 8.5 * u, x + 47.5 * u, y + 13.5 * u],
              fill=acc)


def icon_controller(d, x, y, s, ink, acc):
    u = s / 54.0
    d.rounded_rectangle([x + 5 * u, y + 17 * u, x + 49 * u, y + 39 * u],
                        radius=9 * u, fill=ink)
    d.rectangle([x + 15 * u, y + 23 * u, x + 21 * u, y + 33 * u],
                fill=rgb(CREAM))
    d.rectangle([x + 13 * u, y + 25 * u, x + 23 * u, y + 31 * u],
                fill=rgb(CREAM))
    d.ellipse([x + 33 * u, y + 21 * u, x + 39 * u, y + 27 * u], fill=acc)
    d.ellipse([x + 40 * u, y + 28 * u, x + 46 * u, y + 34 * u],
              fill=rgb(AMBER))


def icon_palette(d, x, y, s, ink, acc):
    u = s / 54.0
    d.ellipse([x + 9 * u, y + 9 * u, x + 45 * u, y + 45 * u], fill=ink)
    d.ellipse([x + 30 * u, y + 27 * u, x + 39 * u, y + 36 * u],
              fill=rgb(CREAM))
    for dx, dy, c in ((17, 15, acc), (27, 12, rgb(AMBER)),
                      (15, 26, rgb(GREEN))):
        d.ellipse([x + dx * u, y + dy * u, x + (dx + 6) * u,
                   y + (dy + 6) * u], fill=c)


def icon_bolt(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 31 * u, y + 5 * u, x + 15 * u, y + 30 * u,
           x + 24 * u, y + 30 * u, x + 19 * u, y + 49 * u,
           x + 39 * u, y + 21 * u, x + 29 * u, y + 21 * u],
       fill=rgb(AMBER), outline=ink, width=max(1, int(1.6 * u)))


def icon_ballot(d, x, y, s, ink, acc):
    u = s / 54.0
    d.rectangle([x + 18 * u, y + 7 * u, x + 36 * u, y + 35 * u],
                fill=rgb(PAPER), outline=ink, width=max(2, int(2 * u)))
    d.line([x + 22 * u, y + 20 * u, x + 26 * u, y + 24 * u,
            x + 33 * u, y + 14 * u], fill=acc,
           width=max(2, int(3 * u)), joint="curve")
    d.rectangle([x + 9 * u, y + 33 * u, x + 45 * u, y + 47 * u], fill=ink)
    d.line([x + 15 * u, y + 33 * u, x + 39 * u, y + 33 * u],
           fill=acc, width=max(2, int(3 * u)))


def icon_leaf(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 40 * u, y + 8 * u, x + 45 * u, y + 26 * u,
           x + 36 * u, y + 42 * u, x + 20 * u, y + 46 * u,
           x + 9 * u, y + 36 * u, x + 12 * u, y + 18 * u,
           x + 24 * u, y + 9 * u], fill=rgb(GREEN))
    d.line([x + 14 * u, y + 42 * u, x + 38 * u, y + 13 * u],
           fill=rgb(CREAM), width=max(2, int(2.2 * u)))
    d.line([x + 14 * u, y + 42 * u, x + 9 * u, y + 49 * u],
           fill=ink, width=max(2, int(2.4 * u)))


def icon_tanker(d, x, y, s, ink, acc):
    u = s / 54.0
    # hull
    _p(d, [x + 5 * u, y + 31 * u, x + 49 * u, y + 31 * u,
           x + 44 * u, y + 41 * u, x + 11 * u, y + 41 * u], fill=ink)
    # deck cargo blocks
    d.rectangle([x + 13 * u, y + 25 * u, x + 27 * u, y + 31 * u],
                fill=acc)
    d.rectangle([x + 16 * u, y + 19 * u, x + 25 * u, y + 25 * u],
                fill=ink)
    # bridge tower
    d.rectangle([x + 35 * u, y + 15 * u, x + 44 * u, y + 31 * u],
                fill=ink)
    d.rectangle([x + 37.5 * u, y + 18.5 * u, x + 41.5 * u, y + 22 * u],
                fill=rgb(CREAM))
    d.line([x + 39 * u, y + 15 * u, x + 39 * u, y + 9 * u],
           fill=ink, width=max(2, int(2 * u)))
    # waves
    d.arc([x + 6 * u, y + 42 * u, x + 18 * u, y + 50 * u],
          start=180, end=360, fill=acc, width=max(2, int(2 * u)))
    d.arc([x + 20 * u, y + 42 * u, x + 32 * u, y + 50 * u],
          start=180, end=360, fill=acc, width=max(2, int(2 * u)))
    d.arc([x + 34 * u, y + 42 * u, x + 46 * u, y + 50 * u],
          start=180, end=360, fill=acc, width=max(2, int(2 * u)))


def icon_football(d, x, y, s, ink, acc):
    u = s / 54.0
    cx, cy = x + 27 * u, y + 27 * u
    d.ellipse([x + 8 * u, y + 8 * u, x + 46 * u, y + 46 * u],
              fill=rgb(PAPER), outline=ink, width=max(2, int(2.2 * u)))
    # centre pentagon
    pts = []
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + 8 * u * math.cos(ang),
                    cy + 8 * u * math.sin(ang)))
    d.polygon(pts, fill=acc)
    # seams from pentagon vertices out to the rim
    for px, py in pts:
        dx, dy = px - cx, py - cy
        norm = math.hypot(dx, dy)
        d.line([px, py, cx + dx / norm * 18 * u,
                cy + dy / norm * 18 * u], fill=ink,
               width=max(1, int(1.8 * u)))
    # grass line
    d.line([x + 10 * u, y + 49 * u, x + 44 * u, y + 49 * u],
           fill=rgb(GREEN), width=max(2, int(2.4 * u)))


def icon_drone(d, x, y, s, ink, acc):
    u = s / 54.0
    for cx, cy in ((13, 13), (41, 13), (13, 41), (41, 41)):
        d.line([x + 27 * u, y + 27 * u, x + cx * u, y + cy * u],
               fill=ink, width=max(2, int(2.4 * u)))
    for cx, cy in ((13, 13), (41, 13), (13, 41), (41, 41)):
        d.ellipse([x + (cx - 6) * u, y + (cy - 3) * u,
                   x + (cx + 6) * u, y + (cy + 3) * u],
                  outline=ink, width=max(1, int(1.8 * u)))
    d.rounded_rectangle([x + 19 * u, y + 20 * u, x + 35 * u,
                         y + 34 * u], radius=3 * u, fill=ink)
    d.ellipse([x + 24 * u, y + 30 * u, x + 30 * u, y + 36 * u],
              fill=acc)


def icon_crate(d, x, y, s, ink, acc):
    u = s / 54.0
    d.rectangle([x + 5 * u, y + 15 * u, x + 49 * u, y + 43 * u],
                outline=ink, width=max(2, int(2.6 * u)))
    for vx in (13, 21, 29, 37):
        d.line([x + vx * u, y + 16 * u, x + vx * u, y + 42 * u],
               fill=ink, width=max(1, int(1.8 * u)))
    d.ellipse([x + 35 * u, y + 4 * u, x + 51 * u, y + 20 * u],
              fill=acc)
    d.line([x + 47 * u, y + 7 * u, x + 39 * u, y + 17 * u],
           fill=rgb(PAPER), width=max(1, int(1.8 * u)))
    d.ellipse([x + 39.5 * u, y + 6.5 * u, x + 43.5 * u,
               y + 10.5 * u], outline=rgb(PAPER),
              width=max(1, int(1.4 * u)))
    d.ellipse([x + 42.5 * u, y + 13.5 * u, x + 46.5 * u,
               y + 17.5 * u], outline=rgb(PAPER),
              width=max(1, int(1.4 * u)))


def icon_chip(d, x, y, s, ink, acc):
    u = s / 54.0
    for p in (14, 24, 34):
        d.line([x + p * u, y + 5 * u, x + p * u, y + 13 * u],
               fill=ink, width=max(2, int(2.2 * u)))
        d.line([x + p * u, y + 41 * u, x + p * u, y + 49 * u],
               fill=ink, width=max(2, int(2.2 * u)))
        d.line([x + 5 * u, y + p * u, x + 13 * u, y + p * u],
               fill=ink, width=max(2, int(2.2 * u)))
        d.line([x + 41 * u, y + p * u, x + 49 * u, y + p * u],
               fill=ink, width=max(2, int(2.2 * u)))
    d.rectangle([x + 13 * u, y + 13 * u, x + 41 * u, y + 41 * u],
                fill=ink)
    d.rectangle([x + 21 * u, y + 21 * u, x + 33 * u, y + 33 * u],
                outline=rgb(CREAM), width=max(1, int(1.8 * u)))
    d.ellipse([x + 24.5 * u, y + 24.5 * u, x + 29.5 * u,
               y + 29.5 * u], fill=acc)


def icon_lock(d, x, y, s, ink, acc):
    u = s / 54.0
    d.arc([x + 15 * u, y + 5 * u, x + 39 * u, y + 32 * u],
          start=180, end=360, fill=ink, width=max(2, int(3.4 * u)))
    d.line([x + 15 * u, y + 18 * u, x + 15 * u, y + 26 * u],
           fill=ink, width=max(2, int(3.4 * u)))
    d.line([x + 39 * u, y + 18 * u, x + 39 * u, y + 26 * u],
           fill=ink, width=max(2, int(3.4 * u)))
    d.rounded_rectangle([x + 10 * u, y + 24 * u, x + 44 * u,
                         y + 48 * u], radius=3 * u, fill=ink)
    d.ellipse([x + 24 * u, y + 31 * u, x + 30 * u, y + 37 * u],
              fill=acc)
    d.line([x + 27 * u, y + 35 * u, x + 27 * u, y + 42 * u],
           fill=acc, width=max(2, int(2.6 * u)))


def icon_tower(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 20 * u, y + 48 * u, x + 23 * u, y + 12 * u,
           x + 31 * u, y + 12 * u, x + 34 * u, y + 48 * u],
       fill=ink)
    d.line([x + 27 * u, y + 12 * u, x + 27 * u, y + 5 * u],
           fill=ink, width=max(2, int(2 * u)))
    d.ellipse([x + 25 * u, y + 3 * u, x + 29 * u, y + 7 * u],
              fill=acc)
    for wy in (18, 25, 32, 39):
        d.rectangle([x + 24.5 * u, y + wy * u, x + 29.5 * u,
                     y + (wy + 3.5) * u], fill=rgb(CREAM))
    d.line([x + 14 * u, y + 48 * u, x + 40 * u, y + 48 * u],
           fill=acc, width=max(2, int(2.4 * u)))


def icon_medal(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 16 * u, y + 5 * u, x + 24 * u, y + 5 * u,
           x + 27 * u, y + 24 * u, x + 21 * u, y + 26 * u],
       fill=acc)
    _p(d, [x + 38 * u, y + 5 * u, x + 30 * u, y + 5 * u,
           x + 27 * u, y + 24 * u, x + 33 * u, y + 26 * u],
       fill=ink)
    d.ellipse([x + 14 * u, y + 22 * u, x + 40 * u, y + 48 * u],
              fill=rgb(AMBER), outline=ink,
              width=max(1, int(1.6 * u)))
    cx, cy = x + 27 * u, y + 35 * u
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = (7.5 if i % 2 == 0 else 3.2) * u
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=rgb(PAPER))


def icon_rocket(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 27 * u, y + 4 * u, x + 35 * u, y + 14 * u,
           x + 35 * u, y + 34 * u, x + 19 * u, y + 34 * u,
           x + 19 * u, y + 14 * u], fill=ink)
    d.ellipse([x + 23 * u, y + 15 * u, x + 31 * u, y + 23 * u],
              fill=rgb(CREAM))
    _p(d, [x + 19 * u, y + 28 * u, x + 11 * u, y + 38 * u,
           x + 19 * u, y + 38 * u], fill=acc)
    _p(d, [x + 35 * u, y + 28 * u, x + 43 * u, y + 38 * u,
           x + 35 * u, y + 38 * u], fill=acc)
    _p(d, [x + 23 * u, y + 38 * u, x + 31 * u, y + 38 * u,
           x + 27 * u, y + 49 * u], fill=rgb(AMBER))


def icon_trophy(d, x, y, s, ink, acc):
    u = s / 54.0
    d.arc([x + 5 * u, y + 10 * u, x + 21 * u, y + 30 * u],
          start=90, end=300, fill=ink, width=max(2, int(2.6 * u)))
    d.arc([x + 33 * u, y + 10 * u, x + 49 * u, y + 30 * u],
          start=240, end=90, fill=ink, width=max(2, int(2.6 * u)))
    _p(d, [x + 16 * u, y + 8 * u, x + 38 * u, y + 8 * u,
           x + 36 * u, y + 26 * u, x + 18 * u, y + 26 * u],
       fill=rgb(AMBER), outline=ink, width=max(1, int(1.4 * u)))
    d.rectangle([x + 24 * u, y + 26 * u, x + 30 * u, y + 36 * u],
                fill=ink)
    d.rectangle([x + 18 * u, y + 36 * u, x + 36 * u, y + 41 * u],
                fill=ink)
    d.line([x + 14 * u, y + 47 * u, x + 40 * u, y + 47 * u],
           fill=acc, width=max(2, int(2.4 * u)))


def icon_radio(d, x, y, s, ink, acc):
    u = s / 54.0
    d.line([x + 14 * u, y + 22 * u, x + 42 * u, y + 5 * u],
           fill=ink, width=max(2, int(2 * u)))
    d.ellipse([x + 40 * u, y + 3 * u, x + 45 * u, y + 8 * u],
              fill=acc)
    d.rounded_rectangle([x + 7 * u, y + 20 * u, x + 47 * u,
                         y + 47 * u], radius=3 * u, fill=ink)
    d.ellipse([x + 12 * u, y + 27 * u, x + 26 * u, y + 41 * u],
              outline=rgb(CREAM), width=max(1, int(1.8 * u)))
    d.ellipse([x + 16.5 * u, y + 31.5 * u, x + 21.5 * u,
               y + 36.5 * u], fill=rgb(CREAM))
    for wy in (27, 32, 37):
        d.line([x + 31 * u, y + wy * u, x + 43 * u, y + wy * u],
               fill=acc if wy == 32 else rgb(CREAM),
               width=max(1, int(1.8 * u)))


def icon_cross(d, x, y, s, ink, acc):
    u = s / 54.0
    d.rectangle([x + 23 * u, y + 8 * u, x + 31 * u, y + 42 * u],
                fill=ink)
    d.rectangle([x + 14 * u, y + 17 * u, x + 40 * u, y + 24 * u],
                fill=ink)
    _p(d, [x + 10 * u, y + 48 * u, x + 16 * u, y + 41 * u,
           x + 38 * u, y + 41 * u, x + 44 * u, y + 48 * u],
       fill=acc)


def icon_candle(d, x, y, s, ink, acc):
    u = s / 54.0
    _p(d, [x + 27 * u, y + 6 * u, x + 31.5 * u, y + 14 * u,
           x + 27 * u, y + 21 * u, x + 22.5 * u, y + 14 * u],
       fill=rgb(AMBER), outline=acc, width=max(1, int(1.2 * u)))
    d.line([x + 27 * u, y + 21 * u, x + 27 * u, y + 24 * u],
           fill=ink, width=max(2, int(2 * u)))
    d.rectangle([x + 19 * u, y + 23 * u, x + 35 * u, y + 46 * u],
                fill=ink)
    d.ellipse([x + 24.5 * u, y + 28 * u, x + 29.5 * u,
               y + 33 * u], fill=rgb(CREAM))
    d.line([x + 13 * u, y + 48 * u, x + 41 * u, y + 48 * u],
           fill=acc, width=max(2, int(2.4 * u)))


ICONS = {"summit": icon_summit, "gavel": icon_gavel, "tank": icon_tank,
         "burst": icon_burst, "bridge": icon_bridge, "virus": icon_virus,
         "shield": icon_shield, "swirl": icon_swirl, "chart": icon_chart,
         "controller": icon_controller, "palette": icon_palette,
         "bolt": icon_bolt, "ballot": icon_ballot, "leaf": icon_leaf,
         "tanker": icon_tanker, "football": icon_football,
         "drone": icon_drone, "crate": icon_crate, "chip": icon_chip,
         "lock": icon_lock, "tower": icon_tower, "medal": icon_medal,
         "rocket": icon_rocket, "trophy": icon_trophy,
         "radio": icon_radio, "cross": icon_cross,
         "candle": icon_candle}


# -----------------------------------------------------------------
# Page sections
# -----------------------------------------------------------------

def draw_masthead(d):
    d.line([MARGIN, 12, W - MARGIN, 12], fill=rgb(INK), width=3)
    d.line([MARGIN, 17, W - MARGIN, 17], fill=rgb(INK), width=1)
    center_text(d, W / 2, 22, stories.MASTHEAD, serif(60), rgb(INK))
    center_text(d, W / 2, 90, stories.DATE_LINE, bold(23), rgb(INK))
    center_text(d, W / 2, 120, stories.SUBLINE, bold(12), rgb(RED))
    d.line([MARGIN, 140, W - MARGIN, 140], fill=rgb(INK), width=1)


def draw_region_bar(d):
    y0, y1 = 148, 168
    total = float(sum(stories.REGION_COUNTS.values()))
    x = float(MARGIN)
    labels = []
    for name in stories.REGION_ORDER:
        wseg = CW * stories.REGION_COUNTS[name] / total
        d.rectangle([x, y0, x + wseg - 2, y1],
                    fill=rgb(stories.REGION_COLORS[name]))
        labels.append((x + wseg / 2, name))
        x += wseg
    fnt = bold(10)
    placed = []
    limit = float(W - MARGIN)
    for cx, name in reversed(labels):
        text = "%s %d" % (name, stories.REGION_COUNTS[name])
        tw = d.textlength(text, font=fnt)
        lx = min(max(cx - tw / 2, MARGIN), limit - tw)
        placed.append((lx, text, name))
        limit = lx - 5
    for lx, text, name in placed:
        d.text((lx, y1 + 3), text, font=fnt,
               fill=rgb(stories.REGION_COLORS[name]))


def draw_tag_chip(d, right_x, y, tag):
    fnt = bold(8)
    tw = d.textlength(tag, font=fnt)
    w = tw + 9
    fill = rgb(RED) if tag == "CLAIM" else rgb(GREEN)
    d.rounded_rectangle([right_x - w, y, right_x, y + 13], radius=3,
                        fill=fill)
    d.text((right_x - w + 4.5, y + 2), tag, font=fnt,
           fill=rgb(PAPER))
    return w


CARD_H = 55  # v3: 16 leads in 8 rows (was 14 in 7 rows of 63px)


def draw_lead_story(d, st, x, y, w, warnings):
    d.rounded_rectangle([x, y, x + w, y + CARD_H], radius=4,
                        fill=rgb(PAPER), outline=rgb(LINE), width=1)
    color = stories.REGION_COLORS[st["region"]]
    # icon panel
    ix, iy, isz = x + 5, y + 5, 45
    d.rounded_rectangle([ix, iy, ix + isz, iy + isz], radius=5,
                        fill=tint(color, 0.78))
    ICONS[st["icon"]](d, ix, iy, isz, rgb(INK), rgb(RED))
    # number badge
    bx, by, br = x + 12, y + 10, 10
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=rgb(RED),
              outline=rgb(PAPER), width=2)
    nf = bold(10)
    num = str(st["num"])
    nw = d.textlength(num, font=nf)
    d.text((bx - nw / 2, by - 6.5), num, font=nf, fill=rgb(PAPER))
    # text block
    tx = x + 57
    tw = x + w - 6 - tx
    right = tx + tw
    kicker = "%s \u00b7 %s" % (st["region"], st["topic"])
    d.text((tx, y + 2), kicker, font=bold(9), fill=rgb(color))
    src_right = right
    if st["tag"]:
        src_right -= draw_tag_chip(d, right, y + 1, st["tag"]) + 5
    sf = reg(8)
    sw = d.textlength(st["source"], font=sf)
    d.text((src_right - sw, y + 2.5), st["source"], font=sf,
           fill=rgb(GRAY))
    hf = bold(11)
    hlines = wrap(d, st["headline"], hf, tw)
    if len(hlines) > 2:
        warnings.append("headline wraps >2: #%d" % st["num"])
    hy = y + 14
    for ln in hlines[:2]:
        d.text((tx, hy), ln, font=hf, fill=rgb(INK))
        hy += 12
    smax = 2 if len(hlines) == 1 else 1
    slines = wrap(d, st["summary"], reg(9), tw)
    if len(slines) > smax:
        warnings.append("summary wraps >%d: #%d (%d lines)"
                        % (smax, st["num"], len(slines)))
    sy = y + 15 + 12 * min(len(hlines), 2)
    for ln in slines[:smax]:
        d.text((tx, sy), ln, font=reg(9), fill=rgb("#333333"))
        sy += 11


def draw_lead_grid(d, warnings):
    y0 = 186
    colw = (CW - 12) / 2
    rowh = CARD_H
    for i, st in enumerate(stories.STORIES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (colw + 12)
        y = y0 + row * (rowh + 2)
        draw_lead_story(d, st, x, y, colw, warnings)


def resolve_pins(pins, box, mindist=15.0):
    """Deterministic repulsion so numbered badges never overlap."""
    x0, y0, x1, y1 = box
    pts = [[px, py] for px, py in pins]
    for _ in range(400):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                dist = math.hypot(dx, dy)
                if dist < mindist:
                    if dist < 0.01:
                        dx, dy, dist = 0.3, 0.7, math.hypot(0.3, 0.7)
                    push = (mindist - dist) / 2.0
                    ux, uy = dx / dist, dy / dist
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
                    moved = True
        for p in pts:
            p[0] = min(max(p[0], x0 + 8), x1 - 8)
            p[1] = min(max(p[1], y0 + 8), y1 - 8)
        if not moved:
            break
    return [(p[0], p[1]) for p in pts]


def draw_map(d):
    x0, y0, w, h = MARGIN, 661, 608, 132
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=4,
                        fill=rgb(PAPER), outline=rgb(LINE), width=1)
    d.text((MARGIN, 645), "THE MAP \u2014 PINS MATCH THE STORY NUMBERS",
           font=bold(11), fill=rgb(INK))
    cw = w / mapdata.GRID_W
    ch = h / mapdata.GRID_H
    for r, row in enumerate(mapdata.MAP_ROWS):
        for c, cell in enumerate(row):
            if cell == " ":
                continue
            region = mapdata.REGION_OF_CHAR[cell]
            cx, cy = mapdata.cell_xy(c, r, x0, y0, w, h)
            d.ellipse([cx - cw * 0.34, cy - ch * 0.34,
                       cx + cw * 0.34, cy + ch * 0.34],
                      fill=tint(stories.REGION_COLORS[region], 0.25))
    raw = [mapdata.pin_xy(st["pin"][0], st["pin"][1], x0, y0, w, h)
           for st in stories.STORIES]
    fixed = resolve_pins(raw, (x0, y0, x0 + w, y0 + h))
    nf = bold(8)
    for st, (rx, ry), (fx, fy) in zip(stories.STORIES, raw, fixed):
        d.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=rgb(INK))
        if math.hypot(fx - rx, fy - ry) > 5:
            d.line([rx, ry, fx, fy], fill=rgb(RED), width=1)
        r = 7
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=rgb(RED),
                  outline=rgb(PAPER), width=1)
        num = str(st["num"])
        nw = d.textlength(num, font=nf)
        d.text((fx - nw / 2, fy - 5), num, font=nf, fill=rgb(PAPER))


def draw_date_check(d):
    x0, y0, w = 644, 645, 356
    d.rounded_rectangle([x0, y0, x0 + w, y0 + 92], radius=4,
                        fill=tint(RED, 0.9), outline=rgb(RED), width=1)
    d.text((x0 + 9, y0 + 7), stories.DATE_CHECK_TITLE, font=bold(10),
           fill=rgb(RED))
    y = y0 + 25
    for item in stories.DATE_CHECK:
        d.text((x0 + 9, y), "\u2022 " + item, font=reg(9),
               fill=rgb(INK))
        y += 13.5


def draw_legend(d):
    x0, y0 = 644, 745
    d.rounded_rectangle([x0, y0, x0 + 356, y0 + 48], radius=4,
                        fill=rgb(PAPER), outline=rgb(LINE), width=1)
    rows = [["ASIA", "AMERICAS", "EUROPE", "MIDDLE EAST"],
            ["AFRICA", "WORLD", "OCEANIA"]]
    fnt = bold(9)
    for ri, row in enumerate(rows):
        x = x0 + 9
        y = y0 + 7 + ri * 20
        for name in row:
            d.rectangle([x, y + 1, x + 10, y + 11],
                        fill=rgb(stories.REGION_COLORS[name]))
            label = "%s %d" % (name, stories.REGION_COUNTS[name])
            d.text((x + 14, y), label, font=fnt, fill=rgb(INK))
            x += 14 + d.textlength(label, font=fnt) + 13


def digest_layout(d, fnt, lh, colw):
    """Flow digest items into 3 columns; return (placed, overflow)."""
    numw = 21
    placed = []
    col = 0
    y = 0.0
    maxy = 146
    for item in stories.DIGEST:
        text = item["headline"]
        reserve = 40 if item["tag"] else 0
        lines = wrap(d, text, fnt, colw - numw - reserve)
        need = max(1, len(lines)) * lh
        if y + need > maxy and col < 2:
            col += 1
            y = 0.0
        if y + need > maxy and col == 2:
            return placed, True
        placed.append((item, lines, col, y))
        y += need + 1.0
    return placed, False


def draw_digest(d, warnings):
    y0 = 801
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 22], fill=rgb(INK))
    d.text((MARGIN + 10, y0 + 4), stories.DIGEST_HEADER, font=bold(12),
           fill=rgb(PAPER))
    top = y0 + 28
    colw = (CW - 28) / 3
    size, lh = 9, 11.0
    placed, overflow = digest_layout(d, reg(size), lh, colw)
    if overflow:
        size, lh = 8, 10.5
        placed, overflow = digest_layout(d, reg(size), lh, colw)
    if overflow:
        warnings.append("digest overflow at font %d" % size)
    fnt = reg(size)
    nf = bold(size)
    for item, lines, col, yoff in placed:
        x = MARGIN + col * (colw + 14)
        y = top + yoff
        num = str(item["num"])
        d.text((x, y), num, font=nf, fill=rgb(RED))
        ly = y
        for ln in lines:
            d.text((x + 21, ly), ln, font=fnt, fill=rgb(INK))
            ly += lh
        if item["tag"]:
            lastw = d.textlength(lines[-1], font=fnt)
            draw_tag_chip(d, x + 21 + lastw + 38, ly - lh + 1,
                          item["tag"])


def draw_footer(d):
    d.line([MARGIN, 983, W - MARGIN, 983], fill=rgb(INK), width=1)
    center_text(d, W / 2, 988, stories.FOOTER, bold(11), rgb(INK))
    center_text(d, W / 2, 1006, stories.SOURCES, reg(9), rgb(GRAY))


def build_image():
    img = Image.new("RGB", (W, H), rgb(CREAM))
    d = ImageDraw.Draw(img)
    warnings = []
    draw_masthead(d)
    draw_region_bar(d)
    draw_lead_grid(d, warnings)
    draw_map(d)
    draw_date_check(d)
    draw_legend(d)
    draw_digest(d, warnings)
    draw_footer(d)
    return img, warnings


def render(path, quality=90):
    img, warnings = build_image()
    img.save(path, "JPEG", quality=quality)
    for w in warnings:
        print("compose warning: " + w, file=sys.stderr)
    return warnings


if __name__ == "__main__":
    render("entry.png")
    print("wrote entry.png")
