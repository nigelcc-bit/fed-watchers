"""Step A4, fomc-preview synthesis: 2y-10y beta re-estimate and December scenario table.
d2y = k * (decision - priced Dec move) + guidance term; k = 0.6 is a pre-registered JUDGEMENT parameter (recalled*, not estimated).
d10y = beta * d2y, beta from OLS of daily d10y on d2y, 2026-01-02 to latest (FRED DGS10, DGS2)."""
import json

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import OUT, fred, ledger, save_parquet

d = pd.concat({"y10": fred("DGS10"), "y2": fred("DGS2")}, axis=1, sort=True).dropna().loc["2026-01-02":]
dd = d.diff().dropna() * 100
fit = sm.OLS(dd.y10, sm.add_constant(dd.y2)).fit(cov_type="HC1")
beta, se = fit.params["y2"], fit.bse["y2"]
ledger("A4_beta_2y10y_2026", "preview", f"beta {beta:.2f} (se {se:.2f}), daily {dd.index[0]:%Y-%m-%d} to {dd.index[-1]:%Y-%m-%d}", len(dd), f"R2 {fit.rsquared:.2f}")
ledger("A4_data_surprise_map", "preview", "not run: no consensus forecasts and no reachable release calendar (BLS/ALFRED blocked)", 0, "INCONCLUSIVE")

tab = pd.read_parquet(OUT.parent / "data" / "fed_priced_path.parquet")
priced_dec = float(tab.loc[tab.meeting == "2026-12-09", "move_bp"].iloc[0])
K = 0.6
S = [  # name, prob (judgement), decision bp, dots/guidance, guidance term on d2y (judgement, bp)
    ("Hold", 0.07, 0, "Hold with hawkish guidance; dots still show 2027 hikes", +3),
    ("+25bp, signal more (base case)", 0.78, 25, "Median 2026 dot met; 2027 median at or above 4.375; 'further firming' language", +3),
    ("+50bp", 0.15, 50, "Front-loaded; guidance that terminal is near ('enough' language) or not", -2),
]
rows = []
for name, p, dec, guide, g in S:
    d2 = K * (dec - priced_dec) + g
    rows.append(dict(scenario=name, prob_judgement=p, decision_bp=dec, dots_guidance=guide, exp_d2y_bp=round(d2, 1),
                     exp_d10y_bp=round(beta * d2, 1), channel="path" if abs(dec - priced_dec) > 5 else "path (guidance)"))
SC = pd.DataFrame(rows)
save_parquet(SC, "dec_scenarios")
json.dump(dict(beta=beta, se=se, n=len(dd), r2=fit.rsquared, k=K, priced_dec_bp=priced_dec), open(OUT / "A4_scenarios.json", "w"), indent=1)
print(f"beta {beta:.3f} se {se:.3f} n {len(dd)} R2 {fit.rsquared:.2f}; priced Dec {priced_dec:.1f}bp")
print(SC.to_string())
