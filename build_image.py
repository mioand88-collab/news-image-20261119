#!/usr/bin/env python3
"""Build entry.png: one 1024x1024 poster summing up the world news of
Thursday, 19 November 2026, as reported that day (Reuters, Yonhap, the
Guardian's APEC live coverage, Al Jazeera and the day's news roundups).

Run locally to regenerate the image the entry ships:
    python3 build_image.py
The grader never runs this file; main.ts copies the finished entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (18, 18, 20)
RED = (178, 32, 40)
BLUE = (24, 62, 122)
RULE = (30, 30, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, width, kicker, head, body, head_size=30, body_size=21):
    draw.text((x, y), kicker, font=font(SANS_B, 17), fill=RED)
    y += 26
    for line in wrap(draw, head, font(SERIF_B, head_size), width):
        draw.text((x, y), line, font=font(SERIF_B, head_size), fill=INK)
        y += head_size + 6
    y += 2
    for line in wrap(draw, body, font(SANS, body_size), width):
        draw.text((x, y), line, font=font(SANS, body_size), fill=(45, 45, 50))
        y += body_size + 6
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 56  # margin

    # Masthead
    d.rectangle([0, 0, W, 138], fill=INK)
    d.text((M, 22), "THE WORLD IN ONE IMAGE", font=font(SERIF_B, 55), fill=(250, 248, 240))
    d.text((M, 96), "Thursday, 19 November 2026  ·  The day's world news, summed up",
           font=font(SANS, 22), fill=(205, 205, 210))

    y = 162
    # Lead story, full width
    y = block(
        d, M, y, W - 2 * M,
        "LEAD · SHENZHEN",
        "Three presidents, one room: the first Trump-Xi-Putin summit",
        "The leaders of the world's three largest nuclear powers held their first-ever "
        "trilateral summit at Shenzhen's Kylin Villa, on the sidelines of APEC. Trump "
        "pressed for nuclear arms control, Beijing resisted making it the centrepiece, "
        "and whether a joint statement would follow was unclear.",
        head_size=33, body_size=21,
    )
    y += 6
    d.line([M, y, W - M, y], fill=RULE, width=3)
    y += 14

    # Two columns
    col_w = (W - 2 * M - 36) // 2
    x2 = M + col_w + 36
    y_left = block(
        d, M, y, col_w,
        "UKRAINE",
        "Crimean Bridge hit a third time",
        "Ukrainian forces struck the bridge's railway section early today, halting rail "
        "traffic days after strikes collapsed a road span. Deep strikes have reportedly "
        "cut Russian refinery processing by 45%.",
    )
    y_right = block(
        d, x2, y, col_w,
        "IRAN & GAZA",
        "Washington weighs new strikes",
        "Trump is weighing fresh strikes on Iran as Israel urges action; Mossad's "
        "director heads to Washington on Friday. In Gaza, Israeli tanks crossed the "
        "ceasefire line in a limited operation.",
    )
    y = max(y_left, y_right) + 4
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 12

    y_left = block(
        d, M, y, col_w,
        "APEC PLENARY",
        "Xi sells openness, pledges $20m",
        "Opening the leaders' plenary, Xi cast China as the defender of an open "
        "Asia-Pacific and pledged $20 million for regional cooperation. Albanese "
        "told Putin to end the war now.",
    )
    y_right = block(
        d, x2, y, col_w,
        "ESPIONAGE",
        "Spy charge in Silicon Valley",
        "A Russian national was charged with spying on and targeting Silicon Valley, "
        "in what US officials called an unacceptable attempt at intimidation.",
    )
    y = max(y_left, y_right) + 4
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 6

    # Bottom strip: three briefs
    briefs = [
        ("TRADE TRUCE", "The US-China truce expires 10 January; rare-earth exports run ~75% below normal."),
        ("OIL", "Brent crude held near $92 as Hormuz energy flows stayed on the summit table."),
        ("NORTH KOREA", "Whether Trump would meet Kim Jong-un in China remained an open question."),
    ]
    bw = (W - 2 * M - 2 * 24) // 3
    for i, (k, t) in enumerate(briefs):
        bx = M + i * (bw + 24)
        d.text((bx, y), k, font=font(SANS_B, 16), fill=BLUE)
        by = y + 21
        for line in wrap(d, t, font(SANS, 16), bw):
            d.text((bx, by), line, font=font(SANS, 16), fill=(45, 45, 50))
            by += 20

    # Footer
    d.rectangle([0, H - 52, W, H], fill=INK)
    d.text((M, H - 38), "Compiled from the day's reporting: Reuters · Yonhap · The Guardian · Al Jazeera",
           font=font(SANS, 19), fill=(220, 220, 224))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
