#!/usr/bin/env python3
"""Poster generator for the news-image-20261119 make.fun entry.

Everything on the poster is the news of Thursday, 19 November 2026:
the Shenzhen trilateral summit leads, GTA VI's launch day is the
feature, and twelve short cards plus a UTC timeline fill the rest of
the page. Each item was checked against two or more independent
reports from that day (Reuters, AP, BBC, Yonhap, Nikkei Asia,
Al Jazeera, Le Monde, WSJ, The Hindu) before it earned a place here.

Running this file rebuilds assets/entry.png and, next to it, the
base64 copy assets/entry.png.b64 that main.py ships. The drawing is
fully deterministic — same data, same fonts, same bytes every run.
"""

import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
ROOT_DIR = Path(__file__).resolve().parent.parent
PNG_OUT = ROOT_DIR / "assets" / "entry.png"
B64_OUT = ROOT_DIR / "assets" / "entry.png.b64"
FONTS = Path("/usr/share/fonts/truetype/liberation")


def rgb(hexpair):
    """'#B3232A' -> (179, 35, 42)."""
    h = hexpair.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAPER = rgb("#FAF6EE")
CARD_BG = rgb("#FFFDF6")
INK = rgb("#172036")
MUTED = rgb("#545860")
NAVY = rgb("#14263F")
GOLD = rgb("#E3B341")
ACCENT_RED = rgb("#B3232A")
HAIRLINE = rgb("#D8D2C4")
WHITE = (255, 255, 255)

LEAD_KICKER = "APEC SUMMIT · SHENZHEN, CHINA"
LEAD_HEAD = "Xi, Trump and Putin sit down for first-ever trilateral summit"
LEAD_DEK = ("Xi opened the APEC leaders' meeting, then faced Trump one-to-one; "
            "by mid-afternoon Putin joined them at Kylin Villa. Nuclear arms "
            "cuts and Iran top Trump's agenda.")

FEATURE_KICKER = "LAUNCH DAY · THE WORLD PLAYS"
FEATURE_HEAD = "GTA VI is here: the 13-year wait ends as the world logs on"
FEATURE_CHIPS = ("METACRITIC 99/100", "2.5M TWITCH VIEWERS — RECORD",
                 "PRE-ORDERS EST. $1.45BN", "PS STORE PRE-ORDER RECORD")

# (section label, label colour, one headline) — three columns, four rows.
CARDS = [
    {"tag": "THE HAGUE", "colour": "#7A4E9E", "head": "World Court delivers Rohingya genocide judgment"},
    {"tag": "ART MARKET", "colour": "#B07C1C", "head": "Van Gogh sells for a record $190.4m in New York"},
    {"tag": "IPO", "colour": "#1F7A6D", "head": "Anthropic prices IPO at $83, valuing it near $1.5tn"},
    {"tag": "NVIDIA", "colour": "#4C8C28", "head": "Record $115.8bn quarter, but Nvidia shares fall 2.9%"},
    {"tag": "MARKETS", "colour": "#A03A6B", "head": "Dollar at 19-month high; gold at 14-month low"},
    {"tag": "UKRAINE WAR", "colour": "#405C8C", "head": "Crimean Bridge hit for the third time this week"},
    {"tag": "WASHINGTON", "colour": "#B3232A", "head": "Jeffries set to be first Black US House Speaker"},
    {"tag": "SPACE", "colour": "#203460", "head": "Voyager 1 reaches one light-day from Earth"},
    {"tag": "TRADE", "colour": "#B26A1B", "head": "EU approves signing trade pact with Indonesia"},
    {"tag": "ISRAEL", "colour": "#5A606E", "head": "Eisenkot's coalition deadline nears: 6 December"},
    {"tag": "RIYADH", "colour": "#966E32", "head": "Missile alert over Riyadh, then the all-clear"},
    {"tag": "INDIA–JAPAN", "colour": "#8C2C3C", "head": "India and Japan open 2+2 defence dialogue"},
]

DAY_LINE = ("11:00* GTA VI unlocks in New Zealand · 00:00 live in the UK · 02:00 APEC plenary opens in Shenzhen · "
            "04:45 Xi meets Trump · 05:00 US unlock · 06:30 first trilateral summit · 08:00 ICJ judgment, The Hague · *18 Nov UTC")
STRIP = "WTI crude falls 3.5% to $83 as US inventories build · GTA VI launch-day leave bookings jump 32%"
CREDIT = "Compiled from Reuters, AP, BBC, Yonhap, Nikkei Asia, Al Jazeera, Le Monde, WSJ and The Hindu — 19 November 2026"


