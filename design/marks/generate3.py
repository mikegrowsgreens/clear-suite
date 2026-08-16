#!/usr/bin/env python3
"""
Clear Suite identity — round three. Variations on the eight marks we already have.

Rounds one and two both replaced the marks. Mike wants the originals varied, not
thrown away, so this file keeps every glyph idea exactly as it shipped — compass
arrows, wind, sprout, four-point star, feed bars, diamond, eye, bolt — and varies
only the treatment around them.

The glyphs had no vector source; they existed only as PNGs. They are redrawn here
as clean paths, which is also the first time they have been optically balanced
against each other (the originals were drawn at different visual weights).

Ten treatments, each applied to all eight, each with a matching hub mark.
"""
import math
import os
import json
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/private/tmp/claude-501/-Users-mikepaulus-Desktop-Claude-Code/"
           "8cd0a4c7-0e3e-4691-a0f9-b32ab0427c12/scratchpad")
PY = os.path.expanduser("~/.claude/skills/logo-design/.venv/bin/python")
OUTLINE = os.path.expanduser("~/.claude/skills/logo-design/scripts/outline-text.py")
FRAUNCES = os.path.join(SCRATCH, "fraunces-display.ttf")

S = 512
C = 256.0
TILE_R = 114
GROUND = "#17120E"
CREAM = "#F3E7DA"
SUITE = "#E8CFA9"

APPS = [
    ("flow",   "#D17C67"), ("air",    "#6C9C8E"),
    ("mind",   "#7B9E46"), ("body",   "#CE7D83"),
    ("feed",   "#9A8DB4"), ("odds",   "#C89B4A"),
    ("sight",  "#8394AE"), ("energy", "#D08A2C"),
]

_g = {}


def fraunces_c(cap, cx, cy, fill):
    if "C" not in _g:
        out = subprocess.run([PY, OUTLINE, FRAUNCES, "C", "--size", "200", "--json"],
                             capture_output=True, text=True, check=True)
        _g["C"] = json.loads(out.stdout)
    d = _g["C"]
    k = cap / d["ascent"]
    return (f'<g transform="translate({cx - d["width"] * k / 2:.2f} '
            f'{cy + d["ascent"] * k / 2:.2f}) scale({k:.5f})">'
            f'<path d="{d["d"]}" fill="{fill}"/></g>')


# ==========================================================================
# The eight glyphs, redrawn. Each is centred on (256,256) and drawn entirely
# in colour `c`, so a treatment can knock it out simply by passing the ground.
# `w` scales stroke weight; `k` scales the whole glyph.
# ==========================================================================

def g_flow(c, w=1.0, k=1.0):
    """Compass — four arrows from a centre ring."""
    sw = 15 * w
    arms = ""
    for a in range(4):
        arms += (f'<g transform="rotate({a * 90} {C} {C})">'
                 f'<rect x="{C - sw / 2:.1f}" y="{C - 86:.1f}" width="{sw:.1f}"'
                 f' height="42" rx="{sw / 2:.1f}" fill="{c}"/>'
                 f'<path d="M{C:.1f},{C - 122:.1f} L{C + 27:.1f},{C - 80:.1f}'
                 f' L{C - 27:.1f},{C - 80:.1f} Z" fill="{c}"/></g>')
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'{arms}'
            f'<circle cx="{C}" cy="{C}" r="25" fill="none" stroke="{c}" stroke-width="{sw:.1f}"/>'
            f'<circle cx="{C}" cy="{C}" r="10" fill="{c}"/></g>')


