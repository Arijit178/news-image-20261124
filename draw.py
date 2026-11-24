#!/usr/bin/env python3
"""Render the Tuesday 24 November 2026 news poster, 1024 by 1024.

A navy masthead names the day, then eight white tiles in two columns
tell the day's stories: the Strait of Hormuz closed after tankers are
hit, the ICJ genocide verdict on Myanmar, a Gaza strike, a NATO space
warning, an attack on Zaporizhzhia, a car bomb in Colombia, UK sanctions
on the Houthis, and an earthquake in Nepal. Every picture is a flat
shape drawn here with Pillow; there are no photographs and no borrowed
artwork. The output is deterministic.
Usage: python3 draw.py  ->  writes entry.png in this folder.
"""

from PIL import Image, ImageDraw, ImageFont
import math

SIZE = 1024
PAPER = (248, 244, 236)
DARK = (22, 26, 36)
NAVY = (16, 36, 64)
GOLD = (198, 160, 38)
MUTED = (88, 94, 106)
CARD = (255, 255, 255)
EDGE = (208, 203, 188)

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
BOLD_PATH = DEJAVU + "DejaVuSans-Bold.ttf"
PLAIN_PATH = DEJAVU + "DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def split_text(canvas, text, face, limit):
    """Break text into lines that fit inside limit pixels."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            test = line + " " + word
            if canvas.textlength(test, font=face) <= limit:
                line = test
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def fit(canvas, text, face, limit, most):
    """Use the face, shrinking it until the text fits in most lines."""
    size = face.size
    while size > 11:
        face_now = load(face.path, size)
        got = split_text(canvas, text, face_now, limit)
        if len(got) <= most:
            return got, face_now
        size -= 1
    face_now = load(face.path, size)
    return split_text(canvas, text, face_now, limit), face_now


def emblem(canvas, shape, cx, cy, radius, colour):
    """Draw one tiny flat emblem from basic shapes."""
    if shape == "burst":
        pts = []
        for i in range(12):
            ang = -90 + i * 30
            rad = radius if i % 2 == 0 else radius * 0.5
            pts.append((cx + rad * math.cos(math.radians(ang)),
                        cy + rad * math.sin(math.radians(ang))))
        canvas.polygon(pts, fill=colour)
    elif shape == "drop":
        canvas.ellipse([cx - radius * 0.7, cy - radius * 0.4,
                        cx + radius * 0.7, cy + radius], fill=colour)
        canvas.polygon([(cx, cy - radius), (cx + radius * 0.7, cy),
                        (cx - radius * 0.7, cy)], fill=colour)
    elif shape == "arrow":
        canvas.line([(cx - radius, cy + radius * 0.5),
                     (cx - radius * 0.25, cy),
                     (cx + radius * 0.25, cy + radius * 0.4),
                     (cx + radius, cy - radius * 0.6)],
                    fill=colour, width=4, joint="curve")
    elif shape == "shield":
        canvas.polygon([(cx - radius * 0.8, cy - radius * 0.6),
                        (cx + radius * 0.8, cy - radius * 0.6),
                        (cx + radius * 0.8, cy + radius * 0.2),
                        (cx, cy + radius),
                        (cx - radius * 0.8, cy + radius * 0.2)],
                       fill=colour)
    elif shape == "globe":
        canvas.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                       outline=colour, width=4)
        canvas.line([cx - radius, cy, cx + radius, cy], fill=colour, width=3)
        canvas.arc([cx - radius * 0.5, cy - radius, cx + radius * 0.5,
                    cy + radius], 270, 90, fill=colour, width=3)
    elif shape == "bolt":
        canvas.polygon([(cx + radius * 0.3, cy - radius),
                        (cx - radius * 0.5, cy + radius * 0.1),
                        (cx, cy + radius * 0.1),
                        (cx - radius * 0.3, cy + radius),
                        (cx + radius * 0.5, cy - radius * 0.1),
                        (cx, cy - radius * 0.1)], fill=colour)
    elif shape == "plus":
        canvas.rectangle([cx - radius * 0.25, cy - radius,
                          cx + radius * 0.25, cy + radius], fill=colour)
        canvas.rectangle([cx - radius, cy - radius * 0.25,
                          cx + radius, cy + radius * 0.25], fill=colour)
    elif shape == "flame":
        canvas.polygon([(cx, cy - radius),
                        (cx + radius * 0.75, cy + radius * 0.2),
                        (cx + radius * 0.3, cy + radius),
                        (cx - radius * 0.3, cy + radius),
                        (cx - radius * 0.75, cy + radius * 0.2)],
                       fill=colour)


# kicker, headline, body, colour, emblem
NEWS = [
    ("STRAIT OF HORMUZ",
     "Iran says four tankers hit; strait closed further",
     "Iran says four tankers were hit by mines and the strait stays "
     "closed until Washington meets Tehran's conditions.",
     (196, 96, 16), "drop"),
    ("THE HAGUE  •  ICJ",
     "Myanmar guilty of genocide against the Rohingya",
     "The world court rules 9-6 on the 2017 crackdown — the first time "
     "the UN's highest court has found a state guilty of genocide.",
     (16, 36, 64), "shield"),
    ("GAZA",
     "Israel kills Hamas security chief in Gaza strike",
     "Brig. Gen. Naeem Abu Nahel is killed in a strike; six others "
     "are killed with him, reports say.",
     (176, 32, 32), "burst"),
    ("SPACE  •  NATO",
     "NATO vows defence as Russia 'may launch nuclear satellite'",
     "Mark Rutte warns of a space threat after reports Russia may "
     "launch a nuclear-armed satellite, dubbed Sputnik-S, in 60 days.",
     (43, 84, 160), "globe"),
    ("ZAPORIZHZHIA  •  UKRAINE",
     "Russian attack kills 2, wounds 40 in Zaporizhzhia",
     "An overnight strike hits an apartment building; four children "
     "are among the wounded.",
     (176, 32, 32), "flame"),
    ("VILLAVICENCIO  •  COLOMBIA",
     "Car bomb injures 23 on eve of FARC deal anniversary",
     "A bomb outside regional government offices wounds 23 people, "
     "on the eve of the peace deal's 10th anniversary.",
     (196, 96, 16), "burst"),
    ("LONDON  •  UK",
     "UK sanctions Yemen's Houthis and four officials",
     "Asset freezes and travel bans target the Houthi movement and "
     "four senior officials.",
     (31, 120, 74), "shield"),
    ("KOSHI  •  NEPAL",
     "Magnitude 5.4 earthquake shakes Nepal",
     "The quake strikes Koshi Province; tremors are felt across India, "
     "Bhutan and Bangladesh.",
     (0, 110, 120), "bolt"),
]


def build():
    pic = Image.new("RGB", (SIZE, SIZE), PAPER)
    pen = ImageDraw.Draw(pic)

    pen.rectangle([0, 0, SIZE, 150], fill=NAVY)
    pen.rectangle([0, 150, SIZE, 156], fill=GOLD)
    head = load(BOLD_PATH, 50)
    words = "THE WORLD IN ONE DAY"
    pen.text(((SIZE - pen.textlength(words, font=head)) / 2, 20),
             words, font=head, fill=(255, 255, 255))
    day = load(BOLD_PATH, 33)
    when = "TUESDAY, 24 NOVEMBER 2026"
    pen.text(((SIZE - pen.textlength(when, font=day)) / 2, 82),
             when, font=day, fill=(255, 214, 90))
    note = load(PLAIN_PATH, 20)
    tag = "Eight stories from around the world  •  Tuesday's news, in one picture"
    pen.text(((SIZE - pen.textlength(tag, font=note)) / 2, 122),
             tag, font=note, fill=(198, 208, 224))

    margin, gap = 20, 16
    top, base = 172, 984
    wide = (SIZE - 2 * margin - gap) // 2
    tall = (base - top - 3 * gap) // 4
    kick = load(BOLD_PATH, 18)
    head_f = load(BOLD_PATH, 26)
    body_f = load(PLAIN_PATH, 20)

    for pos, (kicker, title, body, colour, shape) in enumerate(NEWS):
        col, row = pos % 2, pos // 2
        x = margin + col * (wide + gap)
        y = top + row * (tall + gap)
        pen.rounded_rectangle([x, y, x + wide, y + tall], radius=10,
                              fill=CARD, outline=EDGE, width=1)
        pen.rectangle([x, y, x + wide, y + 6], fill=colour)
        emblem(pen, shape, x + wide - 34, y + 36, 16, colour)
        pen.text((x + 16, y + 20), kicker, font=kick, fill=colour)
        lines, face = fit(pen, title, head_f, wide - 32, 2)
        yy = y + 50
        for line in lines:
            pen.text((x + 16, yy), line, font=face, fill=DARK)
            yy += face.size + 4
        blines, bface = fit(pen, body, body_f, wide - 32, 3)
        yy += 6
        for line in blines:
            pen.text((x + 16, yy), line, font=bface, fill=(52, 58, 70))
            yy += bface.size + 5

    foot = load(PLAIN_PATH, 15)
    credit = "Sources: Reuters, BBC, ICJ, The Statesman  •  24 November 2026"
    pen.text(((SIZE - pen.textlength(credit, font=foot)) / 2, 992),
             credit, font=foot, fill=MUTED)

    pic.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build()
