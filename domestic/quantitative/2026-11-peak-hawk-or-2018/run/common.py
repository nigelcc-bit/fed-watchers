"""Shared helpers for the peak-hawk study. Raw pulls go to <repo>/data/raw/, processed Parquet to
<repo>/data/processed/ and the study's data/ folder. Every test appends a row to outputs/ledger.csv."""
import csv
import datetime as dt
import io
import subprocess
import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[2]
RAW = REPO / "data" / "raw"
PROC = REPO / "data" / "processed"
OUT = STUDY / "outputs"
SDATA = STUDY / "data"
for p in (RAW / "fred", RAW / "yahoo", PROC, OUT, SDATA):
    p.mkdir(parents=True, exist_ok=True)

LEDGER = OUT / "ledger.csv"
UA = {"User-Agent": "Mozilla/5.0 (research script)"}


def _get(url, tries=4, ua=False):
    """Fetch with curl (respects the environment's proxy and CA settings)."""
    for i in range(tries):
        cmd = ["curl", "-sfL", "--http1.1", "-m", "90"] + (["-A", UA["User-Agent"]] if ua else []) + [url]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
        if i == tries - 1:
            raise RuntimeError(f"fetch failed ({r.returncode}): {url}")
        time.sleep(2 ** (i + 1))


def fred(series_id, refresh=False):
    """Latest-vintage FRED series via fredgraph.csv (no API key). Cached under data/raw/fred/."""
    f = RAW / "fred" / f"{series_id}.csv"
    if refresh or not f.exists():
        f.write_bytes(_get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"))
    df = pd.read_csv(f)
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    return df.set_index("date")[series_id]


def yahoo(symbol, start="1950-01-01", refresh=False):
    """Daily closes from Yahoo chart API. Cached under data/raw/yahoo/."""
    safe = symbol.replace("^", "IDX_")
    f = RAW / "yahoo" / f"{safe}.json"
    if refresh or not f.exists():
        p1 = int(pd.Timestamp(start).timestamp())
        p2 = int(time.time())
        url = (f"https://query2.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(symbol)}"
               f"?period1={p1}&period2={p2}&interval=1d&events=history")
        f.write_bytes(_get(url, ua=True))
    j = json.loads(f.read_text())["chart"]["result"][0]
    ts = pd.to_datetime(j["timestamp"], unit="s").normalize()
    q = j["indicators"]["quote"][0]
    adj = j["indicators"].get("adjclose", [{}])[0].get("adjclose")
    df = pd.DataFrame({"close": q["close"], "adjclose": adj if adj else q["close"]}, index=ts)
    df = df[~df.index.duplicated(keep="last")].dropna(subset=["close"])
    df.index.name = "date"
    return df


def ledger(test_id, hypothesis, statistic, n, p_or_posterior):
    new = not LEDGER.exists()
    rows = []
    if not new:
        with open(LEDGER) as fh:
            rows = [r for r in csv.DictReader(fh) if r["test_id"] != test_id]
    rows.append(dict(test_id=test_id, hypothesis=hypothesis, statistic=statistic, n=n,
                     p_or_posterior=p_or_posterior,
                     timestamp=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    with open(LEDGER, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "hypothesis", "statistic", "n", "p_or_posterior", "timestamp"])
        w.writeheader()
        w.writerows(rows)


def save_parquet(df, name, study_copy=True):
    df.to_parquet(PROC / f"peakhawk_{name}.parquet")
    if study_copy:
        df.to_parquet(SDATA / f"{name}.parquet")
