# KL-LAT3' gate: inputs only. Mass-level gap KL-1 vs N2 (c=0.411 frozen from KL-LAT2) in units of combined 1% error.
import numpy as np, math
c=0.411
def kl(n,p,k): return math.sqrt(1+n*(k*k-p*p))      # m_V/m_rho
def n2(n,p,k): return 1+n*c*(k*k-p*p)
print("n  pi/rho K/rho  KL  N2  gap%  z(1%each)")
best={}
for n,name in [(1,'K*'),(2,'phi')]:
  zmax=0
  for p in np.arange(0.15,0.51,0.05):
    for k in np.arange(0.5,1.01,0.05):
      if k<p: continue
      a,b=kl(n,p,k),n2(n,p,k); sig=0.01*math.hypot(a,b)  # 1% on lattice mass, 1% propagated input scale
      z=abs(a-b)/sig
      if z>2: print(name,f"{p:.2f} {k:.2f} {a:.4f} {b:.4f} {100*(a-b)/a:+.2f} {z:.2f}")
      zmax=max(zmax,z)
  print(name,"max z =",round(zmax,2))
