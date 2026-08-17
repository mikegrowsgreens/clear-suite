# Clear Suite — DESIGN.md

The design system for eight quit trackers and their hub. One direction, named and
locked. If a change cannot be justified against this file, it does not ship.

Last updated 2026-08-15 (S5).

---

## 1. The mental model this has to fit

**A private record of your own recovery, kept by you.** Not a treatment, not a
coach, not a game.

Two roles the design must never assign the user:

- **Patient.** Clinical white, thin grey rules, chart-like readouts. This frames
  the user as someone being treated. The product's whole thesis is that they
  already did the hard thing and are free.
- **Player.** Neon on black, glow, fill-to-100 meters, "unlocked". This is the
  visual language of the thing most of them are quitting — five of the eight
  verticals are literally competing with a slot-machine interface.

The user is a **person at the end of a long day, looking at their own book.**
That is the whole brief. Warmth comes from saturated hue, soft light and quiet —
not from paper texture and not from rounded corners alone.

---

## 2. Named direction: **Long Evening**

Long Evening is the *system* — structure, type, spacing, restraint. It ships in
two themes, and both are real designs rather than an inversion of each other:

| Theme | Name | When |
|---|---|---|
| Dark | **Hearth** | default; the 2am open |
| Light | **Field Guide** | daylight; previously undesigned Tailwind slate |

**Reference lock** (round two, `design/directions/warm.html`): Liven, Wayfinder,
Palette Supply, Apron. What was taken from each:

- **Liven** — the screen as a *place* rather than a document. A ground that
  glows from one direction, almost no chrome, no rules, no boxes-within-boxes.
- **Wayfinder** — a single enormous figure carrying the page, set light rather
  than bold, with everything else deferring to it.
- **Palette Supply** — colour used as atmosphere, not as decoration. One accent
  per surface, appearing at low alpha far more often than at full strength.
- **Apron** — editorial serif for the human sentences, geometric sans for the
  measured ones. The typographic split is semantic, not decorative.

Resolved comps: `design/directions/synthesis.html`.

---

## 3. Type

Two families, self-hosted, zero third-party requests (see
`apps/*/vendor/fonts/long-evening.css` and `scripts/vendor-fonts.sh`).

**Sora** — `--font-body`. Weights 200–600 only. The voice of measured things:
counts, labels, controls, body copy. Its 200 is the point of the whole choice —
it holds together at 86px, which is what the day count needs.

**Fraunces** — `--font-display`. Weights 300–600, optical size axis left
variable (12–96) so the wordmark and the pull-quote are genuinely different
cuts rather than one cut scaled. Reserved for **human sentences**: the wordmark,
the pull-quote, the identity-gap figure, section headings.

**Fraunces italic** exists for exactly one element: the user's own stated reason,
in their words. A true italic, not a slant. It is the most personal thing on the
screen and it should not look like a system font.

### Scale

| Role | Family / weight | Size | Notes |
|---|---|---|---|
| Hero figure (days free) | Sora 200 | 86 / 132 desktop | `letter-spacing:-.045em`, `line-height:.95` |
| Wordmark | Fraunces 600 | 21 | |
| Section heading | Fraunces 600 | 18–20 | |
| Identity-gap figure | Fraunces 400 | 27 | |
| Pull-quote | Fraunces 300 | 15.5 | `line-height:1.5` |
| The user's reason | Fraunces 400 *italic* | 12.5 | accent colour, **no opacity** — .9 dropped it to 4.37:1 |
| Body | Sora 300 | 13 | `line-height:1.6` |
| Stat value | Sora 300 | 21 | |
| Label / eyebrow | Sora 400 | 9–10 | `letter-spacing:.15–.2em`, uppercase |
| Category name | Sora 400 | 12.5 | |

**No weight above 600 anywhere.** Sora ships 200–600 here; a `fontWeight:700` is
either clamped or synthesised, and both look worse than the 600. The old design
used 700 twenty-five times per app. That heaviness *was* the old look.

---

## 4. Colour

Ground is a gradient, not a flat fill. Everything else is a token.

### Hearth (dark)

```
ground   radial-gradient(120% 85% at 50% 0%, #2A1E15 0%, #17120E 60%)
surface  rgba(255,235,215,.05)      edge  rgba(255,235,215,.08)
```

