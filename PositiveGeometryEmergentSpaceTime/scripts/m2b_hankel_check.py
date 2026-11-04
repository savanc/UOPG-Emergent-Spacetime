"""M2b: Hankel (EFT-hedron) checks for toy UV completions, per prereg/M2b-eft-hedron-2026-10-10.md.
f_k = forward coefficient sequence = moments of a positive measure on (0, xmax].
Checks: H2 f0 f2 >= f1^2; H3 det 3x3 Hankel >= 0 (where 5 coefficients exist); G f_{k+1} <= xmax f_k.
mpmath, 60 digits. Tolerance for 'violation': relative 1e-40."""
import json
from mpmath import mp, mpf, pi, zeta, polygamma, tan, taylor, gamma, matrix, det, nsum, inf
mp.dps = 60
TOL = mpf('1e-40')

def checks(name, f, xmax, kind):
    out = {"name": name, "kind": kind, "xmax": float(xmax), "f": [mp.nstr(x, 20) for x in f]}
    scale = max(abs(x) for x in f)
    h2 = f[0]*f[2] - f[1]**2
    out["H2_gap"] = mp.nstr(h2, 20); out["H2_rel"] = mp.nstr(h2/scale**2, 12)
    out["H2"] = bool(h2 >= -TOL*scale**2)
    if len(f) >= 5:
        H = matrix([[f[i+j] for j in range(3)] for i in range(3)])
        d = det(H); out["H3_det"] = mp.nstr(d, 20); out["H3"] = bool(d >= -TOL*scale**3)
    G = [xmax*f[k] - f[k+1] for k in range(len(f)-1)]
    out["G_margins"] = [mp.nstr(g, 15) for g in G]
    out["G"] = all(g >= -TOL*scale*max(1, xmax) for g in G)
    if f[0] != 0:
        out["u"] = float(f[1]/(xmax*f[0])); out["v"] = float(f[2]/(xmax**2*f[0]))
    out["all_pass"] = out["H2"] and out["G"] and out.get("H3", True)
    return out

res = []
# T1: single heavy scalar (Bellazzini et al. fn 5): c_{2n} = lam/m^{2n}; f_k = c_{2k+2}; set lam=1, m_h^2=3 (arbitrary)
lam, m2 = mpf(1), mpf(3)
f = [lam/m2**(2*k+2) for k in range(5)]
res.append(checks("T1 single scalar (linear sigma model)", f, 1/m2**2, "positive"))

# T2: type-I forward s tan(pi s) (Adams et al. eq. 27), alpha'=1
ser = taylor(lambda s: s*tan(pi*s), 0, 10)
f_series = [ser[2*k+2] for k in range(5)]
f_pf = [(2/pi)*(2**(2*k+2)-1)*zeta(2*k+2) for k in range(5)]  # partial fractions: poles at s^2=(n+1/2)^2, weight 2/pi
assert all(abs(a-b) < mpf('1e-45')*abs(b) for a, b in zip(f_series, f_pf)), "T2 cross-check failed"
r = checks("T2 type-I forward s*tan(pi s)", f_pf, mpf(4), "positive")
r["closed_form"] = "f0=pi, f1=pi^3/3, f2=2pi^5/15, f3=17pi^7/315, f4=62pi^9/2835"
r["series_vs_partial_fraction_maxrel"] = mp.nstr(max(abs(a-b)/abs(b) for a, b in zip(f_series, f_pf)), 5)
res.append(r)

# T3: type-II Regge part (Adams et al. eq. 64): coefficients of s^4, s^6, s^8
f = [-polygamma(2, 1), -polygamma(4, 1)/192, -polygamma(6, 1)/92160]
# independent cross-check from eq. (61): G(s)=lim_{t->0}[F(s,t)+64/(s t u)] = -(32/s^2) sum_k zeta(2k+1)(s/4)^{2k}
def F(s, t):
    u = -s - t
    return gamma(-s/4)*gamma(-t/4)*gamma(-u/4)/(gamma(1+s/4)*gamma(1+t/4)*gamma(1+u/4))
mp.dps = 120
s0, t0 = mpf('0.3'), mpf('1e-50')
Gnum = F(s0, t0) + 64/(s0*t0*(-s0-t0))
Gser = -(32/s0**2)*nsum(lambda k: zeta(2*k+1)*(s0/4)**(2*k), [1, inf])
mp.dps = 60
t3x = abs(Gnum-Gser)/abs(Gser)
# so -s^4 * G(s) * (1/s^2)... coefficient of s^{2k+4} in s^4*(-G) is 32 zeta(2k+3)/16^{k+1}
f_derived = [32*zeta(2*k+3)/16**(k+1) for k in range(3)]
assert all(abs(a-b) < mpf('1e-45')*abs(b) for a, b in zip(f, f_derived)), "T3 cross-check failed"
r = checks("T3 type-II Regge part (eq. 64)", f, 1/mpf(16), "positive")
r["eq61_vs_series_rel_at_s=0.3"] = mp.nstr(t3x, 5)
r["note"] = "f_k = 32 zeta(2k+3)/16^(k+1); only 3 coefficients quoted, so no H3"
res.append(r)

# T4: colour-ordered type-I, EFT-hedron eq. (3.11): a_k = zeta(k+2), x = 1/n, xmax = 1
res.append(checks("T4 Veneziano colour-ordered a_k=zeta(k+2)", [zeta(k+2) for k in range(5)], mpf(1), "positive"))

# Exact rational toy (same as Lean toy_moments): delta_{1/2} + 2 delta_{1/3} + 3 delta_1
w, x = [1, 2, 3], [mpf(1)/2, mpf(1)/3, mpf(1)]
res.append(checks("Lean toy 3-delta", [sum(a*b**k for a, b in zip(w, x)) for k in range(5)], mpf(1), "positive"))

# Counterexamples
w, x = [1, mpf(-1)/2], [mpf(1)/2, mpf(1)]
res.append(checks("C1 signed delta_{1/2} - 1/2 delta_1", [sum(a*b**k for a, b in zip(w, x)) for k in range(5)], mpf(1), "counterexample"))
res.append(checks("C2 super-soft A=c4 s^4 (c2=0)", [mpf(0), mpf(1), mpf(0)], mpf(1), "counterexample"))
w, x = [mpf(-3)/2, 3, mpf(-1)/2], [mpf(0), mpf(1), mpf(2)]
res.append(checks("C3 (post-prereg) signed, all f_k>0", [sum(a*b**k for a, b in zip(w, x)) for k in range(3)], mpf(2), "counterexample"))

ok = all(r["all_pass"] for r in res if r["kind"] == "positive")
bad = all(not r["all_pass"] for r in res if r["kind"] == "counterexample")
t1 = res[0]; sat = abs(mpf(t1["H2_gap"])) < TOL and all(abs(mpf(g)) < TOL for g in t1["G_margins"])
verdict = "PASS" if (ok and bad and sat) else "FAIL"
for r in res:
    print(json.dumps(r))
print(f"positives all pass: {ok}; counterexamples all fail: {bad}; T1 saturates H2 and G: {sat}")
print("VERDICT (script part):", verdict)
json.dump(res, open("scripts/m2b_hankel_results.json", "w"), indent=1)
