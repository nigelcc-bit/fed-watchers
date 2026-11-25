# reaction-function card

**VERDICT (claim: Fed is behind the curve): INCONCLUSIVE** | confidence 55% (r* unobserved; latest-vintage data)

| Rule band (low-median-high) | Actual | Priced in 12m | Inflation response b_t now vs pre-hike | Variants counted |
|---|---|---|---|---|
| **3.18 / 4.20 / 7.38** (width 420bp) | **3.88** (DFF 2026-11-23) | ~4.54 (Oct 2027 ZQ, A1) | 0.66 (sd 0.10) vs 0.84 in 2025Q4; 1990-2019 mean 0.40 | 96 |

- Secondary band, r* fixed at 1.2 (SEP longer run 3.2 minus 2): 3.88 / 4.19 / 6.58 -> INCONCLUSIVE
- Non-inertial rules only (48): 3.18 / 5.09 / 7.38 -> INCONCLUSIVE
- Inputs: core_pce 3.12% (PCEPILFE 2026-09); core_cpi 2.57% (CPILFESL 2026-09); trimmed_pce 2.26% (PCETRIM12M159SFRBDAL 2026-09); median_cpi 2.80% (MEDCPIM094SFRBCLE 2026-10)
- Gaps: CBO output gap +1.70% (2026-07); unemployment 4.1% (2026-10) vs NROU 4.39 -> Okun gap +0.58
- October 2026 core CPI m/m (CPILFESL, FRED): 0.30% (Waller's 50bp condition was 'around 0.3 percent or even higher')
- Kalman TVP fitted rate now: 3.67; MLE converged: True
- Share of the 96 variants above the actual rate: 90%
- Deviation: median CPI y/y computed from the index MEDCPIM094SFRBCLE; the pre-registered ID MEDCPIM158SFRBCLE is a monthly annualised rate, not y/y.
- Pitfalls: r* moves the whole band (150bp across the three r* values); rules describe the past; inertial variants pull the band toward the actual rate by construction; ALFRED unreachable so all inputs are latest vintage.
