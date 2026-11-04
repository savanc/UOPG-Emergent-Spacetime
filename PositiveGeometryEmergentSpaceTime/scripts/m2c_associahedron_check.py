"""M2c exact checks for the n=5 kinematic associahedron (ABHY arXiv:1711.09102), per
prereg/M2c-associahedron-2026-10-10.md. Exact rationals (fractions) + SymPy for residues."""
import random, itertools, math, json
from fractions import Fraction as F
import sympy as sp

random.seed(20261010)
NAMES = ["X14", "X24", "X25", "X35", "X13"]          # facet k, CCW order; vertex k = facets k, k+1
def lines(c13, c14, c24):                             # X = a*x + b*y + d with x=X13, y=X14
    return [(F(0), F(1), F(0)), (F(-1), F(1), c13), (F(-1), F(0), c13 + c14),
            (F(0), F(-1), c14 + c24), (F(1), F(0), F(0))]
def Xs(L, x, y): return [a * x + b * y + d for a, b, d in L]
def m5(c, x, y):
    X14, X24, X25, X35, X13 = Xs(lines(*c), x, y)
    return 1/(X13*X14) + 1/(X14*X24) + 1/(X24*X25) + 1/(X25*X35) + 1/(X35*X13)
COMPAT = {frozenset({k, (k + 1) % 5}) for k in range(5)}

def vertices(c):
    L = lines(*c); out = {}
    for i, j in itertools.combinations(range(5), 2):
        a1, b1, d1 = L[i]; a2, b2, d2 = L[j]; det = a1 * b2 - a2 * b1
        if det == 0: continue
        x = (-d1 * b2 + d2 * b1) / det; y = (-a1 * d2 + a2 * d1) / det
        if all(v >= 0 for v in Xs(L, x, y)):
            out.setdefault((x, y), set()).update({i, j})
    return out
