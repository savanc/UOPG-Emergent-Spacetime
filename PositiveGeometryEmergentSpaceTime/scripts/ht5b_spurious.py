"""H-T5b (c): spurious-pole cancellation for the n=8 tilings, per prereg (c) with the disclosed correction
Pi_{i=1..k} M_i (Lee/HW; M_{i+4} = M_i on OG so i=1..8 would square every pole)."""
import itertools, functools, json, random
from fractions import Fraction as F
import sympy as sp, mpmath as mp
print = functools.partial(print, flush=True)
src = open("scripts/ht5b_exact.py").read().split('if __name__')[0].replace('HERE = __file__.rsplit("/", 1)[0]', 'HERE = "scripts"')
G = {}; exec(src, G)
Net, forward, fiber, minor_polys, Cm, PAIRS, LAM, COLS, minors = (G[x] for x in
    ("Net", "forward", "fiber", "minor_polys", "Cm", "PAIRS", "LAM", "COLS", "minors"))
mp.mp.dps = 40
N1 = [(1, 2), (2, 3), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')]
Lm = mp.matrix([[mp.mpf(x.numerator) / x.denominator for x in r] for r in LAM])
def Cmp(m): return mp.matrix(Cm(dict(zip(PAIRS, m))))
odd, even = [0, 2, 4, 6], [2*i+1 for i in range(4)]
def gauge(C):
    A = mp.matrix([[C[r, c] for c in odd] for r in range(4)]); Ai = A**-1; return Ai * C
def O_of(m):
    C = gauge(Cmp(m)); return [C[r, c] for r in range(4) for c in even]
def rhoH(m):
    h = mp.mpf(10) ** -15; o0 = O_of(m)
    Gm = mp.matrix(16, 6)
    for a in range(6):
        mm = list(m); mm[a] += h; mm2 = list(m); mm2[a] -= h
        o1, o2 = O_of(mm), O_of(mm2)
        for r in range(16): Gm[r, a] = (o1[r] - o2[r]) / (2*h)
    return mp.sqrt(mp.det(Gm.T * Gm))
def PiM(m):
    C = gauge(Cmp(m)); p = mp.mpf(1)
    for i in range(4):
        cols = [(i + j) % 8 for j in range(4)]
        p *= mp.det(mp.matrix([[C[r, c] for c in cols] for r in range(4)]))
    return p
def Phi(m):
    Y = Cmp(m) * Lm; Yh = mp.matrix([[Y[r, c] for c in range(4)] for r in range(4)])**-1 * Y
    return [Yh[0, 4], Yh[0, 5], Yh[1, 4], Yh[1, 5], Yh[2, 4]]
def detDPhi_v(m, v):
    h = mp.mpf(10) ** -15; D = mp.matrix(6, 6)
    for a in range(6):
        mm = list(m); mm[a] += h; mm2 = list(m); mm2[a] -= h
        p1, p2 = Phi(mm), Phi(mm2)
        for r in range(5): D[r, a] = (p1[r] - p2[r]) / (2*h)
        D[5, a] = v[a]
    return mp.det(D)
def residue(m0, v, s0):
    ms = lambda s: [m0[i] + s * v[i] for i in range(6)]
    dP = mp.diff(lambda s: PiM(ms(s)), s0)
    vv = sum(x*x for x in v)
    return rhoH(ms(s0)) * vv / (detDPhi_v(ms(s0), v) * dP), dP
def roots_for(polys, Z):
    g = None
    for I in Z: g = polys[I] if g is None else sp.gcd(g, polys[I])
    return [mp.mpf(str(sp.N(r, 50))) for r in sp.Poly(g, G["s"]).real_roots()]
Zs = {"A0": frozenset(COLS.index(c) for c in [(0,1,2,3),(4,5,6,7)]), "A2": frozenset(COLS.index(c) for c in [(0,1,6,7),(2,3,4,5)]),
      "A1": frozenset(COLS.index(c) for c in [(0,1,2,7),(3,4,5,6)]), "A3": frozenset(COLS.index(c) for c in [(0,5,6,7),(1,2,3,4)])}
random.seed(7); out = {}
walls = {"HW {cell0,cell2}": (("A0", "A2"), [(2, 3), (1, 2)]),       # N1 minus both edges -> cell0 ∩ cell2
         "cyclic {cell1,cell3}": (("A1", "A3"), [(2, 'c')])}        # plus (4,c)->inf below
for name, ((ka, kb), dels) in walls.items():
    E = [e for e in N1 if e not in dels]
    if name.startswith("cyclic"):
        E = [tuple(4 if v == 'c' else v for v in e) for e in E if e != (4, 'c')]
    net = Net(4, E)
    rt = lambda: F(random.randint(100, 900), 1000)
    mstar, C, _ = forward(net, [rt() for _ in E])
    z = [COLS[I] for I, d in enumerate(minors(C)) if d == 0]
    print(name, "wall net", E, "tau", net.tau(), "zero minors", z)
    w = [F(random.randint(-500, 500), 1000) for _ in range(6)]
    rows = []
    for e in range(2, 9):
        eps = F(1, 10**e)
        m = {p: mstar[p] + eps * w[i] for i, p in enumerate(PAIRS)}
        Y = G["matmul"](Cm(m), LAM)
        fb, why = fiber(Y); P = minor_polys(*fb)
        m0 = [mp.mpf(x.numerator) / x.denominator for x in fb[0]]; v = [mp.mpf(x.numerator) / x.denominator for x in fb[1]]
        ra, rb = roots_for(P, Zs[ka]), roots_for(P, Zs[kb])
        sa, sb = min(((a, b) for a in ra for b in rb), key=lambda ab: abs(ab[0] - ab[1]))
        Ra, _ = residue(m0, v, sa); Rb, _ = residue(m0, v, sb)
        rows.append((e, float(abs(sa - sb)), mp.nstr(Ra, 8), mp.nstr(Rb, 8), mp.nstr(Ra + Rb, 8)))
        print(f"  eps=1e-{e}: |sA-sB|={float(abs(sa-sb)):.3e}  Omega_A={mp.nstr(Ra,8)}  Omega_B={mp.nstr(Rb,8)}  sum={mp.nstr(Ra+Rb,8)}")
    out[name] = rows
json.dump(out, open("scripts/ht5b_spurious.json", "w"), indent=1)
