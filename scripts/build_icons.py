#!/usr/bin/env python3
"""
Build every Clear Suite identity asset from one source of truth.

WHY THIS EXISTS: before S5 the marks existed only as PNGs with no vector source,
so a colour change meant remapping pixels and a shape change was impossible. The
eight glyphs are now defined here as paths. Everything shipped — app icons,
maskable icons, favicons, apple-touch-icons and the nine Open Graph cards — is
derived from this file, so the suite can never drift out of sync again.

  scripts/build-icons.sh          # bootstraps the venv, then runs this

Design contract is DESIGN.md. The decisions this file encodes:

  - Treatment is "Two-tone": a filled accent disc with a cream glyph. Chosen
    over the shipped hairline ring, which disappeared entirely at favicon size.
  - Disc colours are NOT the Hearth accents. Cream on Hearth measures 2.09-2.54:1,
    under the 3:1 floor for meaningful graphics. Each disc is mixed ~70% from its
    Hearth accent toward its Field Guide accent, which puts cream at 4.5:1 on all
    eight while keeping the hue and leaving the disc itself 3.4:1 on the ground.
  - Glyph scales carry a measured optical-weight correction. Rendered ink coverage
    ranged 2.24% (bolt) to 3.63% (eye); each glyph is nudged toward the 3.06%
    median by (median/ink)^0.3 — a damped correction, because fully equalising
    ink makes the compact glyphs look bloated.
  - The hub finally has its own mark: a Fraunces C in the same treatment. It used
    to borrow Clear Flow's icon, which made the parent look like a ninth sibling.
"""
import json
import math
import os
import subprocess
import sys
import tempfile

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(ROOT, "apps")
FONT_SRC = os.path.join(APPS_DIR, "clearflow", "vendor", "fonts")
WORK = tempfile.mkdtemp(prefix="clear-icons-")

S = 512                 # icon canvas
C = 256.0
TILE_R = 114            # ~22%, the iOS squircle approximation
GROUND = "#17120E"      # --bg-deep, Hearth
CREAM = "#F3E7DA"       # --text-primary, Hearth
SUITE = "#80633F"       # the hub's own disc; brass, not borrowed from an app

# Disc colour per app, and the Hearth accent it derives from (kept for the record).
APPS = [
    ("clearflow",   "flow",   "Clear Flow",   "#A3523E", "#D17C67", "alcohol"),
    ("clearair",    "air",    "Clear Air",    "#4D7066", "#6C9C8E", "vaping and nicotine"),
    ("clearmind",   "mind",   "Clear Mind",   "#587132", "#7B9E46", "cannabis"),
    ("clearbody",   "body",   "Clear Body",   "#A54D55", "#CE7D83", "sugar"),
    ("clearfeed",   "feed",   "Clear Feed",   "#71628B", "#9A8DB4", "social media"),
    ("clearodds",   "odds",   "Clear Odds",   "#83642B", "#C89B4A", "gambling"),
    ("clearsight",  "sight",  "Clear Sight",  "#5A6A82", "#8394AE", "porn"),
    ("clearenergy", "energy", "Clear Energy", "#8F5F1F", "#D08A2C", "caffeine"),
]

# Measured optical-weight correction — see the module docstring.
WEIGHT = {"flow": 1.061, "air": 0.955, "mind": 1.035, "body": 1.019,
          "feed": 1.000, "odds": 0.963, "sight": 0.950, "energy": 1.098}


# ---------------------------------------------------------------------------
# Type. The vendored faces are variable woff2; instantiate static cuts so glyph
# outlines can be pulled without a rasteriser that knows about font variations.
# ---------------------------------------------------------------------------
_fonts, _paths = {}, {}


def face(name):
    if name not in _fonts:
        src, axes = {
            "fraunces": ("fraunces-latin.woff2", {"opsz": 96, "wght": 600}),
            "sora": ("sora-latin.woff2", {"wght": 400}),
            "sora-light": ("sora-latin.woff2", {"wght": 300}),
        }[name]
        f = TTFont(os.path.join(FONT_SRC, src))
        _fonts[name] = instantiateVariableFont(f, axes, inplace=False)
    return _fonts[name]


