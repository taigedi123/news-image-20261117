#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: one 1024x1024 infographic summing up
Tuesday 17 November 2026. Deterministic: same input -> same PNG bytes
(Pillow writes no timestamps into PNG chunks). Run: python3 draw.py"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)      # paper
NAVY = (20, 33, 61)       # masthead
GOLD = (201, 162, 39)
INK = (24, 24, 24)
MUTED = (74, 74, 74)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
LINE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, color, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def bridge_icon(d, x, y, s, c1, c2):
    # suspension bridge with a collapsed middle span
    d.line([(x, y + 58 * s), (x + 150 * s, y + 58 * s)], fill=c1, width=max(3, int(4 * s)))
    d.line([(x + 178 * s, y + 58 * s), (x + 260 * s, y + 58 * s)], fill=c1, width=max(3, int(4 * s)))
    for tx in (x + 28 * s, x + 205 * s):
        d.line([(tx, y + 58 * s), (tx, y)], fill=c1, width=max(3, int(5 * s)))
        d.line([(tx - 16 * s, y), (tx + 16 * s, y)], fill=c1, width=max(3, int(5 * s)))
    # cables
    d.arc([x - 6 * s, y - 34 * s, x + 130 * s, y + 58 * s], 200, 340, fill=c2, width=max(2, int(3 * s)))
    d.arc([x + 130 * s, y - 34 * s, x + 266 * s, y + 58 * s], 200, 340, fill=c2, width=max(2, int(3 * s)))
    # collapsed span falling into the water
    d.line([(x + 150 * s, y + 58 * s), (x + 164 * s, y + 84 * s)], fill=c1, width=max(3, int(4 * s)))
    for i in range(3):
        wx = x + (i * 70 + 10) * s
        d.arc([wx, y + 92 * s, wx + 56 * s, y + 108 * s], 180, 360, fill=c2, width=max(2, int(3 * s)))


def tanker_icon(d, x, y, s, c1, c2):
    # oil tanker on waves, with a mine starburst
    d.rectangle([x, y + 30 * s, x + 210 * s, y + 62 * s], fill=c1)
    d.polygon([(x, y + 62 * s), (x + 30 * s, y + 88 * s), (x + 180 * s, y + 88 * s), (x + 210 * s, y + 62 * s)], fill=c1)
    d.rectangle([x + 150 * s, y + 8 * s, x + 185 * s, y + 30 * s], fill=c2)
    d.rectangle([x + 158 * s, y - 8 * s, x + 164 * s, y + 8 * s], fill=c2)
    for i in range(4):
        d.rectangle([x + (10 + i * 34) * s, y + 34 * s, x + (36 + i * 34) * s, y + 50 * s], outline=WHITE, width=max(2, int(2 * s)))
    for i in range(3):
        wx = x + (i * 80 + 5) * s
        d.arc([wx, y + 96 * s, wx + 60 * s, y + 112 * s], 180, 360, fill=c2, width=max(2, int(3 * s)))
    # mine burst above the bow
    cx, cy = x + 232 * s, y + 6 * s
    for a in range(0, 360, 45):
        import math
        r1, r2 = 6 * s, 16 * s
        x1 = cx + r1 * math.cos(math.radians(a)); y1 = cy + r1 * math.sin(math.radians(a))
        x2 = cx + r2 * math.cos(math.radians(a)); y2 = cy + r2 * math.sin(math.radians(a))
        d.line([(x1, y1), (x2, y2)], fill=(178, 34, 34), width=max(2, int(3 * s)))
    d.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s], fill=(178, 34, 34))


def summit_icon(d, x, y, s, c1, c2):
    # three flag circles: China, USA, Russia
    cols = [(222, 41, 16), (38, 84, 160), (200, 200, 200)]
    labels = ["CN", "US", "RU"]
    for i, (col, lab) in enumerate(zip(cols, labels)):
        cx = x + (30 + i * 62) * s
        d.ellipse([cx - 28 * s, y, cx + 28 * s, y + 56 * s], fill=col, outline=NAVY, width=max(2, int(3 * s)))
        f = font(SANS_B, int(20 * s))
        tw = d.textlength(lab, font=f)
        d.text((cx - tw / 2, y + 15 * s), lab, font=f, fill=WHITE if i != 2 else NAVY)
    # handshake arc below
    d.arc([x + 10 * s, y + 62 * s, x + 180 * s, y + 108 * s], 180, 360, fill=c2, width=max(2, int(3 * s)))


def hub_icon(d, x, y, s, c1, c2):
    # globe with a location pin
    cx, cy = x + 70 * s, y + 55 * s
    d.ellipse([cx - 55 * s, cy - 55 * s, cx + 55 * s, cy + 55 * s], outline=c1, width=max(3, int(4 * s)))
    d.ellipse([cx - 55 * s, cy - 55 * s, cx + 55 * s, cy + 55 * s], fill=(214, 232, 240))
    d.ellipse([cx - 55 * s, cy - 55 * s, cx + 55 * s, cy + 55 * s], outline=c1, width=max(3, int(4 * s)))
    d.ellipse([cx - 24 * s, cy - 55 * s, cx + 24 * s, cy + 55 * s], outline=c1, width=max(2, int(3 * s)))
    d.line([(cx - 55 * s, cy), (cx + 55 * s, cy)], fill=c1, width=max(2, int(3 * s)))
    d.arc([cx - 55 * s, cy - 28 * s, cx + 55 * s, cy + 28 * s], 0, 360, fill=c1, width=max(2, int(2 * s)))
    # pin
    px, py = x + 160 * s, y + 20 * s
    d.ellipse([px - 22 * s, py, px + 22 * s, py + 44 * s], fill=(178, 34, 34))
    d.polygon([(px - 20 * s, py + 32 * s), (px + 20 * s, py + 32 * s), (px, py + 66 * s)], fill=(178, 34, 34))
    d.ellipse([px - 9 * s, py + 11 * s, px + 9 * s, py + 29 * s], fill=WHITE)


