#!/usr/bin/env python3
"""CASCADE-1b r2 figure (post-run; reads sims/cascade1b/cascade1b_r2_live.json only)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parents[2]
d = json.loads((R / "sims/cascade1b/cascade1b_r2_live.json").read_text())
fig, axs = plt.subplots(1, 3, figsize=(15, 4.2), gridspec_kw={"width_ratios": [1.3, 1, 1.2]})
ax = axs[0]
for r, n in enumerate((4, 5, 6)):
    for k, v in enumerate(d.get(f"V_D_n{n}", [])):
        c = "#2e7d32" if v["zero_only"] else "#c62828"
        ax.add_patch(plt.Rectangle((k, -r), 0.9, 0.8, color=c))
        ax.text(k + 0.45, -r + 0.4, f"X{v['B'][0]}{v['B'][1]}", ha="center", va="center", fontsize=7, color="white")
    ax.text(-0.2, -r + 0.4, f"n={n}", ha="right", va="center", fontsize=9)
ax.set_xlim(-1, 9.2); ax.set_ylim(-2.2, 1.0); ax.axis("off")
ax.set_title("V_D per causal diamond (checker v3)\ngreen = {0} only (SIMULATED)", fontsize=9)
ax = axs[1]
cells = list(d["cells"].keys())
K = [d["cells"][c]["K_final"] for c in cells]; N = [d["cells"][c]["N_off"] for c in cells]
x = range(len(cells))
ax.bar([i - 0.2 for i in x], K, 0.4, label="K (final-family dim)", color="#1565c0")
ax.bar([i + 0.2 for i in x], N, 0.4, label="N_off (offsets)", color="#9e9e9e")
for i, c in enumerate(cells):
    ax.text(i, max(K[i], N[i]) + 0.2, d["cells"][c]["outcome"], ha="center", fontsize=7, rotation=90, va="bottom")
ax.set_xticks(list(x)); ax.set_xticklabels(cells, rotation=45, fontsize=8); ax.set_ylim(0, 13)
ax.legend(fontsize=7, loc="upper left"); ax.set_title("H re-test per cell: K vs N_off", fontsize=9)
ax = axs[2]
ho = d.get("heldout_n6_EM", {})
fc = ho.get("factor_count", []); e37 = ho.get("eq37_points", [])
pts = sorted({h["point"] for h in fc})
okf = [sum(h["ok"] for h in fc if h["point"] == p) for p in pts]
oke = [sum(h["ok"] for h in e37 if h["point"] == p) for p in pts]
ctl = d.get("control_offfamily", {})
labels = [f"pt {p}" for p in pts] + ["control\n(off Θ3)"]
ax.bar(range(len(pts)), okf, 0.4, color="#2e7d32", label="factor count ok (of 30)")
ax.bar([p + 0.4 for p in range(len(pts))], oke, 0.4, color="#66bb6a", label="eq. 3.7 ok (of 12)")
if ctl:
    ax.bar(len(pts), ctl["pass_count"], 0.4, color="#c62828", label="control factor count ok (of 30)")
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=8); ax.set_ylim(0, 32)
ax.legend(fontsize=7, loc="upper right"); ax.set_title(f"held-out n=6 EM (BLIND); eq. 3.7 symbolic: {str(ho.get('eq37_symbolic'))[:40]}", fontsize=8)
fig.suptitle(f"CASCADE-1b run {d['run_id']} (seed {d['seed']}): {d.get('verdict')}", fontsize=10)
out = R / "figures/cascade1b-r2-2026-10-24.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(out)
