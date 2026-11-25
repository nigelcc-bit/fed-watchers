"""Step C, small-sample-truth: honest odds on the 2018 analogy (H3).
Event: a Fed rate-increase date while the S&P 500 close is >= 10% below its 252-session high (closes up to that date).
Clustered within 63 sessions (first date kept). Outcomes O1 (63-session low within first 20 sessions), O2 (63-session return > 0),
O3 (reversal within 92 calendar days). Beta-binomial posteriors, Hoeffding bounds, base rates from all >=10%-drawdown days."""
import numpy as np
import pandas as pd
from scipy import stats

from common import OUT, fred, ledger, save_parquet, yahoo

DELTA, M = 0.10, 8

spx = yahoo("^GSPC", start="1950-01-01")["close"]
spx = spx[spx > 0]
dd = spx / spx.rolling(252, min_periods=252).max() - 1
pos = pd.Series(np.arange(len(spx)), index=spx.index)

# ---------- rate-increase dates ----------
tar = pd.concat([fred("DFEDTAR").dropna(), fred("DFEDTARU").dropna()]).sort_index()
tar = tar[~tar.index.duplicated(keep="last")]
tar_up = tar[tar.diff() > 0].index
tar_dn = tar[tar.diff() < 0].index
ff = fred("FEDFUNDS").dropna()
ffd = ff.diff()
proxy_up_m = ffd[(ffd >= 0.25) & (ffd.index < "1982-09-01") & (ffd.index >= "1954-07-01")].index
proxy_dn_m = ffd[(ffd <= -0.25) & (ffd.index < "1982-09-01")].index


def first_session_on_or_after(d):
    i = spx.index.searchsorted(d)
    return spx.index[i] if i < len(spx) else None


cands = []
for d in proxy_up_m:
    s = first_session_on_or_after(d)
    if s is not None:
        cands.append((s, "proxy_FEDFUNDS_monthly", d))
for d in tar_up:
    s = first_session_on_or_after(d)
    if s is not None:
        cands.append((s, "target", d))
C = pd.DataFrame(cands, columns=["session", "source", "raw_date"]).drop_duplicates("session").sort_values("session")
C["dd"] = C.session.map(dd)
Q = C[C.dd <= -0.10].copy()

# ---------- cluster within 63 sessions ----------
ev, last = [], None
for r in Q.itertuples():
    p = pos[r.session]
    if last is None or p - last > 63:
        ev.append(dict(session=r.session, source=r.source, raw_date=r.raw_date, dd=r.dd, cluster_size=1))
    else:
        ev[-1]["cluster_size"] += 1
    last = p  # cluster extends while qualifying hikes keep arriving within 63 sessions
E = pd.DataFrame(ev, columns=["session", "source", "raw_date", "dd", "cluster_size"])


def outcomes(t):
    p = pos[t]
    if p + 63 >= len(spx):
        return dict(o1=np.nan, o2=np.nan, fwd63=np.nan, low_day=np.nan, low_dd=np.nan)
    w = spx.iloc[p:p + 64]
    k = int(np.argmin(w.values))
    return dict(o1=float(k <= 20), o2=float(w.iloc[-1] > w.iloc[0]), fwd63=w.iloc[-1] / w.iloc[0] - 1, low_day=k, low_dd=w.min() / w.iloc[0] - 1)


def reversal(t, source):
    end = t + pd.Timedelta(days=92)
    if source == "target":
        cut = [d for d in tar_dn if t < d <= end]
        return (1.0 if cut else 0.0), (f"cut {cut[0]:%Y-%m-%d}" if cut else "no cut within 92d")
    cut = [d for d in proxy_dn_m if t < d <= end]
    return (1.0 if cut else 0.0), (f"FEDFUNDS monthly fall {cut[0]:%Y-%m}" if cut else "no monthly fall >=25bp within 92d (proxy)")


rows = []
for r in E.itertuples():
    o = outcomes(r.session)
    rv, note = reversal(r.session, r.source)
    rows.append(dict(event_date=r.session.date(), source=r.source, drawdown_at_event=r.dd, cluster_hikes=r.cluster_size, **o, o3=rv, o3_note=note))
EV = pd.DataFrame(rows)
EV["o12"] = ((EV.o1 == 1) & (EV.o2 == 1)).astype(float)
EV.loc[EV.o1.isna(), "o12"] = np.nan

