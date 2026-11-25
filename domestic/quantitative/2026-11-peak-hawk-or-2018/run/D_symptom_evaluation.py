"""Step D, symptom-evaluation (H4): equities falling while the Fed leans hawkish.
Differential and thresholds fixed in PREREGISTRATION.md. Panel readings are changes or spreads; percentiles are
vs the same-length change since 2000 (or since series start). Scored with the skill's scripts/panel_score.py."""
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

from common import OUT, fred, ledger, save_parquet, yahoo

SKILL = Path("/root/.claude/skills/synced/fdb1fdea-2075-46d8-81e2-d9c43f662812_c4742ecd-5b1c-496e-b526-a6fc8d45f0ed/symptom-evaluation/scripts/panel_score.py")

spx = yahoo("^GSPC", start="1950-01-01")["close"]
y26 = spx.loc["2026-01-01":]
hi_date = y26.idxmax()
hi = y26.max()
last_date = spx.index[-1]
k = len(spx.loc[hi_date:]) - 1  # sessions since the high
dd_now = spx.iloc[-1] / spx.rolling(252).max().iloc[-1] - 1
dd_from_high = spx.iloc[-1] / hi - 1
trough_date = spx.loc[hi_date:].idxmin()
trough_dd = spx.loc[hi_date:].min() / hi - 1


def chg_since(s, d0, d1=None):
    s = s.dropna()
    a = s.loc[:d0].iloc[-1]
    b = s.loc[:d1].iloc[-1] if d1 is not None else s.iloc[-1]
    return b - a, a, b, s.index[-1]


def hist_changes(s, n, start="2000-01-01"):
    s = s.dropna().loc[start:]
    return (s - s.shift(n)).dropna().tolist()


readings, facts = [], {}

# P1 drawdown from 252-session high
dd = (spx / spx.rolling(252).max() - 1).loc["2000-01-01":]
readings.append(dict(name="S&P 500 drawdown vs 252-session high", channel="P", value=round(float(dd_now), 4),
                     history=dd.round(4).tolist(), direction="low", evidence="verified"))
# P2 equal-weight vs cap-weight since the high
rsp, spy = yahoo("RSP", "2003-01-01")["adjclose"], yahoo("SPY", "2000-01-01")["adjclose"]
rel = np.log(rsp / spy.reindex(rsp.index)).dropna()
rel_chg, _, _, _ = chg_since(rel, hi_date)
rsp_dd = rsp.iloc[-1] / rsp.loc[hi_date:].max() - 1 if False else rsp.iloc[-1] / rsp.loc[:hi_date].iloc[-1] - 1
spy_dd = spy.iloc[-1] / spy.loc[:hi_date].iloc[-1] - 1
readings.append(dict(name="Equal-wt minus cap-wt (log RSP/SPY) since high", channel="P", value=round(float(rel_chg), 4),
                     history=[round(x, 4) for x in hist_changes(rel, k, "2004-01-01")], direction="high", evidence="verified"))
facts.update(rsp_since_high=float(rsp_dd), spy_since_high=float(spy_dd))

# C1 Baa-10y change since high (daily) and level percentile
baa = fred("BAA10Y")
c1, baa0, baa1, baad = chg_since(baa, hi_date)
lvl_pct = float((baa.dropna().loc["2000-01-01":] < baa1).mean() * 100)
readings.append(dict(name="Baa-10y change since high (pp)", channel="C", value=round(float(c1), 3),
                     history=[round(x, 3) for x in hist_changes(baa, k)], direction="high", evidence="verified"))
# monthly check of the brief's claim (Baa - GS10, Oct 2026 average)
bm, g10 = fred("BAA"), fred("GS10")
msp = (bm - g10).dropna()
oct_m = float(msp.loc["2026-10-01"]) if pd.Timestamp("2026-10-01") in msp.index else np.nan
oct_pct = float((msp.loc["2000-01-01":] < oct_m).mean() * 100)
daily_oct = float(baa.loc["2026-10-01":"2026-10-31"].mean())
facts.update(baa10y_start=float(baa0), baa10y_now=float(baa1), baa10y_date=str(baad.date()), baa10y_level_pct_2000=lvl_pct,
             baa_gs10_oct2026_monthly=oct_m, baa_gs10_oct2026_pct_2000=oct_pct, baa10y_oct2026_daily_avg=daily_oct)

