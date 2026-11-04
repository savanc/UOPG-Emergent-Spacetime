"""H-T5b: exact (certified) membership of n=8 OMA samples in the 5-dim Ising/BCFW cells.
Method per prereg/H-T5b-exact-membership-2026-10-12.md: linear fiber in GP chart m, positroid zero sets,
exact real-root isolation + Sturm-certified signs. Run with <local path> (see requirements-lock.txt)."""
import itertools, json, sys, time, random, functools
print = functools.partial(print, flush=True)
from fractions import Fraction as F
import numpy as np, sympy as sp, mpmath as mp
HERE = __file__.rsplit("/", 1)[0]
src = open(f"{HERE}/ht5_tiling.py").read(); head = src[:src.index("def Lam")]
g = {"__name__": "ht5head", "__file__": f"{HERE}/ht5_tiling.py"}; exec(head, g)
Net = g["Net"]
n, k = 4, 4
PAIRS = list(itertools.combinations(range(1, 5), 2))
COLS = list(itertools.combinations(range(8), 4))
LAM = [[F(x) ** p for p in range(6)] for x in range(1, 9)]          # 8 x 6 moment curve

def corr_exact(net, t):
    num = {}; Z = F(0)
    for mask, key in net.subs:
        w = F(1)
        for i in range(len(net.edges)):
            if mask >> i & 1: w *= t[i]
        if key is None: Z += w
        else: num[key] = num.get(key, F(0)) + w
    return {p: num.get(p, F(0)) / Z for p in PAIRS}
def Cm(m):  # GP matrix, m: dict pair->value (any ring)
    M = [[0] * 8 for _ in range(4)]
    for i in range(1, 5):
        for j in range(1, 5):
            if i == j: M[i-1][2*i-2] = M[i-1][2*i-1] = 1
            else:
                v = (-1) ** (i + j + (1 if i < j else 0)) * m[(min(i, j), max(i, j))]
                M[i-1][2*j-2] = v; M[i-1][2*j-1] = -v
    return M