| Token | Value | Role |
|---|---|---|
| `--bg-deep` | `#17120E` | the ground's base, behind the gradient |
| `--bg-card` | `rgba(255,235,215,.05)` | every panel. Translucent, never a lighter grey |
| `--bg-card-hover` | `rgba(255,235,215,.08)` | |
| `--text-hi` | `#FFF3E6` | the hero figure and stat values only |
| `--text-primary` | `#F3E7DA` | body |
| `--text-secondary` | `#C8B29A` | supporting sentences |
| `--text-muted` | `#A79383` | 9–11px metadata |
| `--accent-primary` | per app, below | labels, eyebrows, the reason line |
| `--accent-glow` | accent @ 10% | accent surfaces; never a shadow |

### Field Guide (light)

```
ground   radial-gradient(60% 38% at 6% 97%, rgba(184,138,66,.20) 0%, rgba(184,138,66,0) 72%), #D8DFCB
surface  rgba(252,250,242,.58)      edge  rgba(30,42,25,.13)
```

| Token | Value | Role |
|---|---|---|
| `--bg-deep` | `#D8DFCB` | sage ground under the ochre corner wash |
| `--bg-card` | `rgba(252,250,242,.58)` | translucent paper over sage, never flat white |
| `--text-hi` | `#141F0E` | |
| `--text-primary` | `#1E2A19` | |
| `--text-secondary` | `#3A4633` | |
| `--text-muted` | `#4A5640` | **was `#66765A`** — see ledger L6 |

### Per-app accents — custom-mixed, no Tailwind

Each app gets its own hue; both themes get their own value of it, because a
colour that clears contrast on umber does not clear it on sage.

| App | Vertical | Hearth | Field Guide |
|---|---|---|---|
| Clear Flow | alcohol | `#D17C67` | `#8C3D2A` |
| Clear Air | vaping / nicotine | `#6C9C8E` | `#3E5C53` |
| Clear Mind | cannabis | `#7B9E46` | `#475B28` |
| Clear Body | sugar | `#CE7D83` | `#92373F` |
| Clear Feed | social media | `#9A8DB4` | `#5E4F78` |
| Clear Odds | gambling | `#C89B4A` | `#6C5121` |
| Clear Sight | porn | `#8394AE` | `#48576E` |
| Clear Energy | caffeine | `#D08A2C` | `#754E19` |
| *danger* (`--rose`) | destructive / lapse | `#E28C79` | `#8E2E1B` |

Hue families come from the synthesis comps; the exact values are the nearest
tone in each family that clears 4.5:1 on **both** the ground and a card.

### Contrast — measured, worst case, both surfaces

Worst case in dark is *a card over the lightest point of the gradient*
(`#35281F`), not the deep end. Worst case in light is the *bare ochre-washed
ground* (`#D2CEB0`), not the card. Every value below is the lower of the two.

| | Hearth | Field Guide |
|---|---|---|
| text-primary | 11.70 | 9.42 |
| text-secondary | 6.98 | 6.27 |
| text-muted | 4.84 | 4.89 |
| accents (range across 8 apps) | 4.60 – 5.59 | 4.60 – 4.72 |
| danger | 5.60 | 5.16 |

Everything clears **4.5:1**, which is the bar because the suite sets real
information at 9–11px. Re-run the numbers before changing any colour; there is
no headroom in the accents.

---

## 5. Space, shape, motion

- **Radius.** `--radius-md:18px` is the card. Soft, generous, one value doing
  most of the work. `--radius-sm:12px` for controls, `--radius-lg:24px` for
  modals, pills stay fully round.
- **Panels are translucent, never bordered.** A card is `--bg-card` with no
  border. Borders appear only as `edge` hairlines between list rows.
- **Quiet is a feature.** Vertical rhythm 8 / 14 / 22 / 30. If a screen feels
  empty, that is the design; do not fill it.
- **Motion** stays as-is: `--ease-out: cubic-bezier(.16,1,.3,1)`, entrances only,
  staggered 60–80ms, and a full `prefers-reduced-motion` bypass. No motion is
  ever the carrier of information.

---

## 6. Layout

