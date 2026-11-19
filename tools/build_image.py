#!/usr/bin/env python3
"""Render the entry image for make.fun's news-image-20261119 bounty.

The image sums up the world news of Thursday, 19 November 2026 on one
1024x1024 newspaper-style poster: a masthead naming the day, one lead
story (the first-ever Xi–Trump–Putin trilateral summit in Shenzhen),
a GTA VI launch-day feature with its headline numbers, twelve news
cards, a UTC timeline of the day and an "also today" strip. Every
story below was cross-checked against at least two independent news
reports published on 19 November 2026 (Reuters, AP, BBC, Yonhap,
Nikkei Asia, Al Jazeera, Le Monde, WSJ, The Hindu and the digests
that cite them).

The render is deterministic: fixed data, fixed fonts, no clock, no
network. It writes a preview at assets/entry.png and the shipped
asset at assets/entry.png.b64 (the same PNG, base64-encoded on one
line, so the repository stays plain text); the shipped program
(main.py) decodes that asset and writes /output/entry.png.
"""

import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "entry.png"
OUT_B64 = ROOT / "assets" / "entry.png.b64"

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SERIF_BOLD = str(FONT_DIR / "LiberationSerif-Bold.ttf")
SANS = str(FONT_DIR / "LiberationSans-Regular.ttf")
SANS_BOLD = str(FONT_DIR / "LiberationSans-Bold.ttf")

PAPER = (250, 246, 238)
CARD = (255, 253, 246)
INK = (23, 32, 54)
GREY = (84, 88, 96)
NAVY = (20, 38, 63)
GOLD = (227, 179, 65)
RED = (179, 35, 42)
BORDER = (216, 210, 196)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
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


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


LEAD = {
    "kicker": "APEC SUMMIT · SHENZHEN, CHINA",
    "headline": "Xi, Trump and Putin sit down for first-ever trilateral summit",
    "sub": ("Xi opened the APEC leaders' meeting, then faced Trump one-to-one; "
            "by mid-afternoon Putin joined them at Kylin Villa. Nuclear arms "
            "cuts and Iran top Trump's agenda."),
}

FEATURE = {
    "kicker": "LAUNCH DAY · THE WORLD PLAYS",
    "headline": "GTA VI is here: the 13-year wait ends as the world logs on",
    "chips": ["METACRITIC 99/100", "2.5M TWITCH VIEWERS — RECORD",
              "PRE-ORDERS EST. $1.45BN", "PS STORE PRE-ORDER RECORD"],
}

CARDS = [
    ("THE HAGUE", (122, 78, 158),
     "World Court delivers Rohingya genocide judgment"),
    ("ART MARKET", (176, 124, 28),
     "Van Gogh sells for a record $190.4m in New York"),
    ("IPO", (31, 122, 109),
     "Anthropic prices IPO at $83, valuing it near $1.5tn"),
    ("NVIDIA", (76, 140, 40),
     "Record $115.8bn quarter, but Nvidia shares fall 2.9%"),
    ("MARKETS", (160, 58, 107),
     "Dollar at 19-month high; gold at 14-month low"),
    ("UKRAINE WAR", (64, 92, 140),
     "Crimean Bridge hit for the third time this week"),
    ("WASHINGTON", (179, 35, 42),
     "Jeffries set to be first Black US House Speaker"),
    ("SPACE", (32, 52, 96),
     "Voyager 1 reaches one light-day from Earth"),
    ("TRADE", (178, 106, 27),
     "EU approves signing trade pact with Indonesia"),
    ("ISRAEL", (90, 96, 110),
     "Eisenkot's coalition deadline nears: 6 December"),
    ("RIYADH", (150, 110, 50),
     "Missile alert over Riyadh, then the all-clear"),
    ("INDIA–JAPAN", (140, 44, 60),
     "India and Japan open 2+2 defence dialogue"),
]

TIMELINE = ("11:00* GTA VI unlocks in New Zealand · 00:00 live in the UK · "
            "02:00 APEC plenary opens in Shenzhen · 04:45 Xi meets Trump · "
            "05:00 US unlock · 06:30 first trilateral summit · "
            "08:00 ICJ judgment, The Hague · *18 Nov UTC")

ALSO = ("WTI crude falls 3.5% to $83 as US inventories build · "
        "GTA VI launch-day leave bookings jump 32%")
