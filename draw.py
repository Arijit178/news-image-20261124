#!/usr/bin/env python3
"""Draw Tuesday 24 November 2026 as a one-page newspaper poster.

The page is 1024 square. A dark masthead carries the title and the
date, and below it eight news cards are arranged in two columns and
four rows. Each card has a coloured top rule, a place label, a bold
headline, a short paragraph, and a small geometric mark drawn with
Pillow primitives. No photograph or borrowed artwork is used anywhere.
Running this file writes entry.png next to it, and the bytes are the
same every time it runs.
"""

import math
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
BACKGROUND = (247, 243, 235)
INK = (24, 28, 40)
MASTHEAD = (14, 34, 62)
ACCENT = (199, 161, 39)
GREY = (90, 96, 108)
CARD_FILL = (255, 255, 255)
CARD_LINE = (210, 205, 190)
BODY_INK = (54, 60, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
STRONG = FONT_DIR + "DejaVuSans-Bold.ttf"
REGULAR = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, words, face, width):
    """Wrap words to the given pixel width, returning a list of lines."""
    lines = []
    for paragraph in words.split("\n"):
        current = ""
        for word in paragraph.split():
            candidate = word if not current else current + " " + word
            if draw.textlength(candidate, font=face) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def shrink(draw, words, face, width, limit):
    """Shrink a font until the wrapped text fits in at most limit lines."""
    size = face.size
    while size > 11:
        current = font(face.path, size)
        if len(wrap(draw, words, current, width)) <= limit:
            return wrap(draw, words, current, width), current
        size -= 1
    current = font(face.path, size)
    return wrap(draw, words, current, width), current


def mark(draw, kind, cx, cy, r, colour):
    """A small geometric mark: star, drop, globe, shield, flame, bolt."""
    if kind == "star":
        points = []
        for i in range(12):
            angle = math.radians(-90 + i * 30)
            radius = r if i % 2 == 0 else r * 0.45
            points.append((cx + radius * math.cos(angle),
                           cy + radius * math.sin(angle)))
        draw.polygon(points, fill=colour)
    elif kind == "drop":
        draw.ellipse([cx - r * 0.7, cy - r * 0.4, cx + r * 0.7, cy + r],
                     fill=colour)
        draw.polygon([(cx, cy - r), (cx + r * 0.7, cy),
                      (cx - r * 0.7, cy)], fill=colour)
    elif kind == "globe":
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
        draw.line([cx - r, cy, cx + r, cy], fill=colour, width=3)
        draw.arc([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r],
                 270, 90, fill=colour, width=3)
    elif kind == "shield":
        draw.polygon([(cx - r * 0.8, cy - r * 0.6), (cx + r * 0.8, cy - r * 0.6),
                      (cx + r * 0.8, cy + r * 0.2), (cx, cy + r),
                      (cx - r * 0.8, cy + r * 0.2)], fill=colour)
    elif kind == "flame":
        draw.polygon([(cx, cy - r), (cx + r * 0.75, cy + r * 0.2),
                      (cx + r * 0.3, cy + r), (cx - r * 0.3, cy + r),
                      (cx - r * 0.75, cy + r * 0.2)], fill=colour)
    elif kind == "bolt":
        draw.polygon([(cx + r * 0.3, cy - r), (cx - r * 0.5, cy + r * 0.1),
                      (cx, cy + r * 0.1), (cx - r * 0.3, cy + r),
                      (cx + r * 0.5, cy - r * 0.1), (cx, cy - r * 0.1)],
                     fill=colour)