# C2 CCC minus BB OAS change since high
ccc, bb, hy = fred("BAMLH0A3HYC"), fred("BAMLH0A1HYBB"), fred("BAMLH0A0HYM2")
cccbb = (ccc - bb).dropna()
c2, cb0, cb1, cbd = chg_since(cccbb, hi_date)
hyc, hy0, hy1, _ = chg_since(hy, hi_date)
readings.append(dict(name="CCC minus BB OAS change since high (pp)", channel="C", value=round(float(c2), 3),
                     history=[round(x, 3) for x in hist_changes(cccbb, k, "1997-01-01")], direction="high", evidence="verified"))
facts.update(cccbb_start=float(cb0), cccbb_now=float(cb1), cccbb_date=str(cbd.date()), hy_oas_start=float(hy0), hy_oas_now=float(hy1),
             hy_oas_change=float(hyc), cccbb_history_start=str(cccbb.index[0].date()))

# X1 real 10y change (and breakeven change, reported)
dfii, be, d10, d2 = fred("DFII10"), fred("T10YIE"), fred("DGS10"), fred("DGS2")
x1, r0, r1, _ = chg_since(dfii, hi_date)
xbe, be0, be1, _ = chg_since(be, hi_date)
x10, _, y10now, _ = chg_since(d10, hi_date)
x2y, _, y2now, _ = chg_since(d2, hi_date)
readings.append(dict(name="Real 10y (DFII10) change since high (pp)", channel="X", value=round(float(x1), 3),
                     history=[round(x, 3) for x in hist_changes(dfii, k, "2003-01-01")], direction="high", evidence="verified"))
facts.update(real10_change=float(x1), be10_change=float(xbe), d10_change=float(x10), d2_change=float(x2y), y10_now=float(y10now), y2_now=float(y2now))

# X2 60-session equity-bond correlation (S&P returns vs 10y yield changes)
df = pd.concat({"r": np.log(spx).diff(), "dy": d10.diff()}, axis=1, sort=True).dropna()
corr = df.r.rolling(60).corr(df.dy).dropna()
readings.append(dict(name="60d corr(S&P returns, d10y)", channel="X", value=round(float(corr.iloc[-1]), 3),
                     history=corr.loc["2000-01-01":].round(3).tolist(), direction="low", evidence="verified"))
facts.update(eq_bond_corr_now=float(corr.iloc[-1]), eq_bond_corr_at_high=float(corr.loc[:hi_date].iloc[-1]))

# F (composite) NFCI change since first October reading
nfci, anfci = fred("NFCI"), fred("ANFCI")
oct_first = nfci.loc["2026-10-01":].index[0]
f1, n0, n1, nd = chg_since(nfci, oct_first)
w = len(nfci.loc[oct_first:]) - 1
readings.append(dict(name="Chicago Fed NFCI change since first Oct reading", channel="F", value=round(float(f1), 3),
                     history=[round(x, 3) for x in hist_changes(nfci, w)], direction="high", evidence="verified"))
facts.update(nfci_oct_first=float(n0), nfci_now=float(n1), nfci_date=str(nd.date()), anfci_now=float(anfci.dropna().iloc[-1]),
             nfci_level_pct_2000=float((nfci.loc["2000-01-01":] < n1).mean() * 100))

# R1 SLOOS net % tightening C&I to large and middle-market firms: change vs prior survey
sl = fred("DRTSCILM").dropna()
r1 = float(sl.iloc[-1] - sl.iloc[-2])
readings.append(dict(name="SLOOS net % tightening C&I (latest minus prior)", channel="R", value=round(r1, 2),
                     history=[round(x, 2) for x in sl.diff().dropna().loc["2000-01-01":].tolist()], direction="high", evidence="verified"))
