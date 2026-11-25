# Pre-registration: Peak hawk or 2018 replay?

Written 2026-11-25, committed before any H2/H3/H4 outcome data is pulled or any result is computed.
Folder: `domestic/quantitative/2026-11-peak-hawk-or-2018/`.

## 0. Disclosure of what was seen before this file was written

Honest record, so a reader can judge contamination:

1. **Primary documents read in full**: Sep and Oct 2026 FOMC statements and minutes, Sep 2026 SEP, Waller speeches of 3 Sep, 8 Oct, 10 Nov and 20 Nov 2026 (see `SOURCES.md`). These are H1 inputs; reading them is required to define the redline. I have therefore already formed an informal impression of the minutes (Oct adds "more than 25 basis points could warrant consideration" and two hawkish dissents; Sep was a unanimous hike). The H1 scoring rubric below is fixed regardless.
2. **Data-availability probes**: one `tail -2` of FRED DFF, SP500, BAA10Y, VIXCLS, DFEDTARU, NFCI (latest two prints: DFF 3.88, SP500 7237 on 23 Nov, BAA10Y 1.59, VIX 26.62, NFCI -0.478). No history, percentiles or changes were computed.
3. **Fed funds futures snapshot** (IBKR, delayed, 25 Nov 2026 ~06:15 UTC) pulled to confirm fed-priced can run. I did a rough mental split and saw that the December contract implies close to a full 25bp hike and that cumulative pricing through January is somewhere around 40bp. The H1 pricing threshold below is therefore tied to **what Waller floated (50bp by the January meeting)**, not chosen from the data, and a sensitivity row is pre-registered.
4. Nothing about historical S&P 500 behaviour around FOMC hikes (H3) has been pulled. Nothing about spread history, NFCI history, or Taylor-rule inputs (H2, H4) has been pulled.

## 1. Skills and routes

| Step | Skill | Route |
|---|---|---|
| A | fomc-preview (with fed-priced, fedspeak-score, reaction-function, data-surprise-map) | Installed; invoked via Skill tool; sub-skill SKILL.md files read from the installed skill directory |
| B | statement-delta | Installed; invoked via Skill tool |
| C | small-sample-truth | Installed; invoked via Skill tool |
| D | symptom-evaluation | Installed; invoked via Skill tool (uses its `scripts/panel_score.py`) |
| Later | fomc-reaction | After 9 Dec 2026, separate commit |

## 2. Hypotheses, tests and thresholds

### H1 Peak hawkishness

Claim: the Waller remarks and the October minutes are a hawkish shift relative to (a) Waller's own prior stance and (b) market pricing, and they mark the peak.

**H1a Waller shift (fedspeak-score).**
- Prior stance = average of Waller's 3 Sep and 8 Oct 2026 speeches. Now = 10 Nov 2026 speech (primary). The 18 Nov CNBC interview is secondary-only and is scored in a robustness row, never in the headline.
- Score each speech on four items, -2 (dovish) to +2 (hawkish): inflation assessment, labour market, policy path signal, balance of risks. Sum ranges -8 to +8.
- Shift = sum(now) - sum(prior). Weight for a governor = 0.5 (skill default, a judgement). Weighted shift = 0.5 x shift.
- **"Is a shift" if raw shift >= +1.** HAWKISH SURPRISE label (skill rule) if weighted shift >= 1 (raw >= 2) and it goes beyond pricing.

**H1b Pricing (fed-priced).**
- What Waller floated = 50bp of cumulative tightening by the 27 Jan 2027 meeting (either 50bp in Dec, or 25bp plus a January follow-up).
- **"Pricing already reflects as much or more" if cumulative priced hikes through the January 2027 meeting >= 50bp.** Sensitivity row: >= 45bp (allowing ~5bp futures risk premium). Both reported.
- Method: ZQ futures, r = 100 - price, meeting-month split per the skill; for late-month meetings (Dec 9 is day 9 of 31, usable; Jan 27 is day 27 of 31, use the February contract instead).

**H1c Minutes redline (statement-delta).**
- Redline Oct 2026 minutes against Sep 2026 minutes on these aligned sections: inflation assessment, inflation expectations, labour market, financial conditions, policy decision discussion, outlook/guidance, votes and dissents, financial-stability discussion (new in Oct; scored as an insertion).
- Each change scored -2 to +2. Net score = sum. Robustness: a mechanical keyword count (hawkish vs dovish terms, list fixed in `run/B_statement_delta.py` before it is run on the text) as a second scorer.
- Bands: **net <= -2: net dovish vs Sep. -1 to +1: flat. >= +2: more hawkish than Sep.**

