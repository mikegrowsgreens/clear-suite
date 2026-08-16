#!/usr/bin/env python3
"""
Scan the eight apps and the hub for claims on the S2b retire-list.

WHY THIS EXISTS: S2 was scoped to three findings and grew to sixty-five, because
the same claim recurs in four vocabularies and a phrase list keeps missing it.
This greps for the *vocabulary*, and it reports every hit with its line so each
one can be rewritten individually — the retire-list items are not find-and-replace.

  python3 scripts/audit_claims.py            # all patterns
  python3 scripts/audit_claims.py combustion # one group

Item numbers refer to the CLAIMS TO RETIRE list in the per-substance audit,
~/.claude/plans/please-do-a-full-ethereal-lake-agent-a05e29e900db21a4b.md.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = ["clearflow", "clearair", "clearmind", "clearbody", "clearfeed",
        "clearodds", "clearsight", "clearenergy", "landing"]

# group -> (applies-to, item refs, regex)
PATTERNS = {
    "combustion": (
        {"clearair"}, "#11 combustion timeline shown to vapers",
        r"cilia|carbon monoxide|carboxyhaem|\btar\b|lung cancer|"
        r"oxygen level|smok(?:ing|er)"),
    "lung-30pct": (
        {"clearair"}, "#7 lung function up 30%",
        r"lung function (?:increase|up|improv)|30%|thirty percent"),
    "chd-1yr": (
        {"clearair"}, "#8 heart disease risk halved at 1 year",
        r"heart[- ]disease risk|heart disease risk|risk (?:is )?half|halve"),
    "exact-times": (
        {"clearair"}, "#10 '20 minutes' and '12 hours' as exact figures",
        r"[Tt]wenty [Mm]inutes|20 minutes|12 hours|twelve hours"),
    "alcohol-bp": (
        {"clearflow"}, "#14 BP improves within 24 hours",
        r"blood pressure|\bBP\b"),
    "skin": (
        {"clearflow", "clearbody"}, "#21 clearer skin on any stated date",
        r"skin\b"),
    "immune": (
        {"clearflow", "clearair", "clearbody", "clearmind", "clearenergy"},
        "#20 immune rebound on any stated date",
        r"immun(?:e|ity)|white blood cell|infection"),
    "hba1c": (
        {"clearbody"}, "#27 HbA1c before 3 months",
        r"HbA1c|A1C|glycated|blood sugar (?:normal|stabil)"),
    "inflammation": (
        {"clearbody", "clearflow"}, "#28 inflammation/CRP milestone",
        r"inflammat|\bCRP\b|C-reactive"),
    "dental": (
        {"clearbody"}, "#31 dental claim before 1 year",
        r"dental|teeth|tooth|enamel|cavit"),
    "wellbeing": (
        {"clearfeed"}, "#41 abstinence improves wellbeing stated as fact",
        r"wellbeing|well-being|happier|mood improve|life satisfaction"),
    "attention": (
        {"clearfeed"}, "#42/#43 attention-span recovery, goldfish",
        r"attention span|focus (?:return|restor|improv)|goldfish|"
        r"deep work|concentration (?:return|restor)"),
    "flatline": (
        {"clearsight"}, "#35 the porn flatline",
        r"flatline|flat line|rewir|reboot"),
    "porn-ed": (
        {"clearsight"}, "#36/#37 porn-induced ED, testosterone",
        r"erectile|\bED\b|testosterone|libido"),
    # Cross-cutting families S2 retired. Re-run to catch regressions.
    "s2-regression": (
        set(APPS), "S2 families — must stay at zero",
        r"receptor|endocannabinoid|reward system|recalibrat|dopamine|adenosine|"
        r"peaks? and passe?s?"),
    # Design contract, not the claims audit.
    "meters": (
        set(APPS), "DESIGN.md ban #3 — fill-to-100 meters",
        r"\bpct\s*:\s*100\b"),
}


def scan(groups):
    total = 0
    for name in groups:
        applies, ref, rx = PATTERNS[name]
        pat = re.compile(rx, re.I)
        hits = []
        for app in APPS:
            if app not in applies:
                continue
            p = os.path.join(ROOT, "apps", app, "index.html")
            if not os.path.exists(p):
                continue
            for n, line in enumerate(open(p, encoding="utf-8"), 1):
                for m in pat.finditer(line):
                    s = max(0, m.start() - 60)
                    hits.append((app, n, m.group(0),
                                 line[s:m.end() + 60].strip()))
        total += len(hits)
        flag = "" if hits else "  (clean)"
        print(f"\n### {name} — {ref} — {len(hits)} hit(s){flag}")
        for app, n, tok, ctx in hits[:60]:
            print(f"  {app:12} {n:>5}  {tok:<18} …{ctx}…")
        if len(hits) > 60:
            print(f"  … and {len(hits) - 60} more")
    print(f"\nTOTAL {total} hit(s) across {len(groups)} group(s)")
    return total


if __name__ == "__main__":
    sel = sys.argv[1:] or list(PATTERNS)
    bad = [s for s in sel if s not in PATTERNS]
    if bad:
        sys.exit(f"unknown group(s): {bad}\navailable: {list(PATTERNS)}")
    scan(sel)