class Poster:
    """Draws the whole page top to bottom, one band at a time."""

    def __init__(self):
        self.img = Image.new("RGB", (SIDE, SIDE), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.serif = ImageFont.truetype(str(FONTS / "LiberationSerif-Bold.ttf"), 63)
        self.date_f = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 37)
        self.body = ImageFont.truetype(str(FONTS / "LiberationSans-Regular.ttf"), 20)

    def width_of(self, text, fnt):
        return self.d.textlength(text, font=fnt)

    def middle(self, y, text, fnt, colour):
        self.d.text(((SIDE - self.width_of(text, fnt)) / 2, y), text, font=fnt, fill=colour)

    def wrapped(self, text, fnt, limit):
        """Split text into the fewest lines that each fit within limit px."""
        out, pending = [], ""
        for word in text.split(" "):
            attempt = word if pending == "" else pending + " " + word
            if self.width_of(attempt, fnt) <= limit:
                pending = attempt
            else:
                out.append(pending)
                pending = word
        if pending != "":
            out.append(pending)
        return out

    def paragraph(self, x, y, text, fnt, colour, limit, step):
        for line in self.wrapped(text, fnt, limit):
            self.d.text((x, y), line, font=fnt, fill=colour)
            y += step
        return y

    def masthead(self):
        d = self.d
        d.rectangle([0, 0, SIDE, 148], fill=NAVY)
        self.middle(18, "THE WORLD TODAY", self.serif, WHITE)
        self.middle(94, "Thursday, 19 November 2026", self.date_f, GOLD)
        d.rectangle([0, 148, SIDE, 154], fill=GOLD)
        note = ImageFont.truetype(str(FONTS / "LiberationSans-Regular.ttf"), 16)
        self.middle(160, "One page · the whole day · every story checked against at least two independent reports", note, MUTED)

    def lead_story(self):
        d = self.d
        d.rectangle([24, 186, SIDE - 24, 386], fill=CARD_BG, outline=HAIRLINE, width=2)
        d.rectangle([24, 186, 34, 386], fill=ACCENT_RED)
        kick = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 24)
        head = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 38)
        d.text((54, 198), LEAD_KICKER, font=kick, fill=ACCENT_RED)
        y = self.paragraph(54, 230, LEAD_HEAD, head, INK, SIDE - 54 - 44, 44)
        dek = ImageFont.truetype(str(FONTS / "LiberationSans-Regular.ttf"), 20)
        self.paragraph(54, y + 4, LEAD_DEK, dek, MUTED, SIDE - 54 - 44, 24)

    def feature(self):
        d = self.d
        d.rectangle([24, 396, SIDE - 24, 512], fill=NAVY)
        kick = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 19)
        head = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 28)
        d.text((48, 406), FEATURE_KICKER, font=kick, fill=GOLD)
        d.text((48, 432), FEATURE_HEAD, font=head, fill=WHITE)
        chip_f = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 15)
        cx = 48
        for label in FEATURE_CHIPS:
            w = self.width_of(label, chip_f)
            d.rectangle([cx, 474, cx + w + 16, 502], outline=GOLD, width=2)
            d.text((cx + 8, 480), label, font=chip_f, fill=WHITE)
            cx += w + 26

    def card(self, x, y, w, h, item):
        d = self.d
        colour = rgb(item["colour"])
        d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=HAIRLINE, width=2)
        d.rectangle([x, y, x + w, y + 5], fill=colour)
        tag_f = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 15)
        tw = self.width_of(item["tag"], tag_f)
        d.rectangle([x + 12, y + 12, x + 12 + tw + 14, y + 34], fill=colour)
        d.text((x + 19, y + 15), item["tag"], font=tag_f, fill=WHITE)
        head_f = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 19)
        self.paragraph(x + 12, y + 40, item["head"], head_f, INK, w - 24, 22)

    def card_grid(self):
        top, height, gap_y, gap_x = 522, 84, 6, 8
        col_w = (SIDE - 48 - 2 * gap_x) // 3
        for idx, item in enumerate(CARDS):
            row, col = divmod(idx, 3)
            self.card(24 + col * (col_w + gap_x), top + row * (height + gap_y),
                      col_w, height, item)

    def closing_bands(self):
        d = self.d
        label_f = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 18)
        d.text((24, 884), "THE DAY IN UTC", font=label_f, fill=ACCENT_RED)
        small = ImageFont.truetype(str(FONTS / "LiberationSans-Regular.ttf"), 17)
        self.paragraph(24, 906, DAY_LINE, small, INK, SIDE - 48, 21)
        also_f = ImageFont.truetype(str(FONTS / "LiberationSans-Bold.ttf"), 19)
        d.text((24, 956), "ALSO TODAY", font=also_f, fill=ACCENT_RED)
        strip_x = 24 + self.width_of("ALSO TODAY  ", also_f)
        d.text((strip_x, 957), STRIP, font=small, fill=INK)
        credit_f = ImageFont.truetype(str(FONTS / "LiberationSans-Regular.ttf"), 15)
        self.middle(998, CREDIT, credit_f, MUTED)

    def render(self):
        self.masthead()
        self.lead_story()
        self.feature()
        self.card_grid()
        self.closing_bands()
        PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
        self.img.save(PNG_OUT, format="PNG", optimize=True)
        encoded = base64.b64encode(PNG_OUT.read_bytes()).decode("ascii")
        B64_OUT.write_text(encoded + "\n", encoding="ascii")
        print("poster:", PNG_OUT.stat().st_size, "bytes ->", PNG_OUT)
        print("asset: ", B64_OUT.stat().st_size, "bytes ->", B64_OUT)


if __name__ == "__main__":
    Poster().render()
