#!/usr/bin/env python3
"""The World in One Picture - 21 November 2026.

Draws a newspaper front page summing up Saturday 21 November 2026's
world news and writes it to /output/entry.png (1024x1024, <= 1 MiB).

Fully deterministic: fixed strings, fixed layout, no randomness, no
network, no clock. Two runs write identical bytes.

Lead story: COP31 climate talks in Antalya go into overtime after a
fossil-fuel deadlock (third draft due Saturday). Supporting stories:
Wall Street slides into correction, Estonia shuts its Russia border,
Mongolia's president resigns, a vendor cyberattack hits JPMorgan /
Visa / Mastercard, India fight back in the Wellington Test, and
Hyundai unveils the 2027 Elantra. Footer ticker carries the smaller
items of the day.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("/output/entry.png")
W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952 usable width

# ---- palette: cream newsprint, navy ink, signal red, teal -----------------
PAPER = (247, 243, 232)
INK = (20, 33, 61)
INK_SOFT = (52, 64, 92)
RED = (179, 32, 44)
RED_DARK = (141, 24, 34)
TEAL = (15, 118, 110)
TEAL_DARK = (11, 84, 79)
GOLD = (212, 160, 60)
GREY = (122, 122, 110)
RULE = (196, 188, 168)
SKY_TOP = (253, 224, 148)
SKY_MID = (178, 214, 205)
SKY_BOT = (120, 178, 168)
SEA = (23, 94, 110)
WHITE = (255, 255, 255)
CREAM_DIM = (232, 226, 208)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF_REG = lambda s: font("DejaVuSerif.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def spaced(draw, x, y, text, fnt, fill, tracking=3, center=None):
    """Draw text with extra letter tracking; optionally centered on cx."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    if center is not None:
        x = center - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def accent_bar(draw, x, y, color=RED, w=44, h=5):
    draw.rectangle([x, y, x + w, y + h], fill=color)


def story_cell(draw, x, y, w, kicker, headline, deck, hlead=23):
    """One supporting-story cell: accent bar, kicker, headline, deck."""
    accent_bar(draw, x, y + 2)
    kf = F_SANS_B(13)
    draw.text((x, y + 12), kicker, font=kf, fill=RED_DARK)
    hf = F_SANS_B(19)
    lines = wrap(draw, headline, hf, w)
    yy = draw_lines(draw, x, y + 34, lines, hf, INK, hlead)
    df = F_SANS(13)
    dlines = wrap(draw, deck, df, w)
    draw_lines(draw, x, yy + 4, dlines, df, INK_SOFT, 17)
    return y