# Pre-registered: for events from 1994, a pause signalled in the next statement within 92 days also counts as reversal.
# Checked from federalreserve.gov statement text; filled in PAUSE_CHECKS below after reading each statement.
PAUSE_CHECKS = {  # event_date(str) -> (bool, "source | quote"); texts saved in data/raw/fomc/
    "2018-12-20": (True, "FOMC statement 2019-01-30 (monetary20190130a.htm): 'the Committee will be patient'"),
    "2022-05-05": (False, "statements 2022-06-15 and 2022-07-27 both raised the range; 'anticipates that ongoing increases'"),
    "2023-03-23": (True, "FOMC statement 2023-06-14 (monetary20230614a.htm): 'Holding the target range steady at this meeting'"),
}
for i, r in EV.iterrows():
    k = str(r.event_date)
    if k in PAUSE_CHECKS and r.o3 == 0 and PAUSE_CHECKS[k][0]:
        EV.loc[i, "o3"] = 1.0
        EV.loc[i, "o3_note"] = "explicit pause: " + PAUSE_CHECKS[k][1]
    elif k in PAUSE_CHECKS:
        EV.loc[i, "o3_note"] += " | pause check: " + PAUSE_CHECKS[k][1]


# ---------- base rates: all >=10% drawdown days ----------
def base_rates(start):
    days = dd[(dd <= -0.10) & (dd.index >= start)].index
    o = pd.DataFrame([outcomes(t) for t in days], index=days).dropna()
    return dict(o1=o.o1.mean(), o2=o.o2.mean(), o12=((o.o1 == 1) & (o.o2 == 1)).mean(), n_days=len(o))


def card(c, n, p0):
    if n == 0:
        return dict(c=c, n=n)
    a, b = 1 + c, 1 + n - c
    post = stats.beta(a, b)
    sk = stats.beta(M * p0 + c, M * (1 - p0) + n - c)
    hw = np.sqrt(np.log(2 / DELTA) / (2 * n))
    gap = abs(c / n - p0)
    nstar = np.log(2 / DELTA) / (2 * gap ** 2) if gap > 0 else np.inf
    lo, hi = post.ppf(0.05), post.ppf(0.95)
    pgt = 1 - post.cdf(p0)
    if n < 5:
        v = "INCONCLUSIVE"
    elif lo > p0:
        v = "HOLDS"
    elif 0.75 <= pgt <= 0.95:
        v = "WEAK"
    else:
        v = "KILLED"
    return dict(c=int(c), n=int(n), raw=c / n, post_mean=post.mean(), lo90=lo, hi90=hi, p_gt_base=pgt, base=p0,
                skeptical_mean=sk.mean(), skeptical_lo=sk.ppf(0.05), skeptical_hi=sk.ppf(0.95), hoeffding_hw=hw,
                more_events_to_settle=max(0, int(np.ceil(nstar - n))) if np.isfinite(nstar) else None, verdict=v)


results = []
for label, start, mask in [("full 1954+", "1955-01-01", EV.event_date.astype(str) >= "1954"),
                           ("target-only 1982-09+", "1982-09-27", EV.source == "target")]:
    sub = EV[mask].dropna(subset=["o1"])
    br = base_rates(start)
    for oc, name in [("o12", "Sharp low AND bounce (O1&O2, primary)"), ("o1", "Low within 20 sessions (O1)"), ("o2", "63-session return > 0 (O2)")]:
        c = sub[oc].astype(float).sum()
        r = card(c, len(sub), br[oc])
        results.append(dict(sample=label, claim=name, base_days=br["n_days"], **r))
        ledger(f"C_h3_{label.split()[0]}_{oc}", "H3", f"{name}: {int(c)}/{len(sub)} vs base {br[oc]:.2f}", len(sub),
               f"post mean {r.get('post_mean', float('nan')):.2f}, P>base {r.get('p_gt_base', float('nan')):.2f} -> {r.get('verdict')}")
    # O3 reversal rate (no base rate claim; descriptive)
    c3 = sub.o3.sum()
    ledger(f"C_h3_{label.split()[0]}_o3", "H3", f"Reversal within 92d: {int(c3)}/{len(sub)}", len(sub), "descriptive")
    # Key split
    for rv in (1.0, 0.0):
        s2 = sub[sub.o3 == rv]
        ledger(f"C_h3_{label.split()[0]}_split_rev{int(rv)}", "H3-split", f"O1&O2 given reversal={int(rv)}: {int(s2.o12.astype(float).sum())}/{len(s2)}", len(s2), "descriptive")

R = pd.DataFrame(results)
save_parquet(EV.astype({"event_date": "datetime64[ns]"}), "h3_events")
save_parquet(R, "h3_cards")
EV.to_csv(OUT / "C_h3_events.csv", index=False)
R.to_csv(OUT / "C_h3_cards.csv", index=False)
cand_summary = f"{len(C)} rate-increase dates ({(C.source=='target').sum()} target, {(C.source!='target').sum()} pre-1982 proxy months); {len(Q)} in a >=10% drawdown; {len(EV)} events after 63-session clustering"
print(cand_summary)
print(EV.to_string())
print(R[["sample", "claim", "c", "n", "raw", "post_mean", "lo90", "hi90", "base", "p_gt_base", "more_events_to_settle", "verdict"]].to_string())
(OUT / "C_candidates_summary.txt").write_text(cand_summary + "\n")