def det(A):  # exact Bareiss-free Laplace for small (<=4) with Fractions
    A = [list(r) for r in A]; N = len(A); d = F(1)
    for c in range(N):
        p = next((r for r in range(c, N) if A[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c + 1, N):
            f = A[r][c] / A[c][c]
            if f: A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return d
def minors(C): return [det([[C[r][c] for c in I] for r in range(4)]) for I in COLS]
def matmul(A, B): return [[sum(a * b for a, b in zip(r, col)) for col in zip(*B)] for r in A]
def forward(net, t): m = corr_exact(net, t); C = Cm(m); return m, C, matmul(C, LAM)

msym = {p: sp.Symbol(f"m{p[0]}{p[1]}") for p in PAIRS}; mvec = [msym[p] for p in PAIRS]
s = sp.Symbol("s")
def fiber(Y):
    Ys = sp.Matrix(Y); ker = Ys.nullspace()
    if len(ker) != 2: return None, "kerdim%d" % len(ker)
    lt = sp.Matrix(LAM) * sp.Matrix.hstack(*ker)                  # 8 x 2
    eqs = list(sp.Matrix(Cm(msym)) * lt)
    A, b = sp.linear_eq_to_matrix(eqs, mvec)
    r = A.rank()
    if r != 5: return None, "rank%d" % r
    sol = A.gauss_jordan_solve(b)
    x, par = sol[0], sol[1]
    x0 = x.subs({q: 0 for q in par}); v = x.subs({q: 1 for q in par}) - x0
    return ([F(int(sp.fraction(e)[0]), int(sp.fraction(e)[1])) for e in x0],
            [F(int(sp.fraction(e)[0]), int(sp.fraction(e)[1])) for e in v]), "ok"
def minor_polys(m0, v):
    pts = [F(j) for j in range(5)]
    vals = [minors(Cm({p: m0[i] + q * v[i] for i, p in enumerate(PAIRS)})) for q in pts]
    polys = []
    for I in range(70):
        polys.append(sp.Poly(sp.interpolate(list(zip([sp.Rational(q.numerator, q.denominator) for q in pts],
                     [sp.Rational(vv[I].numerator, vv[I].denominator) for vv in vals])), s), s))
    return polys
def certified_sign(P, fac, a, b):
    """sign of P at the unique root of irreducible fac in [a,b]; 0 if fac | P."""
    if P.is_zero: return 0, a, b
    if P.rem(fac).is_zero: return 0, a, b
    for _ in range(200):
        if P.count_roots(a, b) == 0:
            mid = (a + b) / 2; val = P.eval(mid); return (1 if val > 0 else -1), a, b
        mid = (a + b) / 2
        if fac.eval(mid) == 0: a = b = mid; continue
        if fac.count_roots(a, mid) > 0: b = mid
        else: a = mid
    return None, a, b
def membership(polys, Z):
    """Return (in_cell: 0/1/None, root info). Z = frozenset of minor indices zero on the cell."""
    gz = None
    for I in Z:
        gz = polys[I] if gz is None else sp.gcd(gz, polys[I])
    if gz is None or gz.is_zero: return None, "gcd0"
    if gz.degree() == 0: return 0, "noroot"
    found = 0; unc = False; roots = []
    for fac, _ in gz.factor_list()[1]:
        for (a, b), _m in fac.intervals():
            a, b = sp.Rational(a), sp.Rational(b); ok = True
            for I in range(70):
                if I in Z: continue
                sg, a, b = certified_sign(polys[I], fac, a, b)
                if sg is None: unc = True; ok = False; break
                if sg <= 0: ok = False; break
            if ok: found = 1; roots.append((fac.as_expr(), float((a + b) / 2)))
    if found: return 1, roots
    return (None if unc else 0), "uncertified" if unc else "certified-out"

def rat(x, D=10**12): return F(x).limit_denominator(D)
if __name__ == "__main__":
    T0 = time.time(); random.seed(2026); out = {}
    tops = {"N1": [(1, 2), (2, 3), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')],
            "N2": [(1, 'd'), (2, 'd'), ('d', 'c'), ('c', 3), ('c', 4), (2, 3)],
            "N3": [(1, 'd'), (2, 'd'), (2, 3), ('d', 3), ('d', 4), (3, 4)]}
    # realising networks of the four 5-dim cells (from H-T5 provenance, N1 only)
    cellnets = {(4, 6, 7, 1, 8, 2, 3, 5): ("N1", (2, 3), "0"), (5, 6, 8, 7, 1, 2, 4, 3): ("N1", (4, 'c'), "inf"),
                (5, 7, 6, 8, 1, 3, 2, 4): ("N1", (1, 2), "0"), (6, 5, 7, 8, 2, 1, 3, 4): ("N1", (2, 'c'), "0")}
    taus = sorted(cellnets)
    def degen(E, e, lim):
        i = E.index(e)
        if lim == "0": return [x for j, x in enumerate(E) if j != i]
        a, b = e; keep, gone = (a, b) if isinstance(a, int) else (b, a)
        return [tuple(keep if v == gone else v for v in x) for j, x in enumerate(E) if j != i]
    nets = {t: Net(4, degen(tops[G], e, lim)) for t, (G, e, lim) in cellnets.items()}
    for t in taus: assert nets[t].tau() == t, (t, nets[t].tau())
    rt = lambda: F(random.randint(1, 999), 1000)
    Zs = {}
    for t in taus:
        zs = [frozenset(I for I, d in enumerate(minors(forward(nets[t], [rt() for _ in nets[t].edges])[1])) if d == 0) for _ in range(2)]
        assert zs[0] == zs[1]; Zs[t] = zs[0]
        print("cell", t, "zero minors:", len(Zs[t]), [COLS[I] for I in sorted(Zs[t])])
    topZ = frozenset(I for I, d in enumerate(minors(forward(Net(4, tops["N1"]), [rt() for _ in range(6)])[1])) if d == 0)
    print("top cell zero minors:", len(topZ))
    # positivity sanity: forward points have all minors >= 0 (GP positive branch)
    def classify(Y):
        fb, why = fiber(Y)
        if fb is None: return None, why
        P = minor_polys(*fb)
        res = []
        for t in taus:
            mem, info = membership(P, Zs[t]); res.append(mem)
        return res, "ok"
    # ---- validation gate: 40 forward points, 10 per cell ----
    mp.mp.dps = 40; gate = True; maxerr = mp.mpf(0)
    for c, t in enumerate(taus):
        for _ in range(10):
            m, C, Y = forward(nets[t], [rt() for _ in nets[t].edges])
            assert all(d >= 0 for d in minors(C))
            fb, why = fiber(Y); P = minor_polys(*fb); Z = Zs[t]
            gz = None
            for I in Z: gz = P[I] if gz is None else sp.gcd(gz, P[I])
            rr = [r for r in gz.real_roots() if r.is_Rational]
            errs = [max(abs(mp.mpf(sp.Rational(fb[0][i] + sp.Rational(r) * fb[1][i]).p) / sp.Rational(fb[0][i] + sp.Rational(r) * fb[1][i]).q - mp.mpf(m[p].numerator) / m[p].denominator) for i, p in enumerate(PAIRS)) for r in rr]
            e = min(errs) if errs else mp.inf; maxerr = max(maxerr, e)
            res, _ = classify(Y)
            if e != 0 or res is None or res[c] != 1: gate = False; print("GATE FAIL", t, e, res)
    print("validation gate:", "PASS" if gate else "FAIL", " max round-trip error (40 dps):", mp.nstr(maxerr, 5))
    out["gate"] = gate
    if not gate: json.dump(out, open(f"{HERE}/ht5b_exact.json", "w")); sys.exit(1)
    # ---- samples ----
    sets = {}
    U = json.load(open(f"{HERE}/ht5_R200_u.json"))
    sets["R200"] = [forward(Net(4, tops["N1"]), [rat(float(np.tanh(np.exp(u)))) for u in us])[2] for us in U]
    # Uniform-in-m on the positive region. By GP the region lies in (0,1)^6 (ferromagnetic correlations), so rejection
    # from [0,1]^6 has the same distribution as rejection from the prereg box [-1,1]^6, with 64x the acceptance (deviation disclosed).
    fu, tries = [], 0
    rngf = np.random.default_rng(2026)
    while len(fu) < 1000:
        mm = rngf.integers(0, 10**6, size=(200000, 6)) / 10**6; tries += 200000
        Cf = np.array([Cm(dict(zip(PAIRS, r))) for r in mm[:1]], dtype=float)  # shape check
        CC = np.zeros((len(mm), 4, 8))
        for i in range(1, 5):
            for j in range(1, 5):
                if i == j: CC[:, i-1, 2*i-2] = CC[:, i-1, 2*i-1] = 1
                else:
                    v = (-1) ** (i + j + (1 if i < j else 0)) * mm[:, PAIRS.index((min(i, j), max(i, j)))]
                    CC[:, i-1, 2*j-2] = v; CC[:, i-1, 2*j-1] = -v
        mn = np.min(np.stack([np.linalg.det(CC[:, :, list(I)]) for I in COLS]), 0)
        for row in mm[mn > -1e-9]:
            mq = {p: F(int(round(x * 10**6)), 10**6) for p, x in zip(PAIRS, row)}; C = Cm(mq)
            if all(d > 0 for d in minors(C)): fu.append(matmul(C, LAM))
            if len(fu) == 1000: break
    print("F-unif acceptance:", 1000, "/", tries); out["funif_tries"] = tries
    sets["F-unif"] = fu
    sets["F-net"] = [forward(Net(4, tops[G]), [rt() for _ in range(6)])[2] for G in ("N2", "N3") for _ in range(250)]
    B = []
    for _ in range(100):
        tt = [rt() for _ in range(6)]; tt[random.randrange(6)] = random.choice([F(1, 10**6), 1 - F(1, 10**6)])
        B.append(forward(Net(4, tops["N1"]), tt)[2])
    sets["B-near"] = B
    sets["B-on"] = [forward(nets[taus[i % 4]], [rt() for _ in range(5)])[2] for i in range(20)]
    results = {}
    for name, Ys in sets.items():
        R = []
        for Y in Ys: R.append(classify(Y)[0])
        results[name] = R
        pat = {}
        for r in R: pat[str(r)] = pat.get(str(r), 0) + 1
        print(f"{name}: N={len(R)} patterns {pat}  ({time.time()-T0:.0f}s)", flush=True)
    out["results"] = results
    main = [r for nm in ("R200", "F-unif", "F-net") for r in results[nm]]
    good = [r for r in main if r is not None and None not in r]
    print("main certified non-degenerate:", len(good), "of", len(main))
    for a, b in itertools.combinations(range(4), 2):
        both = sum(1 for r in good if r[a] and r[b]); neither = sum(1 for r in good if not r[a] and not r[b])
        print(f"pair {taus[a]} {taus[b]}: both {both} neither {neither}  -> {'TILES' if both == neither == 0 and len(good)==len(main) else 'no'}"
              + (f"  95% UB uncovered 3/N = {3/len(good):.4f}" if neither == 0 else ""))
    # R200 vs H-T5
    json.dump(out, open(f"{HERE}/ht5b_exact.json", "w"), default=str)
