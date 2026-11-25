"""Step A3, reaction-function: 96-variant Taylor-type rule band vs actual, plus a Kalman-filtered
time-varying-coefficient rule (i = a + b*pi + c*gap, random-walk coefficients, filtered).
Latest-vintage FRED data (ALFRED unreachable) -> look-ahead flagged for any historical reading."""
import itertools
import json

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from common import OUT, fred, ledger, save_parquet

ASOF = pd.Timestamp("2026-11-25")


# ---------- inflation measures (latest available 12-month rate) ----------
infl = {}
src = {}
for name, sid, kind in [("core_pce", "PCEPILFE", "index"), ("core_cpi", "CPILFESL", "index"),
                        ("trimmed_pce", "PCETRIM12M159SFRBDAL", "rate"), ("median_cpi", "MEDCPIM094SFRBCLE", "index")]:
    s = fred(sid).dropna()
    if kind == "index":
        s = s.asfreq("MS")
        y = (s / s.shift(12) - 1) * 100
    else:
        y = s.asfreq("MS")
    y = y.dropna()
    infl[name] = float(y.iloc[-1])
    src[name] = f"{sid} {y.index[-1]:%Y-%m}"

# Oct 2026 core CPI m/m (Waller's condition)
cc = fred("CPILFESL").dropna()
cc_mm = (cc / cc.shift(1) - 1) * 100
oct_mm = float(cc_mm.loc["2026-10-01"]) if pd.Timestamp("2026-10-01") in cc_mm.index else np.nan

# ---------- gaps ----------
un = fred("UNRATE").dropna()
nrou = fred("NROU").dropna()
u_last, u_date = float(un.iloc[-1]), un.index[-1]
q = u_date.to_period("Q").start_time
u_star = float(nrou.loc[:q].iloc[-1])
gap_u = -2 * (u_last - u_star)
gdp = fred("GDPC1").dropna()
pot = fred("GDPPOT").dropna()
og = ((gdp / pot.reindex(gdp.index)) - 1) * 100
gap_y, gap_y_date = float(og.dropna().iloc[-1]), og.dropna().index[-1]
gaps = {"output_gap_cbo": gap_y, "okun_unemp_gap": gap_u}

dff = fred("DFF").dropna()
actual = float(dff.iloc[-1])
rstars = {"0.5": 0.5, "1.2_SEP": 1.2, "2.0_T93": 2.0}
RHO = 0.85

rows = []
for (iname, pi), (gname, g), (rname, rs) in itertools.product(infl.items(), gaps.items(), rstars.items()):
    for gc, rule in [(0.5, "taylor93"), (1.0, "balanced")]:
        r_ = rs + pi + 0.5 * (pi - 2) + gc * g
        rows.append(dict(rule=rule, inertial=False, infl=iname, gap=gname, rstar=rname, implied=r_))
        rows.append(dict(rule=rule, inertial=True, infl=iname, gap=gname, rstar=rname, implied=RHO * actual + (1 - RHO) * r_))
band = pd.DataFrame(rows)
assert len(band) == 96
lo, med, hi = band.implied.min(), band.implied.median(), band.implied.max()
width = (hi - lo) * 100
sub = band[band.rstar == "1.2_SEP"]
lo2, med2, hi2 = sub.implied.min(), sub.implied.median(), sub.implied.max()
ni = band[~band.inertial]
lo3, med3, hi3 = ni.implied.min(), ni.implied.median(), ni.implied.max()


def verdict(a, l, m, h):
    if (h - l) * 100 > 200:
        return "INCONCLUSIVE"
    if a < l:
        return "HOLDS"
    if a < m:
        return "WEAK"
    return "KILLED"


v_main = verdict(actual, lo, med, hi)
v_sep = verdict(actual, lo2, med2, hi2)
v_ni = verdict(actual, lo3, med3, hi3)
ledger("A3_h2_band_full96", "H2", f"band {lo:.2f}/{med:.2f}/{hi:.2f} width {width:.0f}bp vs actual {actual:.2f}", 96, v_main)
ledger("A3_h2_band_rstarSEP", "H2-sec", f"band {lo2:.2f}/{med2:.2f}/{hi2:.2f} vs actual {actual:.2f}", 32, v_sep)
ledger("A3_h2_band_noninertial", "H2-rob", f"band {lo3:.2f}/{med3:.2f}/{hi3:.2f} vs actual {actual:.2f}", 48, v_ni)

# ---------- Kalman TVP rule, quarterly 1990Q1+ ----------
ff = fred("FEDFUNDS").dropna()
pce = fred("PCEPILFE").dropna()
qi = ff.resample("QS").mean()
qpi = ((pce / pce.shift(12) - 1) * 100).resample("QS").mean()
qu = un.resample("QS").mean()
qn = nrou.resample("QS").last()
qgap = -2 * (qu - qn)
D = pd.concat({"i": qi, "pi": qpi, "gap": qgap}, axis=1, sort=True).dropna().loc["1990-01-01":]
y = D["i"].values
X = np.column_stack([np.ones(len(D)), D["pi"].values, D["gap"].values])
T, k = X.shape


