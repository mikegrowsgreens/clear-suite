# Clear Suite — handoff

Last updated 2026-08-15 (S5). Keep this current; it is the first thing a fresh session reads.

## State

Eight quit-tracker PWAs + hub. Free forever, local-first, AGPL. Live at
`<app>.mikegrowsgreens.com`, hub at `clearsuite.mikegrowsgreens.com`.

**2026-08-15: evidence rebuild shipped and deployed.** A brand audit turned into a
clinical / behaviour-change review (~200 graded sources). Commits `caf987e`, `66f07e0`
on `main`, deployed to all nine surfaces and verified live.

Research briefings live at `~/.claude/plans/please-do-a-full-ethereal-lake*.md` —
the main plan file plus four agent briefings (behaviour-change mechanisms and identity,
harms of tracking apps, per-substance claims audit, digital therapeutics and attrition).
**The per-substance claims audit is the gating input for the next slice.**

### What shipped

**Privacy.** Self-hosted DM Sans + DM Serif Display into `apps/*/vendor/fonts/`.
Google Fonts was the last outbound call and leaked each user's IP plus a `Referer`
naming the subdomain — telling Google someone was on a porn- or gambling-recovery
tracker — against a stated promise that data never leaves the device. All nine
surfaces now make **zero third-party requests**, verified live. The hub also moved
off Inter onto the apps' own typeface, closing a cross-surface split.

**Safety.** Clear Flow: real withdrawal window (seizures 6–48h, DTs to ~day 8, so
feeling fine at 72h is not past it), the kindling effect, and medical guidance on
restart — ASAM 2020 rec IV.5 treats a return to drinking as a clinical escalation
criterion, not a counter event. Clear Air: CYP1A2 warning (Cormac 2010 — clozapine
≥1000 µg/L went 4.2% → 41.7% after a hospital smoking ban). Clear Body: hypoglycaemia
screen for insulin and sulfonylureas. Clear Sight: onboarding no longer assumes
addiction — distress in that population tracks moral incongruence, not use frequency
(Grubbs 2019/2020). Clear Sight and Clear Odds: 988 in the lapse flow, the
highest-risk screen in each.

**Honest numbers.** Killed the composite "% RECOVERED". `getWeightedHealth()` took one
input — elapsed time — so everyone who quit the same morning saw an identical figure;
it credited the calendar and printed it as a claim about the person's body. Replaced by:
cumulative days free across every run (never zeroed by a slip); a stat tile showing
cravings/urges **met** instead of duplicating the day count; the notes people write in
hard moments resurfaced as "You wrote this"; a new `IdentityCheck` component (two
sliders and the gap — BCT 13.5 was the strongest individual technique in Black 2020,
OR 1.34, N=43,992; in Dingle 2015 the change in that gap explained 34–49% of outcome
variance); and a hideable day count (Olatunji 2011; NICE NG183 1.4.3).

Also: favicons on all eight apps, `--text-muted` brought to AA (2.38:1 → 5.13:1 dark,
2.34:1 → 5.04:1 light), `prefers-reduced-motion`, "Achievement Unlocked" →
"Milestone Reached", per-app untinting of input/modal surfaces that were Clear Air's
teal in all eight, title/OG/manifest normalisation.

### Things that were corrected mid-flight — do not re-litigate

- **Badges and streaks are not the problem.** Direct tests (Mekler) found points/levels/
  leaderboards did not undermine autonomy or competence, and gamified smoking cessation
  has RCT support (RR 1.91 <6mo, 1.37 ≥6mo, 15 RCTs, N=5,075). The overjustification
  literature is the wrong frame here — it concerns tangible rewards for intrinsically
  interesting tasks.
- **Streak-reset harm is largely unproven.** The design choice is defensible because the
  burden of proof sits on the reset and has never been met, not because a citation exists.
- **"A slip is not a reset" was already right** before any of this work.
- **Clear Air is one of the more honest apps**, not the least — it uses "Evidence basis:"
  rather than "Sources:", and had already stripped carbon-monoxide claims because vaping
  produces negligible CO.

## Conventions

- Eight apps are one template. A fix propagates eight times; script it, then verify all eight.
- **Verify in a browser, not just by grep.** Each app is a separate preview server
  (`clear-flow` … `clear-sight` in the parent `.claude/launch.json`); seed
  `<app>_onboarded='true'` and `<app>_data` in localStorage to land on the dashboard.
  Only five preview servers may run at once — stop one before starting the next. If the
  limit is reported while nothing is actually listening, the registry is stale from another
  session; `python3 -m http.server <port> --directory apps/<app>` serves them just as well.