**Mobile** — one 440px column, unchanged in structure.

**Desktop (≥1024px) is new work, not a restyle.** Today every app is a 400px
column stranded in a void. Long Evening puts the two things worth reading side
by side:

```
┌──────────────────────────┬──────────────────────────┐
│ wordmark                 │  You wrote this          │
│                          │                          │
│ 233                      │  identity gap            │
│ DAYS FREE                │                          │
│ 104d this run · since …  │  recovery categories     │
│ "my reason"              │                          │
│ [ stats row ]            │                          │
└──────────────────────────┴──────────────────────────┘
   1.05fr                      .95fr, edge hairline
```

Left is the count and what it bought. Right is the look-back and the identity
gap — the two things that are *evidence about the person* rather than about the
clock. The hero figure goes to 132px, because at that width 86px looks timid.

---

## 7. Ban list

Not stylistic preferences. Each of these has a reason attached.

1. **No emoji as iconography.** Emoji are inconsistent across platforms, cannot
   be coloured, and read as decoration on screens about serious things.
2. **No stock Tailwind swatches.** All 32 accents used to be Tailwind defaults,
   which is exactly why the hub squinted down to eight coloured dots. Accents
   are mixed for this palette or they are not used.
3. **No fill-to-100 progress meters.** They are reward meters. They also invite
   exactly the bug S3 fixed, where reaching a milestone made the number drop.
   Show the honest, complete fact instead: `in 23h 59m`.
4. **No unlock / reward vocabulary.** "Achievement Unlocked" is already gone.
   Milestones are *reached*, not earned; nothing is withheld from the user.
5. **No clinical sterility.** No pure white, no `#000`, no thin grey rules, no
   chart chrome. See §1.
6. **No neon or glow on dark.** `--accent-glow` is a low-alpha *surface fill*,
   never a `box-shadow` halo.
7. **No weight above 600.** See §3.
8. **No third-party requests, ever.** Not fonts, not analytics, not an icon CDN.
   This is a privacy promise made in the product copy, not a preference.
9. **No composite scores.** Killed in S1 and it stays killed. A number that
   takes only elapsed time as input is a claim about the calendar dressed up as
   a claim about the person.

---

## 8. Decision ledger