def draw_lead_visual(img, draw, x, y, w, h):
    """Flat illustration panel: sun, globe with warming gauge, smokestacks,
    and a deadline timeline running past its mark."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=SKY_MID,
                           outline=RULE, width=1)
    # sky bands
    band_h = h // 3
    draw.rectangle([x + 2, y + 2, x + w - 2, y + band_h], fill=SKY_TOP)
    draw.rectangle([x + 2, y + band_h, x + w - 2, y + 2 * band_h],
                   fill=SKY_MID)
    # sun, top left
    sx, sy, sr = x + 92, y + 52, 34
    for r, col in ((sr + 16, (253, 236, 180)), (sr + 8, (250, 214, 110))):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(247, 183, 51))
    # sun rays
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1 = sx + int((sr + 20) * math.cos(a))
        y1 = sy + int((sr + 20) * math.sin(a))
        x2 = sx + int((sr + 30) * math.cos(a))
        y2 = sy + int((sr + 30) * math.sin(a))
        draw.line([x1, y1, x2, y2], fill=(247, 183, 51), width=4)

    # globe, centre-left
    gx, gy, gr = x + 330, y + h // 2 - 6, 74
    globe = Image.new("RGBA", (gr * 2 + 8, gr * 2 + 8), (0, 0, 0, 0))
    gd = ImageDraw.Draw(globe)
    gd.ellipse([4, 4, 4 + gr * 2, 4 + gr * 2], fill=(23, 94, 110, 255))
    # land blobs
    gd.ellipse([28, 30, 92, 66], fill=(56, 142, 92, 255))
    gd.ellipse([86, 84, 140, 122], fill=(56, 142, 92, 255))
    gd.ellipse([104, 34, 138, 62], fill=(46, 122, 82, 255))
    # latitude lines
    for yy in (44, 78, 112):
        gd.arc([4, yy - 10, 4 + gr * 2, yy + 10], 200, 340,
               fill=(255, 255, 255, 110), width=2)
    gd.ellipse([4, 4, 4 + gr * 2, 4 + gr * 2],
               outline=(255, 255, 255, 200), width=3)
    img.paste(globe, (gx - gr - 4, gy - gr - 4), globe)

    # thermometer gauge, right of globe
    tx = x + 480
    draw.rounded_rectangle([tx, y + 26, tx + 26, y + h - 58], radius=13,
                           fill=WHITE, outline=INK, width=2)
    draw.rounded_rectangle([tx + 6, y + 52, tx + 20, y + h - 64], radius=7,
                           fill=(232, 226, 208))
    draw.rounded_rectangle([tx + 6, y + 78, tx + 20, y + h - 64], radius=7,
                           fill=RED)
    draw.ellipse([tx - 6, y + h - 78, tx + 32, y + h - 52], fill=RED,
                 outline=INK, width=2)
    draw.ellipse([tx + 2, y + h - 70, tx + 24, y + h - 60], fill=RED_DARK)
    tf = F_SANS_B(20)
    draw.text((tx + 40, y + 66), "1.5°C", font=tf, fill=RED_DARK)
    sf = F_SANS(14)
    draw.text((tx + 40, y + 92), "warming limit", font=sf, fill=INK_SOFT)
    draw.text((tx + 40, y + 110), "now in sight", font=sf, fill=INK_SOFT)

    # smokestacks, far right, standing on the panel's bottom edge
    bx = x + w - 210
    base = y + h - 8
    for i, (sx0, sh) in enumerate(((0, 74), (34, 96), (68, 62))):
        draw.rectangle([bx + sx0, base - sh, bx + sx0 + 26, base],
                       fill=(52, 64, 92))
        draw.rectangle([bx + sx0 - 3, base - sh - 6, bx + sx0 + 29,
                        base - sh], fill=(20, 33, 61))
        for j, r in enumerate((9, 7, 5)):
            draw.ellipse([bx + sx0 + 4 + j * 2, base - sh - 20 - j * 14,
                          bx + sx0 + 4 + j * 2 + r * 2,
                          base - sh - 20 - j * 14 + r * 2],
                         fill=(226, 222, 210))
    # "IN OVERTIME" tag, top-right corner of the panel
    tag = "IN OVERTIME"
    tag_f = F_SANS_B(13)
    tag_w = int(draw.textlength(tag, font=tag_f)) + 22
    tag_x = x + w - tag_w - 14
    draw.rounded_rectangle([tag_x, y + 12, tag_x + tag_w, y + 38], radius=13,
                           fill=RED)
    draw.text((tag_x + 11, y + 17), tag, font=tag_f, fill=WHITE)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    draw.rectangle([0, 0, W, 116], fill=INK)
    title_f = F_SERIF(52)
    draw.text((W // 2, 22), "THE WORLD IN ONE PICTURE", font=title_f,
              fill=WHITE, anchor="ma")
    spaced(draw, 0, 88, "SATURDAY  •  21 NOVEMBER 2026  •  WORLD EDITION",
           F_SANS_B(15), GOLD, tracking=4, center=W // 2)
    draw.rectangle([0, 116, W, 121], fill=RED)

    # ---- lead story ----------------------------------------------------
    y = 140
    spaced(draw, MARGIN, y, "CLIMATE  •  ANTALYA, TÜRKIYE",
           F_SANS_B(15), RED_DARK, tracking=2)
    y = 164
    draw.text((MARGIN, y), "COP31 IN OVERTIME", font=F_SERIF(62), fill=INK)
    y = 234
    sub = ("Fossil-fuel deadlock drags the climate talks past their "
           "deadline as a third draft is due on Saturday")
    y = draw_lines(draw, MARGIN, y, wrap(draw, sub, F_SERIF_REG(26), CW),
                   F_SERIF_REG(26), INK_SOFT, 32)
    y += 8
    deck = ("Nearly 200 nations are deadlocked over a draft deal that drops "
            "every mention of fossil fuels and a $120bn adaptation fund. "
            "The EU warns the summit risks becoming a “fossil summit”.")
    y = draw_lines(draw, MARGIN, y, wrap(draw, deck, F_SANS(16), CW),
                   F_SANS(16), INK_SOFT, 21)
    y += 12
    draw_lead_visual(img, draw, MARGIN, y, CW, 196)
    y += 196 + 10
    cap_f = F_SERIF_REG(14)
    draw.text((MARGIN, y),
              "Delegates in Antalya race the clock as the summit spills into "
              "Saturday, with the 1.5°C limit now in sight.",
              font=cap_f, fill=GREY)
    y += 24
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    draw.line([MARGIN, y + 4, W - MARGIN, y + 4], fill=RULE, width=1)

    # ---- supporting stories, 3 x 2 grid --------------------------------
    grid_y = y + 18
    col_w = (CW - 2 * 26) // 3  # 300
    row_h = 138
    stories = [
        ("MARKETS",
         "Wall Street slides into correction",
         "US stocks fell about 3.7% on Friday as AI shares sold off, "
         "pushing the S&P 500 and the Dow into correction territory."),
        ("EUROPE",
         "Estonia shuts its Russia border",
         "All crossings closed after suspected arson sabotage; Tallinn "
         "cites a security threat on its eastern frontier."),
        ("ASIA",
         "Mongolia’s president resigns",
         "The resignation sets the stage for a snap election, officials "
         "in Ulaanbaatar confirm."),
        ("CYBER",
         "Banks hit by vendor cyberattack",
         "JPMorgan, Visa and Mastercard report incidents at outside "
         "providers; core payment networks stay unaffected."),
        ("SPORT",
         "India fight back in Wellington",
         "India reach 159 for 1 at stumps on day two of the first Test, "
         "trailing New Zealand by 209 runs."),
        ("MOTORS",
         "Hyundai unveils new Elantra",
         "The eighth-generation sedan debuts at the Los Angeles Auto "
         "Show, with hybrid options and new connected tech."),
    ]
    for i, (kick, head, dk) in enumerate(stories):
        cx = MARGIN + (i % 3) * (col_w + 26)
        cy = grid_y + (i // 3) * (row_h + 16)
        story_cell(draw, cx, cy, col_w, kick, head, dk)

    # ---- footer ticker --------------------------------------------------
    tick_y = grid_y + 2 * row_h + 16 + 14
    draw.rectangle([0, tick_y, W, tick_y + 46], fill=INK)
    tick = ("WARSAW SEEKS MORE NATO FORCES AFTER MISSILE INCURSION   •   "
            "DENMARK ALLEGES RUSSIAN PLOT TO KILL US-UKRAINIAN   •   "
            "NIKHIL GUPTA JAILED 19+ YEARS IN US   •   PANAMA THREATENS "
            "COP31 WALKOUT   •   SENSEX RALLIES 898 POINTS")
    tf = F_SANS_B(13)
    tlines = wrap(draw, tick, tf, CW)
    ty = tick_y + 7
    for line in tlines:
        draw.text((MARGIN, ty), line, font=tf, fill=WHITE)
        ty += 17

    foot_y = tick_y + 46 + 10
    draw.text((W // 2, foot_y),
              "Compiled from wire reports  •  Saturday 21 November 2026  •  "
              "All stories first reported on 21 November 2026 (UTC)",
              font=F_SANS(12), fill=GREY, anchor="ma")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({path.stat().st_size} bytes)")
