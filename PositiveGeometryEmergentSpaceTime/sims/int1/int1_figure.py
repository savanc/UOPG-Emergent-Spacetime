#!/usr/bin/env python3
"""INT-1 figure (not a scoring script): reads sims/int1/int1_live.json, run INT1-2026-10-22-r1.
Slice c13' = 1 of the n = 5 offset space; colour = f-vector of the (massive => shifted) polygon; lines = walls."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
R = Path(__file__).resolve().parents[2]
d = json.loads((R / 'sims/int1/int1_live.json').read_text())
g = d['figure_grid_c13eq1']
labs = sorted({tuple(f) for _, _, f in g})
idx = {l: i for i, l in enumerate(labs)}
xs = sorted({a for a, _, _ in g}); ys = sorted({b for _, b, _ in g})
Z = np.full((len(ys), len(xs)), np.nan)
for a, b, f in g:
    Z[ys.index(b), xs.index(a)] = idx[tuple(f)]
fig, ax = plt.subplots(figsize=(7, 6))
cm = plt.get_cmap('tab10', len(labs))
im = ax.imshow(Z, origin='lower', extent=(xs[0] - .05, xs[-1] + .05, ys[0] - .05, ys[-1] + .05), cmap=cm,
               vmin=-.5, vmax=len(labs) - .5, interpolation='nearest')
t = np.linspace(-2, 2, 3)
kw = dict(color='k', lw=1)
ax.axvline(0, **kw); ax.axhline(0, **kw); ax.axvline(-1, **kw)
ax.plot(t, -t, **kw); ax.plot(t, -1 - t, **kw)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
ax.set_xlabel("c14'"); ax.set_ylabel("c24'")
ax.set_title(fontsize=9, label="INT-1 (run INT1-2026-10-22-r1): n=5 f-vector on slice c13'=1\nwalls c14'=0, c24'=0, c13'+c14'=0, c14'+c24'=0, c13'+c14'+c24'=0")
cb = fig.colorbar(im, ticks=range(len(labs))); cb.ax.set_yticklabels([str(l) for l in labs])
cb.set_label('(f0, f1); grid points on walls show wall types')
fig.tight_layout()
out = R / 'figures/int1-chambers-2026-10-22.png'
fig.savefig(out, dpi=150)
print(out)
