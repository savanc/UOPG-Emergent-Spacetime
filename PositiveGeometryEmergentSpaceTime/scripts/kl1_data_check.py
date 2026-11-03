"""MR-1f + KS-1 data check (after prereg eb69103). Sources read from pdgLive 2026 DataBlocks on 2026-10-13."""
import numpy as np, json, math, kl1_theory as k
rng = np.random.default_rng(1780); N = 4000
q = lambda a, b: math.hypot(a, b)
S = {  # m, Gamma (GeV), BR(Kpi); asym errors symmetrised to the larger side
 "S1 PDG 2026": {1: dict(m=(0.89556, 0.00020), G=(0.0471, 0.0005), BR=(1.0, 0.0)),
                 2: dict(m=(1.4324, 0.0013), G=(0.109, 0.005), BR=(0.499, 0.012)),
                 3: dict(m=(1.779, 0.008), G=(0.161, 0.017), BR=(0.188, 0.010)),
                 4: dict(m=(2.048, 0.009), G=(0.199, 0.027), BR=(0.099, 0.012))},
 "S2 LASS (ASTON 88; K4* m,G ASTON 86)": {1: dict(m=(0.8959, q(.0005, .0002)), G=(0.0508, q(.0008, .0009)), BR=(1.0, 0.0)),
                 2: dict(m=(1.4312, q(.0018, .0007)), G=(0.1165, q(.0036, .0017)), BR=(0.485, q(.006, .020))),
                 3: dict(m=(1.781, q(.008, .004)), G=(0.203, q(.030, .008)), BR=(0.187, q(.008, .008))),
                 4: dict(m=(2.062, q(.014, .013)), G=(0.221, q(.048, .027)), BR=(0.099, 0.012))}}
mls2 = {J: k.mJ2(J) for J in (1, 2, 3, 4)}
predLS = k.pred({J: math.sqrt(v) for J, v in mls2.items()})
out = {"pred_LS_masses": predLS, "mass2_LS": mls2}
# cache width(J, m2) on a grid for MC speed
from functools import lru_cache
W = lru_cache(None)(lambda J, m2r: k.width(J, m2r))
wf = lambda J, m: W(J, round(m*m, 5))
for name, d in S.items():
    print("==", name)
    # KS-1 masses
    for J in (2, 3, 4):
        m, sm = d[J]["m"]; p = mls2[J]; sig = math.hypot(0.05*p, 2*m*sm); z = (m*m - p)/sig
        lo, hi = mls2[J-1], (mls2[J+1] if J < 4 else mls2[J] + 1/k.ap)
        f = min(1, 4*sig/(hi - lo))
        v = "PASS" if abs(z) <= 2 else "FAIL" if abs(z) > 3 else "INCONCLUSIVE"
        print(f"KS-1 J={J}: m_data={m:.4f}, m_LS={math.sqrt(p):.4f}, dm2/m2={(m*m-p)/p:+.3f}, z={z:+.2f} -> {v}; null f={f:.2f}")
        out[f"KS1|{name}|J{J}"] = dict(m=m, mLS=math.sqrt(p), z=z, verdict=v, null=f)
    # MR-1f width ratios
    m1 = rng.normal(*d[1]["m"], N); G1 = rng.normal(*d[1]["G"], N)
    for J in (2, 3, 4):
        mJ = rng.normal(*d[J]["m"], N); GJ = rng.normal(*d[J]["G"], N); BR = rng.normal(*d[J]["BR"], N)
        Rd = GJ*BR/G1; Rc = float(np.median(Rd)); sd = float(np.std(Rd))
        PV1 = wf(J, d[J]["m"][0])/wf(1, d[1]["m"][0]); PV2 = predLS[J]; sc = abs(PV1 - PV2)/2
        sth = math.hypot(0.30, 0.10*(J-1))*PV1; tot = math.sqrt(sth**2 + sd**2 + sc**2); z = (Rc - PV1)/tot
        wp = d[J]["G"][0]/d[J]["m"][0] < 0.25 and d[J]["BR"][1]/d[J]["BR"][0] <= 0.5
        v = ("PASS" if abs(z) <= 2 else "FAIL" if abs(z) > 3 else "INCONCLUSIVE") if wp else "INCONCLUSIVE (data)"
        u = np.exp(rng.uniform(math.log(Rc/10), math.log(10*Rc), 200000)); f = float(np.mean(np.abs(Rc - u)/np.sqrt((math.hypot(0.30, 0.10*(J-1))*u)**2 + sd**2 + sc**2) <= 2))
        print(f"MR-1f R{J}: data={Rc:.4f}±{sd:.4f}; LS V1={PV1:.4f} V2={PV2:.4f}; data/LS={Rc/PV1:.2f}; sth={sth:.4f}; z={z:+.2f} -> {v}; null f={f:.2f}")
        out[f"MR1f|{name}|R{J}"] = dict(data=Rc, sd=sd, V1=PV1, V2=PV2, z=z, verdict=v, null=f)
json.dump(out, open("kl1_data_check.json", "w"), indent=1)
