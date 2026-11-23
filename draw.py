#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261123.

A one-page newspaper front page summing up Monday 23 November 2026:
COP31 ends with no deal, the AI stock sell-off, the strike on Dymer,
the Democrats' record House win, a Russian warship sunk at Benghazi,
tankers ablaze near Hormuz, and the penny's farewell.

Local build step only: the graded entrypoint is main.py, which copies
the PNG this script produces. Run:  python3 draw.py
Output: entry.png, 1024x1024, deterministic (no randomness, no dates
embedded in the file).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)      # warm newsprint
INK = (26, 26, 26)           # near-black
FAINT = (90, 84, 70)         # captions / footer
RED = (179, 38, 30)          # lead kicker, accents
BLUE = (31, 78, 121)         # section labels
BOX = (236, 228, 207)        # pictogram tile
BOX_EDGE = (216, 205, 178)   # tile border
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- pictograms, each drawn inside a 72x72 tile at (x, y) -----------------

def icon_chart(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.line([(x + 14, y + 58), (x + 14, y + 14)], fill=INK, width=3)
    d.line([(x + 14, y + 58), (x + 60, y + 58)], fill=INK, width=3)
    pts = [(x + 18, y + 24), (x + 30, y + 32), (x + 42, y + 40), (x + 56, y + 52)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon([(x + 56, y + 52), (x + 48, y + 50), (x + 54, y + 44)], fill=RED)


def icon_burst(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    cx, cy = x + 36, y + 36
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 26 if i % 2 == 0 else 11
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(214, 90, 20))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=PAPER)


def icon_dome(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.pieslice([x + 20, y + 14, x + 52, y + 46], 180, 360, fill=BLUE)
    d.rectangle([x + 34, y + 10, x + 38, y + 16], fill=BLUE)
    d.rectangle([x + 18, y + 44, x + 54, y + 50], fill=BLUE)
    for cx in (x + 23, x + 34, x + 45):
        d.rectangle([cx, y + 50, cx + 4, y + 60], fill=BLUE)
    d.rectangle([x + 16, y + 60, x + 56, y + 64], fill=BLUE)


def icon_ship(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.line([(x + 36, y + 14), (x + 36, y + 40)], fill=INK, width=3)
    d.polygon([(x + 36, y + 14), (x + 50, y + 20), (x + 36, y + 26)], fill=RED)
    d.polygon([(x + 16, y + 40), (x + 58, y + 40), (x + 52, y + 52), (x + 22, y + 52)],
              fill=(31, 78, 121))
    for wy in (58, 64):
        d.line([(x + 16, y + wy), (x + 58, y + wy)], fill=BLUE, width=2)


def icon_flame(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.polygon([(x + 36, y + 12), (x + 50, y + 36), (x + 44, y + 52),
               (x + 28, y + 52), (x + 22, y + 36)], fill=(214, 90, 20))
    d.polygon([(x + 36, y + 30), (x + 44, y + 44), (x + 36, y + 54),
               (x + 28, y + 44)], fill=(232, 164, 32))


def icon_coin(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.ellipse([x + 14, y + 14, x + 58, y + 58], fill=(201, 162, 39),
              outline=(146, 110, 11), width=3)
    f = font(SANS_BOLD, 26)
    d.text((x + 36 - d.textlength("1¢", font=f) / 2, y + 22), "1¢",
           font=f, fill=(90, 64, 8))


ICONS = {
    "chart": icon_chart,
    "burst": icon_burst,
    "dome": icon_dome,
    "ship": icon_ship,
    "flame": icon_flame,
    "coin": icon_coin,
}

STORIES = [
    ("chart", "MARKETS · TOKYO", RED,
     "AI sell-off sinks world markets",
     "Nikkei -5.06%, S&P 500 -3.7% as AI fears spread; regulators step in."),
    ("burst", "WAR · UKRAINE", RED,
     "Strike on Dymer kills at least 10",
     "Russian strike hits flats north of Kyiv; a boy aged 7 is pulled out alive."),
    ("dome", "POLITICS · WASHINGTON", BLUE,
     "Democrats' biggest House win since 1992",
     "At least 258 seats after a North Carolina recount seals the majority."),
    ("ship", "CONFLICT · LIBYA", BLUE,
     "Russian warship sinks at Benghazi",
     "The corvette Merkury goes down after a suspected Ukrainian sea-drone attack."),
    ("flame", "WAR · HORMUZ", RED,
     "Tankers ablaze near Hormuz",
     "Two supertankers hit mines and catch fire as Iran warns over a US blockade."),
    ("coin", "USA · WASHINGTON", BLUE,
     "Penny's 232-year run ends",
     "Trump signs the Common Cents Act; the one-cent coin is on its way out."),
]


def draw_cell(d, x, y, w, h, story):
    key, kicker, colour, headline, body = story
    ICONS[key](d, x, y + 6)
    tx = x + 88
    tw = w - 88
    kf = font(SANS_BOLD, 15)
    d.text((tx, y + 6), kicker, font=kf, fill=colour)
    hf = font(SANS_BOLD, 24)
    lines = wrap(d, headline, hf, tw)[:2]
    ly = y + 28
    for line in lines:
        d.text((tx, ly), line, font=hf, fill=INK)
        ly += 30
    bf = font(SANS, 18)
    blines = wrap(d, body, bf, tw)[:2]
    by = ly + 4
    for line in blines:
        d.text((tx, by), line, font=bf, fill=INK)
        by += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 40
    cx = W // 2
    right = W - mx

    hline(d, mx, right, 30, 3)
    hline(d, mx, right, 36, 1)
    centred(d, cx, 52, "The World in One Page", font(SERIF_BOLD, 56))
    centred(d, cx, 128, "—  MONDAY, 23 NOVEMBER 2026  —",
            font(SANS_BOLD, 22), fill=FAINT)
    hline(d, mx, right, 168, 2)

    # Lead story: COP31.
    d.text((mx, 190), "CLIMATE · ANTALYA, TURKEY", font=font(SANS_BOLD, 20), fill=RED)
    d.text((mx, 216), "COP31 ends with no deal", font=font(SANS_BOLD, 58), fill=INK)
    stand = ("The climate summit closed after the European Union and about 130 nations "
             "rejected a draft text that left out fossil fuels.")
    sf = font(SANS, 23)
    ly = 292
    for line in wrap(d, stand, sf, right - mx):
        d.text((mx, ly), line, font=sf, fill=INK)
        ly += 31

    # Markets strip.
    hline(d, mx, right, 372, 1)
    centred(d, cx, 384, "NIKKEI -5.06%  ·  S&P 500 -3.70%  ·  GOLD +2.72%  ·  BRENT $89.96",
            font(SANS_BOLD, 20))
    hline(d, mx, right, 416, 1)

    # Grid: 2 columns x 3 rows of stories.
    gx, gy = mx, 436
    col_w = (right - mx - 20) // 2
    row_h, gap = 168, 14
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_cell(d, gx + col * (col_w + 20), gy + row * (row_h + gap),
                  col_w, row_h, story)

    # Footer.
    hline(d, mx, right, 972, 1)
    centred(d, cx, 984, "All events of Monday 23 November 2026 · Drawn from wire reports",
            font(SANS, 15), fill=FAINT)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
