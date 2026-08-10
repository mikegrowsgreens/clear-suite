/* Clear Suite service worker.
   The ONLY per-app difference in this file is the APP constant below.

   HARD RULE: never rename this file and never change its scope. Doing so
   orphans every existing registration and strands installed users forever.

   Design note: the document is fetched network-first, so CONTENT ships
   without needing a new worker. SW_REV below only needs bumping when the
   logic in THIS file changes — forgetting it is now harmless. */
const APP = 'clearodds';
const SW_REV = 6;

const SHELL_CACHE  = APP + '-shell-' + SW_REV;
const VENDOR_CACHE = APP + '-vendor';
const OURS   = new RegExp('^' + APP + '-');      // every cache this app owns
const LEGACY = new RegExp('^' + APP + '-v\\d');  // clearair-v5-0 etc.

const SHELL = ['/index.html', '/manifest.json', '/icon-192.png', '/icon-512.png'];
const VENDOR = [
  '/vendor/react-18.2.0.production.min.js',
  '/vendor/react-dom-18.2.0.production.min.js',
  '/vendor/babel-7.23.9.min.js'
];

const SW_BOOT = Date.now();

/* FNV-1a over the HTML. This hash IS the version — there is no constant to
   forget. Synchronous and ~instant for 80KB; deliberately not SubtleCrypto
   (async, and needless API-support risk on older iOS). */
function hash(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = (h * 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, '0');
}

function broadcast(msg) {
  return self.clients.matchAll({ type: 'window', includeUncontrolled: true })
    .then(cs => cs.forEach(c => c.postMessage(msg)));
}

/* install — allSettled, never all. A single 404 must NEVER fail the install:
   a failed install means the new worker never activates and users stay on the
   old worker forever, which is the worst outcome available. */
self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const shell = await caches.open(SHELL_CACHE);
    await Promise.allSettled(SHELL.map(u => shell.add(new Request(u, { cache: 'reload' }))));

    const vendor = await caches.open(VENDOR_CACHE);
    const have = new Set((await vendor.keys()).map(r => new URL(r.url).pathname));
    await Promise.allSettled(
      VENDOR.filter(u => !have.has(u)).map(u => vendor.add(new Request(u, { cache: 'reload' })))
    );

    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    const legacyFound = keys.filter(k => LEGACY.test(k));

    /* Prefix-scoped: a positive assertion about what this app owns.
       localStorage is not reachable from here at all, by design. */
    await Promise.all(
      keys.filter(k => OURS.test(k) && k !== SHELL_CACHE && k !== VENDOR_CACHE)
          .map(k => caches.delete(k))
    );

    await self.clients.claim();

    /* One-time migration nudge: only for clients that were on the legacy
       worker, and only on a cold launch (within 15s of this worker booting).
       Without it users converge on the second launch instead of the first. */
    if (legacyFound.length && Date.now() - SW_BOOT < 15000) {
      const wins = await self.clients.matchAll({ type: 'window' });
      for (const c of wins) {
        try { if (typeof c.navigate === 'function') await c.navigate(c.url); }
        catch (_) { /* Safari support varies; next launch converges anyway */ }
      }
    }

    await broadcast({ type: 'SW_ACTIVATED', rev: SW_REV });
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  /* SAME-ORIGIN GUARD. We never respond to cross-origin requests, so we can
     never hand HTML back as the body of a failed script request. */
  if (url.origin !== self.location.origin) return;

  if (req.mode === 'navigate' || req.destination === 'document') {
    e.respondWith(handleDocument());
    return;
  }
  if (url.pathname.startsWith('/vendor/')) {
    e.respondWith(cacheFirst(req, VENDOR_CACHE));
    return;
  }
  e.respondWith(staleWhileRevalidate(req, SHELL_CACHE));
});

/* Network-first document. cache:'no-store' means a mis-set Cache-Control on
   either deploy target (or a CDN in front) cannot serve us a stale document. */
async function handleDocument() {
  const cache = await caches.open(SHELL_CACHE);
  const KEY = '/index.html';
  try {
    const fresh = await fetch(new Request(KEY, {
      cache: 'no-store', credentials: 'same-origin', redirect: 'follow'
    }));
    if (!fresh.ok) throw new Error('status ' + fresh.status);
    if (!(fresh.headers.get('content-type') || '').includes('text/html')) throw new Error('not html');

    const body = await fresh.clone().text();
    const next = hash(body);
    const prev = await cache.match(KEY);
    const prevHash = prev ? hash(await prev.clone().text()) : null;

    await cache.put(KEY, fresh.clone());
    await cache.put('/', fresh.clone());

    if (prevHash && prevHash !== next) {
      broadcast({ type: 'HTML_REPLACED', version: next, previous: prevHash });
    }
    return fresh;
  } catch (_) {
    const cached = (await cache.match(KEY)) || (await cache.match('/'));
    if (cached) return cached;
    return new Response(
      '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">' +
      '<title>Offline</title><body style="margin:0;display:grid;place-items:center;height:100vh;' +
      'font:400 15px/1.5 system-ui;background:#060a0a;color:#94a3b8">' +
      '<p>You are offline. Reopen when you have a connection.</p>',
      { status: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  }
}

async function cacheFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req);
  if (hit) return hit;
  try {
    const resp = await fetch(req);
    /* Poison guard: try_files can turn a missing /vendor/* file into a 200
       text/html response. Caching that under a script URL would brick the app
       for a year under immutable. Refuse to cache HTML for a non-document. */
    const isHtml = (resp.headers.get('content-type') || '').includes('text/html');
    if (resp.ok && !isHtml) cache.put(req, resp.clone());
    return resp;
  } catch (_) {
    return new Response('/* offline: asset unavailable */',
      { status: 504, statusText: 'Offline', headers: { 'Content-Type': 'text/plain' } });
  }
}

async function staleWhileRevalidate(req, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req);
  const net = fetch(req)
    .then(resp => { if (resp.ok) cache.put(req, resp.clone()); return resp; })
    .catch(() => null);
  if (hit) return hit;
  return (await net) || new Response('', { status: 504, statusText: 'Offline' });
}

self.addEventListener('message', e => {
  const d = e.data || {};
  if (d.type === 'CHECK_UPDATE') {
    e.waitUntil(checkForUpdate());
  } else if (d.type === 'GET_VERSION') {
    e.waitUntil((async () => {
      const cache = await caches.open(SHELL_CACHE);
      const cached = await cache.match('/index.html');
      const v = cached ? hash(await cached.clone().text()) : null;
      const reply = { type: 'VERSION', version: v, rev: SW_REV };
      if (e.ports && e.ports[0]) e.ports[0].postMessage(reply);
      else if (e.source) e.source.postMessage(reply);
    })());
  } else if (d.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/* Called while a session is already running. Writes the new HTML into cache
   immediately (so the next launch is fresh even offline) and tells the page.
   Never reloads — the user may be mid-craving-log. */
async function checkForUpdate() {
  try {
    const cache = await caches.open(SHELL_CACHE);
    const fresh = await fetch(new Request('/index.html', { cache: 'no-store' }));
    if (!fresh.ok) return;
    if (!(fresh.headers.get('content-type') || '').includes('text/html')) return;

    const next = hash(await fresh.clone().text());
    const prev = await cache.match('/index.html');
    const prevHash = prev ? hash(await prev.clone().text()) : null;
    if (!prevHash || prevHash === next) return;

    await cache.put('/index.html', fresh.clone());
    await cache.put('/', fresh.clone());
    await broadcast({ type: 'UPDATE_READY', version: next, previous: prevHash });
  } catch (_) {}
}
