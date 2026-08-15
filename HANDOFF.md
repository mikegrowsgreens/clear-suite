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

**S2 · Finish the claims pass** — next up. Three findings, one coherent slice:
- ~9 dopamine-receptor claims in Clear Body / Clear Feed / Clear Mind. No human evidence
  supports a fixed dopamine-recovery timeline; the load-bearing citation (Volkow 2001)
  measured transporters, n=5, over 12–17 months.
- **"Cravings peak in 10–20 minutes and pass"** — 5 places in Clear Sight, plus "15
  minutes" in Clear Energy (`clearenergy:265`). Craving-episode duration has never been
  measured in minutes; this is Marlatt-era clinical lore.
- **Clear Flow's sleep timeline is optimistic in the direction that matters.** It claims
  "deep sleep returning" at 60 days and "sleep architecture largely recovered" at 180.
  Slow-wave sleep normalises at **21–27 months**, sleep is still objectively impaired at
  two months, and insomnia roughly **doubles relapse risk** — so someone sleeping badly at
  day 90 is being told they should be fixed by now.

**S3 · Framing consistency** — two empty-state patterns (Flow/Air/Mind have a CTA, the
other five do not); setup taglines split between poetic and flat category labels; the
next-milestone percentage still renders in seven apps as a credit-balance display; and
"days free" is avoidance-shaped where approach-framed goals succeeded 58.9% vs 47.1%
(Oscarsson 2020, N=1,066).

**S4 · Visual direction** — blocked on Mike's pick. Nine directions rendered at equal
fidelity (see the plan file). Gates `DESIGN.md`, which this repo has never had. The
constraint from the research: the system must express *identity evidence*, not *reward*,
which favours the record-like directions (A Clinical Daylight, D Ledger, H Chart).

**S5 · Identity assets** — blocked on S4. Suite mark (none exists; the hub currently
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
