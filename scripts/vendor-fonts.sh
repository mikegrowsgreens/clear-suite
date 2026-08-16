#!/usr/bin/env bash
# Vendor the Long Evening typefaces into apps/*/vendor/fonts/.
#
# WHY THIS EXISTS: the apps promise that data never leaves the device, so they
# make zero third-party requests. Google Fonts leaked each user's IP plus a
# Referer naming the subdomain (telling Google someone was on a porn- or
# gambling-recovery tracker). Fonts are therefore self-hosted, and this script
# is the provenance record for how the files in vendor/fonts/ were produced.
#
# Run it only when the typefaces change. It needs network + python3.
#
#   scripts/vendor-fonts.sh
#
# Sizes matter: these are the render-blocking bytes on a first visit. Fraunces
# ships with opsz 9..144 and wght 100..900; we clip both axes to what the design
# actually uses, which roughly halves each file. The italic is used for exactly
# one element (the user's own reason, in their words) at one size, so its optical
# axis is pinned rather than kept variable.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'

echo "→ venv + fonttools"
python3 -m venv "$WORK/venv" >/dev/null
"$WORK/venv/bin/pip" install -q "fonttools[woff]" brotli

echo "→ fetching source faces from Google"
curl -sf -m 60 -A "$UA" \
  "https://fonts.googleapis.com/css2?family=Sora:wght@200..600&display=swap" > "$WORK/sora.css"
curl -sf -m 60 -A "$UA" \
  "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..400&display=swap" > "$WORK/fraunces.css"

WORK="$WORK" "$WORK/venv/bin/python3" - <<'PY'
import os, re, subprocess, sys, urllib.request
work = os.environ['WORK']
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
LATINEXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'

# (stem, source css, font-style, axis limits) -> the six files we ship
JOBS = [
    ('sora',            'sora.css',     'normal', ['wght=200:600']),
    ('fraunces',        'fraunces.css', 'normal', ['opsz=12:96', 'wght=300:600']),
    ('fraunces-italic', 'fraunces.css', 'italic', ['opsz=18',    'wght=300:400']),
]

def source_url(css, style, block):
    """Pull the woff2 URL for one (style, unicode-block) pair out of Google's CSS."""
    head = {'latin': 'U+0000-00FF', 'latinext': 'U+0100-02BA'}[block]
    for m in re.finditer(r'@font-face\s*\{(.*?)\}', css, re.S):
        b = m.group(1)
        if re.search(r'font-style:\s*%s' % style, b) and re.search(r'unicode-range:\s*%s' % re.escape(head), b):
            return re.search(r'url\((https://[^)]+)\)', b).group(1)
    raise SystemExit('no %s/%s face found' % (style, block))

def run(*a):
    subprocess.run(a, check=True, stdout=subprocess.DEVNULL)

venv = os.path.join(work, 'venv', 'bin')
for stem, cssname, style, axes in JOBS:
    css = open(os.path.join(work, cssname)).read()
    for block, unicodes in (('latin', LATIN), ('latinext', LATINEXT)):
        raw = os.path.join(work, '%s-%s.src.woff2' % (stem, block))
        with urllib.request.urlopen(urllib.request.Request(source_url(css, style, block), headers=UA), timeout=60) as r:
            open(raw, 'wb').write(r.read())
        # woff2 -> ttf so the instancer can clip axes, then subset back to woff2
        from fontTools.ttLib import TTFont
        f = TTFont(raw); f.flavor = None; f.save(raw + '.ttf')
        run(venv + '/fonttools', 'varLib.instancer', '-o', raw + '.pin.ttf', raw + '.ttf', *axes)
        out = os.path.join(work, '%s-%s.woff2' % (stem, block))
        run(venv + '/pyftsubset', raw + '.pin.ttf', '--output-file=' + out, '--flavor=woff2',
            '--unicodes=' + unicodes, '--layout-features=kern,liga', '--no-hinting')
        print('  %-28s %6.1f KB' % (os.path.basename(out), os.path.getsize(out) / 1024))
PY

echo "→ writing vendor/fonts/ into all nine surfaces"
for app in "$ROOT"/apps/*/; do
  dest="$app/vendor/fonts"
  mkdir -p "$dest"
  cp "$WORK"/sora-*.woff2 "$WORK"/fraunces-*.woff2 "$dest"/ 2>/dev/null || true
  # only the six shipped faces, never the .src/.ttf intermediates
  rm -f "$dest"/*.src.woff2 "$dest"/*.ttf
done
echo "✓ done. long-evening.css in each vendor/fonts/ is hand-maintained; check it matches."
