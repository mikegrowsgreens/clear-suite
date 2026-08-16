#!/usr/bin/env python3
"""
Clear Suite identity — round two. Originals.

Round one was rejected, correctly: ten parameter sweeps rather than ten marks.
A rect or a circle moved around a brown tile by formula, with no type, no
drawn character and no warmth — the opposite of Field Guide.

What changes here:
  - real Fraunces outlines where a letterform belongs
  - every tile carries its app's own light, so eight apps are eight evenings
    rather than one brown tile eight times
  - figures are 60-72% of the tile instead of 35%
  - the per-app difference is hue and object, not a parameter step

Atmosphere lives in the ground gradient. The figure stays flat, so the mark
still survives mono and the derive pipeline.
"""
import json
import math
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/private/tmp/claude-501/-Users-mikepaulus-Desktop-Claude-Code/"
           "8cd0a4c7-0e3e-4691-a0f9-b32ab0427c12/scratchpad")
PY = os.path.expanduser("~/.claude/skills/logo-design/.venv/bin/python")
OUTLINE = os.path.expanduser("~/.claude/skills/logo-design/scripts/outline-text.py")
FRAUNCES = os.path.join(SCRATCH, "fraunces-display.ttf")

S = 512
C = S / 2
TILE_R = 114

APPS = [
    ("flow",   "Clear Flow",   "#D17C67"),
    ("air",    "Clear Air",    "#6C9C8E"),
    ("mind",   "Clear Mind",   "#7B9E46"),
    ("body",   "Clear Body",   "#CE7D83"),
    ("feed",   "Clear Feed",   "#9A8DB4"),
    ("odds",   "Clear Odds",   "#C89B4A"),
    ("sight",  "Clear Sight",  "#8394AE"),
    ("energy", "Clear Energy", "#D08A2C"),
]
SUITE = "#E8CFA9"
CREAM = "#F3E7DA"

_glyphs = {}


def glyph(text, size=200):
    """Real outlined Fraunces. Baseline at zero, y already flipped."""
    key = (text, size)
    if key not in _glyphs:
        out = subprocess.run(
            [PY, OUTLINE, FRAUNCES, text, "--size", str(size), "--json"],
            capture_output=True, text=True, check=True)
        _glyphs[key] = json.loads(out.stdout)
    return _glyphs[key]


def centred_glyph(text, cap, cx, cy, fill, size=200):
    """Place a glyph optically centred on (cx, cy) at the given cap height."""
    g = glyph(text, size)
    k = cap / g["ascent"]
    w = g["width"] * k
    x = cx - w / 2
    y = cy + (g["ascent"] * k) / 2
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.5f})">'
            f'<path d="{g["d"]}" fill="{fill}"/></g>')


def head(defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
            f'width="{S}" height="{S}">\n<defs>\n'
            f'<radialGradient id="g" cx="50%" cy="0%" r="120%">'
            f'<stop offset="0%" stop-color="#2A1E15"/>'
            f'<stop offset="60%" stop-color="#17120E"/></radialGradient>\n'
            f'<clipPath id="t"><rect width="{S}" height="{S}" rx="{TILE_R}"/></clipPath>\n'
            f'{defs}</defs>\n'
            f'<rect width="{S}" height="{S}" rx="{TILE_R}" fill="url(#g)"/>\n'
            f'<g clip-path="url(#t)">')


def wash(col, cx="50%", cy="100%", op=".30"):
    """The app's own light in the tile. This is what makes eight evenings."""
    return (f'<radialGradient id="w" cx="{cx}" cy="{cy}" r="95%">'
            f'<stop offset="0%" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="100%" stop-color="{col}" stop-opacity="0"/>'
            f'</radialGradient>')


def tile(col, body, wcx="50%", wcy="100%", wop=".30"):
    return (head(wash(col, wcx, wcy, wop))
            + f'<rect width="{S}" height="{S}" fill="url(#w)"/>'
            + body + "</g></svg>")


# --------------------------------------------------------------------------
# O1 Aperture — the Fraunces C the whole suite is named for, at display size.
# --------------------------------------------------------------------------
def o1(i, col):
    return tile(col, centred_glyph("C", 300, C, C + 4, col), wcy="8%", wop=".26")


# --------------------------------------------------------------------------
# O2 Seal — a wax seal with the C struck into it. A record you closed yourself.
# --------------------------------------------------------------------------
def o2(i, col):
    r, n = 168, 26
    pts = []
    for k in range(n * 2):
        a = math.pi * k / n
        rr = r + (13 if k % 2 else 0)
        pts.append(f"{C + rr * math.cos(a):.1f},{C + rr * math.sin(a):.1f}")
    return tile(col,
                f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
                + centred_glyph("C", 176, C, C + 2, "#17120E"),
                wcy="14%", wop=".22")


