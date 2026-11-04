"""TH-1 theory (no data): ππ threshold parameters of the Lovelace–Shapiro amplitude (MR-1b conventions).
Mπ = 1 units. α(s) = α0 + α' s with α(Mπ²) = 1/2 (Adler) and α(mρ²) = 1. A(s,t,u) = -λ[V(s,t)+V(s,u)-V(t,u)].
Re t_ℓ^I = q^{2ℓ}(a_ℓ^I + b_ℓ^I q² + ...), t_ℓ = 1/(64π) ∫ P_ℓ(z) T^I dz. Ratios are λ-independent."""
import mpmath as mp, json, sys
mp.mp.dps = 30
def run(r):
    ap = 1/(2*(r**2-1)); a0 = mp.mpf(1)/2 - ap
    al = lambda x: a0 + ap*x
    V = lambda x, y: mp.gamma(1-al(x))*mp.gamma(1-al(y))/mp.gamma(1-al(x)-al(y))
    A = lambda s, t, u: -(V(s,t)+V(s,u)-V(t,u))
    # λ from LO matching dA/ds = 1/F^2 at symmetric point (control only)
    T = {0: lambda s,t,u: 3*A(s,t,u)+A(t,s,u)+A(u,t,s), 1: lambda s,t,u: A(t,s,u)-A(u,t,s), 2: lambda s,t,u: A(t,s,u)+A(u,t,s)}
    def proj(I, l, q2):
        s = 4*(1+q2)
        f = lambda z: mp.legendre(l, z)*T[I](s, -2*q2*(1-z), -2*q2*(1+z))
        return mp.quad(f, [-1, 1])/(64*mp.pi)
    def ab(I, l):
        c = mp.taylor(lambda q2: proj(I, l, q2), 0, l+1)
        return c[l], c[l+1]
    res = {}
    for (I, l) in [(0,0),(2,0),(1,1),(0,2),(2,2),(1,3)]:
        a, b = ab(I, l); res[f"{l}{I}"] = (a, b)
    # LO-ChPT control normalisation: slope of A in s at symmetric point
    sl = mp.diff(lambda s: A(s, (4-s)/2, (4-s)/2), mp.mpf(4)/3)
    return res, sl
if __name__ == "__main__":
    out = {}
    for name, r in (("phys", mp.mpf("775.26")/mp.mpf("139.57")),):
        res, sl = run(r)
        Fpi = mp.mpf("92.28")/mp.mpf("139.57")  # f_pi in pion units (input, MR-1b ledger)
        lam = 1/(sl*Fpi**2)
        a11 = lam*res["11"][0]; aLO = 1/(24*mp.pi*Fpi**2)
        R1 = res["11"][1]/res["11"][0]; R2 = res["20"][1]/res["22"][1]; R3 = res["31"][0]/res["11"][0]
        print(f"r={float(r):.4f}")
        for k, (a, b) in res.items(): print(f"  l,I={k}: a={float(lam*a):+.4e} b={float(lam*b):+.4e} (lambda-normalised)")
        print(f"CONTROL a11 LS={float(a11):.4f} vs LO ChPT 1/(24 pi F^2)={float(aLO):.4f} ratio={float(a11/aLO):.3f}")
        print(f"PRED R1=b11/a11={float(R1):+.5f}  R2=b20/b22={float(R2):+.5f}  R3=a31/a11={float(R3):+.4e}")
        out = dict(r=float(r), R1=float(R1), R2=float(R2), R3=float(R3), control=float(a11/aLO),
                   params={k: [float(lam*a), float(lam*b)] for k, (a, b) in res.items()})
    json.dump(out, open("th1_pred.json", "w"), indent=1)