def ccw(pts):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    return sorted(pts, key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
def br(x, y, Z1, Z2): return (Z1[0]*Z2[1] - Z2[0]*Z1[1]) - x*(Z2[1] - Z1[1]) + y*(Z2[0] - Z1[0])
def tri(x, y, A, B, C): return br(A[0], A[1], B, C)**2 / (br(x, y, A, B) * br(x, y, B, C) * br(x, y, C, A))
def fan(poly, x, y, start=0):
    P = poly[start:] + poly[:start]
    return sum(tri(x, y, P[0], P[i], P[i + 1]) for i in range(1, len(P) - 1))
def abhy513(c, x, y):   # ABHY eq. (5.13) triangles, written in planar variables
    X14, X24, X25, X35, X13 = Xs(lines(*c), x, y)
    ABC = (X13 + X25)*(X14 + X35) / (X13*X35*(X14*X25 - X13*X35))
    ACD = (X13 + X25)**2*(X24 - X25 + X35) / (X25*(-X14*X25 - X13*X24 + X13*X25)*(X14*X25 - X13*X35))
    ADE = (X13 - X14 + X24)*(-X24 + X14 + X25) / (X14*X24*(-X14*X25 - X13*X24 + X13*X25))
    return ABC + ACD + ADE
def interior(poly):
    w = [F(random.randint(1, 9)) for _ in poly]; s = sum(w)
    return (sum(wi*p[0] for wi, p in zip(w, poly))/s, sum(wi*p[1] for wi, p in zip(w, poly))/s)

res = {"vertex_checks": 0, "identity_checks": 0, "abhy513_sign": set(), "residue_checks": 0, "failures": []}
for trial in range(25):
    c = tuple(F(random.randint(1, 30), random.randint(1, 7)) for _ in range(3))
    V = vertices(c)
    pred = [(c[0], F(0)), (c[0]+c[1], c[1]), (c[0]+c[1], c[1]+c[2]), (F(0), c[1]+c[2]), (F(0), F(0))]
    ok = len(V) == 5 and set(V) == set(pred) and all(frozenset(a) in COMPAT and len(a) == 2 for a in V.values())
    res["vertex_checks"] += ok
    if not ok: res["failures"].append(("vertices", c))
    poly = ccw(list(V))
    for _ in range(6):
        x, y = interior(poly)
        try:
            f0, f2, m, a = fan(poly, x, y, 0), fan(poly, x, y, 2), m5(c, x, y), abhy513(c, x, y)
        except ZeroDivisionError:
            continue
        if f0 == m and f2 == m: res["identity_checks"] += 1
        else: res["failures"].append(("identity", c, x, y))
        res["abhy513_sign"].add("+" if a == m else ("-" if a == -m else "neither"))

# residues on all five facets, symbolic in (c13, c14, c24) and the facet parameter
c13, c14, c24, x, y, t, e = sp.symbols("c13 c14 c24 x y t e", positive=True)
X = [y, y - x + c13, c13 + c14 - x, c14 + c24 - y, x]
M = sum(1/(X[k]*X[(k+1) % 5]) for k in range(5))
facet_param = {   # point on facet (X_k = 0) with parameter t, and a transverse direction increasing X_k
    0: ({x: t, y: 0}, (0, 1)), 1: ({x: t, y: t - c13}, (-1, 0)), 2: ({x: c13 + c14, y: t}, (-1, 0)),
    3: ({x: t, y: c14 + c24}, (0, -1)), 4: ({x: 0, y: t}, (1, 0))}
residues = {}
for k, (pt, (dx, dy)) in facet_param.items():
    sub = {x: pt[x] + e*dx, y: pt[y] + e*dy}
    Xk = sp.simplify(X[k].subs(sub)); assert sp.simplify(Xk - e) == 0
    r = sp.simplify(sp.limit((Xk*M).subs(sub), e, 0))
    prev, nxt = X[(k - 1) % 5].subs(pt), X[(k + 1) % 5].subs(pt)
    amp4 = 1/prev + 1/nxt
    Lsum = sp.simplify(prev + nxt)          # constant on the facet: segment length (-u of n=4)
    seg = Lsum/(prev*(Lsum - prev))         # canonical form of segment [0, L] in variable prev
    good = sp.simplify(r - amp4) == 0 and sp.simplify(r - seg) == 0 and not Lsum.has(t)
    residues[NAMES[k]] = {"residue": str(r), "4pt": f"1/{NAMES[(k-1)%5]} + 1/{NAMES[(k+1)%5]}", "L": str(Lsum), "ok": bool(good)}
    res["residue_checks"] += good

# counterexamples
def poly_of(c): return ccw(list(vertices(c)))
cx = (F(-1), F(2), F(1))
Pq = poly_of(cx); diffs = []
for _ in range(10):
    xq, yq = interior(Pq)
    try: diffs.append((fan(Pq, xq, yq), m5(cx, xq, yq)))
    except ZeroDivisionError: pass
counter = {
    "c13<0 (c=(-1,2,1)): vertices": [tuple(map(str, p)) for p in Pq], "n_vertices": len(Pq),
    "active facets": sorted({NAMES[i] for a in vertices(cx).values() for i in a}),
    "canonical form != m5 at all test points": all(a != b for a, b in diffs),
    "example (Omega_quad, m5)": [str(diffs[0][0]), str(diffs[0][1])],
    "c14+c24<0 (c=(1,1,-2)): vertices": len(vertices((F(1), F(1), F(-2)))),
    "c=0: vertices": [tuple(map(str, p)) for p in vertices((F(0), F(0), F(0)))],
}
soft = []
for _ in range(10):
    xs, ys = F(random.randint(1, 50), 7), F(random.randint(1, 50), 11)
    try: soft.append(m5((F(0), F(0), F(3)), xs, ys) == 0)
    except ZeroDivisionError: pass
counter["soft limit c13=c14=0: m5 == 0 at all test points"] = all(soft) and len(soft) > 0

# Catalan cross-check (n=6)
def diags(n): return [(i, j) for i in range(n) for j in range(n) if i + 1 < j and not (i == 0 and j == n - 1)]
def cross(p, q): return (p[0] < q[0] < p[1] < q[1]) or (q[0] < p[0] < q[1] < p[1])
def ntri(n): return sum(1 for s in itertools.combinations(diags(n), n - 3) if not any(cross(p, q) for p, q in itertools.combinations(s, 2)))
cat = {n: ntri(n) for n in (4, 5, 6, 7, 8)}

res["abhy513_sign"] = sorted(res["abhy513_sign"])
verdict = (res["vertex_checks"] == 25 and res["identity_checks"] >= 100 and not res["failures"]
           and res["residue_checks"] == 5 and counter["n_vertices"] == 4
           and counter["canonical form != m5 at all test points"]
           and counter["c14+c24<0 (c=(1,1,-2)): vertices"] == 0 and len(counter["c=0: vertices"]) == 1
           and counter["soft limit c13=c14=0: m5 == 0 at all test points"])
out = {"summary": res, "residues": residues, "counterexamples": counter, "triangulation_counts": cat,
       "VERDICT (script part)": "PASS" if verdict else "FAIL"}
print(json.dumps(out, indent=1, default=str))