**H1 verdict mapping (for the claim "this is peak hawkishness").**
- HOLDS: H1a shift yes AND H1b priced >= 50bp AND H1c flat (-1 to +1).
- WEAK: H1a shift yes AND exactly one of (H1b met, H1c flat or dovish) holds.
- KILLED: H1a not a shift; OR H1c net dovish (<= -2) [prompt's kill rule: if the minutes are net dovish the "hawkish shift" premise fails]; OR (H1b not met AND H1c >= +2), meaning hawkish room remains and the minutes are still escalating, i.e. not a peak.
- Confidence capped at 60% because H1c is a judgement score.

### H2 Insufficient restriction (reaction-function)

- Rule family (all counted): Taylor 1993 (gap coef 0.5), balanced approach (gap coef 1.0), and inertial versions of both (rho = 0.85, lagged actual rate) = 4 rule forms.
- Inflation measures (4): core PCE y/y (PCEPILFE), core CPI y/y (CPILFESL), Dallas Fed trimmed-mean PCE 12m (PCETRIM12M159SFRBDAL), Cleveland Fed median CPI y/y (MEDCPIM158SFRBCLE). Where a 12-month change is missing for Oct 2026 (no Oct 2025 CPI collection), use the latest available month and say so.
- Gap measures (2): CBO output gap (GDPC1 vs GDPPOT, %), and unemployment gap via Okun: -2 x (UNRATE - NROU).
- r* (3): 0.5, 1.2 (Sep 2026 SEP longer-run median 3.2 minus 2), 2.0 (Taylor 1993). NY Fed HLW is unreachable from this environment; flagged.
- Total variants: 4 x 4 x 2 x 3 = **96**. Band = min, median, max across all 96.
- Actual rate = latest effective fed funds (DFF). Priced in 12 months = from fed-priced (Nov 2027 contract, or nearest).
- Kalman TVP: i_t = a_t + b_t pi_t + c_t gap_t + e_t, coefficients random walks, filtered (not smoothed), quarterly 1990Q1 onward, core PCE and Okun unemployment gap. Report b_t now vs 2025Q4 (pre-hike) and vs its 1990-2019 mean. State-noise variances by MLE.
- **Verdict (claim: the Fed is behind the curve): HOLDS if actual < band low; WEAK if band low <= actual < band median; KILLED if actual >= band median; INCONCLUSIVE if band width (max - min) > 200bp.** Because the r* range alone spans 150bp, INCONCLUSIVE is a live possibility; a secondary band with r* fixed at 1.2 is pre-registered and reported alongside, but the headline verdict follows the full-family rule.
- Real-time caveat: ALFRED is unreachable, so all inputs are latest-vintage. Flagged as look-ahead for any historical comparison.

### H3 The 2018 analogy (small-sample-truth)

- Claim: "When the Fed tightens into an equity drawdown, a sharp low and strong bounce follow."
- **Event class (fixed now):** a date on which the Fed raised its federal funds target, while the S&P 500 close on that date is >= 10% below its prior 252-session high close (computed from closes up to and including that date only). Cluster: qualifying dates within 63 sessions of the previous qualifying date are merged into one event, dated at the first.
- Rate-increase dates: FRED DFEDTAR (1982-09-27 to 2008-12-15) and DFEDTARU (2008-12-16 onward): any day the target rises. Before 1982-09 there is no target series on FRED; for 1954-1982 use increases in the daily effective rate's **monthly** average (FEDFUNDS) of >= 25bp, dated at the first trading day of that month, as a coarse proxy. Results reported for the full sample and for the 1982+ target-only subsample separately; the pre-1982 proxy is flagged as low quality.
- The "hawkish statement/minutes" extension from 1994 is **not run**: scoring every statement since 1994 is out of scope for this session. Stated here so it is not added later.
- S&P 500 daily closes: Yahoo Finance ^GSPC. Index levels are not revised; point-in-time is not an issue for prices.
- **Outcomes per event:**
  - O1 sharp low: the minimum close over sessions [t, t+63] falls within [t, t+20]. (yes/no)
  - O2 bounce: 63-session forward price return > 0. (yes/no)
  - O3 reversal: a target cut within 92 calendar days; for events from 1994 on, also yes if the next statement within 92 days explicitly signals a pause (checked from federalreserve.gov text, recorded with quote). Pre-1994: cut-only, flagged.
  - Primary claim outcome: **O1 AND O2** jointly.
- **Base rates** (reference class): all trading days 1955+ (or the subsample start) where the S&P 500 is >= 10% below its 252-session high, outcomes computed the same way (O1, O2, O1&O2). These overlap heavily; they are a reference, not independent trials.
- **Method:** uniform prior Beta(1,1) headline; skeptical prior Beta(m p0, m(1-p0)) with m = 8 as robustness. 90% credible intervals; Hoeffding half-width with delta = 0.10; P(rate > base); events needed to settle.
- **Verdict (small-sample-truth rules):** HOLDS if the 90% interval excludes the base rate (above); WEAK if P(rate > base) in [0.75, 0.95]; KILLED if the interval straddles the base rate and the raw rate is the main evidence; **INCONCLUSIVE if n < 5.**
- **Key split:** tabulate O1&O2 conditional on O3 yes/no. Dec 2018 reversal checked from the 30 Jan 2019 FOMC statement text, not memory.

### H4 Wealth channel and credit (symptom-evaluation)

- **Symptom (restated):** the S&P 500 fell from its 2026 high while the Fed leaned hawkish (Sep hike, Dec hike priced). Window: 6 Oct 2026 (the high cited in the brief; to be verified) to the latest close.
- **Differential (written before the panel):**
  - (a) Transmitting as intended: broad tightening of financial conditions via the wealth channel, credit confirming.
  - (b) Not transmitting: financial conditions still loose; the equity dip is not a policy-tightening signal.
  - (c) Pocket stress: AI / data-centre / levered credit is stressed but aggregate spreads mask it.
  - (d) Artefact: monthly-average lags, index composition (cap-weight concentration), or a VIX spike that is a price echo.
  - (e) Benign / non-policy: an AI earnings and capex repricing that would have happened at any policy rate (included as the benign branch).
- **Panel** (max two per channel; ratios, spreads or changes only):
  - P: S&P 500 drawdown from 252-session high; equal-weight vs cap-weight (RSP/SPY) relative performance since 6 Oct (composition test).
  - C: Baa-10y (BAA10Y) change since 6 Oct and percentile since 2000; CCC minus BB OAS change since 6 Oct (two-population spread). HY OAS reported as context.
  - X: real 10y (DFII10) vs 10y breakeven (T10YIE) change since 6 Oct; 60-session equity-bond correlation (S&P returns vs 10y yield changes).
  - S/F composite: Chicago Fed NFCI level and change since early Oct (and ANFCI). Classified C/F for the independence rule; flagged as a composite.
  - R (non-price): SLOOS net share of banks tightening C&I standards to large and middle-market firms (DRTSCILM), latest vs prior quarter. Initial claims 4-week average change (ICSA) as second R reading.
  - Live monitor only (no verdict weight): CRWV vs QQQ relative performance since 6 Oct; CRWV CDS and the 19 Nov data-centre loan auction remain UNVERIFIED.
- **Pre-registered thresholds:**
  - Credit confirming (aggregate): BAA10Y up >= 25bp since 6 Oct, or HY OAS up >= 75bp.
  - Aggregate loose: BAA10Y below its 2000+ 25th percentile, and NFCI < 0.
  - Conditions tightening: NFCI up >= +0.10 since the first October reading.
  - Pocket: CCC-BB widening >= 100bp since 6 Oct while the aggregate is NOT confirming.
  - Composition artefact: equal-weight drawdown less than half the cap-weight drawdown.
- **Discriminators:** (a) vs (b): NFCI change plus BAA10Y change (both past thresholds = a; neither = b). (a/b) vs (c): CCC-BB change with aggregate not confirming. (d): RSP/SPY and daily vs monthly BAA agreement.
- **H4 verdict (claim: "tightening is transmitting and credit confirms the equity weakness"):** HOLDS if (a) leads with credit confirming and the independence rule satisfied; WEAK if (c) leads (stress real but pocketed); KILLED if (b) or (e) leads; INCONCLUSIVE if the panel fails the independence rule or (d) leads. Confidence follows the skill rubric (never above "Supported" on one observation date).

## 3. December FOMC preview (step A synthesis)

- Priced: Dec, Jan, Mar, Apr meetings, hold/25/50 odds, terminal; vs Sep SEP medians.
- Scenario table: hold, 25bp, 50bp. Expected d2y = k x (decision minus priced Dec move) + guidance effect, with k = 0.6 a **judgement parameter (recalled*, not estimated)**; d10y via the 2y-10y beta re-estimated by OLS on daily changes 2026-01-02 to latest. S&P reaction stated qualitatively from H3 and H4 readings, not as a number.
- Probabilities in the scenario table are judgement.
- Conditional reads and kill conditions written in RESULT.md before 8 Dec and scored after 9 Dec by fomc-reaction. RESULT.md original verdicts are not edited afterwards.

## 4. data-surprise-map

- Consensus forecasts are not available; release dates require ALFRED or BLS (both unreachable). If release dates cannot be obtained from a reachable primary source, data-surprise-map is reported as **not run (INCONCLUSIVE: no consensus, no release calendar)** rather than approximated. A one-line statement of the October CPI print (from FRED CPILFESL) is given instead.

## 5. Ledger

Every test, variant and threshold check is logged in `outputs/ledger.csv` with columns test_id, hypothesis, statistic, n, p_or_posterior, timestamp. Killed results are reported with the same prominence as survivors.

## 6. What would make me revise this plan (and how)

Any deviation after this commit is logged in RESULT.md under "Deviations from pre-registration" with the reason. No threshold above is changed after seeing results.
