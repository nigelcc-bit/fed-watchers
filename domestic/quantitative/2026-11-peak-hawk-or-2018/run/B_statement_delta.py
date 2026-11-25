"""Step B, statement-delta: redline Oct 27-28 2026 minutes vs Sep 15-16 2026 minutes (and the two statements).
Scorer 1 (headline): judgement score per aligned change, -2..+2; quotes verified verbatim against data/raw/fomc.
Scorer 2 (robustness): fixed keyword lists below, written before this script was first run on the text."""
import re

import pandas as pd

from common import OUT, RAW, ledger, save_parquet

F = RAW / "fomc"
sep = (F / "fomcminutes20260916.txt").read_text()
octm = (F / "fomcminutes20261028.txt").read_text()
sep_st = (F / "monetary20260916a.txt").read_text()
oct_st = (F / "monetary20261028a.txt").read_text()

# section, old (Sep, verbatim or "(absent)"), new (Oct, verbatim or "(absent)"), score, why, cosmetic?
R = [
    ("Inflation assessment", "had not seen sufficient progress on lowering inflation", "inflation pressures in the economy were broad based", +1,
     "Breadth language strengthens ('most'); partly offset by tariff effects 'appeared to be waning'", False),
    ("Inflation expectations", "measures of short-term inflation expectations were elevated",
     "risk of elevated inflation becoming entrenched", 0, "Same concern in both sets; Sep already flagged five years above target", False),
    ("Inflation risks", "Participants generally assessed inflation risk as skewed to the upside", "The vast majority saw upside risks to this outlook", 0,
     "Upside skew unchanged; Oct adds offsetting view that AI scrutiny could reduce inflation pressures", False),
    ("Labour market", "A majority of participants assessed that the labor market had strengthened a bit recently",
     "Many pointed to signs of modest tightening in the labor market", 0, "Same direction; risks balanced in both", False),
    ("Activity (statement)", "Economic activity is expanding at a solid pace", "Economic activity is expanding at a strong pace", +1,
     "Upgrade from solid to strong", True),
    ("Activity (minutes)", "(absent)", "growth remained uneven", -1,
     "New: interest-sensitive sectors weak, lower- and middle-income strain", False),
    ("Financial conditions", "financial conditions appeared to be supportive of economic growth",
     "a majority of participants noted a tightening in financial conditions since the September meeting", -1,
     "Tighter conditions do some of the Fed's work; lowers the bar for holding", False),
    ("Policy decision", "all participants supported raising the target range", "most participants expressed support for maintaining the target range", -1,
     "Hike to hold, citing 'benefits in accumulating additional information' and a 'gradual approach'", False),
    ("Votes and dissents", "Voting against this action:\nNone", "Lisa D. Cook and Beth M. Hammack, who preferred to raise", +2,
     "Two hawkish dissents; 'some' favoured +25bp and called the stance 'not sufficiently restrictive'", False),
    ("Guidance: breadth (most -> almost all)", "another increase in the target range for the federal funds rate would likely be appropriate by year end",
     "almost all participants judged that, under their baseline outlooks", +1, "Most to almost all on further firming", False),
    ("Guidance: size", "(absent)", "an increase of more than 25 basis points could warrant consideration at the next meeting", +1,
     "New: a couple open a 50bp door, conditional on unfavourable inflation data", False),
    ("Guidance: stance", "(absent)", "a shift to a more restrictive policy stance could become necessary", +1, "New: a few float a more restrictive stance", False),
    ("Guidance: pacing", "(absent)", "evaluated by considering the overall path of the federal funds rate over time", -1,
     "New: several de-emphasise meeting-by-meeting action, i.e. no rush", False),
    ("Statement guidance verb", "Today's policy action will support a timelier return", "The accumulation of more information will help the Committee determine", -1,
     "From action to wait-and-see; largely mechanical given the hold", True),
    ("Financial stability (new section)", "(absent)", "returns on AI investment turned out to be disappointing", 0,
     "Two-sided: flags AI-debt fragility, but 'several' say monetary policy is not the tool for it", False),
]


def norm(t):
    return re.sub(r"\s+", " ", t)


S, O, SS, OS = map(norm, (sep, octm, sep_st, oct_st))
rows = []
for sec, old, new, sc, why, cosm in R:
    old_ok = old == "(absent)" or norm(old) in S or norm(old) in SS
    new_ok = new == "(absent)" or norm(new) in O or norm(new) in OS
    rows.append(dict(section=sec, old=old.replace("\n", " "), new=new, score=sc, why=why, likely_cosmetic=cosm, old_verified=old_ok, new_verified=new_ok))
