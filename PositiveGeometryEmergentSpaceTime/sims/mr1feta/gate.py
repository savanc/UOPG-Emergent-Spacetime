# MR-1f-eta gate: inputs only (masses, GeV; PDG-level, declared inputs, not targets).
mpi,meta,mK,mrho=0.1396,0.5479,0.4937,0.7753
t_dual=2*meta**2; t_lo=(6*meta**2+2*mpi**2)/9
print(f"dual su zero t = {t_dual:.4f} GeV^2; LO ChPT zero t0 = {t_lo:.4f} GeV^2; gap = {t_dual-t_lo:.4f}")
print(f"LO amplitude on dual line / at t=0: {(9*t_dual-6*meta**2-2*mpi**2)/(-6*meta**2-2*mpi**2):+.3f}")