def scales_icon(d, x, y, s, c1, c2):
    # scales of justice
    d.line([(x + 95 * s, y), (x + 95 * s, y + 88 * s)], fill=c1, width=max(3, int(5 * s)))
    d.line([(x + 20 * s, y + 12 * s), (x + 170 * s, y + 12 * s)], fill=c1, width=max(3, int(5 * s)))
    d.line([(x + 40 * s, y + 96 * s), (x + 150 * s, y + 96 * s)], fill=c1, width=max(3, int(5 * s)))
    for cx in (x + 20 * s, x + 170 * s):
        d.line([(cx, y + 12 * s), (cx, y + 52 * s)], fill=c2, width=max(2, int(3 * s)))
        d.arc([cx - 30 * s, y + 44 * s, cx + 30 * s, y + 84 * s], 0, 180, fill=c2, width=max(2, int(3 * s)))


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=GOLD)
    f_kicker = font(SANS_B, 28)
    d.text((48, 18), "THE WORLD IN ONE DAY  •  FIVE STORIES", font=f_kicker, fill=GOLD)
    f_date = font(SERIF_B, 54)
    d.text((48, 50), "TUESDAY 17 NOVEMBER 2026", font=f_date, fill=WHITE)
    f_sub = font(SANS, 24)
    d.text((48, 116), "The day's most consequential world news, at a glance", font=f_sub, fill=(200, 210, 225))

    # ---- hero panel: Kerch Bridge ----
    hx, hy, hw, hh = 32, 168, 960, 240
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=14, fill=PANEL, outline=LINE, width=2)
    d.rounded_rectangle([hx, hy, hx + hw, hy + 44], radius=14, fill=(178, 34, 34))
    d.rectangle([hx, hy + 30, hx + hw, hy + 44], fill=(178, 34, 34))
    f_tag = font(SANS_B, 23)
    d.text((hx + 22, hy + 9), "TOP STORY  •  UKRAINE", font=f_tag, fill=WHITE)
    bridge_icon(d, hx + 26, hy + 96, 0.85, NAVY, GOLD)
    tx = hx + 280
    f_h = font(SANS_B, 34)
    y = text_block(d, tx, hy + 58, wrap(d, "Kerch Bridge hit again — road span collapses", f_h, hw - 300), f_h, INK)
    f_b = font(SANS, 23)
    text_block(d, tx, y + 6, wrap(d, "Zelenskyy hails an \u201cunprecedented operation\u201d. Russia strikes Kyiv\u2019s Dnipro bridges, cutting heat, water and power.", f_b, hw - 300), f_b, MUTED)

    # ---- 2x2 grid ----
    stories = [
        ("MIDDLE EAST", (38, 84, 160), tanker_icon,
         "Mines hit tankers near Hormuz",
         "Iran drones target a US radar base in Bahrain \u2014 intercepted. Third US carrier USS Theodore Roosevelt arrives."),
        ("SUMMIT", (20, 90, 60), summit_icon,
         "Xi\u2013Trump\u2013Putin to meet Thursday",
         "China confirms the first three-way summit, 19 November in Shenzhen, on the APEC sidelines."),
        ("EUROPE", (120, 70, 140), hub_icon,
         "Five EU states agree Rwanda \u2018return hub\u2019",
         "Germany, Denmark, Austria, Greece and the Netherlands plan a joint hub for rejected asylum seekers."),
        ("WEST BANK", (150, 100, 20), scales_icon,
         "UK sanctions Israeli settlement builders",
         "Eight construction firms blacklisted over West Bank settlements. A settler kills a 72-year-old woman in Jericho."),
    ]
    gw, gh, gap = 472, 258, 16
    for i, (tag, accent, icon, head, body) in enumerate(stories):
        x = 32 + (i % 2) * (gw + gap)
        y0 = 420 + (i // 2) * (gh + 10)
        d.rounded_rectangle([x, y0, x + gw, y0 + gh], radius=14, fill=PANEL, outline=LINE, width=2)
        d.rounded_rectangle([x, y0, x + gw, y0 + 38], radius=14, fill=accent)
        d.rectangle([x, y0 + 24, x + gw, y0 + 38], fill=accent)
        d.text((x + 18, y0 + 7), tag, font=font(SANS_B, 21), fill=WHITE)
        icon(d, x + 18, y0 + 54, 0.62, NAVY, accent)
        f_h = font(SANS_B, 26)
        text_block(d, x + 190, y0 + 52, wrap(d, head, f_h, gw - 208), f_h, INK)
        f_b = font(SANS, 21)
        text_block(d, x + 18, y0 + 158, wrap(d, body, f_b, gw - 36), f_b, MUTED)

    # ---- footer ----
    f_f = font(SANS, 21)
    d.text((32, 964), "Five stories from Tuesday 17 November 2026  •  Events first reported that day", font=f_f, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    draw()
