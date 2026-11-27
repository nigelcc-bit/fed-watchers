# Quick lookups

Small, fast studies that answer one question with a verdict card. Each lives in `quick-lookups/YYYY-MM-DD-<slug>/`.

## Conventions
- **`PREREG.md` is committed first**, before any statistic is computed. It holds the question, the differential, the tests, the thresholds and the verdict rule, and it discloses anything seen beforehand.
- **`run.py` reruns end to end** from `data/raw/` to `data/` (small processed CSVs) and `outputs/` (charts, `trials.csv`, `results.json`).
- **`data/raw/` is gitignored.** Raw data packs stay local; only small processed files are committed.
- **`RESULT.md` opens with the verdict card:**
  ```
  VERDICT: HOLDS | WEAK | KILLED | INCONCLUSIVE | confidence NN%
  Claim: ...
  Method: ...
  Data: ... | Trials counted: N
  ```
  It then gives a headline table, the conclusion, "Would change if" with a date, the strongest rival explanation, killed results, caveats, deviations from the pre-registration, and a list of files.
- **Every test and variant is counted** in `outputs/trials.csv`. Killed results are reported as prominently as survivors.
- **Plain language, bold key numbers, no em dashes.** Add the study's section to the repo-level `FINDINGS.md`.

These conventions mirror the `useless-data` repo's quick-lookups, whose own README and `RESEARCH_PROTOCOL.md` were not readable from the session that created this folder.

## Index

| Date | Study | Question | Verdict | Confidence |
|---|---|---|---|---|
| 2026-11-27 | [token-pricing](2026-11-27-token-pricing/RESULT.md) | Are falling AI token prices a crack in the AI revenue thesis, or Jevons-style elastic demand? | KILLED (fragile: WEAK if successor models count as the same product) | 45% |
