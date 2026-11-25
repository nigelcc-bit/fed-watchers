"""Step A2, fedspeak-score: Waller now (10 Nov 2026) vs his prior (3 Sep, 8 Oct 2026).
Scores are judgement on the pre-registered 4-item rubric (-2..+2 each). Evidence phrases are verbatim from
data/raw/fomc/waller*.txt. Weight 0.5 for a governor (skill default, judgement)."""
import pandas as pd

from common import OUT, ledger, save_parquet

S = [  # speech, item, score, evidence (verbatim, short)
    ("2026-09-03", "inflation", 1, "if inflation comes in hot, I would consider a rate hike"),
    ("2026-09-03", "labour", 0, "real side of the economy as solid"),
    ("2026-09-03", "policy_path", 1, "it may not take much acceleration in inflation to nudge me"),
    ("2026-09-03", "risks", 0, "only slightly restricting aggregate demand"),
    ("2026-10-08", "inflation", 2, "obviously higher than we want, above our target"),
    ("2026-10-08", "labour", 0, "the labor market continued to be solid and stable"),
    ("2026-10-08", "policy_path", 1, "I anticipate additional hikes"),
    ("2026-10-08", "risks", 1, "will lead consumers, investors, and price-setting businesses to revise up"),
    ("2026-11-10", "inflation", 2, "Let's just say it. September's inflation data were bad."),
    ("2026-11-10", "labour", 0, "I see the labor market as stable"),
    ("2026-11-10", "policy_path", 2, "a 50 basis point hike in the policy rate should be considered"),
    ("2026-11-10", "risks", 2, "could be larger than previously though and persist well into 2027"),
]
df = pd.DataFrame(S, columns=["speech", "item", "score", "evidence"])
tot = df.groupby("speech")["score"].sum()
prior = (tot["2026-09-03"] + tot["2026-10-08"]) / 2
now = tot["2026-11-10"]
shift = now - prior
w = 0.5
wshift = w * shift

# Robustness rows (pre-registered): prior = Oct 8 only; Nov 10 path scored +1 (his stated base case is 25bp);
# CNBC 18 Nov (secondary only, UNVERIFIED) path +2 -> same as headline.
rob = {
    "prior=Oct8 only": now - tot["2026-10-08"],
    "Nov10 path scored +1 (base case 25bp)": (now - 1) - prior,
    "both of the above": (now - 1) - tot["2026-10-08"],
}
# Versus pricing: Dec priced ~99% +25, ~1% +50 (A1). Floating 50bp goes beyond pricing.
beyond_pricing = True
label = "HAWKISH SURPRISE" if (wshift >= 1 and beyond_pricing) else ("IN LINE" if shift < 1 else "HAWKISH SHIFT (not beyond pricing)")

ledger("A2_h1a_waller_shift", "H1a", f"raw shift {shift:+.1f} (now {now} vs prior {prior}); weighted {wshift:+.2f}", 3, "shift" if shift >= 1 else "no shift")
for k, v in rob.items():
    ledger(f"A2_h1a_rob_{k[:20].replace(' ', '_')}", "H1a-rob", f"raw shift {v:+.1f} ({k})", 3, "shift" if v >= 1 else "no shift")

save_parquet(df, "fedspeak_waller")
lines = ["# fedspeak-score card: Governor Waller (voter in 2026)", "",
         f"**VERDICT: {label}** | confidence 70% (judgement scoring of primary texts; Q&A at CNBC not used)", "",
         "| Speaker (role, voter?) | Score now | Prior | Shift | Weighted shift | Fits pricing? |", "|---|---|---|---|---|---|",
         f"| Waller (governor, votes) | {now:+d} (10 Nov) | {prior:+.1f} (avg 3 Sep, 8 Oct) | **{shift:+.1f}** | {wshift:+.2f} | No: floats 50bp vs ~1% priced for Dec |", "",
         "| Speech | Inflation | Labour | Path | Risks | Sum |", "|---|---|---|---|---|---|"]
for sp in ["2026-09-03", "2026-10-08", "2026-11-10"]:
    r = df[df.speech == sp].set_index("item")["score"]
    lines.append(f"| {sp} | {r.inflation:+d} | {r.labour:+d} | {r.policy_path:+d} | {r.risks:+d} | {tot[sp]:+d} |")
lines += ["", "Robustness (raw shift):"] + [f"- {k}: {v:+.1f} ({'shift' if v >= 1 else 'no shift'})" for k, v in rob.items()]
lines += ["", "Evidence (verbatim):"] + [f"- {r.speech} {r.item}: \"{r.evidence}\"" for r in df.itertuples()]
lines += ["", "Notes: the 50bp remark is conditional on Oct core CPI near 0.3% or higher; his stated base case was +25bp. "
          "The speech was given 10 Nov, before the blackout (starts 28 Nov). The 18 Nov CNBC interview is UNVERIFIED (host unreachable)."]
(OUT / "A2_fedspeak_score.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
