"""H-T5d: certified membership at n=10 (k=5) for rules R1 (neighbour cuts) and R2 (tree networks).
Method per prereg/H-T5d-neighbour-rule-n10-2026-10-12.md: exact affine 3-plane fiber in GP coordinates,
lex Groebner basis of the cell's zero-minor ideal, exact real-root isolation, rigorous interval (mpmath iv) signs."""
import itertools, json, sys, time, random, functools, multiprocessing as mpr
from fractions import Fraction as F
import numpy as np, sympy as sp, mpmath as mp, flint
print = functools.partial(print, flush=True)
src = open("scripts/ht5_tiling.py").read(); head = src[:src.index("def Lam")]
g = {"__name__": "ht5head"}; exec(head, g); Net = g["Net"]
K = 5; PAIRS = list(itertools.combinations(range(1, K+1), 2)); COLS = list(itertools.combinations(range(2*K), K))
LAM = [[F(x) ** p for p in range(K+2)] for x in range(1, 2*K+1)]
iv = mp.iv; iv.dps = 80

def corr(net, t):
    num = {}; Z = F(0)
    for mask, key in net.subs:
        w = F(1)
        for i in range(len(net.edges)):
            if mask >> i & 1: w *= t[i]
        if key is None: Z += w
        else: num[key] = num.get(key, F(0)) + w
    return {p: num.get(p, F(0)) / Z for p in PAIRS}
def Cm(m, one=1):
    M = [[0*one] * (2*K) for _ in range(K)]
    for i in range(1, K+1):
        for j in range(1, K+1):
            if i == j: M[i-1][2*i-2] = M[i-1][2*i-1] = one
            else:
                v = (-1) ** (i + j + (1 if i < j else 0)) * m[(min(i, j), max(i, j))]
                M[i-1][2*j-2] = v; M[i-1][2*j-1] = -v
    return M
def det_exact(A):
    A = [list(r) for r in A]; N = len(A); d = F(1)
    for c in range(N):
        p = next((r for r in range(c, N) if A[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c+1, N):
            f = A[r][c] / A[c][c]
            if f: A[r] = [a - f*b for a, b in zip(A[r], A[c])]
    return d
def det_generic(A):  # Laplace with memo over column subsets (works for flint polys and iv)
    N = len(A); memo = {}
    def rec(row, cols):
        if row == N: return 1
        key = (row, cols)
        if key in memo: return memo[key]
        s = 0; sign = 1
        for idx, c in enumerate(cols):
            if A[row][c] != 0:
                term = A[row][c] * rec(row+1, cols[:idx] + cols[idx+1:])
                s = s + term if sign > 0 else s - term
            sign = -sign
        memo[key] = s; return s
    return rec(0, tuple(range(N)))
def minors_exact(C): return [det_exact([[C[r][c] for c in I] for r in range(K)]) for I in COLS]
def matmul(A, B): return [[sum(a*b for a, b in zip(r, col)) for col in zip(*B)] for r in A]
def forward(net, t): m = corr(net, t); C = Cm(m); return m, C, matmul(C, LAM)

R = flint.fmpq_mpoly_ctx.get(("a", "b", "c"), "lex")
A_, B_, C_ = R.gens()
sa, sb, sc = sp.symbols("a b c")
def fq(x): return flint.fmpq(x.numerator, x.denominator)
def fiber(Y):
    Ys = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r] for r in Y]); ker = Ys.nullspace()
    if len(ker) != 2: return None
    lt = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r] for r in LAM]) * sp.Matrix.hstack(*ker)
    ms = {p: sp.Symbol(f"m{p[0]}{p[1]}") for p in PAIRS}; mv = [ms[p] for p in PAIRS]
    A, b = sp.linear_eq_to_matrix(list(sp.Matrix(Cm(ms)) * lt), mv)
    if A.rank() != 7: return None
    x, par = A.gauss_jordan_solve(b)
    if len(par) != 3: return None
    x0 = x.subs({q: 0 for q in par})
    V = [x.subs({q: (1 if j == i else 0) for j, q in enumerate(par)}) - x0 for i in range(3)]
    tofrac = lambda e: F(int(sp.fraction(e)[0]), int(sp.fraction(e)[1]))
    return [tofrac(e) for e in x0], [[tofrac(V[i][r]) for i in range(3)] for r in range(10)]
def zpolys(fb, Z):
    m0, V = fb
    mpoly = {p: fq(m0[r]) + fq(V[r][0]) * A_ + fq(V[r][1]) * B_ + fq(V[r][2]) * C_ for r, p in enumerate(PAIRS)}
    Cp = Cm(mpoly, one=R.from_dict({(0, 0, 0): 1}))
    out = []
    for I in Z:
        d = det_generic([[Cp[r][c] for c in COLS[I]] for r in range(K)])
        out.append(sp.sympify(str(d).replace("^", "**"), locals={"a": sa, "b": sb, "c": sc}))
    return out