facts.update(sloos_latest=float(sl.iloc[-1]), sloos_prior=float(sl.iloc[-2]), sloos_date=str(sl.index[-1].date()))

# R2 initial claims 4-week average, % change since the high
ic = fred("ICSA").dropna().rolling(4).mean().dropna()
icw = len(ic.loc[hi_date:])
icc = float(ic.iloc[-1] / ic.loc[:hi_date].iloc[-1] - 1)
ich = (ic / ic.shift(max(icw, 1)) - 1).dropna().loc["2000-01-01":]
readings.append(dict(name="Initial claims 4wk avg % change since high", channel="R", value=round(icc, 4),
                     history=ich.round(4).tolist(), direction="high", evidence="verified"))
facts.update(claims4w_now=float(ic.iloc[-1]), claims_date=str(ic.index[-1].date()))

# Live monitor only: CRWV vs QQQ since high; VIX / VIX3M
try:
    crwv, qqq = yahoo("CRWV", "2025-03-01")["adjclose"], yahoo("QQQ", "2025-03-01")["adjclose"]
    facts.update(crwv_since_high=float(crwv.iloc[-1] / crwv.loc[:hi_date].iloc[-1] - 1), qqq_since_high=float(qqq.iloc[-1] / qqq.loc[:hi_date].iloc[-1] - 1))
except Exception as e:
    facts.update(crwv_error=str(e))
vix, vix3m = fred("VIXCLS").dropna(), fred("VXVCLS").dropna()
ratio = (vix / vix3m).dropna()
facts.update(vix_now=float(vix.iloc[-1]), vix_date=str(vix.index[-1].date()), vix_vix3m_now=float(ratio.iloc[-1]), vix_vix3m_max_since_high=float(ratio.loc[hi_date:].max()),
             vix_on_2026_11_20=float(vix.loc["2026-11-20"]) if pd.Timestamp("2026-11-20") in vix.index else None)

facts.update(high_date=str(hi_date.date()), high=float(hi), last_date=str(last_date.date()), last=float(spx.iloc[-1]), sessions_since_high=k,
             dd_from_high=float(dd_from_high), dd_252=float(dd_now), trough_date=str(trough_date.date()), trough_dd=float(trough_dd))

# ---------- pre-registered thresholds ----------
T = {}
T["credit_confirming"] = bool(c1 >= 0.25 or hyc >= 0.75)
T["aggregate_loose"] = bool(lvl_pct < 25 and n1 < 0)
T["conditions_tightening"] = bool(f1 >= 0.10)
T["pocket"] = bool(c2 >= 1.00 and not T["credit_confirming"])
T["composition_artefact"] = bool(abs(rsp_dd) < 0.5 * abs(spy_dd)) if spy_dd < 0 else False
for kk, v in T.items():
    ledger(f"D_h4_{kk}", "H4", kk, 1, str(v))

# differential reading
if T["credit_confirming"] and T["conditions_tightening"]:
    lead = "(a) transmitting, credit confirming"
elif T["pocket"]:
    lead = "(c) pocket stress masked by aggregates"
elif T["composition_artefact"]:
    lead = "(d) artefact"
elif T["aggregate_loose"] and not T["conditions_tightening"]:
    lead = "(b) not transmitting, conditions loose"
else:
    lead = "mixed: partial tightening, credit not confirming"
facts["lead"] = lead
facts["thresholds"] = T

panel = dict(symptom="S&P 500 falling from its 2026 high while the Fed leans hawkish", asof=str(last_date.date()), readings=readings)
pj = OUT / "D_panel.json"
pj.write_text(json.dumps(panel))
scored = subprocess.run(["python3", str(SKILL), str(pj), "--md"], capture_output=True, text=True).stdout
(OUT / "D_panel_scored.md").write_text(scored)
(OUT / "D_facts.json").write_text(json.dumps(facts, indent=1, default=str))
save_parquet(pd.DataFrame([{k_: v for k_, v in r.items() if k_ != "history"} for r in readings]), "h4_panel")
print(scored)
print(json.dumps(facts, indent=1, default=str))
