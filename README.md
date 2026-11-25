# fed-watchers

Research archive for Fed-watching and macro work: bot reports,
quantitative studies, economic data, and international economics.

## Structure
- domestic/        US / Federal Reserve research (qualitative/, quantitative/)
- international/    non-US economies (qualitative/, quantitative/)
- data/            raw/ and processed/ + DATA_DICTIONARY.md
- lib/             shared code (data pulls, event-study harness)
- docs/            methodology and conventions
- FINDINGS.md      machine-readable summary of every study and note (see below)
- scripts/         repo tooling (check_findings.py)

## Conventions
- Store tabular data as Parquet where possible.
- Any single file over ~50 MB needs Git LFS - ask first.
- No secrets, API keys, or live trading parameters (repo is public).

## Findings
`FINDINGS.md` is the single, machine-readable summary of every research output in this repo. All findings belong to the bot **Vera** (`owner_bot: vera`).

- **One section per study or note.** The heading is the study folder or note path. The next line is `Status: complete | interim | Run: YYYY-MM-DD | Source: <RESULT.md or note path>`, followed by one ```yaml block holding a list of 3-8 findings.
- **Replace on re-run.** Re-running a study replaces its whole section; it never adds a second one. Keep each finding's `id` (`fw-<study-slug>-<short-key>`) stable across re-runs.
- **Schema.** Every field is required; use `null` (or `[]` for lists) where a field does not apply:
  `id`, `study`, `type` (quant | qual), `region` (US | country | global), `topic`, `claim`, `verdict` (supported | killed | weak | prior-only | inconclusive | interim), `confidence` (the study's own figure, quoted, e.g. `"55%"`, else null), `numbers`, `source_file`, `run_date`, `valid_until`, `owner_bot`, `links_to`, `people`.
- **What a claim is.** `claim` is the plain-English statement that was tested (max 30 words), and `verdict` is what the test found. Killed and weak findings are recorded too: "we tested it and it failed" is a finding. Claims carry no buy/sell/hold language.
- **Numbers.** Each string in `numbers` must appear verbatim in `source_file`. Do not round, convert or recompute.
- **Staleness.** Set `valid_until` for anything market-priced or time-sensitive (e.g. the next pricing re-run date). Otherwise use null.
- **Links and people.** Qualitative findings point via `links_to` to the quantitative finding that tested them, and vice versa. `people` lists only public officials named for on-record statements. Commentators and private individuals are never named; claims describe them as "one camp".

`scripts/check_findings.py` enforces all of this and runs in CI (`.github/workflows/findings.yml`) with its tests. It fails on bad yaml, missing fields or bad values, duplicate ids or sections, numbers not found verbatim, unknown links, and complete studies or notes with no section (any folder under `domestic/` or `international/` with a `RESULT.md`, or any non-template `.md` under `*/qualitative/`). It only warns when `valid_until` has passed. Run it locally with:

```bash
python3 scripts/check_findings.py && python3 -m pytest -q tests/
```