def ivq(x): return iv.mpf([sp.Rational(x).p, sp.Rational(x).p]) / sp.Rational(x).q if False else iv.mpf(x.p) / iv.mpf(x.q)
st = sp.Symbol("st")
def ev(e, subs):
    P = sp.Poly(e, *subs.keys()); tot = iv.mpf(0)
    for mon, co in P.terms():
        co = sp.Rational(co); t = iv.mpf(co.p) / iv.mpf(co.q)
        for var_val, pw in zip(subs.values(), mon): t = t * var_val ** pw
        tot = tot + t
    return tot
def solve_points(polys):
    """Real solutions as rigorous interval boxes (a,b,c), via a separating linear form st = c + l1 a + l2 b
    and a lex Groebner basis in shape position {a - A(st), b - B(st), c - C(st), g(st)}. Flags: posdim / notshape."""
    G0 = sp.groebner(polys, sa, sb, sc, order="grevlex")
    if list(G0.exprs) == [1]: return []
    if not G0.is_zero_dimensional: return "posdim"
    for (l1, l2) in [(2, 3), (5, -7), (11, 13), (-17, 19), (23, 29)]:
        Gb = sp.groebner(list(G0.exprs) + [st - sc - l1*sa - l2*sb], sa, sb, sc, st, order="lex")
        ex = list(Gb.exprs)
        uni = [e for e in ex if e.free_symbols <= {st}]
        lin = {}
        for v in (sa, sb, sc):
            cand = [e for e in ex if v in e.free_symbols and e.free_symbols <= {v, st} and sp.degree(e, v) == 1]
            if cand: lin[v] = cand[0]
        if len(uni) != 1 or len(lin) != 3: continue
        pu = sp.Poly(uni[0], st)
        if sp.degree(sp.gcd(pu, pu.diff(st))) > 0: continue          # non-radical: try another form
        boxes = []; bad = False
        for (l, r), _m in pu.intervals(eps=sp.Rational(1, 10**45)):
            l, r = sp.Rational(l), sp.Rational(r)
            lI, rI = iv.mpf(l.p) / iv.mpf(l.q), iv.mpf(r.p) / iv.mpf(r.q); tI = iv.mpf([lI.a, rI.b])
            vals = []
            for v in (sa, sb, sc):
                co = sp.Poly(lin[v], v).all_coeffs()
                den = ev(co[0], {st: tI})
                if 0 in den: bad = True; break
                vals.append(-ev(co[1], {st: tI}) / den)
            if bad: break
            boxes.append(tuple(vals))
        if not bad: return boxes
    return "notshape"
def classify_cell(fb, Z, Zset):
    pts = solve_points(zpolys(fb, Z))
    if isinstance(pts, str): return None, pts
    m0, V = fb; unc = False
    for (aI, bI, cI) in pts:
        mI = {p: iv.mpf(m0[r].numerator) / m0[r].denominator + (iv.mpf(V[r][0].numerator) / V[r][0].denominator) * aI
              + (iv.mpf(V[r][1].numerator) / V[r][1].denominator) * bI + (iv.mpf(V[r][2].numerator) / V[r][2].denominator) * cI
              for r, p in enumerate(PAIRS)}
        CI = Cm(mI, one=iv.mpf(1)); ok = True; u = False
        for I, cols in enumerate(COLS):
            if I in Zset: continue
            d = det_generic([[CI[r][c] for c in cols] for r in range(K)])
            if d.a > 0: continue
            ok = False
            if d.b >= 0: u = True
            break
        if ok: return 1, "in"
        unc = unc or u
    return (None, "uncertified") if unc else (0, "out")

