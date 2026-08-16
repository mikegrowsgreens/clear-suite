# Clear Suite — handoff

Last updated 2026-08-15. Keep this current; it is the first thing a fresh session reads.

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
- **Validate JSX before every commit** with the vendored Babel in Node — there is no build step:
  `node -e '...Babel.transform(...)'` over each `<script type="text/babel">` block.
- Never bump `CACHE_NAME`; never rename `sw.js`. The document is network-first.
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

**S2b · The remaining retire-list items** — not started, and each needs its own careful
rewrite rather than a find-and-replace. From the audit's 45-item list, still live in the
apps: nicotine's "lung function up 30%" / "heart disease risk halved at 1 year" /
"20 minutes" and "12 hours" as exact figures; **the entire combustion timeline shown to
vapers** (CO, cilia, tar — physically meaningless without combustion, and the audit's
single biggest structural error); alcohol's "BP improves within 24 hours" (directionally
wrong — biphasic rebound), clearer-skin and immune claims on any date; sugar's HbA1c and
inflammation milestones; social media's wellbeing promises (pooled effect null) and
anything at 3 months or 1 year; and porn's flatline framing. Audit sections are keyed by
domain in the plan file.

**S3 · Framing consistency** — two empty-state patterns (Flow/Air/Mind have a CTA, the
other five do not); setup taglines split between poetic and flat category labels; the
next-milestone percentage still renders in seven apps as a credit-balance display; and
"days free" is avoidance-shaped where approach-framed goals succeeded 58.9% vs 47.1%
(Oscarsson 2020, N=1,066).

**S4 · Visual direction — DECIDED 2026-08-15. Named direction: "Long Evening".**

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

**Desktop is new work, not a restyle.** At 1440 every app is a 400px column in a void; the
synthesis puts the look-back and the identity gap in a second column.

**Known fix before building:** light-mode secondary `#66765A` is 3.56:1 on the sage ground —
passes for large text, fails for the 10px category descriptions. Darken it. Everything else
checks out (dark 15.3:1 body / 5.5:1 secondary / 6.1–7.3:1 accents; light 11:1 body).

Next step is `DESIGN.md` — named aesthetic, reference lock, tokens with roles, ban list (no
emoji as iconography, no stock Tailwind swatches, no fill-to-100 progress, no unlock/reward
vocabulary, no clinical sterility), decision ledger — then roll across the eight apps and hub.

**S5 · Identity assets** — unblocked now that S4 is decided. Suite mark (none exists; the hub currently
borrows Clear Flow's icon), hub favicon and manifest, and nine real 1200×630 OG cards —
every share currently renders as a small square app icon.

**S6 · Optional one-person share** — needs a decision. Harkin's largest moderator:
monitoring shared with one other person **d+ = 0.47** vs private and unshared **0.19**.
The local-first stance forgoes it. A user-initiated local export is the only version that
does not compromise the privacy position.

**S7 · Recommitment prompt** — BCT 1.9 was the only technique to survive in both Black
2020 (OR 1.30) and Leppin 2024 (digital-specific, b=0.39). Currently absent.

## Open questions

- Self-monitoring is not directionally neutral: across 787,393 BAC readings it reduced
  consumption in heavy drinkers and **increased** it in lighter ones. Live question for
  Clear Body, Clear Energy and Clear Feed, whose users skew lighter.
- Gambling suicide figures need reconciling before any are published: Karlsson gives
  ~15× SMR, Wang 2026 gives OR 8.52. Quote the range, not a point estimate.
- Five of the eight verticals (vaping as distinct from smoking, sugar, social media, porn,
  caffeine) have effectively no clinical evidence base for digital intervention. Any claim
  of clinical grounding must be scoped to alcohol, nicotine, cannabis and gambling.
