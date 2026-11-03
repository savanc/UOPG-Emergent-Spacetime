"""MR-3b data: g~rho^2 = g^2 f^2/m_rho^2 vs LS prediction 1/(2pi). Prereg commit 8b26408.
Sources fetched 2026-10-12: PDG live rho(770) (M009): m=775.26(23), Gamma=147.4(8) [neutral e+e-];
charged 775.11(34), 149.1(8).  FLAG 2019 (FERMILAB-PUB-19-077-T table): f_pi+=130.2(8) MeV, Nf=2+1 F_pi/F=1.062(7).
m_pi+ = 139.57 MeV (memory). Width formula Gamma = g^2 p^3/(6 pi m^2) (memory)."""
import math
mpi=139.57; pred=1/(2*math.pi); lo,hi=pred*(1-.36),pred*(1+.36)
def gt(m,G,f):
    p=math.sqrt(m*m/4-mpi*mpi); g2=6*math.pi*m*m*G/p**3
    return g2, g2*f*f/m/m
rows=[("PDG neutral, f=130.2/sqrt2 (FLAG/PDG)",775.26,147.4,130.2/math.sqrt(2)),
      ("PDG charged, f=130.2/sqrt2",775.11,149.1,130.2/math.sqrt(2)),
      ("PDG neutral, chiral-limit F=f/1.062 (FLAG)",775.26,147.4,130.2/math.sqrt(2)/1.062)]
print(f"prediction 1/(2pi)={pred:.4f}, band [{lo:.3f},{hi:.3f}]; KSRF=0.5")
for n,m,G,f in rows:
    g2,v=gt(m,G,f); print(f"{n}: g={math.sqrt(g2):.3f}  g~rho^2={v:.4f}  ratio data/pred={v/pred:.2f}  in band={lo<=v<=hi}")
# input error (Gamma 0.8, f 0.8/sqrt2) ~ 1.3% -> negligible vs 36%