# ---------- key split: does the bounce depend on a reversal? (beta-binomial difference, Monte Carlo) ----------
rng = np.random.default_rng(20261125)
split_rows = []
for label, mask in [("full 1954+", EV.o1.notna()), ("target-only 1982-09+", (EV.source == "target") & EV.o1.notna())]:
    sub = EV[mask]
    a = sub[sub.o3 == 1]
    b = sub[sub.o3 == 0]
    ca, na, cb, nb = a.o12.sum(), len(a), b.o12.sum(), len(b)
    da = rng.beta(1 + ca, 1 + na - ca, 200000)
    db = rng.beta(1 + cb, 1 + nb - cb, 200000)
    p = float((da > db).mean())
    split_rows.append(dict(sample=label, rev_c=int(ca), rev_n=na, rev_post_mean=(1 + ca) / (2 + na),
                           norev_c=int(cb), norev_n=nb, norev_post_mean=(1 + cb) / (2 + nb), p_rev_gt_norev=p,
                           diff_lo90=float(np.quantile(da - db, 0.05)), diff_hi90=float(np.quantile(da - db, 0.95))))
    ledger(f"C_h3_{label.split()[0]}_split_diff", "H3-split", f"P(O1&O2 | reversal) {int(ca)}/{na} vs no reversal {int(cb)}/{nb}", na + nb, f"P(rev > norev) {p:.3f}")
SP = pd.DataFrame(split_rows)
SP.to_csv(OUT / "C_h3_split.csv", index=False)
print(SP.to_string())

# ---------- card ----------
f, t = R[R["sample"] == "full 1954+"], R[R["sample"] != "full 1954+"]
prim_f = f.iloc[0]
prim_t = t.iloc[0]
overall = "HOLDS" if (prim_f.verdict == "HOLDS" and prim_t.verdict == "HOLDS") else (
    "INCONCLUSIVE" if prim_f.n < 5 else ("KILLED" if "KILLED" in (prim_f.verdict, prim_t.verdict) and prim_f.verdict == "KILLED" else prim_f.verdict))
L = ["# small-sample-truth card: H3, the 2018 analogy", "",
     f"**VERDICT: {overall}** (unconditional claim) | confidence 60% (n = {int(prim_f.n)} events, pre-1982 dates are a monthly proxy)",
     f"Claim: when the Fed hikes into a >=10% S&P 500 drawdown, a sharp low (within 20 sessions) and a bounce (63-session return > 0) follow.",
     f"Events: {cand_summary}.", "",
     "| Sample | Claim | Raw c/n | Posterior mean | 90% interval | Base | P(> base) | Hoeffding +/- | Events to settle | Verdict |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for r in R.itertuples():
    L.append(f"| {r.sample} | {r.claim} | {r.c}/{r.n} | {r.post_mean:.2f} | {r.lo90:.2f}-{r.hi90:.2f} | {r.base:.2f} | {r.p_gt_base:.2f} | {r.hoeffding_hw:.2f} | {r.more_events_to_settle} | **{r.verdict}** |")
L += ["", "Skeptical prior Beta(8 p0, 8 (1-p0)) posterior means: " + "; ".join(f"{r.sample} {r.claim.split(' (')[0]}: {r.skeptical_mean:.2f}" for r in R.itertuples()), "",
      "**Key split: bounce (O1&O2) conditional on a Fed reversal within 92 days**", "",
      "| Sample | With reversal | Without reversal | P(rate with > rate without) | 90% interval of difference |", "|---|---|---|---|---|"]
for r in SP.itertuples():
    L.append(f"| {r.sample} | {r.rev_c}/{r.rev_n} (post {r.rev_post_mean:.2f}) | {r.norev_c}/{r.norev_n} (post {r.norev_post_mean:.2f}) | **{r.p_rev_gt_norev:.2f}** | {r.diff_lo90:+.2f} to {r.diff_hi90:+.2f} |")
L += ["", "Pitfalls: events are few and the pre-1982 hike dates are monthly-average proxies (dated at the month start, so the drawdown filter has mild look-ahead within the month); "
      "base-rate days overlap heavily; the 1994+ hawkish-statement extension was not run (pre-registered). A reversal is only known after the fact, so the split is not a forecast."]
(OUT / "C_small_sample_truth.md").write_text("\n".join(L) + "\n")
