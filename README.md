# fed-watchers

Research archive for Fed-watching and macro work: bot reports,
quantitative studies, economic data, and international economics.

## Structure
- domestic/        US / Federal Reserve research (qualitative/, quantitative/)
- international/    non-US economies (qualitative/, quantitative/)
- data/            raw/ and processed/ + DATA_DICTIONARY.md
- lib/             shared code (data pulls, event-study harness)
- docs/            methodology and conventions

## Conventions
- Store tabular data as Parquet where possible.
- Any single file over ~50 MB needs Git LFS - ask first.
- No secrets, API keys, or live trading parameters (repo is public).
