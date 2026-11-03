"""MR-1 data check (after prereg cb9e4ef). Sources opened 2026-10-12 from pdgLive (PDG 2026, Takahashi et al., IJMPA 41, 2630011)."""
import numpy as np, json
rng = np.random.default_rng(12); N = 400000; mpi = 0.13957
def asym(c, up, dn, n):  # split-normal
    z = rng.standard_normal(n); return c + np.where(z > 0, up, dn)*z
S = {
 "S1 PDG BW averages": dict(mr=(0.77526, 0.00023), Gr=(0.1474, 0.0008*2), mf=(1.2754, 0.0008), Gf=(0.1858, 0.0028, 0.0021), BR=(0.843, 0.028, 0.010)),
 "S2 PDG T-matrix poles": dict(mr=(0.763, 0.002), Gr=(0.145, 0.003), mf=(1.2715, 0.0115), Gf=(0.200, 0.020, 0.020), BR=(0.843, 0.028, 0.010)),
}
# note: S1 rho width error inflated x2 = the PDG scale factor S=2.0 already in the quoted error? (quoted error includes S; we double it conservatively)
def sig(m): return np.sqrt(1 - 4*mpi**2/m**2)
def Rg(mr, Gr, mf, Gf, BR, var):
    if var == "V1": kin = (mf/mr)*sig(mf)**5/sig(mr)**3
    if var == "V2": kin = (mf/mr)*sig(mf)/sig(mr)
    if var == "V3":   # Blatt-Weisskopf R = 5 GeV^-1: sigma^{2J} -> B_J(R q)/B_J(R m/2) (massless-normalised barrier)
        Rb = 5.0; q = lambda m: m*sig(m)/2
        B1 = lambda x: x**2/(1+x**2); B2 = lambda x: x**4/(9+3*x**2+x**4)
        kin = (mf/mr)*sig(mf)*B2(Rb*q(mf))/B2(Rb*mf/2) / (sig(mr)*B1(Rb*q(mr))/B1(Rb*mr/2))
    if var == "V4": mf_ = np.sqrt(3)*mr; kin = np.sqrt(3)*sig(mf_)**5/sig(mr)**3
    return Gf*BR/Gr / (KAPPA*kin)
KAPPA = 0.9  # = (27/20)/sqrt(3) / (1/2 * sqrt(3)) = 27/30; the prereg's '1.8' was an arithmetic slip (see review)
out = {}; sth = 0.32*0.5
for name, d in S.items():
    mr = rng.normal(*d["mr"], N); Gr = rng.normal(*d["Gr"], N); mf = rng.normal(*d["mf"], N)
    Gf = asym(d["Gf"][0], d["Gf"][1], d["Gf"][2], N); BR = asym(d["BR"][0], d["BR"][1], d["BR"][2], N)
    vals = {v: Rg(mr, Gr, mf, Gf, BR, v) for v in ("V1", "V2", "V3", "V4")}
    cen = {v: float(np.median(x)) for v, x in vals.items()}
    sdat = float(np.std(vals["V1"])); sconv = (max(cen.values()) - min(cen.values()))/2
    z = (cen["V1"] - 0.5)/np.sqrt(sth**2 + sdat**2 + sconv**2)
    wp = dict(narrow=bool(d["Gr"][0]/d["mr"][0] < 0.25 and d["Gf"][0]/d["mf"][0] < 0.25), positive=cen["V1"] > 0)
    verdict = "PASS" if abs(z) <= 2 else ("FAIL" if abs(z) > 3 else "INCONCLUSIVE")
    RG = float(np.median(Gf*BR/Gr)); mass2 = float(np.median(mf**2/mr**2))
    print(f"{name}: R_Gamma(data)={RG:.4f}; R_g variants {', '.join(f'{v}={c:.4f}' for v,c in cen.items())}; sigma_data={sdat:.4f} sigma_conv={sconv:.4f}; z={z:+.2f} -> {verdict}; well-posed {wp}; m_f2^2/m_rho^2={mass2:.3f} (pred 3)")
    out[name] = dict(R_Gamma=RG, Rg=cen, sigma_data=sdat, sigma_conv=sconv, z=float(z), verdict=verdict, wellposed=wp, mass_ratio_sq=mass2)
json.dump(out, open("scripts/mr1_data_check.json", "w"), indent=1)
