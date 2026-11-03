#!/usr/bin/env python3
"""CASCADE-1 figure: K_s vs stage for the four cells (reads cascade1_live.json + posthoc/split_mass_diag.json only)."""
import json
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
H = Path(__file__).resolve().parent
d = json.loads((H / 'cascade1_live.json').read_text())
ph = json.loads((H / 'posthoc' / 'split_mass_diag.json').read_text())
fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
st = ['S0', 'S1', 'S2', 'S3', 'S4']
for ax, n, Noff in [(axs[0], 4, 2), (axs[1], 5, 5)]:
    for s, col in [('E0', 'tab:blue'), ('EM', 'tab:red')]:
        c = d['cells'][f'{s}-n{n}']
        K = [r['K'] for r in c['rows']]
        ax.plot(st, K, 'o-', color=col, label=f"{s}: K_final={c['K_final']} ({c['outcome']}, {c['ratio']})")
        for i, k in enumerate(K):
            ax.annotate(str(k), (i, k), textcoords='offset points', xytext=(5, 4), fontsize=8, color=col)
    ax.axhline(Noff, ls='--', color='k', lw=1, label=f'N_off = {Noff}')
    ax.set_yscale('symlog', linthresh=10) if n == 5 else None; ax.set_title(f'n = {n}' + (' (non-blind)' if n == 4 else ' (blind)'))
    ax.set_xlabel('stage'); ax.set_ylabel('K_s = dim Θ_s + f_s'); ax.legend(fontsize=8)
v = d['verdict']
fig.suptitle(f"CASCADE-1 r1 ({d['run_id']}). Locked python verdict: {v}\n"
             f"EM-5 held-out splits: locked 0/10; post-hoc mass-consistent {ph['D2_locus_masses_mapped']}/10 "
             f"(checker defect, see review); Lean split5_of_rel_* PROVED", fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.9])
fig.savefig(H.parents[1] / 'figures' / 'cascade1-2026-10-23.png', dpi=130)
print('ok')