# --------------------------------------------------------------------------
# O3 Window — a lit window seen from outside. Someone is home.
# --------------------------------------------------------------------------
def o3(i, col):
    x, y, w, h, m = 128, 104, 256, 304, 15
    pw, ph = (w - m) / 2, (h - m) / 2
    panes = "".join(
        f'<rect x="{x + cx * (pw + m):.0f}" y="{y + cy * (ph + m):.0f}"'
        f' width="{pw:.0f}" height="{ph:.0f}"'
        f' rx="{"78" if cy == 0 else "10"}" fill="{col}"/>'
        for cy in (0, 1) for cx in (0, 1))
    return tile(col,
                f'<rect x="{x - 26}" y="{y - 26}" width="{w + 52}" height="{h + 52}"'
                f' rx="{(w + 52) / 2:.0f}" fill="{col}" opacity=".13"/>' + panes,
                wcy="55%", wop=".20")


# --------------------------------------------------------------------------
# O4 Moonrise — a fixed horizon and the hour of the evening. A cycle, not a
# score: nothing here fills up, so no app reads as further along than another.
# --------------------------------------------------------------------------
def o4(i, col):
    gy = 356
    ground = (f'<path d="M-20,{gy + 40} Q{C},{gy - 46} {S + 20},{gy + 40}'
              f' L{S + 20},{S + 20} L-20,{S + 20} Z" fill="{col}" opacity=".30"/>')
    if i is None:
        b = f'<circle cx="{C}" cy="196" r="104" fill="{col}"/>'
        for n in range(8):
            a = math.radians(196 + n * 21)
            b += (f'<circle cx="{C + 214 * math.cos(a):.1f}"'
                  f' cy="{300 + 214 * math.sin(a):.1f}" r="15" fill="{col}" opacity=".45"/>')
        return tile(col, b + ground, wcy="72%", wop=".22")
    a = math.radians(200 + i * 20)
    mx, my = C + 208 * math.cos(a), 322 + 208 * math.sin(a)
    return tile(col,
                f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="150" fill="{col}" opacity=".14"/>'
                f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="86" fill="{col}"/>' + ground,
                wcx=f"{100 * mx / S:.0f}%", wcy=f"{100 * my / S:.0f}%", wop=".26")


# --------------------------------------------------------------------------
# O5 Bookmark — your place in your own book.
# --------------------------------------------------------------------------
def o5(i, col):
    x, y, w, h = 116, 84, 280, 344
    rx = 116 + (0 if i is None else 0)
    bx = 168 + (0 if i is None else i * 22)
    ribbon = (f'<path d="M{bx},{y} h58 v168 l-29,-40 l-29,40 z" fill="{col}"/>'
              if i is not None else
              "".join(f'<path d="M{168 + n * 22},{y} h14 v{120 + (n % 2) * 26}'
                      f' l-7,-22 l-7,22 z" fill="{col}"/>' for n in range(8)))
    return tile(col,
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{CREAM}"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{col}" opacity=".10"/>'
                + ribbon, wcy="20%", wop=".24")


# --------------------------------------------------------------------------
# O6 Doorway — a lit door at the end of a long day. You are the one leaving.
# --------------------------------------------------------------------------
def o6(i, col):
    x, w, top, bot = 138, 236, 118, 402
    r = w / 2
    outer = (f'M{x},{bot} L{x},{top + r} A{r},{r} 0 0 1 {x + w},{top + r}'
             f' L{x + w},{bot} Z')
    ins = 56
    xi, wi = x + ins, w - 2 * ins
    ri = wi / 2
    inner = (f'M{xi},{bot} L{xi},{top + ins + ri} A{ri},{ri} 0 0 1 {xi + wi},{top + ins + ri}'
             f' L{xi + wi},{bot} Z')
    return tile(col,
                f'<path d="{outer}" fill="{col}"/>'
                f'<path d="{inner}" fill="#17120E" opacity=".82"/>',
                wcy="30%", wop=".24")


# --------------------------------------------------------------------------
# O7 Lantern — the light you carry. Warm, portable, yours.
# --------------------------------------------------------------------------
def o7(i, col):
    return tile(col,
                f'<path d="M{C},70 a58,58 0 0 1 58,58" fill="none" stroke="{col}"'
                f' stroke-width="19" stroke-linecap="round" opacity=".55"/>'
                f'<path d="M{C},70 a58,58 0 0 0 -58,58" fill="none" stroke="{col}"'
                f' stroke-width="19" stroke-linecap="round" opacity=".55"/>'
                f'<rect x="164" y="140" width="184" height="30" rx="15" fill="{col}"/>'
                f'<path d="M186,186 h140 a26,26 0 0 1 26,26 v146 a26,26 0 0 1 -26,26'
                f' h-140 a26,26 0 0 1 -26,-26 v-146 a26,26 0 0 1 26,-26 z" fill="{col}"/>'
                f'<circle cx="{C}" cy="286" r="52" fill="#17120E" opacity=".55"/>',
                wcy="56%", wop=".26")