| | Decision | Why |
|---|---|---|
| L1 | Round one (nine directions, `directions/index.html`) **rejected** | "Very very sanitized, clinical, sterile — it feels like I'm in a hospital being in our apps." Correct. The research said the mental model is *a record of your own recovery*; that got translated into *hospital*, which casts the user as a patient under treatment — the opposite of the thesis. All nine were also refined serif on white: nine shades of one idea, not nine directions. |
| L2 | Long Evening as the system, Hearth and Field Guide as its themes | Mike: "long evening my favorite style, field guide and hearth best colors." Long Evening's structure and type were the pick; the other two supplied the two grounds. |
| L3 | Light mode is a **designed theme**, not an inversion | The apps already shipped a light/dark toggle and light mode was undesigned Tailwind slate, identical across all eight. This filled a real hole rather than making one. |
| L4 | Per-app accents, two values each | One accent per app makes the suite read as one thing with eight members. Two values per accent because contrast on umber and contrast on sage are different problems. |
| L5 | Sora 200 for the figure, Fraunces for sentences | The split is semantic: measured things in the sans, human things in the serif. It is also what stops the hero figure from reading as a scoreboard. |
| L6 | `--text-muted` light darkened `#66765A` → `#4A5640` | `#66765A` is 3.56:1 on the sage ground. It passes for large text; the suite uses it at 10px for category descriptions, where it fails. |
| L7 | Font stylesheet renamed `fonts.css` → `long-evening.css`, and referenced as `?v=N` | `/vendor/*` is cache-first in the service worker and never revalidated, so reusing the filename would have left every returning user on DM Sans forever. The query version is the cheaper lever for the same problem: bump `?v=` to change the cache key without renaming files. It also escapes a poisoned edge cache — see L10. |
| L8 | Fraunces axes clipped, italic's optical size pinned | These are render-blocking bytes on a first visit. Clipping `opsz`/`wght` to what the design uses roughly halves each file. The italic appears at one size on one element, so it does not need a live axis. |
| L10 | Deploy probes are cache-busted, and the stylesheet carries `?v=` | `/vendor/*` is served `immutable`, so Cloudflare cached the 404 from a `--verify-only` run made *before* the file was uploaded, and pinned it for a year against the real URL. Clear Air's stylesheet 404'd at the edge while being perfectly fine on the box. `deploy.sh` now probes `?probe=$$` so a pre-deploy miss can never poison a live URL, and the page's `?v=` gave the fix without another rename. |
| L9 | "Days free" kept, "Drinks Avoided" kept | S3 call, restated here so it is not reopened: "free" names a state you hold, not a behaviour you abstain from. And there is no honest approach-framed version of a drink you did not drink — better to leave it than to invent one. |
| L11 | The eight marks were **varied, not replaced** | Two full rounds of replacement were rejected. Round one was ten parameter sweeps — a rect or circle moved around a brown tile by formula, no type and no warmth, which is how you get a systems exercise instead of an identity. Round two was ten originals and better, but replacing eight marks people already recognise buys nothing the treatment could not. The glyphs are unchanged; only what surrounds them moved. |
| L12 | Disc colours are **not** the Hearth accents | Cream on the Hearth accents measures 2.09–2.54:1, under the 3:1 floor for meaningful graphics — it looked fine at 84px and failed at favicon size. Each disc is mixed ~70% from its Hearth accent toward its Field Guide accent, which puts cream at 4.5:1 on all eight while keeping the hue and leaving the disc 3.4:1 against the ground. |
| L13 | The hub has its own mark: a Fraunces **C** | It borrowed Clear Flow's icon, which made the parent read as a ninth sibling and meant Clear Flow's mark meant two different things. A letterform is the one shape that can parent eight pictorial glyphs without competing with them. |
| L14 | Glyph scales carry a measured optical-weight correction | Rendered ink coverage ran 2.24% (bolt) to 3.63% (eye) — a 1.6× spread, visible as some marks looking bolder than others in the same row. Each is nudged toward the 3.06% median by `(median/ink)^0.3`. Damped deliberately: fully equalising ink makes the compact glyphs look bloated. |
| L15 | `apple-touch-icon` is full-bleed, and a maskable variant exists | iOS applies its own mask, so a pre-rounded tile comes back double-rounded with dark wedges in the corners. Android launchers mask too, hence the separate `purpose:maskable` icon with the figure inside the 80% safe area. |
| L19 | A render error degrades to a card, never a white screen | On 2026-08-15 a null read in `Recommit` unmounted the whole tree and Clear Flow went blank in real use. The one-line bug was trivial; the white screen was the actual harm, because on an app whose only job is holding someone's record it is indistinguishable from losing it. Every app now has a `Boundary`: one at the root, and one around each card that renders from a user-written store. The fallback leads with **"Your record is safe"** rather than an error, because that is the only question the user has. It touches no storage and sends nothing — "Copy details" puts the stack on the clipboard for the user to forward if they choose, which is the only reporting compatible with zero network requests. |
| L18 | Chrome icons are SVG, and S4's "0 emoji" check was wrong | The theme toggle and settings button used `U+2699 ⚙`, `U+2600 ☀` and `U+263E ☾`. All three are Extended_Pictographic — emoji by the only definition that matters to ban list §7.1 — and they render differently on every platform, which is the reason for the ban. S4 verified "0 emoji render anywhere" and missed them because a toggle only ever renders one of its three states at a time, so the sun and moon were invisible to a single-state check. **Count glyphs in the source, not pixels on one screen.** |
| L17 | The recommitment prompt sits **at the milestone**, and asks rather than congratulates | BCT 1.9 is the only technique to survive in both Black 2020 (OR 1.30) and Leppin 2024 (b = 0.39, digital-specific). It is placed at the milestone because that is where the risk is: Kivetz 2006 documents post-reward resetting (pace falls to opening levels once a reward is collected, p < .01), so a milestone-heavy app manufactures its own troughs. Fishbach 2006 (F(1,95) = 12.60, p < .001) settles the wording — a completed subgoal framed as *attainment* reduced interest in continuing, the same subgoal framed as *commitment* increased it. Hence "One Week in. Is this still what you want?" rather than a congratulation, which is also ban-list §7.4. It is snoozable and accepts an empty answer, because a prompt you cannot decline is coercion and autonomy is the mechanism the rest of the app runs on. |
| L16 | Manifest `theme_color` corrected to `#17120E` | All eight still carried pre-S4 near-blacks — and eight *different* ones (`#060a0a`, `#06080f`, `#0c0806` …). The HTML `theme-color` was right, so the PWA splash and the Android task switcher were the last surfaces never rebranded. The offline page in `sw.js` was the same leftover and is now Hearth. |

