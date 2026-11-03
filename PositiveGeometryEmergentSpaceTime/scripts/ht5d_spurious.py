"""H-T5d (c): spurious-pole cancellation on internal walls at n=10 via Grothendieck residues on the 3-dim fiber.
Tile form Omega_tau(Y) = h * prod(vanishing M) / det d(Ma,Mb,Mc)/d(a,b,c) at p_tau, with
h = rho_H det(V^T V) / (det[DPhi; V^T] prod_{i=1..5} M_i)  (Lee/HW measure, gauge G2).
Orientation (disclosed deviation): each tile's form is signed to be positive at a generic interior point of that tile."""
import itertools, json, functools, random, sys
from fractions import Fraction as F
import sympy as sp, mpmath as mp
print = functools.partial(print, flush=True)
exec(open("scripts/ht5d_exact.py").read().split('if __name__')[0])
mp.mp.dps = 40
Lm = mp.matrix([[mp.mpf(x.numerator) / x.denominator for x in r] for r in LAM])
odd, even = [2*i for i in range(5)], [2*i+1 for i in range(5)]
CONS = [tuple((i + j) % 10 for j in range(5)) for i in range(10)]
def Cmp(mv): return mp.matrix(Cm(dict(zip(PAIRS, mv)), one=mp.mpf(1)))
def gauge(C):
    A = mp.matrix([[C[r, c] for c in odd] for r in range(5)]); return A**-1 * C
def O_of(mv): C = gauge(Cmp(mv)); return [C[r, c] for r in range(5) for c in even]
def jac(fun, x, nout, h=mp.mpf(10)**-15):
    J = mp.matrix(nout, len(x))
    for a in range(len(x)):
        xp = list(x); xp[a] += h; xm = list(x); xm[a] -= h
        fp, fm = fun(xp), fun(xm)
        for r in range(nout): J[r, a] = (fp[r] - fm[r]) / (2*h)
    return J
def rhoH(mv): G = jac(O_of, mv, 25); return mp.sqrt(mp.det(G.T * G))
def Mcons(mv):
    C = gauge(Cmp(mv)); return [mp.det(mp.matrix([[C[r, c] for c in cols] for r in range(5)])) for cols in CONS[:5]]
def Phi(mv):
    Y = Cmp(mv) * Lm; Yh = mp.matrix([[Y[r, c] for c in range(5)] for r in range(5)])**-1 * Y
    return [Yh[0, 5], Yh[0, 6], Yh[1, 5], Yh[1, 6], Yh[2, 5], Yh[2, 6], Yh[3, 5]]
def vanishing_classes(Z):
    Zc = {COLS[I] for I in Z}
    return sorted({i % 5 for i, cols in enumerate(CONS) if tuple(sorted(cols)) in Zc})
def tile_form(fb, abc, cls):
    m0, V = fb
    Vm = [[mp.mpf(V[r][i].numerator) / V[r][i].denominator for i in range(3)] for r in range(10)]
    M0 = [mp.mpf(x.numerator) / x.denominator for x in m0]
    mof = lambda x: [M0[r] + sum(Vm[r][i] * x[i] for i in range(3)) for r in range(10)]
    mv = mof(abc)
    Ms = Mcons(mv)
    J3 = jac(lambda x: [Mcons(mof(x))[i] for i in cls], list(abc), 3)
    D = mp.matrix(10, 10); DP = jac(Phi, mv, 7)
    for r in range(7):
        for c in range(10): D[r, c] = DP[r, c]
    for i in range(3):
        for c in range(10): D[7+i, c] = Vm[c][i]
    VtV = mp.matrix([[sum(Vm[r][i]*Vm[r][j] for r in range(10)) for j in range(3)] for i in range(3)])
    other = mp.mpf(1)
    for i in range(5):
        if i not in cls: other *= Ms[i]
    return rhoH(mv) * mp.det(VtV) / (mp.det(D) * other * mp.det(J3)), [mp.nstr(Ms[i], 5) for i in cls]
def roots_near(fb, Z, target):
    pts = solve_points(zpolys(fb, Z))
    if isinstance(pts, str) or not pts: return None
    mids = [[mp.mpf(mp.mpf(x.a) + mp.mpf(x.b)) / 2 for x in box] for box in pts]
    return min(mids, key=lambda p: sum((p[i] - target[i])**2 for i in range(3)))
def fibcoords(fb, m):
    m0, V = fb
    Vm = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r] for r in V])
    rhs = sp.Matrix([sp.Rational((m[i] - m0[i]).numerator, (m[i] - m0[i]).denominator) for i in range(10)])
    xx = (Vm.T * Vm).inv() * Vm.T * rhs
    return [mp.mpf(sp.Rational(x).p) / sp.Rational(x).q for x in xx]
