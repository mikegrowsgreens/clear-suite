# Clear Suite

Four free, private quit trackers. No account, no ads, no analytics, no server.

| App | For | Live |
|-----|-----|------|
| **Clear Flow** | Alcohol | [clearflow.mikegrowsgreens.com](https://clearflow.mikegrowsgreens.com) |
| **Clear Air** | Nicotine / vaping | [clearair.mikegrowsgreens.com](https://clearair.mikegrowsgreens.com) |
| **Clear Mind** | Cannabis | [clearmind.mikegrowsgreens.com](https://clearmind.mikegrowsgreens.com) |
| **Clear Body** | Fast food & added sugar | [clearbody.mikegrowsgreens.com](https://clearbody.mikegrowsgreens.com) |

Add any of them to your home screen and it works offline, forever, for free.

## The privacy claim, and how to check it

Everything you enter stays in your browser's `localStorage`, on your own device. There is no account, no backend, and no analytics — **not even Google Analytics**, which was removed in August 2026 precisely because the apps claimed "no tracking" while it was running.

You don't have to take that on trust, which is the point of this repo being public and AGPL-licensed: read `apps/*/index.html` and look for a network call. The only outbound request the apps make is for Google Fonts. Nothing else leaves your device.

## Not medical advice

These apps show physiological recovery timelines drawn from published cessation research. They are **not a medical device**, they don't diagnose or treat anything, and they contain no medication guidance of any kind. For anything about your health, talk to a doctor.

**If you drink heavily, read this before using Clear Flow.** People who are physically dependent on alcohol can become seriously ill — or die — if they suddenly stop completely. If you get shaking hands, sweating, anxiety, trouble sleeping, or see things that aren't there while sobering up, talk to a doctor or a local alcohol service before stopping. Clear Flow says this during onboarding, before it will count a single day.

Crisis support, in every app: **988** (Suicide & Crisis Lifeline) and **1-800-662-4357** (SAMHSA National Helpline).

## What the evidence actually says

Honest framing, because the alternative is marketing: the pooled evidence for standalone quit-tracker apps is **null** — odds ratio 1.03 (95% CI 0.85–1.26) across 9 RCTs and 12,967 adults ([JMIR 2023](https://www.jmir.org/2023/1/e43242)), and Cochrane reached the same conclusion. So no claim is made that this app will make you quit.

What it is: an accurate, private, free place to see what your body is doing — for people whose alternative is an ad-supported tracker that monetizes their relapse data.

## Design principles

- **You're already free.** Freedom is complete the moment you stop; it doesn't accumulate. Nothing is locked behind time served, and milestones show what your body is doing rather than a reward to be earned.
- **A slip is not a reset.** Restarting the clock keeps your craving log and your history, and the day count is cumulative across attempts. Nothing you already healed gets undone.
- **A craving is the dependence leaving**, not a test of character. The word "willpower" appears nowhere in the product.
- **Never a bare zero** as the only number on screen.

## Architecture

Each app is a single `index.html` — inline React 18 via Babel-standalone, no build step, no bundler. Data is `localStorage` only.

```
apps/<app>/
  index.html      the whole app
  sw.js           service worker (identical across apps except the APP constant)
  manifest.json
  vendor/         React, ReactDOM, Babel — self-hosted, version in the filename
  Caddyfile       note: /vendor/* has no try_files, deliberately
  Dockerfile
```

**Updates.** The document is fetched network-first, so a change to `index.html` reaches installed apps without touching the service worker. The version is a content hash computed in the browser — there's no constant to bump. A live session gets a dismissible "new version ready" banner; it never force-reloads, because you might be mid-craving-log. Service worker caches are the only thing an update may clear — `localStorage` isn't reachable from a service worker at all.

**Deploying.** `scripts/deploy.sh` rsyncs to the server, then verifies the bytes actually landed and the cache headers are right. Note that Cloudflare sits in front and will override Caddy's `Cache-Control` on `sw.js` unless a cache rule says otherwise — the script checks for exactly this.

## Support

Issues are open and I read them. **A response isn't promised**, there's no roadmap, and nothing is guaranteed — this is a free thing maintained by one person in spare time. Pull requests are welcome; forks are entirely fine.

## Licence

[AGPL-3.0](LICENSE). Use it, fork it, run it. If you host a modified version, publish your changes — that's the deal, and it's what keeps the privacy claim verifiable for the next person.

Not affiliated with, endorsed by, or licensed by any commercial cessation programme.
