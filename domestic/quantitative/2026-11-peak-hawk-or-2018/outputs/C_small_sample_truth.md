# small-sample-truth card: H3, the 2018 analogy

**VERDICT: KILLED** (unconditional claim) | confidence 60% (n = 13 events, pre-1982 dates are a monthly proxy)
Claim: when the Fed hikes into a >=10% S&P 500 drawdown, a sharp low (within 20 sessions) and a bounce (63-session return > 0) follow.
Events: 175 rate-increase dates (94 target, 81 pre-1982 proxy months); 35 in a >=10% drawdown; 13 events after 63-session clustering.

| Sample | Claim | Raw c/n | Posterior mean | 90% interval | Base | P(> base) | Hoeffding +/- | Events to settle | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| full 1954+ | Sharp low AND bounce (O1&O2, primary) | 5/13 | 0.40 | 0.21-0.61 | 0.45 | 0.34 | 0.34 | 353 | **KILLED** |
| full 1954+ | Low within 20 sessions (O1) | 6/13 | 0.47 | 0.26-0.67 | 0.49 | 0.41 | 0.34 | 1351 | **KILLED** |
| full 1954+ | 63-session return > 0 (O2) | 8/13 | 0.60 | 0.39-0.79 | 0.61 | 0.48 | 0.34 | 107127 | **KILLED** |
| target-only 1982-09+ | Sharp low AND bounce (O1&O2, primary) | 3/5 | 0.57 | 0.27-0.85 | 0.44 | 0.76 | 0.55 | 56 | **WEAK** |
| target-only 1982-09+ | Low within 20 sessions (O1) | 3/5 | 0.57 | 0.27-0.85 | 0.48 | 0.69 | 0.55 | 104 | **KILLED** |
| target-only 1982-09+ | 63-session return > 0 (O2) | 4/5 | 0.71 | 0.42-0.94 | 0.61 | 0.74 | 0.55 | 39 | **KILLED** |

Skeptical prior Beta(8 p0, 8 (1-p0)) posterior means: full 1954+ Sharp low AND bounce: 0.41; full 1954+ Low within 20 sessions: 0.47; full 1954+ 63-session return > 0: 0.61; target-only 1982-09+ Sharp low AND bounce: 0.50; target-only 1982-09+ Low within 20 sessions: 0.53; target-only 1982-09+ 63-session return > 0: 0.69

**Key split: bounce (O1&O2) conditional on a Fed reversal within 92 days**

| Sample | With reversal | Without reversal | P(rate with > rate without) | 90% interval of difference |
|---|---|---|---|---|
| full 1954+ | 4/5 (post 0.71) | 1/8 (post 0.20) | **0.99** | +0.15 to +0.81 |
| target-only 1982-09+ | 3/3 (post 0.80) | 0/2 (post 0.25) | **0.97** | +0.08 to +0.90 |

Pitfalls: events are few and the pre-1982 hike dates are monthly-average proxies (dated at the month start, so the drawdown filter has mild look-ahead within the month); base-rate days overlap heavily; the 1994+ hawkish-statement extension was not run (pre-registered). A reversal is only known after the fact, so the split is not a forecast.