def g_air(c, w=1.0, k=1.0):
    """Wind — three lines, each hooking back on itself."""
    sw = 17 * w
    rows = [(-46, -92, 46, 26), (2, -96, 66, 30), (50, -74, 30, 24)]
    p = ""
    for dy, x0, x1, r in rows:
        y = C + dy
        p += (f'<path d="M{C + x0},{y} H{C + x1} a{r},{r} 0 1 1 {-r * 0.62:.1f},{r * 1.42:.1f}"'
              f' fill="none" stroke="{c}" stroke-width="{sw:.1f}"'
              f' stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">{p}</g>'


def g_mind(c, w=1.0, k=1.0):
    """Sprout — a stem and two leaves."""
    sw = 15 * w
    stem = (f'<path d="M{C},{C + 104} V{C - 26}" fill="none" stroke="{c}"'
            f' stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<path d="M{C - 34},{C + 108} h68" fill="none" stroke="{c}"'
            f' stroke-width="{sw:.1f}" stroke-linecap="round"/>')
    leaf_r = (f'<path d="M{C + 2},{C - 22} C{C + 10},{C - 74} {C + 52},{C - 96}'
              f' {C + 86},{C - 100} C{C + 86},{C - 62} {C + 52},{C - 22} {C + 2},{C - 22} Z"'
              f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>')
    leaf_l = (f'<path d="M{C - 2},{C - 22} C{C - 10},{C - 66} {C - 42},{C - 84}'
              f' {C - 72},{C - 88} C{C - 72},{C - 56} {C - 42},{C - 22} {C - 2},{C - 22} Z"'
              f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>')
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'{stem}{leaf_l}{leaf_r}</g>')


def g_body(c, w=1.0, k=1.0):
    """Four-point star with four satellites."""
    R, waist = 116, 26
    pts = []
    for a in range(8):
        r = R if a % 2 == 0 else waist
        th = math.radians(a * 45 - 90)
        pts.append(f"{C + r * math.cos(th):.1f},{C + r * math.sin(th):.1f}")
    dots = "".join(
        f'<circle cx="{C + 76 * math.cos(math.radians(a * 90 - 45)):.1f}"'
        f' cy="{C + 76 * math.sin(math.radians(a * 90 - 45)):.1f}"'
        f' r="{13 * w:.1f}" fill="{c}"/>' for a in range(4))
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<polygon points="{" ".join(pts)}" fill="{c}"/>{dots}</g>')


def g_feed(c, w=1.0, k=1.0):
    """Feed — three bars and a marker."""
    h = 28 * w
    rows = [(-52, -80, 24), (0, -80, 62), (52, -80, 42)]
    p = ""
    for dy, x0, x1 in rows:
        p += (f'<rect x="{C + x0}" y="{C + dy - h / 2:.1f}" width="{x1 - x0}"'
              f' height="{h:.1f}" rx="{h / 2:.1f}" fill="{c}"/>')
    p += f'<circle cx="{C + 66}" cy="{C - 52}" r="{16 * w:.1f}" fill="{c}"/>'
    return f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">{p}</g>'


def g_odds(c, w=1.0, k=1.0):
    """Diamond with a centre pip."""
    sw, R = 16 * w, 108
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<polygon points="{C},{C - R} {C + R},{C} {C},{C + R} {C - R},{C}"'
            f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<circle cx="{C}" cy="{C}" r="{26 * w:.1f}" fill="{c}"/></g>')


def g_sight(c, w=1.0, k=1.0):
    """Eye — two arcs that do not meet, and a pupil."""
    sw = 16 * w
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<path d="M{C - 112},{C - 6} A126,126 0 0 1 {C + 112},{C - 6}"'
            f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<path d="M{C - 112},{C + 6} A126,126 0 0 0 {C + 112},{C + 6}"'
            f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{C}" cy="{C}" r="30" fill="none" stroke="{c}" stroke-width="{sw:.1f}"/>'
            f'<circle cx="{C}" cy="{C}" r="13" fill="{c}"/></g>')


def g_energy(c, w=1.0, k=1.0):
    """Bolt."""
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<path d="M{C + 34},{C - 122} L{C - 66},{C + 10} L{C - 4},{C + 10}'
            f' L{C - 32},{C + 122} L{C + 68},{C - 14} L{C + 6},{C - 14} Z" fill="{c}"/></g>')


GLYPH = {"flow": g_flow, "air": g_air, "mind": g_mind, "body": g_body,
         "feed": g_feed, "odds": g_odds, "sight": g_sight, "energy": g_energy}


# ==========================================================================
# Tile scaffolding
# ==========================================================================

def svg(defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
            f'width="{S}" height="{S}">\n<defs>{defs}</defs>\n'
            f'<clipPath id="t"><rect width="{S}" height="{S}" rx="{TILE_R}"/></clipPath>'
            f'<g clip-path="url(#t)">{body}</g></svg>')


HEARTH = (f'<radialGradient id="g" cx="50%" cy="0%" r="120%">'
          f'<stop offset="0%" stop-color="#2A1E15"/>'
          f'<stop offset="60%" stop-color="{GROUND}"/></radialGradient>')


def warm(col, op=".26", cy="100%"):
    return (f'<radialGradient id="w" cx="50%" cy="{cy}" r="95%">'
            f'<stop offset="0%" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="100%" stop-color="{col}" stop-opacity="0"/></radialGradient>')


def ground(col=None, op=".26", cy="100%"):
    d = HEARTH + (warm(col, op, cy) if col else "")
    b = f'<rect width="{S}" height="{S}" fill="url(#g)"/>'
    if col:
        b += f'<rect width="{S}" height="{S}" fill="url(#w)"/>'
    return d, b


def glyph_of(app, c, w=1.0, k=1.0):
    return GLYPH[app](c, w, k) if app else fraunces_c(196 * k, C, C + 2, c)


# ==========================================================================
# Ten treatments
# ==========================================================================

