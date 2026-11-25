"""Step A1, fed-priced: meeting-by-meeting implied path from CBOT 30-day fed funds futures (ZQ).
Input: data/raw/futures/zq_snapshot_20261125.json (IBKR MCP snapshot, delayed quotes; mid of bid/ask).
Method per the fed-priced skill: r = 100 - price; meeting-month split; next-month contract for late meetings."""
import json

import pandas as pd

from common import RAW, OUT, fred, ledger, save_parquet

snap = json.loads((RAW / "futures" / "zq_snapshot_20261125.json").read_text())
fut = pd.DataFrame(snap["rows"]).set_index("contract_month")
fut["mid"] = (fut["bid"] + fut["ask"]) / 2
fut["rate"] = 100 - fut["mid"]
stamp = max(fut["ts_utc"])

dff = fred("DFF")
effr = float(dff.dropna().iloc[-1])
effr_date = dff.dropna().index[-1].date()
upper = float(fred("DFEDTARU").dropna().iloc[-1])
mid_target = upper - 0.125
spread_bp = (effr - mid_target) * 100

r = fut["rate"].to_dict()
rows = []
# Dec 9 2026: day 9 of 31, new rate effective Dec 10 -> 9 days at r_pre
r_pre = r["202611"]  # Nov average = current effective rate (no Nov meeting)
dec_post = (r["202612"] * 31 - r_pre * 9) / 22
# Jan 27 2027: late in month (27/31) -> use Feb contract (no Feb meeting) as post-Jan rate
jan_post = r["202702"]
# Mar 17 2027: day 17 of 31 -> split March, r_pre = Feb average
mar_post = (r["202703"] * 31 - r["202702"] * 17) / 14
# Apr 28 2027: late (28/30) -> May contract (no May meeting)
apr_post = r["202705"]

path = [("2026-12-09", r_pre, dec_post), ("2027-01-27", dec_post, jan_post),
        ("2027-03-17", jan_post, mar_post), ("2027-04-28", mar_post, apr_post)]


def probs(move):
    steps = move / 0.25
    if steps <= 0:
        return dict(p_cut=min(1, -steps), p_hold=1 - min(1, -steps), p_25=0.0, p_50=0.0)
    if steps <= 1:
        return dict(p_cut=0.0, p_hold=1 - steps, p_25=steps, p_50=0.0)
    return dict(p_cut=0.0, p_hold=0.0, p_25=2 - steps, p_50=steps - 1)


base = r_pre
for m, pre, post in path:
    mv = post - pre
    rows.append(dict(meeting=m, rate_pre=pre, implied_rate=post, move_bp=mv * 100,
                     cumulative_bp=(post - base) * 100, **probs(mv)))
tab = pd.DataFrame(rows)
end2026 = dec_post
end2027 = r["202712"]
terminal = max(fut["rate"])
terminal_month = fut["rate"].idxmax()

sep = {"2026": 4.125, "2027": 4.125}  # Sep 2026 SEP median midpoints (Table 1 / Figure 2)
gap26 = (end2026 - spread_bp / 100 - sep["2026"]) * 100
gap27 = (end2027 - spread_bp / 100 - sep["2027"]) * 100

cum_jan = tab.loc[tab.meeting == "2027-01-27", "cumulative_bp"].iloc[0]
h1b_50 = cum_jan >= 50
h1b_45 = cum_jan >= 45
ledger("A1_h1b_cum_jan_ge50", "H1b", f"cum priced through Jan27 = {cum_jan:.1f}bp vs 50bp floated", 1, "met" if h1b_50 else "not met")
ledger("A1_h1b_cum_jan_ge45", "H1b-sens", f"cum priced through Jan27 = {cum_jan:.1f}bp vs 45bp", 1, "met" if h1b_45 else "not met")
ledger("A1_gap_vs_dots_2026", "fed-priced", f"end-2026 implied minus SEP median = {gap26:+.1f}bp", 1, "n/a")
ledger("A1_gap_vs_dots_2027", "fed-priced", f"end-2027 implied minus SEP median = {gap27:+.1f}bp", 1, "n/a")

save_parquet(tab, "fed_priced_path")
fut.reset_index().to_parquet(RAW / "futures" / "zq_snapshot_20261125.parquet")

lines = [f"# fed-priced card (data stamp: IBKR delayed ZQ quotes, latest {stamp}; EFFR {effr:.2f} on {effr_date})", "",
         f"Target range upper {upper:.2f}; EFFR minus target midpoint = {spread_bp:+.1f}bp (adjusted in dot gaps).", "",
         "| Meeting | P(cut) | P(hold) | P(+25) | P(+50) | Implied rate | Cumulative bp |", "|---|---|---|---|---|---|---|"]
for _, x in tab.iterrows():
    lines.append(f"| {x.meeting} | {x.p_cut:.0%} | {x.p_hold:.0%} | {x.p_25:.0%} | {x.p_50:.0%} | {x.implied_rate:.3f} | {x.cumulative_bp:+.1f} |")
lines += ["", f"- End-2026 implied {end2026:.3f} vs SEP median 4.125 (EFFR-adjusted gap {gap26:+.1f}bp)",
          f"- End-2027 implied (Dec 2027 contract average) {end2027:.3f} vs SEP median 4.125 (gap {gap27:+.1f}bp)",
          f"- Terminal (max monthly average on the curve): {terminal:.3f} in {terminal_month}",
          f"- Cumulative priced through the 27 Jan 2027 meeting: **{cum_jan:.1f}bp** (H1b threshold 50bp: {'met' if h1b_50 else 'NOT met'}; 45bp sensitivity: {'met' if h1b_45 else 'NOT met'})",
          "- Pitfalls: futures embed a risk premium; Dec split uses 9 pre-meeting days; quotes are delayed and go stale. Re-run on the day."]
(OUT / "A1_fed_priced.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
