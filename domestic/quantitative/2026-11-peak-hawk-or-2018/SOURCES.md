# Primary-source checks (section 2.1)

Checked 2026-11-25. Raw text copies are in `data/raw/fomc/` (HTML stripped to text). Quotes are under 15 words.

| # | Claim | Status | Primary source | Date | Quote (verbatim, under 15 words) |
|---|---|---|---|---|---|
| 1 | Waller signalled openness to a 50bp hike | **VERIFIED (conditional form)** | Waller, "The Economic Outlook and Some Thoughts on Labor Market Dynamism", https://www.federalreserve.gov/newsevents/speech/waller20261110a.htm | 2026-11-10 | "I believe a 50 basis point hike in the policy rate should be considered" |
| 1a | Condition attached to it | VERIFIED | same speech | 2026-11-10 | "with core CPI inflation around 0.3 percent or even higher" |
| 1b | His base case in the same speech | VERIFIED | same speech | 2026-11-10 | "I am leaning toward supporting an increase in our policy rate of 25 basis points" |
| 1c | Stronger version: "may need to shock people" with 50bp, or 25bp plus a January signal (CNBC Squawk Box) | **UNVERIFIED (secondary only)** | CNBC article https://www.cnbc.com/2026/11/18/federal-reserve-governor-christopher-waller.html could not be fetched (host blocked from this environment). Known only from search-result summaries. | 2026-11-18 | none quoted; no transcript retrieved |
| 1d | October core CPI came in at 0.3% m/m (i.e. Waller's 50bp condition was met) | **UNVERIFIED from BLS** (bls.gov blocked); to be checked against FRED CPILFESL in step A | secondary: search summaries of the 10 Nov BLS release | 2026-11-10 | n/a |
| 1e | "After a weak equity stretch" | **Not supported by the primary text.** The 10 Nov speech conditions 50bp on CPI, not equities; it does not mention the stock market falling. It cites "a booming stock market" as supporting consumption. | same speech | 2026-11-10 | "Consumption growth was helped by a booming stock market" |
| 2 | Latest FOMC minutes | VERIFIED | Minutes of Oct 27-28, 2026, https://www.federalreserve.gov/monetarypolicy/fomcminutes20261028.htm (released 2026-11-18 per FOMC calendar page) | 2026-11-18 | "an increase of more than 25 basis points could warrant consideration" |
| 2a | Previous minutes (comparison set) | VERIFIED | Minutes of Sep 15-16, 2026, https://www.federalreserve.gov/monetarypolicy/fomcminutes20260916.htm (released 2026-10-07) | 2026-10-07 | "all participants supported raising the target range" |
| 2b | October decision: hold at 3.75-4.00%, 10-2, two dissents for +25bp | VERIFIED | Statement, https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm | 2026-10-28 | "preferred to raise the target range for the federal funds rate by 1/4" |
| 2c | September decision: +25bp to 3.75-4.00%, 12-0 | VERIFIED | Statement, https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm | 2026-09-16 | "decided to raise the target range for the federal funds rate by 1/4" |
| 3 | Who chairs the FOMC | **VERIFIED: Kevin Warsh** | Oct 2026 minutes attendance list (same URL as row 2); also Fed speeches list ("Chairman Kevin Warsh", 16 Nov 2026) | 2026-11-18 | "Kevin Warsh, Chairman" |
| 3a | FOMC Vice Chair | VERIFIED: John C. Williams | Oct 2026 minutes attendance | 2026-11-18 | "John C. Williams, Vice Chair" |
| 4 | Date of the December 2026 FOMC | **VERIFIED: December 8-9, 2026 (SEP meeting)** | FOMC calendar, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm ; also Oct minutes | checked 2026-11-25 | "next meeting of the Committee would be held on Tuesday-Wednesday, December 8-9" |
| 4a | Blackout period | Derived from skill rule (second Saturday before the meeting): starts **Sat 2026-11-28** | fomc-preview / fedspeak-score skill rule | n/a | n/a |
| 4b | 2027 meetings (for pricing splits) | VERIFIED (tentative per Fed) | FOMC calendar page | checked 2026-11-25 | "January 26-27 March 16-17 April 27-28" |
| 5 | September 2026 SEP: median end-2026 funds rate 4.1, end-2027 4.1, longer run 3.2 | VERIFIED | https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm Table 1 | 2026-09-16 | "Federal funds rate 4.1 4.1 3.9 3.6 3.2" |
| 5a | Dot distribution end-2026: 12 at 4.125, 4 at 4.375, 2 at 3.875 | VERIFIED | same, Figure 2 | 2026-09-16 | n/a (table) |
| 6 | Waller's prior stance (for fedspeak shift) | VERIFIED | Sep 3 2026 speech https://www.federalreserve.gov/newsevents/speech/waller20260903a.htm ; Oct 8 2026 speech https://www.federalreserve.gov/newsevents/speech/waller20261008a.htm | 2026-09-03, 2026-10-08 | Sep 3: "if inflation comes in hot, I would consider a rate hike"; Oct 8: "I anticipate additional hikes" |
| 7 | Waller voted with the majority to hold in October | VERIFIED | Oct statement vote list; Nov 10 speech | 2026-10-28 | "I supported the FOMC majority in holding monetary policy" |

## Context claims from the brief (section 5), status before analysis

| Claim | Status |
|---|---|
| Fed hiked 16 Sep 2026 to 3.75-4.00%, first hike since 2023 | Hike and range VERIFIED (row 2c). "First since 2023" not checked from a primary source; Waller's 8 Oct speech says policy setting was maintained "from December 2025 through September". UNVERIFIED as worded. |
| Effective fed funds 3.88% | To be pulled from FRED DFF in step A |
| December hike ~69% priced (early Nov, single source) | UNVERIFIED; superseded by this session's futures pull |
| Baa-10y 1.46pp Oct average, 1.6th percentile since 2000 | To be recomputed from FRED in step D |
| VIX 35.89 on 20 Nov; VIX/VIX3M 1.16 | To be recomputed from FRED in step D |
| SPY 715.87 vs 779.09, about -8% from 6 Oct high | To be recomputed in step D |
| Midterm-year drawdown median -19.8% | Not re-tested in this study; carried as recalled* only |
| CRWV 5y CDS ~1,067-1,195bp; 19 Nov data-centre loan auction stalled | UNVERIFIED (no CDS source reachable); live-monitor only, not used in any verdict |

## Sources that could not be reached from this environment

cnbc.com, bls.gov, newyorkfed.org (ACM term premium, HLW r*), api.stlouisfed.org / alfred.stlouisfed.org (real-time vintages), cboe.com, econ.yale.edu. Each affected step says so.
