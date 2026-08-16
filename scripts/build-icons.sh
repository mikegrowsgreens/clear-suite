#!/usr/bin/env bash
# Build every Clear Suite identity asset — app icons, maskable icons, favicons,
# apple-touch-icons, the hub's own mark, and the nine Open Graph cards.
#
# WHY THIS EXISTS: before S5 the eight marks were PNG-only with no vector source,
# so recolouring meant remapping pixels and reshaping was impossible. The glyphs
# now live in scripts/build_icons.py and everything shipped is derived from them.
#
#   scripts/build-icons.sh
#
# Needs python3 and librsvg. The fonts are read from the already-vendored woff2
# in apps/clearflow/vendor/fonts/, so this does NOT need network — unlike
# vendor-fonts.sh, which fetches the faces themselves.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

command -v rsvg-convert >/dev/null || {
  echo "need rsvg-convert:  brew install librsvg" >&2; exit 1; }

# Cached next to the repo, not in it — see .gitignore.
VENV="${TMPDIR:-/tmp}/clear-suite-icons-venv"
if [ ! -x "$VENV/bin/python3" ]; then
  echo "→ venv + fonttools"
  python3 -m venv "$VENV" >/dev/null
  "$VENV/bin/pip" install -q "fonttools[woff]" brotli
fi

echo "→ building icons, favicons and OG cards"
"$VENV/bin/python3" "$ROOT/scripts/build_icons.py"

echo "→ done. Changed files:"
git -C "$ROOT" status --short -- apps/ | sed 's/^/   /'
