#!/usr/bin/env python3
"""Contact sheets for the S5 exploration. Judge at real sizes, never at 1024."""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

from generate import CONCEPTS, APPS

HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, "svg")
CACHE = os.path.join(HERE, ".raster")
os.makedirs(CACHE, exist_ok=True)

BG = (13, 11, 9)
INK = (243, 231, 218)
DIM = (150, 132, 116)


def font(sz, bold=False):
    for p in ("/System/Library/Fonts/Supplemental/Helvetica.ttc",
              "/System/Library/Fonts/HelveticaNeue.ttc"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz, index=1 if bold else 0)
    return ImageFont.load_default()


def png(slug, size):
    out = os.path.join(CACHE, f"{slug}@{size}.png")
    if not os.path.exists(out):
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                        os.path.join(SVG, f"{slug}.svg"), "-o", out], check=True)
    return Image.open(out).convert("RGBA")


ROW_H = 172
W = 1424
PAD = 28
LABEL_W = 236


def wrap_text(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build(concepts, path, title):
    h = 84 + len(concepts) * ROW_H + 20
    im = Image.new("RGB", (W, h), BG)
    d = ImageDraw.Draw(im)
    d.text((PAD, 26), title, font=font(19, True), fill=INK)
    d.text((PAD, 54), "hub mark  ·  eight members at 84px  ·  the same eight at 16px (favicon, actual size)",
           font=font(12), fill=DIM)

    y = 84
    small = font(11)
    for slug, name, thesis, _fn in concepts:
        d.line([(PAD, y), (W - PAD, y)], fill=(38, 32, 26), width=1)
        d.text((PAD, y + 16), name, font=font(15, True), fill=INK)
        for n, ln in enumerate(wrap_text(d, thesis, small, LABEL_W)):
            d.text((PAD, y + 38 + n * 15), ln, font=small, fill=DIM)

        x = PAD + LABEL_W + 22
        s = png(f"{slug}-suite", 104)
        im.paste(s, (x, y + 32), s)
        d.text((x + 38, y + 142), "hub", font=font(10), fill=DIM)

        x += 136
        for app, _label, _col in APPS:
            m = png(f"{slug}-{app}", 84)
            im.paste(m, (x, y + 42), m)
            x += 94

        x += 20
        strip_x = x
        for app, _label, _col in APPS:
            m = png(f"{slug}-{app}", 16)
            im.paste(m, (x, y + 76), m)
            x += 24
        d.text((strip_x, y + 102), "16px", font=font(10), fill=DIM)
        y += ROW_H

    im.save(path)
    print("wrote", path, im.size)


if __name__ == "__main__":
    build(CONCEPTS[:5], os.path.join(HERE, "sheet-1.png"),
          "Clear Suite · S5 identity exploration — sheet 1 of 2")
    build(CONCEPTS[5:], os.path.join(HERE, "sheet-2.png"),
          "Clear Suite · S5 identity exploration — sheet 2 of 2")
