#!/usr/bin/env bash
# Ship to the DigitalOcean box and PROVE the bytes changed.
#
#   scripts/deploy.sh                 -> all eight apps
#   scripts/deploy.sh clearair        -> one app
#   scripts/deploy.sh --verify-only   -> check what is live (use after a git push/Railway build)
#
# Why this exists: the old workflow relied on remembering to bump CACHE_NAME.
# The service worker no longer needs that (the document is network-first), so
# the only remaining discipline is "did the files actually land". This checks.
set -euo pipefail

HOST="${CLEAR_HOST:?set CLEAR_HOST, e.g. root@203.0.113.10}"
DOMAIN_SUFFIX="${CLEAR_DOMAIN_SUFFIX:-mikegrowsgreens.com}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

VERIFY_ONLY=0
[ "${1:-}" = "--verify-only" ] && { VERIFY_ONLY=1; shift; }
APPS=("${@:-}"); [ -z "${APPS[0]:-}" ] && APPS=(clearair clearflow clearmind clearbody clearfeed clearodds clearsight clearenergy)

hdr()    { curl -fsSI "$1" | tr -d '\r' | awk 'tolower($1)=="cache-control:"{sub(/^[^ ]+ /,"");print}'; }
served() { curl -fsS "$1" 2>/dev/null | shasum -a 256 | cut -c1-12; }

fail=0
for app in "${APPS[@]}"; do
  src="$ROOT/apps/$app"; url="https://$app.$DOMAIN_SUFFIX"
  [ -d "$src" ] || { echo "no such app: $app" >&2; exit 1; }

  local_html="$(shasum -a 256 "$src/index.html" | cut -c1-12)"
  local_sw="$(shasum -a 256 "$src/sw.js"        | cut -c1-12)"
  before_html="$(served "$url/index.html" || echo none)"

  if [ "$VERIFY_ONLY" -eq 0 ]; then
    # No --delete: stale version-named vendor files are harmless, and --delete
    # would destroy anything on the box that isn't in the repo.
    rsync -av --exclude Caddyfile --exclude Dockerfile --exclude .dockerignore \
      --exclude .DS_Store "$src/" "$HOST:/var/www/$app/"
  fi

  after_html="$(served "$url/index.html" || echo none)"
  after_sw="$(served   "$url/sw.js"      || echo none)"

  echo "-- $app"
  printf '   index.html  local %s  live %s  (was %s)\n' "$local_html" "$after_html" "$before_html"
  printf '   sw.js       local %s  live %s\n'           "$local_sw"   "$after_sw"

  [ "$after_html" = "$local_html" ] || { echo "   FAIL index.html live != local"; fail=1; }
  [ "$after_sw"   = "$local_sw"   ] || { echo "   FAIL sw.js live != local";      fail=1; }
  [ "$before_html" != "$after_html" ] || echo "   note: HTML unchanged, clients will see no update"

  # sw.js must revalidate or installed users are stranded. Cloudflare's default
  # 4h browser TTL overrides Caddy here, so this check is load-bearing.
  for p in /index.html /sw.js /manifest.json; do
    cc="$(hdr "$url$p" || echo MISSING)"
    printf '   %-34s %s\n' "$p" "$cc"
    case "$cc" in
      *no-cache*|*no-store*) ;;
      *) echo "   FAIL $p must be no-cache (check the Cloudflare cache rule, not just Caddy)"; fail=1;;
    esac
  done

  for v in react-18.2.0.production.min.js react-dom-18.2.0.production.min.js babel-7.23.9.min.js \
           fonts/fonts.css fonts/dmsans-latin.woff2 fonts/dmserif-latin.woff2; do
    code="$(curl -fsS -o /dev/null -w '%{http_code}' "$url/vendor/$v" || echo 000)"
    ct="$(curl -fsSI "$url/vendor/$v" | tr -d '\r' | awk 'tolower($1)=="content-type:"{print $2}')"
    printf '   %-34s %s %s\n' "/vendor/$v" "$code" "$ct"
    [ "$code" = "200" ] || { echo "   FAIL vendor missing"; fail=1; }
    case "$ct" in text/html*) echo "   FAIL vendor served as HTML - try_files is swallowing the 404"; fail=1;; esac
  done

  # The fonts are the privacy guarantee: if they 404, the page still renders on a
  # fallback face and nobody notices, so this has to be checked, not assumed.
  if curl -fsS "$url/index.html" 2>/dev/null | grep -q 'fonts\.googleapis\.com'; then
    echo "   FAIL live HTML still references Google Fonts - third-party request restored"; fail=1
  fi

  # The poison case: a missing vendor file must 404, never return the document.
  # No -f here: we WANT the status code of an error response, and -f makes
  # curl exit nonzero on 404 so the || fallback used to append a second "404".
  nf="$(curl -sS -o /dev/null -w '%{http_code}' "$url/vendor/__missing__.js" || echo 000)"
  printf '   %-34s %s (want 404)\n' "/vendor/__missing__.js" "$nf"
  [ "$nf" = "404" ] || { echo "   FAIL missing vendor file does not 404"; fail=1; }
done

# The hub. It was never in this script, so it silently stayed a release behind —
# which mattered the moment the hub started carrying its own vendored fonts.
# Different docroot (/var/www/clearsuite), different host, and no service worker.
if [ -z "${SKIP_LANDING:-}" ]; then
  src="$ROOT/apps/landing"; url="https://clearsuite.$DOMAIN_SUFFIX"
  local_html="$(shasum -a 256 "$src/index.html" | cut -c1-12)"
  before_html="$(served "$url/index.html" || echo none)"
  if [ "$VERIFY_ONLY" -eq 0 ]; then
    rsync -av --exclude Caddyfile --exclude Dockerfile --exclude .dockerignore \
      --exclude .DS_Store "$src/" "$HOST:/var/www/clearsuite/"
  fi
  after_html="$(served "$url/index.html" || echo none)"
  echo "-- landing (clearsuite)"
  printf '   index.html  local %s  live %s  (was %s)\n' "$local_html" "$after_html" "$before_html"
  [ "$after_html" = "$local_html" ] || { echo "   FAIL index.html live != local"; fail=1; }
  for v in fonts/fonts.css fonts/dmsans-latin.woff2; do
    code="$(curl -fsS -o /dev/null -w '%{http_code}' "$url/vendor/$v" || echo 000)"
    printf '   %-34s %s\n' "/vendor/$v" "$code"
    [ "$code" = "200" ] || { echo "   FAIL vendor missing"; fail=1; }
  done
  if curl -fsS "$url/index.html" 2>/dev/null | grep -q 'fonts\.googleapis\.com'; then
    echo "   FAIL live HTML still references Google Fonts"; fail=1
  fi
fi

exit $fail