def text_path(name, text, size, tracking=0.0):
    """Outline a string. Returns (svg_path_d, advance_width, cap_height)."""
    key = (name, text, size, tracking)
    if key in _paths:
        return _paths[key]
    f = face(name)
    upm = f["head"].unitsPerEm
    k = size / upm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    d, x = [], 0.0
    for ch in text:
        gn = cmap.get(ord(ch))
        if gn is None:
            x += upm * 0.3
            continue
        pen = SVGPathPen(gs)
        gs[gn].draw(pen)
        seg = pen.getCommands()
        if seg:
            d.append(f'<path transform="translate({x * k:.3f} 0) scale({k:.6f} {-k:.6f})"'
                     f' d="{seg}"/>')
        x += hmtx[gn][0] + tracking * upm
    cap = f["OS/2"].sCapHeight if hasattr(f["OS/2"], "sCapHeight") else upm * 0.7
    res = ("".join(d), x * k, cap * k)
    _paths[key] = res
    return res


def label(name, text, size, x, y, fill, tracking=0.0, anchor="start"):
    d, w, _cap = text_path(name, text, size, tracking)
    if anchor == "middle":
        x -= w / 2
    return f'<g transform="translate({x:.2f} {y:.2f})" fill="{fill}">{d}</g>', w


# ---------------------------------------------------------------------------
# The eight glyphs. Each is drawn entirely in colour `c` and centred on (C, C),
# so a treatment can recolour or knock one out with a single substitution.
# `w` scales stroke weight, `k` scales the whole glyph.
# ---------------------------------------------------------------------------

def g_flow(c, w, k):
    """Compass — four arrows from a centre ring."""
    sw = 15 * w
    arms = "".join(
        f'<g transform="rotate({a * 90} {C} {C})">'
        f'<rect x="{C - sw / 2:.1f}" y="{C - 86:.1f}" width="{sw:.1f}" height="42"'
        f' rx="{sw / 2:.1f}" fill="{c}"/>'
        f'<path d="M{C:.1f},{C - 122:.1f} L{C + 27:.1f},{C - 80:.1f}'
        f' L{C - 27:.1f},{C - 80:.1f} Z" fill="{c}"/></g>' for a in range(4))
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">{arms}'
            f'<circle cx="{C}" cy="{C}" r="25" fill="none" stroke="{c}" stroke-width="{sw:.1f}"/>'
            f'<circle cx="{C}" cy="{C}" r="10" fill="{c}"/></g>')


def g_air(c, w, k):
    """Wind — three lines, each hooking back on itself."""
    sw = 17 * w
    p = "".join(
        f'<path d="M{C + x0},{C + dy} H{C + x1} a{r},{r} 0 1 1 {-r * .62:.1f},{r * 1.42:.1f}"'
        f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linecap="round"'
        f' stroke-linejoin="round"/>'
        for dy, x0, x1, r in [(-46, -92, 46, 26), (2, -96, 66, 30), (50, -74, 30, 24)])
    return f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">{p}</g>'


def g_mind(c, w, k):
    """Sprout — a stem and two leaves."""
    sw = 15 * w
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<path d="M{C},{C + 104} V{C - 26}" fill="none" stroke="{c}"'
            f' stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<path d="M{C - 34},{C + 108} h68" fill="none" stroke="{c}"'
            f' stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<path d="M{C - 2},{C - 22} C{C - 10},{C - 66} {C - 42},{C - 84}'
            f' {C - 72},{C - 88} C{C - 72},{C - 56} {C - 42},{C - 22} {C - 2},{C - 22} Z"'
            f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{C + 2},{C - 22} C{C + 10},{C - 74} {C + 52},{C - 96}'
            f' {C + 86},{C - 100} C{C + 86},{C - 62} {C + 52},{C - 22} {C + 2},{C - 22} Z"'
            f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linejoin="round"/></g>')


def g_body(c, w, k):
    """Four-point star with four satellites."""
    pts = " ".join(
        f"{C + (116 if a % 2 == 0 else 26) * math.cos(math.radians(a * 45 - 90)):.1f},"
        f"{C + (116 if a % 2 == 0 else 26) * math.sin(math.radians(a * 45 - 90)):.1f}"
        for a in range(8))
    dots = "".join(
        f'<circle cx="{C + 76 * math.cos(math.radians(a * 90 - 45)):.1f}"'
        f' cy="{C + 76 * math.sin(math.radians(a * 90 - 45)):.1f}"'
        f' r="{13 * w:.1f}" fill="{c}"/>' for a in range(4))
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<polygon points="{pts}" fill="{c}"/>{dots}</g>')


