#!/usr/bin/env python3
"""CASCADE-1b r1 figure (post-run; reads cascade1b_live.json + runs/CASCADE1b-2026-10-23-r1/progress.log only)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

R = Path(__file__).resolve().parents[2]
d = json.loads((R / "sims/cascade1b/cascade1b_live.json").read_text())
log = (R / "runs/CASCADE1b-2026-10-23-r1/progress.log").read_text()
n6 = [(1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (2, 6), (3, 5), (3, 6), (4, 6)]  # diamond anchors X_B, checker order
killed = (1, 4) if "pairs: [(1, 4), (1, 5), (2, 4), (2, 5)]" in log else None
rows = []
for n in (4, 5):
    rows.append((n, [(tuple(v["B"]), "zero" if v["zero_only"] else "nonzero") for v in d[f"V_D_n{n}"]]))
st6 = []
for i, B in enumerate(n6):
    if killed and B == killed:
        st6.append((B, "killed"))
    elif killed and i < n6.index(killed):
        st6.append((B, "lost"))
    else:
        st6.append((B, "notrun"))
rows.append((6, st6))
col = {"zero": "#2e7d32", "nonzero": "#c62828", "killed": "#e53935", "lost": "#f9a825", "notrun": "#bdbdbd"}
fig, ax = plt.subplots(figsize=(10, 3.4))
for r, (n, cells) in enumerate(rows):
    for k, (B, s) in enumerate(cells):
        ax.add_patch(plt.Rectangle((k, -r), 0.9, 0.8, color=col[s]))
        ax.text(k + 0.45, -r + 0.4, f"X{B[0]}{B[1]}", ha="center", va="center", fontsize=8, color="white" if s != "notrun" else "black")
    ax.text(-0.2, -r + 0.4, f"n={n}", ha="right", va="center")
ax.set_xlim(-1, 9.2); ax.set_ylim(-2.2, 1.0); ax.axis("off")
ax.set_title(f"CASCADE-1b run {d['run_id']}: V_D per causal diamond (locked checker v2)\nverdict {d['verdict']}", fontsize=10)
ax.legend(handles=[Patch(color=col["zero"], label="V_D = {0} (SIMULATED r1)"),
                   Patch(color=col["lost"], label="finished, result not stored (kill discarded list)"),
                   Patch(color=col["killed"], label="3600 s kill"),
                   Patch(color=col["notrun"], label="not reached")], loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=4, fontsize=7, frameon=False)
out = R / "figures/cascade1b-2026-10-23.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(out)
