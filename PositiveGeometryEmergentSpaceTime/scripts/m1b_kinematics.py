"""M1b B3: exact rational kinematic configurations (prereg prereg/M1b-slice-bridge-2026-10-11.md).
(1,3) mostly-minus, all incoming, s_ij = (p_i+p_j)^2. (2,2): p_i = lambda_i lambdatilde_i^T, s = det(sum)."""
from fractions import Fraction as F
import random, itertools
random.seed(11)
dot = lambda p, q: p[0]*q[0]-p[1]*q[1]-p[2]*q[2]-p[3]*q[3]
add = lambda *ps: tuple(sum(c) for c in zip(*ps))
sq = lambda p: dot(p, p)
def nullvec(E, a, b):  # E (1, nhat), nhat from stereographic rational point
    d = a*a+b*b+1
    return (E, E*2*a/d, E*2*b/d, E*(a*a+b*b-1)/d)
def planar(ps):
    n = len(ps); out = {}
    for i in range(n):
        for L in range(2, n-1):
            idx = [(i+k) % n for k in range(L)]
            key = tuple(sorted(idx)); comp = tuple(sorted(set(range(n))-set(idx)))
            if comp in out or key in out: continue
            out[key] = sq(add(*[ps[j] for j in idx]))
    return out
def rq(): return F(random.randint(-6, 6), random.randint(1, 4))
def close_pair(P, a, b):  # p5 + p6 = P, p5 = E(1,nhat), p6 null
    n5 = nullvec(F(1), a, b); den = 2*dot(P, n5)
    if den == 0: return None
    E = sq(P)/den; p5 = tuple(E*c for c in n5); p6 = tuple(x-y for x, y in zip(P, p5))
    return p5, p6
# n = 4 example
p1 = (F(5), F(0), F(0), F(5)); p3 = (F(5), F(0), F(0), F(-5)); p2 = (F(-5), F(-3), F(0), F(-4)); p4 = (F(-5), F(3), F(0), F(4))
assert all(sq(p) == 0 for p in (p1, p2, p3, p4)) and add(p1, p2, p3, p4) == (0, 0, 0, 0)
print("n=4 (1,3):", [list(map(int, p)) for p in (p1, p2, p3, p4)], "s =", sq(add(p1, p2)), "t =", sq(add(p2, p3)), "u =", sq(add(p1, p3)))
# n = 6 alternating search
found = None
for trial in range(200000):
    ps = [nullvec(F(random.randint(1, 6)) * (1 if k % 2 == 0 else -1), rq(), rq()) for k in range(4)]
    P = tuple(-c for c in add(*ps))
    r = close_pair(P, rq(), rq())
    if r is None: continue
    p5, p6 = r
    if not (p5[0] > 0 and p6[0] < 0): continue
    full = ps + [p5, p6]
    pl = planar(full)
    if all(v < 0 for v in pl.values()):
        found = full; break
print("n=6 (1,3) all-Euclidean:", "FOUND" if found else "not found in 200000 trials")
if found:
    for p in found: print("   ", [str(c) for c in p])
    print("   planar:", {k: str(v) for k, v in planar(found).items()})
# (2,2) n = 5 real spinors
def det2(a, b): return a[0]*b[1]-a[1]*b[0]
def nullspace_int(lam):  # lam: 2 x 5 integer rows -> basis of rational nullspace (3 vectors)
    import sympy as sp
    M = sp.Matrix(lam); ns = M.nullspace()
    return [[F(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in v] for v in ns]
res22 = {}
for want in ['pos', 'neg']:
    for trial in range(20000):
        lam = [[random.randint(-4, 4) for _ in range(5)] for _ in range(2)]
        ns = nullspace_int(lam)
        if len(ns) != 3: continue
        c = [[random.randint(-3, 3) for _ in range(3)] for _ in range(2)]
        lt = [[sum(c[r][k]*ns[k][i] for k in range(3)) for i in range(5)] for r in range(2)]
        L = [(F(lam[0][i]), F(lam[1][i])) for i in range(5)]; Lt = [(lt[0][i], lt[1][i]) for i in range(5)]
        s = [det2(L[i], L[(i+1) % 5])*det2(Lt[i], Lt[(i+1) % 5]) for i in range(5)]
        if (want == 'pos' and all(x > 0 for x in s)) or (want == 'neg' and all(x < 0 for x in s)):
            # check momentum conservation exactly
            mom = [[sum(L[i][a]*Lt[i][b] for i in range(5)) for b in range(2)] for a in range(2)]
            assert all(v == 0 for row in mom for v in row)
            res22[want] = (L, Lt, s); break
    print(f"n=5 (2,2) all planar {want}:", "FOUND" if want in res22 else "not found")
    if want in res22:
        L, Lt, s = res22[want]
        print("   lambda  =", [[str(x) for x in v] for v in L]); print("   ltilde  =", [[str(x) for x in v] for v in Lt]); print("   s_{i,i+1} = <i,i+1>[i,i+1] =", [str(x) for x in s])