def kfilter(params, return_states=False):
    s2e = np.exp(params[0])
    Q = np.diag(np.exp(params[1:4]))
    b = np.zeros(k)
    P = np.eye(k) * 10.0
    ll = 0.0
    out = np.zeros((T, k))
    outP = np.zeros((T, k))
    for t in range(T):
        P = P + Q
        x = X[t]
        f = x @ P @ x + s2e
        e = y[t] - x @ b
        K = P @ x / f
        b = b + K * e
        P = P - np.outer(K, x) @ P
        if t >= 4:
            ll += -0.5 * (np.log(2 * np.pi * f) + e * e / f)
        out[t] = b
        outP[t] = np.sqrt(np.diag(P))
    return (out, outP) if return_states else -ll


res = minimize(kfilter, x0=np.log([0.25, 0.01, 0.001, 0.001]), method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-4, fatol=1e-4))
st, sd = kfilter(res.x, True)
S = pd.DataFrame(st, index=D.index, columns=["a", "b_infl", "c_gap"])
S[["sd_a", "sd_b", "sd_c"]] = sd
b_now, b_now_sd, now_q = S.b_infl.iloc[-1], S.sd_b.iloc[-1], S.index[-1]
b_2025q4 = S.b_infl.loc["2025-10-01"] if pd.Timestamp("2025-10-01") in S.index else np.nan
b_hist = S.b_infl.loc["1990-01-01":"2019-10-01"].mean()
tvp_fit_now = float(X[-1] @ st[-1])
ledger("A3_h2_kalman_b_shift", "H2-tvp", f"b_t {now_q:%Y}Q{now_q.quarter} {b_now:.2f} (sd {b_now_sd:.2f}) vs 2025Q4 {b_2025q4:.2f} vs 1990-2019 mean {b_hist:.2f}", T, "descriptive")

save_parquet(band, "rule_band")
save_parquet(S.reset_index(), "kalman_tvp_rule")

lines = ["# reaction-function card", "",
         f"**VERDICT (claim: Fed is behind the curve): {v_main}** | confidence 55% (r* unobserved; latest-vintage data)", "",
         "| Rule band (low-median-high) | Actual | Priced in 12m | Inflation response b_t now vs pre-hike | Variants counted |", "|---|---|---|---|---|",
         f"| **{lo:.2f} / {med:.2f} / {hi:.2f}** (width {width:.0f}bp) | **{actual:.2f}** (DFF {dff.index[-1]:%Y-%m-%d}) | ~4.54 (Oct 2027 ZQ, A1) | {b_now:.2f} (sd {b_now_sd:.2f}) vs {b_2025q4:.2f} in 2025Q4; 1990-2019 mean {b_hist:.2f} | 96 |", "",
         f"- Secondary band, r* fixed at 1.2 (SEP longer run 3.2 minus 2): {lo2:.2f} / {med2:.2f} / {hi2:.2f} -> {v_sep}",
         f"- Non-inertial rules only (48): {lo3:.2f} / {med3:.2f} / {hi3:.2f} -> {v_ni}",
         f"- Inputs: " + "; ".join(f"{k} {v:.2f}% ({src[k]})" for k, v in infl.items()),
         f"- Gaps: CBO output gap {gap_y:+.2f}% ({gap_y_date:%Y-%m}); unemployment {u_last:.1f}% ({u_date:%Y-%m}) vs NROU {u_star:.2f} -> Okun gap {gap_u:+.2f}",
         f"- October 2026 core CPI m/m (CPILFESL, FRED): {oct_mm:.2f}% (Waller's 50bp condition was 'around 0.3 percent or even higher')",
         f"- Kalman TVP fitted rate now: {tvp_fit_now:.2f}; MLE converged: {res.success}",
         f"- Share of the 96 variants above the actual rate: {(band.implied > actual).mean():.0%}",
         "- Deviation: median CPI y/y computed from the index MEDCPIM094SFRBCLE; the pre-registered ID MEDCPIM158SFRBCLE is a monthly annualised rate, not y/y.",
         "- Pitfalls: r* moves the whole band (150bp across the three r* values); rules describe the past; inertial variants pull the band toward the actual rate by construction; ALFRED unreachable so all inputs are latest vintage."]
pd.Series(dict(lo=lo, med=med, hi=hi, width_bp=width, actual=actual, verdict=v_main, lo_sep=lo2, med_sep=med2, hi_sep=hi2,
               verdict_sep=v_sep, b_now=b_now, b_2025q4=b_2025q4, b_hist=b_hist, oct_core_cpi_mm=oct_mm, **infl, **gaps)).to_json(OUT / "A3_reaction_function.json", indent=1)
band.sort_values("implied").to_csv(OUT / "A3_rule_band_all96.csv", index=False)
(OUT / "A3_reaction_function.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
