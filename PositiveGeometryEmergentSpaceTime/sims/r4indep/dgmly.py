# R4-indep (c): DGMLY pi+ - pi0 EM splitting, narrow rho/a1 + Weinberg sum rules. Run id: r4indep-dgmly-1
import math
alpha=1/137.035999; mrho=775.26; mpip=139.57039; mpi0=134.9768
obs=mpip**2-mpi0**2
for label,ma1 in [("Weinberg m_a1=sqrt2 m_rho",math.sqrt(2)*mrho),("PDG m_a1=1230",1230.0)]:
    for dq2,name in [(1,"Q_u-Q_d=1 (any y_Q, any N_c)")]:
        d=3*alpha/(4*math.pi)*mrho**2*ma1**2/(ma1**2-mrho**2)*math.log(ma1**2/mrho**2)*dq2
        print(f"{label}: pred {d:.0f} MeV^2, obs {obs:.0f} MeV^2, ratio {d/obs:.3f}; charge input {name}")