STAR = [(i, 'c') for i in range(1, 6)]
W5 = STAR + [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
def tree(x):
    l = [(x-1+j) % 5 + 1 for j in range(5)]
    return [(l[0], 'v'), ('u', 'v'), ('w', 'v'), (l[1], 'u'), (l[2], 'u'), (l[3], 'w'), (l[4], 'w')]
CELLNETS = {"R1a": STAR + [(1, 2), (2, 3)], "R1b=T5": STAR + [(1, 2), (3, 4)], "R1c": STAR + [(2, 3), (3, 4)],
            "T1": tree(1), "T2": tree(2), "T3": tree(3), "T4": tree(4)}
RULES = {"R1": ["R1a", "R1b=T5", "R1c"], "R2": ["T1", "T2", "T3", "T4", "R1b=T5"]}
NAMES = list(CELLNETS)
NETS = {k: Net(5, E) for k, E in CELLNETS.items()}
ZS = {}
def setup():
    rnd = random.Random(99)
    for k in NAMES:
        zs = []
        for _ in range(2):
            _, C, _ = forward(NETS[k], [F(rnd.randint(1, 999), 1000) for _ in NETS[k].edges])
            zs.append(tuple(I for I, d in enumerate(minors_exact(C)) if d == 0))
        assert zs[0] == zs[1], k; ZS[k] = zs[0]
setup()
def classify(Y):
    fb = fiber(Y)
    if fb is None: return None
    return [classify_cell(fb, ZS[k], set(ZS[k]))[0] for k in NAMES]
def job(arg):
    name, idx, Y = arg
    try: return name, idx, classify(Y)
    except Exception as e: return name, idx, "ERR " + repr(e)

if __name__ == "__main__":
    T0 = time.time(); out = {"cells": {k: str(NETS[k].tau()) for k in NAMES}, "Zsizes": {k: len(ZS[k]) for k in NAMES}}
    for k in NAMES: print(k, NETS[k].tau(), "|Z| =", len(ZS[k]))
    print("W5 tau", Net(5, W5).tau())
    # ---- validation gate ----
    rnd = random.Random(5); gate = True
    for c, k in enumerate(NAMES):
        for _ in range(8):
            m, C, Y = forward(NETS[k], [F(rnd.randint(1, 999), 1000) for _ in NETS[k].edges])
            assert all(d >= 0 for d in minors_exact(C))
            fb = fiber(Y); m0, V = fb
            # exact coordinates of the forward point on the fiber
            Vm = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r] for r in V])
            rhs = sp.Matrix([sp.Rational((m[p] - m0[r]).numerator, (m[p] - m0[r]).denominator) for r, p in enumerate(PAIRS)])
            xx = (Vm.T * Vm).inv() * Vm.T * rhs
            onfib = Vm * xx == rhs
            polys = zpolys(fb, ZS[k]); Gb = sp.groebner(polys, sa, sb, sc, order="lex")
            root = all(sp.simplify(e.subs({sa: xx[0], sb: xx[1], sc: xx[2]})) == 0 for e in Gb.exprs)
            res = classify(Y)
            if not (onfib and root and res[c] == 1): gate = False; print("GATE FAIL", k, onfib, root, res)
    print(f"validation gate: {'PASS' if gate else 'FAIL'} ({time.time()-T0:.0f}s)"); out["gate"] = gate
    if not gate: json.dump(out, open("scripts/ht5d_exact.json", "w"), indent=1); sys.exit(1)
    # ---- samples ----
    rs = random.Random(2026); W5net = Net(5, W5); jobs = []
    for i in range(600): jobs.append(("F-W5u", i, forward(W5net, [F(rs.randint(1, 999), 1000) for _ in range(10)])[2]))
    for i in range(400):
        t = [F(float(np.tanh(np.exp(rs.uniform(-4, 2))))).limit_denominator(10**12) for _ in range(10)]
        jobs.append(("F-W5log", i, forward(W5net, t)[2]))
    for i in range(100):
        t = [F(rs.randint(1, 999), 1000) for _ in range(10)]; t[rs.randrange(10)] = rs.choice([F(1, 10**6), 1 - F(1, 10**6)])
        jobs.append(("B-near", i, forward(W5net, t)[2]))
    for i, k in enumerate(NAMES * 2):
        jobs.append(("B-on", i, forward(NETS[k], [F(rs.randint(1, 999), 1000) for _ in NETS[k].edges])[2]))
    res = {}
    with mpr.Pool(4) as pool:
        for n_done, (name, idx, r) in enumerate(pool.imap_unordered(job, jobs, chunksize=4)):
            res.setdefault(name, {})[idx] = r
            if n_done % 100 == 0: print(f"  {n_done}/{len(jobs)} done ({time.time()-T0:.0f}s)")
    out["results"] = {nm: [res[nm][i] for i in sorted(res[nm])] for nm in res}
    for nm, R_ in out["results"].items():
        pat = {}
        for r in R_: pat[str(r)] = pat.get(str(r), 0) + 1
        print(f"{nm}: N={len(R_)} patterns {pat}")
    main = out["results"]["F-W5u"] + out["results"]["F-W5log"]
    for rule, tiles in RULES.items():
        ix = [NAMES.index(t) for t in tiles]
        cert = [r for r in main if isinstance(r, list) and all(r[i] is not None for i in ix)]
        over = sum(1 for r in cert if sum(r[i] for i in ix) >= 2); miss = sum(1 for r in cert if sum(r[i] for i in ix) == 0)
        hist = np.bincount([sum(r[i] for i in ix) for r in cert], minlength=len(tiles)+1).tolist()
        print(f"{rule} tiles {tiles}: certified {len(cert)}/{len(main)}; overlaps {over}; misses {miss}; count histogram {hist}"
              + (f"; 95% UB uncovered 3/N = {3/len(cert):.4f}" if miss == 0 and cert else ""))
        out[rule] = dict(certified=len(cert), N=len(main), overlaps=over, misses=miss, hist=hist)
        for nm in ("B-near", "B-on"):
            rr = [r for r in out["results"][nm] if isinstance(r, list) and all(r[i] is not None for i in ix)]
            print(f"   {nm}: certified {len(rr)}, count histogram {np.bincount([sum(r[i] for i in ix) for r in rr], minlength=len(tiles)+1).tolist()}")
    print(f"total {time.time()-T0:.0f}s")
    json.dump(out, open("scripts/ht5d_exact.json", "w"), indent=1, default=str)
