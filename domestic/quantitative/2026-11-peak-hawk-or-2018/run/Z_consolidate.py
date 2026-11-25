"""Consolidate cached raw pulls into Parquet under data/processed/ (long format, one row per series-date)."""
import pandas as pd

from common import PROC, RAW, fred, yahoo

ids = sorted(p.stem for p in (RAW / "fred").glob("*.csv"))
long = pd.concat([fred(s).dropna().rename("value").reset_index().assign(series=s) for s in ids])
long[["series", "date", "value"]].to_parquet(PROC / "peakhawk_fred_series.parquet", index=False)
syms = {"IDX_GSPC": "^GSPC", "RSP": "RSP", "SPY": "SPY", "QQQ": "QQQ", "CRWV": "CRWV"}
yl = pd.concat([yahoo(v).reset_index().assign(symbol=v) for v in syms.values()])
yl[["symbol", "date", "close", "adjclose"]].to_parquet(PROC / "peakhawk_yahoo_daily.parquet", index=False)
print(long.groupby("series").date.agg(["min", "max", "count"]).to_string())
print(yl.groupby("symbol").date.agg(["min", "max", "count"]).to_string())