def g_feed(c, w, k):
    """Feed — three bars and a marker."""
    h = 28 * w
    p = "".join(
        f'<rect x="{C + x0}" y="{C + dy - h / 2:.1f}" width="{x1 - x0}" height="{h:.1f}"'
        f' rx="{h / 2:.1f}" fill="{c}"/>'
        for dy, x0, x1 in [(-52, -80, 24), (0, -80, 62), (52, -80, 42)])
    p += f'<circle cx="{C + 66}" cy="{C - 52}" r="{16 * w:.1f}" fill="{c}"/>'
    return f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">{p}</g>'


def g_odds(c, w, k):
    """Diamond with a centre pip."""
    sw = 16 * w
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<polygon points="{C},{C - 108} {C + 108},{C} {C},{C + 108} {C - 108},{C}"'
            f' fill="none" stroke="{c}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<circle cx="{C}" cy="{C}" r="{26 * w:.1f}" fill="{c}"/></g>')


def g_sight(c, w, k):
    """Eye — two arcs that do not meet, and a pupil."""
    sw = 16 * w
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<path d="M{C - 112},{C - 6} A126,126 0 0 1 {C + 112},{C - 6}" fill="none"'
            f' stroke="{c}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<path d="M{C - 112},{C + 6} A126,126 0 0 0 {C + 112},{C + 6}" fill="none"'
            f' stroke="{c}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{C}" cy="{C}" r="30" fill="none" stroke="{c}" stroke-width="{sw:.1f}"/>'
            f'<circle cx="{C}" cy="{C}" r="13" fill="{c}"/></g>')


def g_energy(c, w, k):
    """Bolt."""
    return (f'<g transform="translate({C} {C}) scale({k}) translate({-C} {-C})">'
            f'<path d="M{C + 34},{C - 122} L{C - 66},{C + 10} L{C - 4},{C + 10}'
            f' L{C - 32},{C + 122} L{C + 68},{C - 14} L{C + 6},{C - 14} Z" fill="{c}"/></g>')


GLYPH = {"flow": g_flow, "air": g_air, "mind": g_mind, "body": g_body,
         "feed": g_feed, "odds": g_odds, "sight": g_sight, "energy": g_energy}


def glyph(key, colour, scale=1.0):
    """The suite's own mark is a Fraunces C; the eight are their own glyphs."""
    if key is None:
        d, w, cap = text_path("fraunces", "C", 300 * scale)
        return (f'<g transform="translate({C - w / 2:.2f} {C + cap / 2:.2f})"'
                f' fill="{colour}">{d}</g>')
    return GLYPH[key](colour, 1.12, 0.82 * scale * WEIGHT[key])


# ---------------------------------------------------------------------------
# Tiles
# ---------------------------------------------------------------------------
HEARTH_DEF = (f'<radialGradient id="g" cx="50%" cy="0%" r="120%">'
              f'<stop offset="0%" stop-color="#2A1E15"/>'
              f'<stop offset="60%" stop-color="{GROUND}"/></radialGradient>')


def icon_svg(key, disc, maskable=False, square=False):
    """The app icon.

    `maskable` shrinks the figure into Android's 80% safe area.
    `square` drops the baked-in corner radius. Required for apple-touch-icon:
    iOS masks it itself, and a pre-rounded tile comes out double-rounded with
    dark wedges in the corners.
    """
    k = 0.72 if maskable else 1.0
    r = 212 * k
    wash = (f'<radialGradient id="w" cx="50%" cy="10%" r="95%">'
            f'<stop offset="0%" stop-color="{disc}" stop-opacity=".24"/>'
            f'<stop offset="100%" stop-color="{disc}" stop-opacity="0"/></radialGradient>')
    body = (f'<rect width="{S}" height="{S}" fill="url(#g)"/>'
            f'<rect width="{S}" height="{S}" fill="url(#w)"/>'
            f'<circle cx="{C}" cy="{C}" r="{r:.1f}" fill="{disc}"/>'
            + glyph(key, CREAM, k))
    if maskable or square:
        # Full-bleed: the launcher or OS supplies the mask.
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}"'
                f' width="{S}" height="{S}"><defs>{HEARTH_DEF}{wash}</defs>{body}</svg>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}"'
            f' width="{S}" height="{S}"><defs>{HEARTH_DEF}{wash}'
            f'<clipPath id="t"><rect width="{S}" height="{S}" rx="{TILE_R}"/></clipPath>'
            f'</defs><g clip-path="url(#t)">{body}</g></svg>')