SOURCES = ("Compiled from Reuters, AP, BBC, Yonhap, Nikkei Asia, Al Jazeera, "
           "Le Monde, WSJ and The Hindu — 19 November 2026")


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    centered(draw, W / 2, 18, "THE WORLD TODAY", font(SERIF_BOLD, 63), (255, 255, 255))
    centered(draw, W / 2, 94, "Thursday, 19 November 2026", font(SANS_BOLD, 37), GOLD)
    draw.rectangle([0, 148, W, 154], fill=GOLD)
    centered(draw, W / 2, 160,
             "One page · the whole day · every story checked against at least two independent reports",
             font(SANS, 16), GREY)


def draw_lead(draw):
    x0, y0, x1, y1 = 24, 186, W - 24, 386
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=2)
    draw.rectangle([x0, y0, x0 + 10, y1], fill=RED)
    tx = x0 + 30
    draw.text((tx, y0 + 12), LEAD["kicker"], font=font(SANS_BOLD, 24), fill=RED)
    y = y0 + 44
    for line in wrap(draw, LEAD["headline"], font(SANS_BOLD, 38), x1 - tx - 20):
        draw.text((tx, y), line, font=font(SANS_BOLD, 38), fill=INK)
        y += 44
    y += 4
    for line in wrap(draw, LEAD["sub"], font(SANS, 20), x1 - tx - 20):
        draw.text((tx, y), line, font=font(SANS, 20), fill=GREY)
        y += 24


def draw_feature(draw):
    x0, y0, x1, y1 = 24, 396, W - 24, 512
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    tx = x0 + 24
    draw.text((tx, y0 + 10), FEATURE["kicker"], font=font(SANS_BOLD, 19), fill=GOLD)
    draw.text((tx, y0 + 36), FEATURE["headline"], font=font(SANS_BOLD, 28),
              fill=(255, 255, 255))
    chip_f = font(SANS_BOLD, 15)
    cx = tx
    cy = y0 + 78
    for chip in FEATURE["chips"]:
        tw = draw.textlength(chip, font=chip_f)
        draw.rectangle([cx, cy, cx + tw + 16, cy + 28], outline=GOLD, width=2)
        draw.text((cx + 8, cy + 6), chip, font=chip_f, fill=(255, 255, 255))
        cx += tw + 26


def draw_card(draw, x0, y0, x1, y1, tag, color, headline):
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=2)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=color)
    chip_f = font(SANS_BOLD, 15)
    tw = draw.textlength(tag, font=chip_f)
    draw.rectangle([x0 + 12, y0 + 12, x0 + 12 + tw + 14, y0 + 34], fill=color)
    draw.text((x0 + 19, y0 + 15), tag, font=chip_f, fill=(255, 255, 255))
    y = y0 + 40
    for line in wrap(draw, headline, font(SANS_BOLD, 19), x1 - x0 - 24)[:2]:
        draw.text((x0 + 12, y), line, font=font(SANS_BOLD, 19), fill=INK)
        y += 22


def draw_timeline(draw):
    y = 884
    draw.text((24, y), "THE DAY IN UTC", font=font(SANS_BOLD, 18), fill=RED)
    y += 22
    for line in wrap(draw, TIMELINE, font(SANS, 17), W - 48)[:2]:
        draw.text((24, y), line, font=font(SANS, 17), fill=INK)
        y += 21


def draw_footer(draw):
    y = 956
    draw.text((24, y), "ALSO TODAY", font=font(SANS_BOLD, 19), fill=RED)
    tx = 24 + draw.textlength("ALSO TODAY  ", font=font(SANS_BOLD, 19))
    draw.text((tx, y + 1), ALSO, font=font(SANS, 17), fill=INK)
    centered(draw, W / 2, 998, SOURCES, font(SANS, 15), GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_feature(draw)
    grid_top, card_h, gap = 522, 84, 6
    col_w = (W - 48 - 2 * 8) // 3
    for i, (tag, color, headline) in enumerate(CARDS):
        row, col = divmod(i, 3)
        x0 = 24 + col * (col_w + 8)
        y0 = grid_top + row * (card_h + gap)
        draw_card(draw, x0, y0, x0 + col_w, y0 + card_h, tag, color, headline)
    draw_timeline(draw)
    draw_footer(draw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    OUT_B64.write_text(base64.b64encode(OUT.read_bytes()).decode("ascii") + "\n",
                       encoding="ascii")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {W}x{H})")
    print(f"wrote {OUT_B64} ({OUT_B64.stat().st_size} bytes, base64)")


if __name__ == "__main__":
    main()
