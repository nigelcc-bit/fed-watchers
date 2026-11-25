# Data Dictionary

| file | series | description | source | frequency | units | vintage |
|------|--------|-------------|--------|-----------|-------|---------|
| processed/example.parquet | DGS10 | US 10Y yield | FRED | daily | % | 2026-11-25 |
| processed/peakhawk_fred_series.parquet | long table: series, date, value | All FRED series below, latest vintage | FRED fredgraph.csv | mixed | mixed | 2026-11-25 |
| raw/fred/ANFCI.csv | ANFCI | Chicago Fed adjusted national financial conditions index | FRED | weekly | index | 2026-11-25 |
| raw/fred/BAA.csv | BAA | Moody's Seasoned Baa corporate bond yield | FRED | monthly | % | 2026-11-25 |
| raw/fred/BAA10Y.csv | BAA10Y | Moody's Baa yield minus 10y Treasury | FRED | daily | pp | 2026-11-25 |
| raw/fred/BAMLH0A0HYM2.csv | BAMLH0A0HYM2 | ICE BofA US High Yield OAS (FRED keeps ~3 years) | FRED/ICE | daily | pp | 2026-11-25 |
| raw/fred/BAMLH0A1HYBB.csv | BAMLH0A1HYBB | ICE BofA BB US High Yield OAS | FRED/ICE | daily | pp | 2026-11-25 |
| raw/fred/BAMLH0A3HYC.csv | BAMLH0A3HYC | ICE BofA CCC & Lower US High Yield OAS | FRED/ICE | daily | pp | 2026-11-25 |
| raw/fred/CPILFESL.csv | CPILFESL | CPI less food and energy, SA (Oct 2025 missing: shutdown) | FRED/BLS | monthly | index | 2026-11-25 |
| raw/fred/DFEDTAR.csv | DFEDTAR | Fed funds target (single), 1982-09 to 2008-12 | FRED | daily | % | 2026-11-25 |
| raw/fred/DFEDTARU.csv | DFEDTARU | Fed funds target range upper limit, 2008-12+ | FRED | daily | % | 2026-11-25 |
| raw/fred/DFF.csv | DFF | Effective federal funds rate | FRED/NY Fed | daily | % | 2026-11-25 |
| raw/fred/DFII10.csv | DFII10 | 10y TIPS real yield | FRED | daily | % | 2026-11-25 |
| raw/fred/DGS10.csv | DGS10 | 10y Treasury constant maturity | FRED | daily | % | 2026-11-25 |
| raw/fred/DGS2.csv | DGS2 | 2y Treasury constant maturity | FRED | daily | % | 2026-11-25 |
| raw/fred/DRTSCILM.csv | DRTSCILM | SLOOS net % of banks tightening C&I standards, large and middle-market firms | FRED/FRB | quarterly | % | 2026-11-25 |
| raw/fred/FEDFUNDS.csv | FEDFUNDS | Effective fed funds, monthly average (pre-1982 hike proxy) | FRED | monthly | % | 2026-11-25 |
| raw/fred/GDPC1.csv | GDPC1 | Real GDP | FRED/BEA | quarterly | bn chained 2017 $ | 2026-11-25 |
| raw/fred/GDPPOT.csv | GDPPOT | CBO real potential GDP | FRED/CBO | quarterly | bn chained 2017 $ | 2026-11-25 |
| raw/fred/GS10.csv | GS10 | 10y Treasury, monthly average | FRED | monthly | % | 2026-11-25 |
| raw/fred/ICSA.csv | ICSA | Initial jobless claims, SA | FRED/DOL | weekly | count | 2026-11-25 |
| raw/fred/MEDCPIM094SFRBCLE.csv | MEDCPIM094SFRBCLE | Cleveland Fed median CPI, index level (y/y computed) | FRED/Cleveland Fed | monthly | index | 2026-11-25 |
| raw/fred/MEDCPIM158SFRBCLE.csv | MEDCPIM158SFRBCLE | Cleveland Fed median CPI, monthly % change at annual rate (pulled in error; not used) | FRED/Cleveland Fed | monthly | % ann. | 2026-11-25 |
| raw/fred/NFCI.csv | NFCI | Chicago Fed national financial conditions index | FRED | weekly | index | 2026-11-25 |
| raw/fred/NROU.csv | NROU | CBO noncyclical rate of unemployment | FRED/CBO | quarterly | % | 2026-11-25 |
| raw/fred/PCEPILFE.csv | PCEPILFE | PCE price index less food and energy | FRED/BEA | monthly | index | 2026-11-25 |
| raw/fred/PCETRIM12M159SFRBDAL.csv | PCETRIM12M159SFRBDAL | Dallas Fed trimmed mean PCE, 12-month | FRED/Dallas Fed | monthly | % | 2026-11-25 |
| raw/fred/T10YIE.csv | T10YIE | 10y breakeven inflation | FRED | daily | % | 2026-11-25 |
| raw/fred/UNRATE.csv | UNRATE | Unemployment rate | FRED/BLS | monthly | % | 2026-11-25 |
| raw/fred/VIXCLS.csv | VIXCLS | CBOE VIX close | FRED/Cboe | daily | index | 2026-11-25 |
| raw/fred/VXVCLS.csv | VXVCLS | CBOE 3-month VIX (VIX3M) close | FRED/Cboe | daily | index | 2026-11-25 |
| processed/peakhawk_yahoo_daily.parquet | ^GSPC, SPY, RSP, QQQ, CRWV | Daily close and adjusted close (raw JSON in raw/yahoo/) | Yahoo Finance chart API | daily | price | 2026-11-25 |
| raw/futures/zq_snapshot_20261125.parquet | ZQ Nov26-Dec27 | CBOT 30-day fed funds futures snapshot (bid/ask/last, delayed) | Interactive Brokers MCP | snapshot | price | 2026-11-25 ~06:15 UTC |
| raw/fomc/*.txt | n/a | FOMC statements, minutes, SEP tables, speeches (HTML stripped to text) | federalreserve.gov | n/a | text | 2026-11-25 |
| processed/peakhawk_fed_priced_path.parquet | derived | Meeting-by-meeting implied path and hike odds (step A1) | derived from ZQ | per meeting | % | 2026-11-25 |
| processed/peakhawk_fedspeak_waller.parquet | derived | Waller rubric scores with verbatim evidence (A2) | derived | per speech | score | 2026-11-25 |
| processed/peakhawk_rule_band.parquet | derived | 96 Taylor-type rule variants (A3) | derived | snapshot | % | 2026-11-25 |
| processed/peakhawk_kalman_tvp_rule.parquet | derived | Kalman-filtered TVP rule coefficients (A3) | derived | quarterly | coef | 2026-11-25 |
| processed/peakhawk_dec_scenarios.parquet | derived | December scenario table (A4) | derived | snapshot | bp | 2026-11-25 |
| processed/peakhawk_minutes_redline.parquet | derived | Oct vs Sep 2026 minutes redline scores (B) | derived | n/a | score | 2026-11-25 |
| processed/peakhawk_h3_events.parquet | derived | H3 events with outcomes O1-O3 (C) | derived | per event | mixed | 2026-11-25 |
| processed/peakhawk_h3_cards.parquet | derived | H3 beta-binomial cards (C) | derived | n/a | prob | 2026-11-25 |
| processed/peakhawk_h4_panel.parquet | derived | H4 symptom panel readings (D) | derived | snapshot | mixed | 2026-11-25 |
