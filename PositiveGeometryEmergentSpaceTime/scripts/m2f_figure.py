"""M2f figure: the one-parameter family A = (s - c)/F^2 that the constant-offset shift allows at n = 4,
its LO scattering lengths versus c/M^2, the hidden-zero point c = M^2 (Weinberg), and NA48/2 bands."""
import math
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
M, F = 139.57039, 130.2 / math.sqrt(2)
x = np.linspace(0.0, 2.0, 400)
k = M ** 2 / (32 * math.pi * F ** 2)
a00 = k * (12 - 5 * x); a20 = -2 * k * x
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for a, y, m, e, lab in ((ax[0], a00, 0.2220, 0.0142, r'$a_0^0$'), (ax[1], a20, -0.0432, 0.0097, r'$a_0^2$')):
    a.plot(x, y, 'k-', label='shift family, LO: ' + lab + r'$(c)$')
    a.axhspan(m - e, m + e, color='tab:blue', alpha=0.25, label='NA48/2 Ke4 (2010), 1σ')
    a.axvline(1.0, color='tab:red', ls='--', label=r'hidden zeros $\Rightarrow c=M^2$ (Weinberg)')
    a.set_xlabel(r'$c/M_\pi^2$  (shift constant; $A\propto s-c$)'); a.set_ylabel(lab)
    a.legend(fontsize=8)
fig.suptitle('M2f: the mass shift allows A = (s − c)/F²; massive hidden zeros fix c = M² (inputs: PDG M_π, F_π; LO only)', fontsize=9)
fig.tight_layout(); fig.savefig('figures/m2f-mass-shift.png', dpi=130)
print('saved figures/m2f-mass-shift.png')
