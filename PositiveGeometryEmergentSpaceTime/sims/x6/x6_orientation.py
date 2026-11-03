#!/usr/bin/env python3
"""X6 / XD-6 / R2 locked checker (chirality_orientation).
(a) parity duality Gr+(k,n) -> Gr+(n-k,n): orthogonal complement + alternating column signs (Marsh-Scott/Galashin-Lam twist)
    keeps all maximal minors of one sign; (b) cyclic reflection i -> n+1-i keeps Gr+ (projectively);
(c) vector-like spectra satisfy all four ACC sums identically; (d) one-generation ACC branch (y_Q=1):
    charge multiset closed under negation (vector-like) iff N_c = 1, for N_c = 1..9.
Usage: x6_orientation.py {planted|broken|live}"""
import sys, itertools, numpy as np, sympy as sp
def tp(k, n, seed):  # totally positive k x n: Vandermonde rows x_j^i, 0<x_1<...<x_n
    x = np.sort(np.random.default_rng(seed).uniform(0.2, 3, n)); return np.array([x**i for i in range(k)])
def minors(M):
    k = M.shape[0]; return [np.linalg.det(M[:, list(c)]) for c in itertools.combinations(range(M.shape[1]), k)]
def onesign(v, tol=1e-9): v = np.array(v); return bool(np.all(v > tol) or np.all(v < -tol))
def dual(M, twist=True):
    n = M.shape[1]; _, _, Vt = np.linalg.svd(M); C = Vt[M.shape[0]:]
    return C * np.array([(-1)**j for j in range(n)]) if twist else C
def reflect(M): return M[:, ::-1]
CASES = [(1,3),(1,4),(2,4),(2,5),(3,6),(2,6),(3,7)]
def parity_ok(twist): return {c: onesign(minors(dual(tp(*c, s), twist))) for c in CASES for s in [0]}
y = sp.symbols('y0:5'); m = sp.symbols('m0:5')
def vl_sums():
    ys = list(y) + [-t for t in y]; ms = list(m) * 2
    return [sp.expand(sum(mi*yi**p for mi, yi in zip(ms, ys))) for p in (1, 3)]
def branch(N):  # (mult, charge) with y_Q = 1, branch y_u = N-1
    return sorted([1]*(2*N) + [N-1]*N + [-N-1]*N + [-N]*2 + [2*N])
def vectorlike(N): b = branch(N); return b == sorted(-t for t in b)
mode = sys.argv[1]
if mode == 'planted':
    p = parity_ok(True); r = {c: onesign(minors(reflect(tp(*c, 1)))) for c in CASES}
    ok = all(p.values()) and all(r.values()) and vl_sums() == [0, 0] and vectorlike(1)
    print("parity", p, "\nreflect", r, "\nVL sums", vl_sums(), "\nN_c=1 vectorlike", vectorlike(1), "\nrecovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':  # untwisted complement must fail positivity somewhere
    p = parity_ok(False); print("untwisted", p)
    if not all(p.values()): raise SystemExit("REJECT: untwisted complement not positive")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'live':
    for s in range(20):
        for c in CASES:
            assert onesign(minors(dual(tp(*c, s)))) and onesign(minors(reflect(tp(*c, s)))), (c, s)
    print("parity+reflection preserve Gr+ on", len(CASES), "cases x 20 seeds: True")
    print("vector-like ACC sums:", vl_sums())
    for N in range(1, 10): print(f"N_c={N}: vectorlike={vectorlike(N)} witten_ok={(N+1)%2==0}")
