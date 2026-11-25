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
`FINDINGS.md` is the single, machine-readable summary of every research output in this repo. Owners are bot IDs, never names: every fed-watchers finding has `owner: fx-115`.

- **One section per study or note.** The heading is the study folder or note path. The next line is `Status: complete | interim | Run: YYYY-MM-DD | Source: <RESULT.md or note path>`, followed by one ```yaml block holding a list of 3-8 findings.
- **Replace on re-run.** Re-running a study replaces its whole section; it never adds a second one. Keep each finding's `id` (`fw-<study-slug>-<short-key>`) stable across re-runs.
- **Schema.** Every field is required; use `null` (or `[]` for lists) where a field does not apply:
  `id`, `study`, `type` (quant | qual), `region` (US | country | global), `topic`, `hypothesis`, `verdict` (supported | killed | weak | prior-only | inconclusive | interim), `finding`, `key_stats`, `confidence` (the study's own figure, quoted, e.g. `"55%"`, else null), `numbers`, `source_file`, `run_date`, `valid_until`, `owner` (`fx-NNN` or `cx-NNN`), `links_to`, `people`.
- **Hypothesis, verdict, finding.** These three are read together and must make sense aloud.
  - `hypothesis` is the statement that was tested, phrased positively (max 30 words). For a qualitative note it is the camp's argument.
  - `verdict` always refers to the hypothesis.
  - `finding` is one plain-English sentence (max 30 words) saying what was actually concluded, written for a non-expert. It is the only text a consumer will speak. For a qualitative note it says what the linked quantitative test concluded about the argument.
  - Killed and weak results are recorded too: "we tested it and it failed" is a finding. Nothing carries buy/sell/hold language.
- **Key stats.** `key_stats` holds 1-3 short, labelled, speakable stats, such as "about 41bp of a possible 50bp priced by January" or "5 of 13 past cases". A bare number like "+2" or "0.40" with no label is not allowed.
- **Numbers.** Each string in `numbers` must appear verbatim in `source_file`; do not round, convert or recompute. Every numeric token in `finding` and `key_stats` (digits with any decimals and a %, bp or pp unit) must also appear as a token in `numbers`. A leading +/- sign is ignored, so "139bp" matches "+139bp". Matching is by whole token, so "9" does not match "40.9bp".
- **Staleness.** Set `valid_until` for anything market-priced or time-sensitive (e.g. the next pricing re-run date). Otherwise use null.
- **Links and people.** Qualitative findings point via `links_to` to the quantitative finding that tested them, and vice versa. `people` lists only public officials named for on-record statements. Commentators and private individuals are never named; hypotheses and findings describe them as "one camp".

`scripts/check_findings.py` enforces all of this and runs in CI (`.github/workflows/findings.yml`) with its tests. It fails on bad yaml, missing fields or bad values (including an owner that is not a bot ID, a hypothesis or finding over 30 words, or unlabelled key stats), duplicate ids or sections, numbers not found verbatim, numbers spoken in `finding` or `key_stats` that are missing from `numbers`, unknown links, and complete studies or notes with no section (any folder under `domestic/` or `international/` with a `RESULT.md`, or any non-template `.md` under `*/qualitative/`). It only warns when `valid_until` has passed. Run it locally with:

```bash
python3 scripts/check_findings.py && python3 -m pytest -q tests/
```