def t1_original(app, col):
    """As it ships today: hairline ring, flat near-black square."""
    d, b = ground()
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="214" fill="#231A13"/>'
               f'<circle cx="{C}" cy="{C}" r="214" fill="none" stroke="{col}" stroke-width="13"/>'
               + glyph_of(app, col, 1.0, 0.80))


def t2_warm(app, col):
    """Same mark, but each app gets its own light instead of the same brown."""
    d, b = ground(col, ".34")
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="206" fill="{col}" opacity=".08"/>'
               f'<circle cx="{C}" cy="{C}" r="206" fill="none" stroke="{col}" stroke-width="15"/>'
               + glyph_of(app, col, 1.05, 0.80))


def t3_solid(app, col):
    """Solid accent disc, glyph knocked out. The 16px answer."""
    d, b = ground(col, ".22", "10%")
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="212" fill="{col}"/>'
               + glyph_of(app, GROUND, 1.15, 0.82))


def t4_bare(app, col):
    """No ring at all. The glyph is the mark, at full size."""
    d, b = ground(col, ".30")
    return svg(d, b + glyph_of(app, col, 1.25, 1.28))


def t5_paper(app, col):
    """Field Guide: a paper disc, glyph in the app's colour."""
    d, b = ground(col, ".24", "12%")
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="212" fill="{CREAM}"/>'
               + glyph_of(app, col, 1.1, 0.82))


def t6_heavy(app, col):
    """The original, drawn at a weight that survives a favicon."""
    d, b = ground(col, ".28")
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="204" fill="none" stroke="{col}"'
               f' stroke-width="30"/>' + glyph_of(app, col, 1.45, 0.76))


def t7_break(app, col):
    """Glyph oversized so it breaks the ring — the ring stops being a frame."""
    d, b = ground(col, ".28")
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="178" fill="none" stroke="{col}"'
               f' stroke-width="11" opacity=".55"/>' + glyph_of(app, col, 1.2, 1.15))


def t8_seal(app, col):
    """Round two's seal, carrying the original glyph instead of a letter."""
    r, n = 206, 30
    pts = []
    for k in range(n * 2):
        a = math.pi * k / n
        rr = r + (15 if k % 2 else 0)
        pts.append(f"{C + rr * math.cos(a):.1f},{C + rr * math.sin(a):.1f}")
    d, b = ground(col, ".22", "12%")
    return svg(d, b + f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
               + glyph_of(app, GROUND, 1.15, 0.80))


def t9_plate(app, col):
    """No circle anywhere — an accent plate, glyph knocked out."""
    d, b = ground(col, ".22", "10%")
    return svg(d, b + f'<rect x="52" y="52" width="408" height="408" rx="118" fill="{col}"/>'
               + glyph_of(app, GROUND, 1.15, 0.86))


def t10_twotone(app, col):
    """Accent disc, cream glyph — the warmest of the filled treatments."""
    d, b = ground(col, ".24", "10%")
    return svg(d, b + f'<circle cx="{C}" cy="{C}" r="212" fill="{col}"/>'
               + glyph_of(app, CREAM, 1.12, 0.82))


TREATMENTS = [
    ("v1-original", "Original",   "Exactly as it ships today, for comparison.", t1_original),
    ("v2-warm",     "Warm",       "Same mark; each app gets its own light instead of the same brown.", t2_warm),
    ("v3-solid",    "Solid",      "Accent disc, glyph knocked out. The 16px answer.", t3_solid),
    ("v4-bare",     "Bare",       "No ring at all. The glyph is the mark, at full size.", t4_bare),
    ("v5-paper",    "Paper",      "A Field Guide paper disc, glyph in the app's colour.", t5_paper),
    ("v6-heavy",    "Heavy",      "The original, drawn at a weight that survives a favicon.", t6_heavy),
    ("v7-break",    "Break",      "Glyph oversized so it breaks the ring; the ring stops framing.", t7_break),
    ("v8-seal",     "Seal",       "A wax seal carrying the original glyph.", t8_seal),
    ("v9-plate",    "Plate",      "No circle anywhere — an accent plate, glyph knocked out.", t9_plate),
    ("v10-twotone", "Two-tone",   "Accent disc, cream glyph. Warmest of the filled treatments.", t10_twotone),
]


def main():
    out = os.path.join(HERE, "svg3")
    os.makedirs(out, exist_ok=True)
    for slug, _n, _t, fn in TREATMENTS:
        open(os.path.join(out, f"{slug}-suite.svg"), "w").write(fn(None, SUITE))
        for app, col in APPS:
            open(os.path.join(out, f"{slug}-{app}.svg"), "w").write(fn(app, col))
    print(f"wrote {len(os.listdir(out))} svgs to {out}")


if __name__ == "__main__":
    main()
