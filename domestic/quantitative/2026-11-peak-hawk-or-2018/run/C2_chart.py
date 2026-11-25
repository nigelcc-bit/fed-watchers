"""Headline chart for H3: S&P 500 63-session paths after each event, split by Fed reversal within 92 days."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import OUT, yahoo

ev = pd.read_csv(OUT / "C_h3_events.csv").dropna(subset=["o1"])
spx = yahoo("^GSPC", start="1950-01-01")["close"]
spx = spx[spx > 0]
BLUE, ORANGE, INK, INK2 = "#257de0", "#f47230", "#191919", "#666666"

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=200)
paths = {1.0: [], 0.0: []}
for r in ev.itertuples():
    p = spx.index.searchsorted(pd.Timestamp(r.event_date))
    w = spx.iloc[p:p + 64].values
    w = 100 * w / w[0]
    paths[r.o3].append(w)
    ax.plot(range(64), w, color=BLUE if r.o3 == 1 else ORANGE, lw=1.0, alpha=0.45)
for rv, col, lab in [(1.0, BLUE, "Fed reversed within 92 days"), (0.0, ORANGE, "No reversal")]:
    m = np.median(np.vstack(paths[rv]), axis=0)
    ax.plot(range(64), m, color=col, lw=2.4, label=f"{lab} (median, n={len(paths[rv])})")
    ax.annotate(f"{m[-1]-100:+.1f}%", (63, m[-1]), xytext=(4, 0), textcoords="offset points", va="center", color=INK, fontsize=9)
ax.axhline(100, color=INK2, lw=0.8)
ax.axvline(20, color=INK2, lw=0.8, ls=":")
ax.text(20.5, ax.get_ylim()[1] - 1, "20 sessions", color=INK2, fontsize=8, va="top")
ax.set_xlabel("Sessions after the hike (event date = 0)", color=INK2)
ax.set_ylabel("S&P 500, event date = 100", color=INK2)
ax.set_title("After hikes into a 10% drawdown, the median path rose 10% when the Fed reversed and was flat when it did not\n(13 events since 1954, thin lines are single events; one reversal case, 1970, still fell 19%)", loc="left", color=INK, fontsize=11)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#e6e6e6", lw=0.6)
ax.legend(frameon=False, loc="lower left", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "C_h3_paths_by_reversal.png")
print("saved")