# --------------------------------------------------------------------------
# O8 Clearing — the name, literally. A dense field with an opening in it.
# --------------------------------------------------------------------------
def o8(i, col):
    cx = C if i is None else 150 + (i % 4) * 71
    cy = C if i is None else (200 if i < 4 else 320)
    strokes = "".join(
        f'<rect x="{54 + n * 27}" y="96" width="9" height="320" rx="4.5" fill="{col}"/>'
        for n in range(15))
    return tile(col,
                f'<mask id="cl"><rect width="{S}" height="{S}" fill="#fff"/>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="104" ry="92" fill="#000"/></mask>'
                f'<g mask="url(#cl)">{strokes}</g>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="104" ry="92" fill="{col}" opacity=".14"/>',
                wcy="50%", wop=".18")


# --------------------------------------------------------------------------
# O9 Bowl — a vessel holding the light. What you kept, not what you gave up.
# --------------------------------------------------------------------------
def o9(i, col):
    return tile(col,
                f'<circle cx="{C}" cy="248" r="132" fill="{col}" opacity=".15"/>'
                f'<circle cx="{C}" cy="252" r="60" fill="{col}"/>'
                f'<path d="M112,300 a144,144 0 0 0 288,0 z" fill="{col}"/>'
                f'<rect x="112" y="288" width="288" height="26" rx="13" fill="{col}"/>',
                wcy="60%", wop=".26")


# --------------------------------------------------------------------------
# O10 Ledger — a card of ruled days with one of them yours.
# --------------------------------------------------------------------------
def o10(i, col):
    x, y, w, h = 108, 96, 296, 320
    rules = ""
    for n in range(6):
        ry = y + 52 + n * 44
        rules += (f'<rect x="{x + 34}" y="{ry}" width="{w - 68}" height="10" rx="5"'
                  f' fill="{col}" opacity=".30"/>')
    if i is None:
        mark = "".join(
            f'<rect x="{x + 34}" y="{y + 52 + n * 44}" width="{w - 68}" height="10"'
            f' rx="5" fill="{col}"/>' for n in range(6))
    else:
        row = i % 6
        mark = (f'<rect x="{x + 34}" y="{y + 52 + row * 44}" width="{w - 68}" height="10"'
                f' rx="5" fill="{col}"/>'
                f'<circle cx="{x + 18}" cy="{y + 57 + row * 44}" r="15" fill="{col}"/>')
    return tile(col,
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{CREAM}"/>'
                + rules + mark, wcy="24%", wop=".22")


CONCEPTS = [
    ("o1-aperture", "Aperture",  "The Fraunces C the suite is named for, at display size.", o1),
    ("o2-seal",     "Seal",      "A wax seal with the C struck into it. A record you closed yourself.", o2),
    ("o3-window",   "Window",    "A lit window seen from outside. Someone is home.", o3),
    ("o4-moonrise", "Moonrise",  "A fixed horizon and the hour of the evening. A cycle, not a score.", o4),
    ("o5-bookmark", "Bookmark",  "Your place in your own book.", o5),
    ("o6-doorway",  "Doorway",   "A lit door at the end of a long day. You are the one leaving.", o6),
    ("o7-lantern",  "Lantern",   "The light you carry. Warm, portable, yours.", o7),
    ("o8-clearing", "Clearing",  "The name, literally: a dense field with an opening in it.", o8),
    ("o9-bowl",     "Bowl",      "A vessel holding the light. What you kept, not what you gave up.", o9),
    ("o10-ledger",  "Ledger",    "A card of ruled days, with one of them yours.", o10),
]


def main():
    svgdir = os.path.join(HERE, "svg2")
    os.makedirs(svgdir, exist_ok=True)
    for slug, _n, _t, fn in CONCEPTS:
        open(os.path.join(svgdir, f"{slug}-suite.svg"), "w").write(fn(None, SUITE))
        for i, (app, _l, col) in enumerate(APPS):
            open(os.path.join(svgdir, f"{slug}-{app}.svg"), "w").write(fn(i, col))
    print(f"wrote {len(os.listdir(svgdir))} svgs to {svgdir}")


if __name__ == "__main__":
    main()