---

## 10. Identity assets

Every mark, icon and share card is generated from `scripts/build_icons.py` and
rebuilt with `scripts/build-icons.sh`. Before S5 the marks were PNG-only with no
vector source, so recolouring meant remapping pixels and reshaping was impossible.

### The treatment: two-tone

A filled accent disc carrying a cream glyph. It replaced a hairline ring that
vanished completely at favicon size. The eight glyphs themselves are unchanged
from what shipped — compass, wind, sprout, four-point star, feed bars, diamond,
eye, bolt — redrawn as paths and optically balanced against each other.

| | Disc | Derived from (Hearth) | cream on disc | disc on ground |
|---|---|---|---|---|
| Clear Flow | `#A3523E` | `#D17C67` | 4.50 | 3.39 |
| Clear Air | `#4D7066` | `#6C9C8E` | 4.51 | 3.39 |
| Clear Mind | `#587132` | `#7B9E46` | 4.51 | 3.39 |
| Clear Body | `#A54D55` | `#CE7D83` | 4.55 | 3.36 |
| Clear Feed | `#71628B` | `#9A8DB4` | 4.51 | 3.38 |
| Clear Odds | `#83642B` | `#C89B4A` | 4.51 | 3.39 |
| Clear Sight | `#5A6A82` | `#8394AE` | 4.52 | 3.38 |
| Clear Energy | `#8F5F1F` | `#D08A2C` | 4.51 | 3.39 |
| **Clear Suite** (hub) | `#80633F` | — (brass, its own) | 4.57 | 3.34 |

Glyph is always `--text-primary` cream `#F3E7DA`. Re-measure before moving any
disc value; these were solved to the bound, so there is no headroom.

### Marks must not disclose

A stranger glancing at the owner's homescreen should not learn what they are
quitting. This is a privacy requirement, not a style one — the product promises
that nothing leaves the device, and an icon is data leaving the device by other
means. It rules out anything literal: a bottle, a vape, a slot machine. The
existing glyphs are abstract enough to pass, which is a further reason they were
kept. **Any future mark has to clear this bar before it is judged on looks.**

### What gets built

Per app and for the hub: `icon-32` (favicon — browsers were downscaling the 192
to 16 and it turned to mush), `icon-180` (apple-touch, full-bleed),
`icon-192` / `icon-512` (`purpose:any`), `icon-maskable-512`, and `og.png`.
The hub additionally gets the eight `<app>-icon.png` used by its cards.

### Open Graph

Nine real 1200×630 cards. Every share used to render as a small square app icon.
Layout is the mark, the wordmark in Fraunces 68, one Sora line, a hairline rule
and the promise — `FREE FOREVER · NO ACCOUNT · NOTHING LEAVES YOUR DEVICE`. The
hub leads with all eight marks in a row instead of a single mark. Apps carry
`summary_large_image`; they were on `summary`, which crops to a square.

---

## 9. Verifying a change

The apps have no build step, so the checks are manual and all of them are cheap.

1. **Validate JSX** with the vendored Babel in Node before every commit. There
   is no compiler to catch you.
2. **Look at it in a browser, not at a grep.** Each app is its own preview
   server (`clear-flow` … `clear-sight` in the parent `.claude/launch.json`);
   seed `<app>_onboarded` and `<app>_data` in localStorage to land on the
   dashboard. Only five may run at once.
3. **Both themes, three widths** — 1440 / 768 / 375. Light mode is the one that
   gets forgotten.
4. **All eight apps.** Eight apps are one template; a fix propagates eight
   times and so does a mistake.
5. **Re-measure contrast** if any colour moved. There is no headroom.