- **Validate JSX before every commit** with the vendored Babel in Node — there is no build step:
  `node -e '...Babel.transform(...)'` over each `<script type="text/babel">` block.
- **`DESIGN.md` is the design contract.** Read it before changing any surface. It carries the
  token table with measured contrast, the ban list, and the decision ledger.
- **Never transition `color`.** See S4 below — a var()-backed colour on an element with a
  colour transition does not re-resolve when the theme changes.
- Never bump `CACHE_NAME`; never rename `sw.js`. The document is network-first.
- **Vendor URLs are `immutable` at the edge, so never request one before it exists.**
  A `--verify-only` run made *before* an upload got a 404 that Cloudflare then pinned for
  a year against the real URL (clearair's `long-evening.css`, 2026-08-15). `deploy.sh` now
  probes `?probe=$$`, and the page references `long-evening.css?v=N` — bump `v` rather than
  renaming the file when the faces change. `clearair.../long-evening.css` (no query) is
  still a poisoned 404 at one PoP; nothing references it, and a CF purge would clear it.
- `SKIP_LANDING` is tested with `-z`, so **`SKIP_LANDING=0` skips the hub**. Unset it to deploy the hub.
- Deploy: `CLEAR_HOST=root@167.172.119.28 scripts/deploy.sh` (add `--verify-only` for a
  read-only check). Apps → `/var/www/<app>/`, hub → `/var/www/clearsuite/`. The script now
  covers the hub and asserts `/vendor/fonts/*` returns 200 and the live HTML contains no
  `fonts.googleapis.com`.
- **Retention is explicitly not a success metric.** Median 30-day retention for this app
  class is 3.3%; the standard response is to add engagement mechanics, which is how the
  category becomes harmful. Front-load value instead.

## Remaining slices

**S2 · Mechanism claims — SHIPPED 2026-08-15** (`9788b26`). 65 edits, 9 surfaces.

The slice was scoped to three findings and grew to one coherent family, because the
same claim recurs in four vocabularies. Keyword greps kept surfacing new instances after
each pass; the sweep that finally closed it greps for the *vocabulary*
(`receptor|endocannabinoid|reward system|recalibrat|reset|peaks? and passe?s?`), not for
individual phrasings. Use that grep, not a phrase list, when auditing this codebase.

- **Dopamine** (Body/Feed/Mind/Sight, 9 claims) — retired. Volkow 2001 measured
  transporters, n=5, 12–17 months, +16–19%, no cognitive gain. Replaced with report-level
  language ("what people report", "nobody has measured this").
- **Adenosine** (Energy, 9 claims incl. "Full adenosine reset" at 90d) — retired.
  Never measured in humans; rodent data contradictory. Replaced with the withdrawal arc,
  which is the most precise evidence in the suite, and with the honest destination — a
  never-user's baseline, not more energy than before (Rogers 2010).
- **CB1** (Mind) — **kept**, it is the one measured receptor finding. What went: the
  10-milestone curve between two scans, the "day 28 reset" event, and a day-14 D'Souza
  cite (he scanned day 2 and day 28). Category renamed `ECS Recovery` → `Withdrawal`;
  the hub's Clear Mind card was updated to match.
- **Craving duration** (15 places, 6 apps) — retired. Never measured in minutes; the
  "whether you act or not" half is contradicted by EMA data showing use lowers craving.
- **Urge surfing** (all 8 apps) — "sitting through one weakens the next" retired.
  Bowen & Marlatt: urges unchanged, behaviour changed. Also stops a normal incubation
  spike reading as failure.
- **Clear Flow sleep** — rebuilt from 180 days to 24 months, with the day-4–5 insomnia
  peak (72%), still-impaired-at-2-months, SWS at 21–27 months, and CBT-I signposting at
  week two (insomnia roughly doubles relapse risk).

**S2b · The remaining retire-list items — SHIPPED AND DEPLOYED 2026-08-15** (`0100e98`).
5 apps, ~45 rewrites. Deploy exits 0; 24 retired claim strings confirmed absent from
production, with live bytes matching local on all five changed apps.

`scripts/audit_claims.py` is the new tool and the thing to reuse: it greps the retire-list
*vocabulary* per app and prints every hit with its line, because a phrase list keeps
missing recurrences. Run it before and after any claims work.

**Two whole categories turned out to be invented, and neither was on the scoped list.**
That is the lesson of this slice: the HANDOFF list named individual milestones, but the
same unsupported idea had been built out into a full six-milestone category twice.

- **Clear Air's "Immune System"** → replaced by **Withdrawal**. No human study puts a date
  on immune recovery after stopping nicotine. Withdrawal is the best-evidenced content in
  the domain (Hughes 2007, 120 studies: peaks week 1, runs 2–4 weeks, and drowsiness and
  fatigue are *not* withdrawal effects).
- **Clear Body's "Inflammation"** → replaced by **Liver & BP**. Retire-list #28: no clean
  evidence gives CRP or IL-6 a timescale for cutting sugar at any point. Liver fat is the
  best-dated finding in the entire domain and wasn't a category at all — Schwarz 2017 took
  it 7.2% → 3.8% in nine days with weight deliberately held stable, so it is the sugar and
  not the weight loss.

**Clear Air — the combustion timeline is gone.** Cilia (day 7 and day 270), the lung-function
milestones, the 1-year heart-disease claim, and the 10y/15y "full recovery" endpoints. The
worst single line was *"Studies of vapers who quit show respiratory symptoms easing within
weeks"* — **no such studies exist**; a targeted search returned 11 hits, every one about
switching *from smoking to* vaping. The app asserted a literature that has never been
written. NASEM 2018 lists respiratory disease, clinical CV outcomes and cancer endpoints
for e-cigarettes as **no available evidence**, so no curve is drawn for any of them. What
was kept is what transfers because it is about nicotine rather than smoke: pharmacokinetics
and withdrawal. A new onboarding slide, "What this app will not tell you", says all of this
to the user directly.

**The rest.** Clear Flow: the 24h BP milestone was directionally *wrong* (alcohol is
biphasic — BP rises from ~13h, so a 24h "improvement" may be a rebound), and the 30-day one
now says the −5.5 mmHg only applies above six drinks a day, since Roerecke found nothing
significant at two or fewer. Clear Body: HbA1c at 30 days is physiologically impossible
(red cells live ~100 days) and now says so; the skin category rebuilt around the one real
datum, acne at twelve weeks, flagged as weight-confounded. Clear Feed: a single positive RCT
was being stated as fact against a preregistered meta-analysis (10 studies, N=4,674) that
found no significant effect — now framed as Allcott's trade-off, and the attention-span
claims are gone. Clear Sight: the flatline is no longer *scheduled* (weeks 2–6, "lifts at
day 45") since it is community-coined and unmeasured, and the erectile-function milestones
went — the larger studies find little or no link to use itself.

**Invariants worth re-checking after any claims edit** (all held): every app still has
exactly 6 categories, weights still sum to 1.0, and milestone times are still ascending
within each category and in the achievement ladder. A one-off script caught a real ordering
bug here — a Clear Body skin milestone collided with a pre-existing 60-day entry I had not
seen — so check ordering, not just JSX.

**Found but deliberately not fixed (out of scope, worth a slice):** a gear emoji renders in
the settings button of all eight apps, which contradicts both DESIGN.md ban #1 and S4's
"0 emoji render anywhere, verified". S4's check evidently looked at content, not chrome.

**S3 · Framing consistency — SHIPPED 2026-08-15.** 8 apps, verified live in a browser
(setup → dashboard → journal tab → settings round-trip) app by app, not just grepped.

- **Empty state.** Five apps (Body/Energy/Feed/Odds/Sight) had no early return: opening
  the journal tab for the first time rendered a row of zeroed stat tiles, the entire
  achievement ladder greyed out, and a "No cravings logged yet" note underneath — a wall
  of zeros as the first thing a new user sees. All eight now early-return the same
  designed empty state (icon, one line of explanation, one CTA). Copy unified across all
  eight, including the three that already had one.
- **Setup taglines.** Air/Flow/Mind said "recovery from the first minute/hour forward" —
  the only three that never named what you quit. Now "from alcohol", "from vaping and
  nicotine", "from cannabis", matching the shape the other five already used.
- **The next-milestone percentage is gone from all eight** (the count was seven; Flow had
  it too). It was `elapsed / nextAch.time` — elapsed against an *absolute* milestone time,
  not progress through the current segment — so it ran **backwards**: day 29 of a 30-day
  milestone read 96%, then day 31 with the next at 60 days read 52%. Reaching a milestone
  dropped your number. It was also a fill-to-100 reward meter, which is on the S4 ban
  list. The row now reads icon + label + "in 23h 59m", which is the honest, complete
  information and was already sitting right next to it.
- **Approach framing (Oscarsson 2020, 58.9% vs 47.1%, N=1,066).** The evidence is about
  how a *goal* is worded, so that is where it was applied:
  - `IdentityCheck` `freeLabel` was `"someone who does not"` in **all eight** — the target
    identity defined purely by negation, on the one slider whose gap is the mechanism
    (Dingle 2015). Now per-app and approach-shaped: "someone who wakes up clear",
    "someone who just breathes", "someone who is fully here", "someone who eats for how
    they want to feel", "someone whose attention is their own", "someone who keeps what
    they earn", "someone at ease with themselves", "someone who runs on their own energy".
  - The gap sentence hardcoded "more the person who does not, than the one who did" and
    **ignored the app's own labels entirely**. It now composes from them: "closer to
    someone who keeps what they earn than to someone who bets".
  - The goal field: "Why are you doing this?" → "What do you want more of?", with the
    helper "Name what you are moving toward, not what you are quitting" and approach-shaped
    placeholders. It existed in only five apps; Air, Flow and Mind now have it too (setup
    field, settings field, and the line under the day count) — config round-trip verified
    in the browser for all three.

**"Days free" was deliberately left alone.** It was on the S3 list as avoidance-shaped, and
it is not. "Free" names a state you hold, not a behaviour you are abstaining from, and the
counter is the honest measure the whole S1 rebuild was built around. Renaming it would have
been cosmetic. Same call on "Drinks Avoided" / "Puffs Avoided" in Air and Flow: those two
are avoidance-shaped and the newer five already use reclaim language ("Hours Reclaimed",
"Hours Back", "Money Kept"), but there is no honest approach-framed version of a drink you
did not drink. Left as-is rather than inventing one.

Also added: per-app entries (`clear-flow`, `clear-air`, …) in the parent
`.claude/launch.json`. Each app hardcodes absolute asset paths (`/vendor/...`), so it has
to be served at its own root — serving `apps/` and browsing to `/clearodds/` 404s every
script. S4 will want these.

**S4 · Visual direction — SHIPPED 2026-08-15. Named direction: "Long Evening".**

Round one (nine directions, `design/directions/index.html`) was **rejected**: "very very
sanitized, clinical, sterile — it feels like I'm in a hospital being in our apps." That was
correct, and the mistake is worth recording so nobody repeats it. The research said the
*mental model* is a record of your own recovery; I translated that into hospital, which
frames the user as a **patient being treated** — the opposite of the product's thesis that
you already did it and you are free. Casino-neon and hospital-white are both the wrong role.
All nine were also refined serif on white: nine shades of one idea, not nine directions.
Warmth comes from saturated hue, soft light and texture — not from paper.

Round two (`design/directions/warm.html`, reference-locked to Liven, Wayfinder, Palette
Supply and Apron) produced the pick — "long evening my favorite style, field guide and
hearth best colors". Resolved in `design/directions/synthesis.html`:

- **Long Evening** = the system. Sora 200 for the hero figure, Fraunces for the wordmark,
  pull-quote and identity gap. Soft 18px cards, low-alpha accent surfaces, generous quiet.
- **Hearth** = the dark theme. `radial-gradient(120% 85% at 50% 0%, #2A1E15, #17120E 60%)`,
  text `#F3E7DA`, secondary `#9C8975`, surface `rgba(255,235,215,.05)`.
- **Field Guide** = the light theme. Ground `#D8DFCB` with a warm ochre corner wash, text
  `#1E2A19`, accent `#6E4E24`, surface `rgba(252,250,242,.58)`. Fills a real hole — light
  mode is currently undesigned Tailwind slate, identical across all eight apps.

**Per-app accents, custom-mixed, no Tailwind:** Flow `#C4563C`, Air `#5E8B7E`, Mind
`#6B8A3D`, Body `#C4636B`, Feed `#8B7BA8`, Odds `#C89B4A`, Sight `#6B7F9E`, Energy `#D08A2C`.

**S4 — SHIPPED AND DEPLOYED 2026-08-15** (`bee7f91`, `197f163`). All nine surfaces
verified live: `long-evening.css?v=2` 200 everywhere, Sora + Fraunces loading, zero
third-party requests, zero rendered emoji. `DESIGN.md` is now the contract; read it before touching any
surface. Rolled across all eight apps and the hub, verified in a browser app by app in both
themes at 375 / 768 / 1440.

- **Type.** DM Sans / DM Serif Display → **Sora + Fraunces**, self-hosted, still zero
  third-party requests. `scripts/vendor-fonts.sh` is the provenance record; it clips the
  variable axes to what the design uses (Fraunces ships opsz 9–144 / wght 100–900, which
  roughly halves per file once clipped). Fraunces italic exists for one element: the user's
  own reason. **The stylesheet had to be renamed** `fonts.css` → `long-evening.css`:
  `/vendor/*` is cache-first in the SW and never revalidated, so reusing the name would have
  left every returning user on DM Sans forever. Any future face change needs a new filename.
- **Colour.** Hearth / Field Guide as designed themes, per-app accents with a **separate
  value per theme** — a colour that clears 4.5:1 on umber does not clear it on sage.
  Everything measured against the true worst case (a card over the *lightest* point of the
  dark gradient; the *bare* ochre-washed ground in light), not the flattering one. The
  handoff's old "6.1–7.3:1 accents" figure was against the deep end of the gradient; against
  the light end the synthesis values were 3.66–4.24 and had to be retuned. Table in DESIGN.md §4.
- **Structure.** Category rings → a typographic row list; the milestone trophy grid → a text
  ladder; all emoji iconography gone (0 emoji render anywhere, verified); cards are
  translucent and unbordered; gradients flattened to flat accent fills; no weight above 600.
- **Desktop** (≥1024) is the two-column layout, with a sticky left column. Below 1024 the
  wrappers are `display:contents`, so mobile is byte-for-byte the layout it was.
- **Marks recoloured, not redesigned.** All 24 icon PNGs were remapped from their old
  Tailwind ramp onto the Long Evening one, because a Long Evening hub with eight neon marks
  looked broken. Designing an actual suite mark is still S5.

**A real bug found and fixed on the way: never transition `color` in these apps.** An
element carrying `transition: all` (or `transition: color`) does **not** re-resolve a
`var()`-backed colour when `data-theme` changes — verified in a minimal in-page probe, while
`background-color` / `border-color` / `opacity` / `transform` all update fine. The tab labels
kept the previous theme's colour indefinitely after a toggle, which was unreadable once the
two themes stopped being two shades of slate. All 87 `transition:'all …'` declarations across
the eight apps are now explicit property lists that exclude colour, and the theme swap is
additionally made instant via a `theme-switching` class. This was latent before S4 and
invisible only because both old themes were grey.

**S5 · Identity assets — SHIPPED AND DEPLOYED 2026-08-15** (`146e781`).

The eight marks were **varied, not replaced**, and that was Mike's call after two rounds of
replacement were rejected. Worth recording so nobody re-runs it: round one was ten *systems*
(`design/marks/sheet-1.png`, `-2`) and every one was a parameter sweep — a rect or circle
moved around a brown tile by formula, no type, no warmth. Round two was ten originals
(`sheet2-*.png`), better, but replacing marks people already recognise bought nothing.
Round three (`sheet3-*.png`) varied the treatment and kept every glyph; Mike picked
**Two-tone** — a filled accent disc with a cream glyph.

- **The eight glyphs are unchanged.** They had no vector source, only PNGs, so they were
  redrawn as paths in `scripts/build_icons.py` — which is also the first time they were
  optically balanced against each other. Ink coverage ran 2.24% (bolt) to 3.63% (eye), a
  1.6× spread; each is nudged toward the median by a damped `(median/ink)^0.3`.
- **Disc colours are not the Hearth accents.** Cream on Hearth measures 2.09–2.54:1, under
  the 3:1 floor — fine at 84px, failed at 16px. Each disc is mixed ~70% toward its Field
  Guide accent, giving cream 4.5:1 on all eight. Table in DESIGN.md §10.
- **The hub has its own mark** — a Fraunces C. It borrowed Clear Flow's icon, which made
  the parent read as a ninth sibling.
- **Nine real 1200×630 OG cards.** Apps moved from `summary` (crops square) to
  `summary_large_image`.
- **New per surface:** `icon-32` (the 192 downscaled to 16 was mush), full-bleed `icon-180`
  for apple-touch (iOS masks it itself; a pre-rounded tile comes back double-rounded),
  `icon-maskable-512`, `og.png`. The hub got its **first** favicon, apple-touch and
  `manifest.json` — it had none.

**Two latent bugs fixed on the way**, both pre-S4 leftovers nothing else would have caught:

- Every manifest still carried a near-black `theme_color`/`background_color`, and eight
  *different* ones (`#060a0a`, `#06080f`, `#0c0806` …). The HTML `theme-color` was correct,
  so the PWA splash and the Android task switcher were the last un-rebranded surfaces.
- The `sw.js` offline page was still `#060a0a` on `#94a3b8` slate — the one screen a user
  sees when everything else has failed was the only surface that looked like a different
  product. Now Hearth. No `SW_REV` bump; the string is not part of any cache key.

**Rebuild with `scripts/build-icons.sh`** (needs `librsvg`; no network — it reads the
already-vendored woff2). `deploy.sh` now asserts all six icon files plus `og.png` return
200 **and** `image/png` on every surface, because `try_files` turns a miss into the HTML
document with a 200, and a missing OG card is invisible until somebody shares a link.

**Verified live.** `--verify-only` exits 0 across all nine surfaces, with 62 new asset URLs
returning 200 `image/png` (8 apps × 6, hub × 6, plus the hub's 8 card marks). JSX compiles
clean in all eight under the vendored Babel; hub and Clear Flow were browser-checked in both
themes; the production `og.png` was pulled back and confirmed to be a real 1200×630.

Two things worth knowing:

- Icons are **stale-while-revalidate** in the service worker, not cache-first, so returning
  users get the old icon once and the new one after. This is *not* the font trap (L7) and
  needs no rename.
- The repo `Caddyfile`s are **excluded from rsync** (`--exclude Caddyfile`) — they are the
  record of intent, not live config. Their `@icons` matcher now lists the new files, but the
  droplet's own Caddy needs the same edit by hand if the new assets should be cached rather
  than falling through to the `no-cache` catch-all. Nothing breaks either way.

**S6 · Optional one-person share** — needs a decision. Harkin's largest moderator:
monitoring shared with one other person **d+ = 0.47** vs private and unshared **0.19**.
The local-first stance forgoes it. A user-initiated local export is the only version that
does not compromise the privacy position.

**S7 · Recommitment prompt — SHIPPED AND DEPLOYED 2026-08-15** (`8de40dc`; live on all eight, verified). BCT 1.9 was the only technique to
survive in both Black 2020 (OR 1.30) and Leppin 2024 (digital-specific, b=0.39), and it
was the best-evidenced technique the suite did not have.

One `Recommit` component, identical in all eight apps, mounted under `IdentityCheck`.

- **It fires at the milestone, and it asks instead of congratulating.** That placement is
  the evidence, not a layout choice: Kivetz 2006 documents post-reward resetting — once a
  reward is collected, pace falls back to opening levels (p < .01) — so a milestone-heavy
  app manufactures its own troughs. Fishbach 2006 (F(1,95)=12.60, p<.001) settles the
  wording: a completed subgoal framed as *attainment* reduced interest in continuing, while
  the same subgoal framed as *commitment* increased it. So it reads "One Week in. Is this
  still what you want?" — which also keeps it clear of ban-list §7.4.
- **Cadence:** once per milestone crossed, and otherwise no more than monthly. "Not now"
  snoozes seven days, and an empty answer is accepted. A prompt you cannot decline is
  coercion, and autonomy is the mechanism the rest of the app runs on.
- **It writes back.** The field is pre-filled with the user's approach-framed goal from S3;
  changing it updates `config.motivation`, so the italic line under the day count changes
  too. Verified end to end in a browser.

Verified in Clear Flow across the whole cycle — due state, save, re-trigger on crossing the
next milestone, snooze, and the goal rewrite propagating to the hero line — plus Field Guide
tokens resolving in light mode, and a second app (Clear Energy) to catch any per-app scope
difference at the mount point.

## Open questions

- Self-monitoring is not directionally neutral: across 787,393 BAC readings it reduced
  consumption in heavy drinkers and **increased** it in lighter ones. Live question for
  Clear Body, Clear Energy and Clear Feed, whose users skew lighter.
- Gambling suicide figures need reconciling before any are published: Karlsson gives
  ~15× SMR, Wang 2026 gives OR 8.52. Quote the range, not a point estimate.
- Five of the eight verticals (vaping as distinct from smoking, sugar, social media, porn,
  caffeine) have effectively no clinical evidence base for digital intervention. Any claim
  of clinical grounding must be scoped to alcohol, nicotine, cannabis and gambling.