red = pd.DataFrame(rows)
assert red.old_verified.all() and red.new_verified.all(), red[~(red.old_verified & red.new_verified)]
net = int(red.score.sum())
net_ex_cosm = int(red[~red.likely_cosmetic].score.sum())
hawk = int(red.score[red.score > 0].sum())
dove = int(red.score[red.score < 0].sum())


def band(x):
    return "net dovish vs Sep" if x <= -2 else ("flat" if x <= 1 else "more hawkish than Sep")


# ---------- Scorer 2: fixed keyword lists ----------
HAWK = ["raise the target range", "raising the target range", "increase in the target range", "further action to raise", "tightening steps",
        "more restrictive", "not sufficiently restrictive", "upside", "entrenched", "broad based", "more than 25 basis points", "too high",
        "persistent", "unanchored", "close call"]
DOVE = ["maintain the target range", "maintaining the target range", "accumulating additional information", "gradual", "downside",
        "weighed", "slowing", "diminish", "temper", "tightening in financial conditions", "waning", "patient"]


def policy_text(t, start_pat):
    i = t.find(start_pat)
    j = t.find("Committee Policy Actions", i)
    return norm(t[i:j]).lower()


ps = policy_text(sep, "Participants' Views on Current Conditions")
po = policy_text(octm, "Policymakers' Discussion of Current Conditions")


def tone(t):
    h = sum(t.count(k) for k in HAWK)
    d = sum(t.count(k) for k in DOVE)
    return h, d, (h - d) / max(h + d, 1), len(t.split())


hs, ds, ts, ws = tone(ps)
ho, do, to, wo = tone(po)
dtone = to - ts
kw_band = "more hawkish than Sep" if dtone > 0.05 else ("net dovish vs Sep" if dtone < -0.05 else "flat")

ledger("B_h1c_redline_net", "H1c", f"net {net:+d} (hawk {hawk:+d}, dove {dove:+d}) over {len(red)} changes", len(red), band(net))
ledger("B_h1c_redline_ex_cosmetic", "H1c-rob", f"net excl. likely-cosmetic {net_ex_cosm:+d}", int((~red.likely_cosmetic).sum()), band(net_ex_cosm))
ledger("B_h1c_redline_dissent_as_1", "H1c-rob", f"net with dissents scored +1 instead of +2: {net - 1:+d}", len(red), band(net - 1))
ledger("B_h1c_keyword_tone", "H1c-rob", f"keyword net tone Sep {ts:+.2f} ({hs}h/{ds}d, {ws}w) -> Oct {to:+.2f} ({ho}h/{do}d, {wo}w); diff {dtone:+.2f}", 2, kw_band)

save_parquet(red, "minutes_redline")
label = "MIXED (hawkish tilt)" if (hawk and dove and abs(net) <= 2) else ("HAWKISH" if net > 0 else "DOVISH")
lines = ["# statement-delta card: Oct 2026 minutes vs Sep 2026 minutes", "",
         f"**VERDICT: {label}** | confidence 50% (judgement scoring; net sits on the band edge)",
         f"Net score **{net:+d}** (hawkish {hawk:+d}, dovish {dove:+d}; {len(red)} changes) -> H1c band: **{band(net)}**",
         f"Excluding likely-cosmetic changes: {net_ex_cosm:+d} ({band(net_ex_cosm)}). Dissents scored +1: {net-1:+d} ({band(net-1)}).",
         f"Keyword scorer: net tone Sep {ts:+.2f} -> Oct {to:+.2f} (diff {dtone:+.2f}) -> {kw_band}.",
         "Versus pricing: as of 25 Nov (A1), December is priced ~99% +25bp and ~1% +50bp. Pricing just before the 18 Nov release was not captured, so the release's own market effect is not measured here.",
         f"Keyword counts: Sep {hs} hawkish / {ds} dovish hits; Oct {ho} / {do}. Hits by term (Oct): " + ", ".join(f"{k}={po.count(k)}" for k in HAWK + DOVE if po.count(k)),
         "Historical analogues: no dataset of past minutes changes and 2y reactions is available in this repo; none quoted.", "",
         "| Section | Old wording (Sep) | New wording (Oct) | Score | Why it matters |", "|---|---|---|---|---|"]
for r in red.itertuples():
    lines.append(f"| {r.section}{' (likely cosmetic)' if r.likely_cosmetic else ''} | {r.old} | {r.new} | {r.score:+d} | {r.why} |")
(OUT / "B_statement_delta.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines[:8]))
