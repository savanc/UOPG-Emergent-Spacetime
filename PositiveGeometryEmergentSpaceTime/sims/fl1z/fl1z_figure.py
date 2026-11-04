#!/usr/bin/env python3
"""FL-1Z figure (drawn after run FL1Z-2026-10-22-r3 from fl1z_live.json; not used for any verdict)."""
import json, collections
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
H = Path(__file__).resolve().parent
d = json.load(open(H / 'fl1z_live.json'))
rows = d['rows']
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
lo, hi = 0.02655, 0.03268
for k, a, xl in (('D1', ax[0], '|τ − ω|  (b̃k = 0)'), ('D2', ax[1], '|b̃k|  (τ = ω)')):
    xs, ys = [], []
    for r in rows:
        if r['tag'].startswith(k):
            x = float(r['tag'].split('=')[1]); xs.append(x * (1 + 0.04 * np.random.default_rng(len(xs)).standard_normal())); ys.append(max(r['rho'], 1e-18))
    a.scatter(xs, ys, s=6, alpha=.5, label='all charged-lepton branches')
    g = collections.defaultdict(list)
    for x, y in zip(xs, ys): g[round(x, 4)].append(y)
    a.axhspan(lo, hi, color='tab:green', alpha=.25, label='NuFit 3σ ρ band')
    a.set_xscale('log'); a.set_yscale('log'); a.set_xlabel(xl); a.set_ylabel('ρ = (m2/m3)²'); a.set_ylim(1e-18, 2)
ax[0].set_title('D1: ρ vs distance from fixed point'); ax[1].set_title('D2: ρ vs b̃k at the fixed point')
ax[0].legend(fontsize=8, loc='lower right')
fig.suptitle('FL-1Z (run FL1Z-2026-10-22-r3): ρ depends on the free distance and on b̃k → NOT-WELL-POSED', fontsize=10)
fig.tight_layout(); out = H.parents[1] / 'figures' / 'fl1z-rho-2026-10-22.png'; fig.savefig(out, dpi=130); print(out)
