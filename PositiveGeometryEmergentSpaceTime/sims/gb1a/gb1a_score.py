"""GB-1a scoring per prereg 17ee8d1. Data: arXiv 2106.00364 (v4 source, Table 34/33 continuum, units sqrt(sigma)),
ONLY the 4++ gs and 2++ gs rows. Stars in the paper = poor fits. N=6,12: no 4++ entry."""
from math import sqrt
data={4:((7.36,0.09,True),(4.742,0.015)),8:((7.20,0.07,True),(4.660,0.020)),10:((7.32,0.15,False),(4.594,0.025))}
pred={"A":(6.940539,1.445998),"B":(6.139960,1.732051)}
def grade(p,v,e):
    d=abs(p-v); rel=d/v
    return ("PASS" if d<=max(2*e,0.05*v) else "PARTIAL" if rel<=0.10 else "FAIL"), rel, d/e
out=[]
for N in (4,6,8,10,12):
    if N not in data: out.append(f"N={N}: no 4++ entry in table -> not scorable"); continue
    (m4,e4,star),(m2,e2)=data[N]; r=m4/m2; er=r*sqrt((e4/m4)**2+(e2/m2)**2)
    out.append(f"N={N}: lattice 4++={m4}({e4}){'*' if star else ''}, 4++/2++={r:.4f}±{er:.4f}")
    for M,(p4,pr) in pred.items():
        g1=grade(p4,m4,e4); g2=grade(pr,r,er)
        out.append(f"   model {M}: 4++ {p4:.3f} -> {g1[0]} (dev {100*g1[1]:.1f}%, {g1[2]:.1f} sigma); ratio {pr:.4f} -> {g2[0]} (dev {100*g2[1]:.1f}%, {g2[2]:.1f} sigma)")
print("\n".join(out))