STORIES = [
    {"place": "STRAIT OF HORMUZ",
     "headline": "Iran says four tankers hit; strait closed further",
     "text": "Iran says four tankers were hit by mines and the strait "
             "stays closed until Washington meets Tehran's conditions.",
     "colour": (196, 96, 16), "mark": "drop"},
    {"place": "THE HAGUE  •  ICJ",
     "headline": "Myanmar guilty of genocide against the Rohingya",
     "text": "The world court rules 9-6 on the 2017 crackdown — the "
             "first time the UN's highest court has found a state "
             "guilty of genocide.",
     "colour": (16, 36, 64), "mark": "shield"},
    {"place": "GAZA",
     "headline": "Israel kills Hamas security chief in Gaza strike",
     "text": "Brig. Gen. Naeem Abu Nahel is killed in a strike; six "
             "others are killed with him, reports say.",
     "colour": (176, 32, 32), "mark": "star"},
    {"place": "SPACE  •  NATO",
     "headline": "NATO vows defence as Russia 'may launch nuclear satellite'",
     "text": "Mark Rutte warns of a space threat after reports Russia "
             "may launch a nuclear-armed satellite, dubbed Sputnik-S, "
             "in 60 days.",
     "colour": (43, 84, 160), "mark": "globe"},
    {"place": "ZAPORIZHZHIA  •  UKRAINE",
     "headline": "Russian attack kills 2, wounds 40 in Zaporizhzhia",
     "text": "An overnight strike hits an apartment building; four "
             "children are among the wounded.",
     "colour": (176, 32, 32), "mark": "flame"},
    {"place": "VILLAVICENCIO  •  COLOMBIA",
     "headline": "Car bomb injures 23 on eve of FARC deal anniversary",
     "text": "A bomb outside regional government offices wounds 23 "
             "people, on the eve of the peace deal's 10th anniversary.",
     "colour": (196, 96, 16), "mark": "star"},
    {"place": "LONDON  •  UK",
     "headline": "UK sanctions Yemen's Houthis and four officials",
     "text": "Asset freezes and travel bans target the Houthi movement "
             "and four senior officials.",
     "colour": (31, 120, 74), "mark": "shield"},
    {"place": "KOSHI  •  NEPAL",
     "headline": "Magnitude 5.4 earthquake shakes Nepal",
     "text": "The quake strikes Koshi Province; tremors are felt across "
             "India, Bhutan and Bangladesh.",
     "colour": (0, 110, 120), "mark": "bolt"},
]


def render():
    page = Image.new("RGB", (PAGE, PAGE), BACKGROUND)
    draw = ImageDraw.Draw(page)

    draw.rectangle([0, 0, PAGE, 150], fill=MASTHEAD)
    draw.rectangle([0, 150, PAGE, 156], fill=ACCENT)
    title_face = font(STRONG, 50)
    title = "THE WORLD IN ONE DAY"
    draw.text(((PAGE - draw.textlength(title, font=title_face)) / 2, 20),
              title, font=title_face, fill=(255, 255, 255))
    date_face = font(STRONG, 33)
    date = "TUESDAY, 24 NOVEMBER 2026"
    draw.text(((PAGE - draw.textlength(date, font=date_face)) / 2, 82),
              date, font=date_face, fill=(255, 214, 90))
    sub_face = font(REGULAR, 20)
    subtitle = "Eight stories from around the world  •  Tuesday's news, in one picture"
    draw.text(((PAGE - draw.textlength(subtitle, font=sub_face)) / 2, 122),
              subtitle, font=sub_face, fill=(198, 208, 224))

    margin = 20
    spacing = 16
    grid_top = 172
    grid_bottom = 984
    card_w = (PAGE - 2 * margin - spacing) // 2
    card_h = (grid_bottom - grid_top - 3 * spacing) // 4
    label_face = font(STRONG, 18)
    title_face = font(STRONG, 26)
    text_face = font(REGULAR, 20)

    for index, story in enumerate(STORIES):
        column = index % 2
        row = index // 2
        x = margin + column * (card_w + spacing)
        y = grid_top + row * (card_h + spacing)
        colour = story["colour"]
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=10,
                               fill=CARD_FILL, outline=CARD_LINE, width=1)
        draw.rectangle([x, y, x + card_w, y + 6], fill=colour)
        mark(draw, story["mark"], x + card_w - 34, y + 36, 16, colour)
        draw.text((x + 16, y + 20), story["place"], font=label_face, fill=colour)
        headline_lines, headline_face = shrink(
            draw, story["headline"], title_face, card_w - 32, 2)
        cursor = y + 50
        for line in headline_lines:
            draw.text((x + 16, cursor), line, font=headline_face, fill=INK)
            cursor += headline_face.size + 4
        body_lines, body_face = shrink(
            draw, story["text"], text_face, card_w - 32, 3)
        cursor += 6
        for line in body_lines:
            draw.text((x + 16, cursor), line, font=body_face, fill=BODY_INK)
            cursor += body_face.size + 5

    credit_face = font(REGULAR, 15)
    credit = "Sources: Reuters, BBC, ICJ, The Statesman  •  24 November 2026"
    draw.text(((PAGE - draw.textlength(credit, font=credit_face)) / 2, 992),
              credit, font=credit_face, fill=GREY)

    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    render()
