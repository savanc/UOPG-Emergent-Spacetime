"""MR-1b data check (after prereg cdef00b). PDG 2026 (pdgLive + 2026 listings PDFs). rho from MR-1 S1."""
import numpy as np, json
rng = np.random.default_rng(1690); N = 400000; mpi = 0.13957
pred = {"rho3": 5/16, "f4": 49/240}; kap = {"rho3": 3/7, "f4": 1/2}; J = {"rho3": 3, "f4": 4}
nlev = {"rho3": 2, "f4": 3}; lsallow = {2: 0.20, 3: 0.30}
mr, Gr = (0.77526, 0.00023), (0.1474, 0.0016)
src = {
 "rho3": {"S1 PDG 2026 avg/fit": dict(m=(1.6888, 0.0021), G=(0.161, 0.010), BR=(0.236, 0.013)),
          "S2 CORDEN 79 (OMEG, pi-p->n2pi)": dict(m=(1.734, 0.010), G=(0.322, 0.035), BR=(0.23, 0.02))},
 "f4":   {"S1 PDG 2026 avg": dict(m=(2.018, 0.011), G=(0.237, 0.018), BR=(0.170, 0.015)),
          "S2 CORDEN 79 (OMEG, pi-p->n2pi)": dict(m=(1.935, 0.013), G=(0.263, 0.057), BR=(0.17, 0.02))},
}
sig = lambda m: np.sqrt(1 - 4*mpi**2/m**2)
q = lambda m: m*sig(m)/2
B = {1: lambda x: x**2/(1+x**2),
     3: lambda x: x**6/(225+45*x**2+6*x**4+x**6),
     4: lambda x: x**8/(11025+1575*x**2+135*x**4+10*x**6+x**8)}
def R(X, m, G, BR, mrho, Grho, var):
    j = J[X]
    if var == "V1": kin = (m/mrho)*sig(m)**(2*j+1)/sig(mrho)**3
    if var == "V2": kin = (m/mrho)*sig(m)/sig(mrho)
    if var == "V3":
        Rb = 5.0; kin = (m/mrho)*sig(m)*B[j](Rb*q(m))/B[j](Rb*m/2) / (sig(mrho)*B[1](Rb*q(mrho))/B[1](Rb*mrho/2))
    if var == "V4":
        mls = np.sqrt(2*nlev[X]+1)*mrho; kin = (mls/mrho)*sig(mls)**(2*j+1)/sig(mrho)**3
    return G*BR/Grho/(kap[X]*kin)
out = {}
for X, S in src.items():
    sth = np.sqrt(0.30**2 + lsallow[nlev[X]]**2)*pred[X]
    for name, d in S.items():
        m = rng.normal(*d["m"], N); G = rng.normal(*d["G"], N); BR = rng.normal(*d["BR"], N)
        mrho = rng.normal(*mr, N); Grho = rng.normal(*Gr, N)
        vals = {v: R(X, m, G, BR, mrho, Grho, v) for v in ("V1", "V2", "V3", "V4")}
        cen = {v: float(np.median(a)) for v, a in vals.items()}
        sd = float(np.std(vals["V1"])); sc = (max(cen.values())-min(cen.values()))/2
        z = (cen["V1"]-pred[X])/np.sqrt(sth**2+sd**2+sc**2)
        wp = d["G"][0]/d["m"][0] < 0.25 and d["BR"][1]/d["BR"][0] <= 0.5 and cen["V1"] > 0
        v = ("PASS" if abs(z) <= 2 else "FAIL" if abs(z) > 3 else "INCONCLUSIVE") if wp else "INCONCLUSIVE (data)"
        m2r = float(np.median(m**2/mrho**2))
        print(f"{X} | {name}: R V1={cen['V1']:.4f} (pred {pred[X]:.4f}, ratio {cen['V1']/pred[X]:.2f}); V2={cen['V2']:.4f} V3={cen['V3']:.4f} V4={cen['V4']:.4f}; "
              f"sd={sd:.4f} sc={sc:.4f} sth={sth:.4f}; z={z:+.2f}; well-posed={wp} (G/m={d['G'][0]/d['m'][0]:.3f}) -> {v}; m^2/m_rho^2={m2r:.2f} (LS {2*nlev[X]+1})")
        out[f"{X}|{name}"] = dict(R=cen, sd=sd, sc=sc, sth=float(sth), z=float(z), wellposed=bool(wp), verdict=v, mass2=m2r)
json.dump(out, open("scripts/mr1b_data_check.json", "w"), indent=1)
