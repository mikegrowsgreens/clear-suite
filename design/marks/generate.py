#!/usr/bin/env python3
"""
Clear Suite identity exploration — S5.

Ten candidate *systems*. A system is not a mark: it is the rule that generates
the suite mark and its eight members. Each is emitted as an app-icon tile
(Hearth ground + accent figure), because the tile is the surface that has to
survive — a homescreen at 60px and a favicon at 16px.

Constraints, from DESIGN.md:
  - no emoji, no neon/glow-as-shadow, no fill-to-100 meters, no weight >600
  - accents are the per-app Hearth values, unmodified
  - non-disclosing: a stranger glancing at the phone learns nothing

Per-app variation must be carried by gross position, angle or extent. Detail
and element-count both die by 16px.
"""
import math
import os
import subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
S = 512           # canvas
C = S / 2         # centre
TILE_R = 114      # tile corner radius (~22%, iOS-ish)

# Hearth accents, DESIGN.md §4. Order is the order they appear in the suite.
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
SUITE = "#E8CFA9"   # warm brass — the hub's own value, not borrowed from an app


def head(extra=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
<defs>
<radialGradient id="ground" cx="50%" cy="0%" r="120%">
<stop offset="0%" stop-color="#2A1E15"/><stop offset="60%" stop-color="#17120E"/>
</radialGradient>
<clipPath id="tile"><rect x="0" y="0" width="{S}" height="{S}" rx="{TILE_R}"/></clipPath>
{extra}
</defs>
<rect x="0" y="0" width="{S}" height="{S}" rx="{TILE_R}" fill="url(#ground)"/>
<g clip-path="url(#tile)">'''


TAIL = "</g></svg>"


def wrap(body, extra=""):
    return head(extra) + body + TAIL


# --------------------------------------------------------------------------
# C1 Field — a 3x3 grid, centre always empty. Each app owns one cell; the hub
# owns all eight. The empty centre is the person, who is not one of the eight.
# --------------------------------------------------------------------------
CELLS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


def c1(i, col):
    g = 118
    b = []
    for n, (dx, dy) in enumerate(CELLS):
        x, y = C + dx * g, C + dy * g
        if i is None:
            b.append(f'<circle cx="{x}" cy="{y}" r="42" fill="{col}"/>')
        elif n == i:
            b.append(f'<circle cx="{x}" cy="{y}" r="50" fill="{col}"/>')
        else:
            b.append(f'<circle cx="{x}" cy="{y}" r="30" fill="{col}" opacity=".18"/>')
    return wrap("".join(b))


# --------------------------------------------------------------------------
# C2 Horizon — the ground rises through the evening. Each app sits at its own
# hour; the hub is all eight hours stacked as rules.
# --------------------------------------------------------------------------
def c2(i, col):
    hs = [372, 348, 324, 300, 276, 252, 228, 204]
    if i is None:
        b = "".join(
            f'<rect x="96" y="{h}" width="320" height="13" rx="6.5" fill="{col}"/>'
            for h in hs)
        return wrap(b)
    h = hs[i]
    return wrap(
        f'<rect x="0" y="{h}" width="{S}" height="{S - h}" fill="{col}"/>'
        f'<rect x="96" y="{h - 62}" width="320" height="13" rx="6.5" fill="{col}" opacity=".45"/>')


# --------------------------------------------------------------------------
# C3 Turn — a seam of light across the tile, at the app's own angle.
# --------------------------------------------------------------------------
def c3(i, col):
    if i is None:
        b = "".join(
            f'<g transform="rotate({n * 45} {C} {C})">'
            f'<rect x="{C - 9}" y="34" width="18" height="96" rx="9" fill="{col}"/></g>'
            for n in range(8))
        return wrap(b)
    th = i * 22.5
    return wrap(
        f'<g transform="rotate({th} {C} {C})">'
        f'<rect x="-140" y="{C}" width="792" height="792" fill="{col}" opacity=".13"/>'
        f'<rect x="-140" y="{C - 9}" width="792" height="18" rx="9" fill="{col}"/></g>')


# --------------------------------------------------------------------------
# C4 Gap — two slabs and the space between them. The gap is the identity gap,
# which is the one mechanism the product actually rests on (Dingle 2015).
# --------------------------------------------------------------------------
def c4(i, col):
    if i is None:
        return wrap(
            f'<rect x="82" y="82" width="150" height="150" rx="34" fill="{col}"/>'
            f'<rect x="280" y="82" width="150" height="150" rx="34" fill="{col}"/>'
            f'<rect x="82" y="280" width="150" height="150" rx="34" fill="{col}"/>'
            f'<rect x="280" y="280" width="150" height="150" rx="34" fill="{col}"/>')
    th = i * 22.5
    return wrap(
        f'<g transform="rotate({th} {C} {C})">'
        f'<rect x="76" y="{C - 178}" width="360" height="152" rx="46" fill="{col}"/>'
        f'<rect x="76" y="{C + 26}" width="360" height="152" rx="46" fill="{col}"/></g>')


# --------------------------------------------------------------------------
# C5 Ember — the last warm light in the room, in the app's own corner.
# --------------------------------------------------------------------------
def c5(i, col):
    if i is None:
        b = f'<circle cx="{C}" cy="{C}" r="196" fill="{col}" opacity=".12"/>'
        b += f'<circle cx="{C}" cy="{C}" r="46" fill="{col}"/>'
        for n in range(8):
            a = math.radians(n * 45 - 90)
            b += (f'<circle cx="{C + 158 * math.cos(a):.1f}" cy="{C + 158 * math.sin(a):.1f}"'
                  f' r="20" fill="{col}" opacity=".42"/>')
        return wrap(b)
    a = math.radians(i * 45 - 90)
    x, y = C + 104 * math.cos(a), C + 104 * math.sin(a)
    return wrap(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="200" fill="{col}" opacity=".14"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="120" fill="{col}" opacity=".16"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="52" fill="{col}"/>')


# --------------------------------------------------------------------------
# C6 Notch — a solid keep with one piece taken out of it. Heaviest silhouette
# in the set; survives mono and 16px by construction.
# --------------------------------------------------------------------------
def c6(i, col):
    ins, r = 92, 66
    if i is None:
        return wrap(
            f'<path fill-rule="evenodd" fill="{col}" d="'
            f'M{ins + r},{ins} h{S - 2 * ins - 2 * r} a{r},{r} 0 0 1 {r},{r}'
            f' v{S - 2 * ins - 2 * r} a{r},{r} 0 0 1 -{r},{r}'
            f' h-{S - 2 * ins - 2 * r} a{r},{r} 0 0 1 -{r},-{r}'
            f' v-{S - 2 * ins - 2 * r} a{r},{r} 0 0 1 {r},-{r} z'
            f' M{C},{C - 84} a84,84 0 1 0 0.1,0 z"/>')
    pts = [(ins, ins), (C, ins), (S - ins, ins), (S - ins, C),
           (S - ins, S - ins), (C, S - ins), (ins, S - ins), (ins, C)]
    bx, by = pts[i]
    return wrap(
        f'<mask id="m"><rect x="0" y="0" width="{S}" height="{S}" fill="#fff"/>'
        f'<circle cx="{bx}" cy="{by}" r="96" fill="#000"/></mask>'
        f'<rect x="{ins}" y="{ins}" width="{S - 2 * ins}" height="{S - 2 * ins}"'
        f' rx="{r}" fill="{col}" mask="url(#m)"/>')


# --------------------------------------------------------------------------
# C7 Rule — one bold line laid across the tile at the app's angle, over a
# soft disc of its own colour.
# --------------------------------------------------------------------------
def c7(i, col):
    if i is None:
        return wrap(
            f'<circle cx="{C}" cy="{C}" r="180" fill="{col}" opacity=".12"/>'
            f'<rect x="70" y="{C - 28}" width="372" height="56" rx="28" fill="{col}"/>')
    th = i * 22.5
    return wrap(
        f'<circle cx="{C}" cy="{C}" r="180" fill="{col}" opacity=".12"/>'
        f'<g transform="rotate({th} {C} {C})">'
        f'<rect x="52" y="{C - 30}" width="408" height="60" rx="30" fill="{col}"/></g>')


# --------------------------------------------------------------------------
# C8 Cairn — stones stacked by hand. A record of a path, not of a score.
# --------------------------------------------------------------------------
def c8(i, col):
    offs = [(-46, 30), (-30, -34), (34, -44), (46, 26),
            (-52, -14), (18, 44), (-14, -50), (52, -22)]
    dx, dx2 = (0, 0) if i is None else offs[i]
    return wrap(
        f'<rect x="{116 + dx * 0.4:.0f}" y="322" width="280" height="82" rx="41" fill="{col}"/>'
        f'<rect x="{146 + dx:.0f}" y="216" width="220" height="80" rx="40" fill="{col}"/>'
        f'<rect x="{178 + dx2:.0f}" y="120" width="156" height="72" rx="36" fill="{col}"/>')


# --------------------------------------------------------------------------
# C9 Aperture — a thick C, opening at the app's own angle. Included so the
# partial-ring idea gets judged rather than assumed; it is the one candidate
# that risks reading as a progress meter (ban list §7.3).
# --------------------------------------------------------------------------
def c9(i, col):
    r, w = 148, 74
    if i is None:
        return wrap(
            f'<circle cx="{C}" cy="{C}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}"/>')
    start, sweep = i * 45 + 46, 268
    a0, a1 = math.radians(start), math.radians(start + sweep)
    x0, y0 = C + r * math.cos(a0), C + r * math.sin(a0)
    x1, y1 = C + r * math.cos(a1), C + r * math.sin(a1)
    return wrap(
        f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 1 1 {x1:.1f},{y1:.1f}" fill="none"'
        f' stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


# --------------------------------------------------------------------------
# C10 Tally — the ledger itself: a baseline, and one day standing on it.
# --------------------------------------------------------------------------
def c10(i, col):
    base = 372
    if i is None:
        b = f'<rect x="76" y="{base}" width="360" height="15" rx="7.5" fill="{col}"/>'
        for n in range(8):
            x = 96 + n * 46
            b += f'<rect x="{x}" y="{base - 116}" width="16" height="116" rx="8" fill="{col}" opacity=".5"/>'
        return wrap(b)
    b = f'<rect x="76" y="{base}" width="360" height="15" rx="7.5" fill="{col}" opacity=".42"/>'
    x = 104 + i * 44
    b += f'<rect x="{x}" y="{base - 196}" width="34" height="196" rx="17" fill="{col}"/>'
    return wrap(b)


CONCEPTS = [
    ("c1-field",    "Field",    "3x3 grid, centre always empty. Each app owns one cell; the hub owns all eight.", c1),
    ("c2-horizon",  "Horizon",  "The ground rises through the evening. Each app is its own hour.", c2),
    ("c3-turn",     "Turn",     "A seam of light across the tile, at the app's own angle.", c3),
    ("c4-gap",      "Gap",      "Two slabs and the space between. The gap is the identity gap.", c4),
    ("c5-ember",    "Ember",    "The last warm light in the room, in the app's own corner.", c5),
    ("c6-notch",    "Notch",    "A solid keep with one piece taken out of it.", c6),
    ("c7-rule",     "Rule",     "One bold line laid across the tile, over a soft disc.", c7),
    ("c8-cairn",    "Cairn",    "Stones stacked by hand. A record of a path, not a score.", c8),
    ("c9-aperture", "Aperture", "A thick C, opening at the app's angle. Risks reading as a meter.", c9),
    ("c10-tally",   "Tally",    "The ledger itself: a baseline, and one day standing on it.", c10),
]


def main():
    svgdir = os.path.join(OUT, "svg")
    os.makedirs(svgdir, exist_ok=True)
    for slug, _name, _thesis, fn in CONCEPTS:
        with open(os.path.join(svgdir, f"{slug}-suite.svg"), "w") as f:
            f.write(fn(None, SUITE))
        for i, (app, _label, col) in enumerate(APPS):
            with open(os.path.join(svgdir, f"{slug}-{app}.svg"), "w") as f:
                f.write(fn(i, col))
    n = len(os.listdir(svgdir))
    print(f"wrote {n} svgs to {svgdir}")


if __name__ == "__main__":
    main()