def wall_test(nameA, nameB, wall_edges, rng):
    wnet = Net(5, wall_edges)
    mstar, Cw, _ = forward(wnet, [F(rng.randint(100, 900), 1000) for _ in wall_edges])
    mstar = [mstar[p] for p in PAIRS]
    iA, iB = NAMES.index(nameA), NAMES.index(nameB)
    # Orientation: sign of each tile form at a generic interior point of that tile (its own forward preimage);
    # a canonical form has no zeros or poles in the tile interior, so this sign is the tile's orientation.
    def own_sign(name, cls):
        mt, _, Yt = forward(NETS[name], [F(rng.randint(100, 900), 1000) for _ in NETS[name].edges])
        fb = fiber(Yt); x = fibcoords(fb, [mt[p] for p in PAIRS]); return mp.sign(tile_form(fb, x, cls)[0])
    w = [F(rng.randint(-500, 500), 1000) for _ in range(10)]   # generic direction; Y(eps) need not be positive
    clsA, clsB = vanishing_classes(ZS[nameA]), vanishing_classes(ZS[nameB])
    if len(clsA) != 3 or len(clsB) != 3: return {"status": f"non-simple crossing {clsA} {clsB}"}
    def forms(w, eps):
        mm = [mstar[i] + eps * w[i] for i in range(10)]
        Y = matmul(Cm(dict(zip(PAIRS, mm))), LAM); fb = fiber(Y)
        tgt = fibcoords(fb, mstar)
        pA, pB = roots_near(fb, ZS[nameA], tgt), roots_near(fb, ZS[nameB], tgt)
        if pA is None or pB is None: return None
        return tile_form(fb, pA, clsA)[0], tile_form(fb, pB, clsB)[0]
    sA, sB = own_sign(nameA, clsA), own_sign(nameB, clsB)
    rows = []
    for e in range(2, 9):
        fA, fB = forms(w, F(1, 10**e))
        a, b = sA * fA, sB * fB
        rows.append((e, mp.nstr(a, 8), mp.nstr(b, 8), mp.nstr(a + b, 8)))
        print(f"   eps=1e-{e}: Omega_A={mp.nstr(a,8)}  Omega_B={mp.nstr(b,8)}  sum={mp.nstr(a+b,8)}")
    big = [max(abs(mp.mpf(r[1])), abs(mp.mpf(r[2]))) for r in rows]; sm = [abs(mp.mpf(r[3])) for r in rows]
    grow = big[-1] / big[0]; sumchg = max(sm) / max(min(sm), mp.mpf(10)**-30)
    verdict = "PASS" if grow >= 1000 and sumchg < 10 else ("FAIL" if grow >= 1000 else "INCONCLUSIVE (no blow-up)")
    return {"status": "ok", "classes": [clsA, clsB], "rows": rows, "growth": mp.nstr(grow, 4), "sum_change": mp.nstr(sumchg, 4), "verdict": verdict}
if __name__ == "__main__":
    rule = sys.argv[1] if len(sys.argv) > 1 else "R2"
    rng = random.Random(11); out = {}
    def tree_wall(x):  # T_x with internal edge (u,v) contracted: leaves x, x+1, x+2 on v; w carries x+3, x+4
        l = [(x-1+j) % 5 + 1 for j in range(5)]
        return [(l[0], 'v'), (l[1], 'v'), (l[2], 'v'), ('w', 'v'), (l[3], 'w'), (l[4], 'w')]
    tn = lambda x: "R1b=T5" if x == 5 else f"T{x}"
    walls = {}
    if rule == "R2":
        for x in range(1, 6): walls[f"{tn(x)}|{tn((x+1) % 5 + 1)}"] = (tn(x), tn((x+1) % 5 + 1), tree_wall(x))
    else:
        walls = {"R1a|R1b=T5": ("R1a", "R1b=T5", STAR + [(1, 2)]), "R1b=T5|R1c": ("R1b=T5", "R1c", STAR + [(3, 4)]),
                 "R1a|R1c": ("R1a", "R1c", STAR + [(2, 3)])}
    for nm, (A, B, E) in walls.items():
        print(nm, "wall net", E, "tau", Net(5, E).tau())
        out[nm] = wall_test(A, B, E, rng); print("  ->", {k: v for k, v in out[nm].items() if k != "rows"})
    json.dump(out, open(f"scripts/ht5d_spurious_{rule}.json", "w"), indent=1, default=str)
