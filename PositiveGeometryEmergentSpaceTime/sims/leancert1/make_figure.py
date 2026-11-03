"""Figure for LEAN-CERT-1 (post-run; reads per_n_probe.json + leancert1_live.json only)."""
import json, statistics as st, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import numpy as np, os
H = os.path.dirname(os.path.abspath(__file__))
pr = json.load(open(f'{H}/per_n_probe.json')); lv = json.load(open(f'{H}/leancert1_live.json'))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
ns = [5, 6, 7]; N = [10, 15, 21]
tc = [st.median(r['type_checking_s'] for r in pr[f'abhy{n}']) for n in ns]
wall = [st.median(r['wall_s'] for r in pr[f'abhy{n}']) for n in ns]
ax[0].loglog(N, tc, 'o-', label='kernel type-check of decide (median of 3)')
ax[0].loglog(N, wall, 's--', label='wall incl. ~4 s Mathlib import')
s = np.polyfit(np.log(N), np.log(tc), 1)[0]
ax[0].set_xlabel('number of Mandelstams C(n,2)  (n = 5, 6, 7)'); ax[0].set_ylabel('seconds')
ax[0].set_title(f'ABHY certificate check cost; slope ≈ {s:.2f} (CONJECTURE beyond n=7)', fontsize=9)
ax[0].axhline(3600, color='r', lw=0.8); ax[0].text(10, 2000, '1 h kill', color='r', fontsize=8)
ax[0].legend(fontsize=8)
ax[1].bar(['gpos', 'n=5', 'n=6', 'n=7'], [st.median(r['type_checking_s'] for r in pr[k]) for k in ['gpos', 'abhy5', 'abhy6', 'abhy7']])
ax[1].set_ylabel('kernel type-check s'); ax[1].set_title(f'per-certificate; peak RSS {pr["peak_rss_children_gb"]} GB (15 GB kill)', fontsize=9)
t = np.linspace(-6, 4, 400); c = [float(x) for x in lv['T1']['cubic_on_line_coeffs(t^0..t^3)']]
ax[2].plot(t, c[0] + c[1]*t + c[2]*t**2 + c[3]*t**3); ax[2].axhline(0, color='k', lw=0.6)
for r in lv['T1']['rational_roots']: ax[2].plot(float(r), 0, 'ro')
ax[2].set_title('T1 cubic ACC on certified line: −18(t+4)(t−2); roots {−4, 2}', fontsize=9); ax[2].set_xlabel('t')
fig.suptitle('LEAN-CERT-1 (run LEANCERT1-2026-10-23-r1): exact certificates checked by kernel decide', fontsize=10)
fig.tight_layout(); fig.savefig(f'{H}/../../figures/leancert1-2026-10-23.png', dpi=130); print('slope', s)
