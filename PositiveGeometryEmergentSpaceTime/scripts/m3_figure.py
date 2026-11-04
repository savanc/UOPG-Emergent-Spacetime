"""M3 figure: L3/L2 at mu = 0.77 GeV, hidden-zero prediction (-2, +-30% band) vs determinations."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math

rows = [  # name, L3, sL3, L2, sL2
    ("BE14 NNLO preferred\n(PRIMARY, Table 3)", -3.07, 0.20, 0.81, 0.04),
    ("BE14 NNLO free fit", -2.80, 0.20, 0.59, 0.04),
    ("BE14 p$^4$ fit (Table 1)", -3.8, 0.3, 1.6, 0.2),
    ("Pich 1995 / BEG 1994", -3.5, 1.1, 1.4, 0.3),
    ("GL 1985", -4.4, 2.5, 1.3, 0.7),
]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.axvspan(-2.6, -1.4, color="tab:green", alpha=0.2, label="hidden zero / LS: $-2\\pm30\\%$")
ax.axvline(-2, color="tab:green", lw=2)
ax.axvline(-3, color="tab:red", ls="--", lw=1.5, label="VMD / Skyrme line: $-3$")
for i, (n, a, sa, b, sb) in enumerate(rows):
    r = a / b
    s = abs(r) * math.hypot(sa / a, sb / b)
    y = len(rows) - i
    ax.errorbar(r, y, xerr=[[2 * s], [2 * s]], fmt="none", ecolor="0.7", elinewidth=1, capsize=3)
    ax.errorbar(r, y, xerr=s, fmt="o", color="k" if i else "tab:blue", capsize=4, ms=6 if i else 8)
    ax.text(-7.9, y, n, va="center", fontsize=8)
ax.set_xlim(-8, -0.5)
ax.set_ylim(0.3, len(rows) + 0.7)
ax.set_yticks([])
ax.set_xlabel("$L_3^r/L_2^r$ at $\\mu=0.77$ GeV  (1σ black, 2σ grey; uncorrelated errors)")
ax.set_title("M3: O(p$^4$) ratio from the 4-point hidden zero vs data — primary test FAILS (3.8σ beyond band)", fontsize=9)
ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
fig.tight_layout()
fig.savefig("figures/m3-lec-ratio.png", dpi=160)
print("wrote figures/m3-lec-ratio.png")