def bare_svg(key, disc):
    """Mark with no tile — for the hub's app cards and for the OG lockups."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}"'
            f' width="{S}" height="{S}">'
            f'<circle cx="{C}" cy="{C}" r="212" fill="{disc}"/>'
            + glyph(key, CREAM) + "</svg>")


# ---------------------------------------------------------------------------
# Open Graph cards. Every share currently renders as a small square app icon;
# these are the first real 1200x630s the suite has had.
# ---------------------------------------------------------------------------
OGW, OGH = 1200, 630

PROMISE = "FREE FOREVER  ·  NO ACCOUNT  ·  NOTHING LEAVES YOUR DEVICE"


def og_svg(key, disc, title, subtitle):
    defs = (f'<radialGradient id="g" cx="50%" cy="0%" r="115%">'
            f'<stop offset="0%" stop-color="#2A1E15"/>'
            f'<stop offset="62%" stop-color="{GROUND}"/></radialGradient>'
            f'<radialGradient id="w" cx="14%" cy="96%" r="82%">'
            f'<stop offset="0%" stop-color="{disc}" stop-opacity=".40"/>'
            f'<stop offset="100%" stop-color="{disc}" stop-opacity="0"/></radialGradient>')

    if key is None:
        # The hub leads with the family, not with a single mark.
        figure = ""
        step = 118
        for n, (_d, k, _n2, dc, _h, _v) in enumerate(APPS):
            figure += (f'<g transform="translate({92 + n * step} 350) scale({96 / S})">'
                       f'<circle cx="{C}" cy="{C}" r="212" fill="{dc}"/>'
                       f'{glyph(k, CREAM, 0.96)}</g>')
        head_y, sub_y = 250, 302
        tx = 92
    else:
        figure = (f'<g transform="translate(92 231) scale({168 / S})">'
                  f'<circle cx="{C}" cy="{C}" r="212" fill="{disc}"/>'
                  f'{glyph(key, CREAM)}</g>')
        head_y, sub_y = 300, 356
        tx = 300

    t, _w = label("fraunces", title, 68, tx, head_y, "#FFF3E6")
    s, _w = label("sora-light", subtitle, 27, tx, sub_y, "#C8B29A")
    p, _w = label("sora", PROMISE, 15, 92, OGH - 62, "#A79383", tracking=0.11)

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OGW} {OGH}"'
            f' width="{OGW}" height="{OGH}"><defs>{defs}</defs>'
            f'<rect width="{OGW}" height="{OGH}" fill="url(#g)"/>'
            f'<rect width="{OGW}" height="{OGH}" fill="url(#w)"/>'
            f'{figure}{t}{s}'
            f'<rect x="92" y="{OGH - 104}" width="{OGW - 184}" height="1"'
            f' fill="{CREAM}" opacity=".13"/>{p}</svg>')


# ---------------------------------------------------------------------------
# Raster
# ---------------------------------------------------------------------------
def render(svg, out, w, h=None):
    src = os.path.join(WORK, os.path.basename(out) + ".svg")
    with open(src, "w") as f:
        f.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h or w), src, "-o", out],
                   check=True)


def main():
    if subprocess.run(["which", "rsvg-convert"], capture_output=True).returncode:
        sys.exit("need rsvg-convert:  brew install librsvg")

    made = 0
    for slug, key, name, disc, _hearth, vertical in APPS:
        d = os.path.join(APPS_DIR, slug)
        icon = icon_svg(key, disc)
        for px in (32, 192, 512):
            render(icon, os.path.join(d, f"icon-{px}.png"), px)
            made += 1
        render(icon_svg(key, disc, square=True), os.path.join(d, "icon-180.png"), 180)
        render(icon_svg(key, disc, maskable=True),
               os.path.join(d, "icon-maskable-512.png"), 512)
        render(og_svg(key, disc, name, f"Your recovery from {vertical}, privately."),
               os.path.join(d, "og.png"), OGW, OGH)
        # The hub's own card art for this app.
        render(bare_svg(key, disc),
               os.path.join(APPS_DIR, "landing", f"{slug}-icon.png"), 256)
        made += 3

    hub = os.path.join(APPS_DIR, "landing")
    hicon = icon_svg(None, SUITE)
    for px in (32, 192, 512):
        render(hicon, os.path.join(hub, f"icon-{px}.png"), px)
        made += 1
    render(icon_svg(None, SUITE, square=True), os.path.join(hub, "icon-180.png"), 180)
    render(icon_svg(None, SUITE, maskable=True),
           os.path.join(hub, "icon-maskable-512.png"), 512)
    render(og_svg(None, SUITE, "Clear Suite",
                  "Eight private recovery trackers. Free forever."),
           os.path.join(hub, "og.png"), OGW, OGH)
    made += 2

    print(f"built {made} assets")


if __name__ == "__main__":
    main()
