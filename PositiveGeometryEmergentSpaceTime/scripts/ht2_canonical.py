"""H-T2 (c): canonical-form checks for E_2, E_3, plus the face counts of E_3, E_4 from matchings (prereg H-T2)."""
import sympy as sp, itertools
from collections import Counter
a, b, c = sp.symbols('a b c', positive=True)
S = a + b + c
x12, x13, x23 = a*b/S, a*c/S, b*c/S          # Y -> Delta (response) conductances
# log-Jacobian det( d log x / d log a ) : dlog x12^dlog x13^dlog x23 = R * dlog a^dlog b^dlog c
xs, ys = [x12, x13, x23], [a, b, c]
J = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(sp.log(xs[i]), ys[j]) * ys[j]))
R = sp.factor(sp.simplify(J.det()))
print("log-Jacobian matrix:", J.applyfunc(sp.factor).tolist())
print("R = det =", R)
print("Omega_3 in Y coords = R/(abc) da db dc ->", sp.factor(R/(a*b*c)))
print("  as a->0 (spoke cut, codim-2 stratum): R ->", sp.limit(R, a, 0), "; so no pole at a=0 (Jacobian degenerates instead)")
print("  as a->oo (spoke contracted, facet): R ->", sp.limit(R, a, sp.oo))
# Grove quadric (Lam Prop 5.35 at n=3) on Y data
L = dict(L123=a*b*c, Lsep=a+b+c, L12=a*b, L13=a*c, L23=b*c)
print("quadric L123*Lsep - e2 =", sp.simplify(L['L123']*L['Lsep'] - (L['L12']*L['L13'] + L['L12']*L['L23'] + L['L13']*L['L23'])))
# residue form in chart L12|3 = 1 solved for y3: check poles = only facets
L123, t, y2 = sp.symbols('L123 t y2')
y3 = (L123*t - y2)/(1 + y2)
form = 1/((1 + y2)*y2*y3)
print("chart L12|3=1, coords (L123,t,y2): density =", sp.factor(form), " (poles only y2=0, y3=0: facets)")
# Face counts from matchings (Lam: strata E_tau <-> matchings, dim = c(tau))
def matchings(s):
    if not s: yield []; return
    x = s[0]
    for i in range(1, len(s)):
        for m in matchings(s[1:i] + s[i+1:]): yield [(x, s[i])] + m
def cr(m): return sum(1 for (p, q), (r, s_) in itertools.combinations(m, 2) if p < r < q < s_ or r < p < s_ < q)
for n in (2, 3, 4):
    cnt = Counter(cr(m) for m in matchings(list(range(1, 2*n+1))))
    print(f"E_{n}: number of strata by dimension c:", dict(sorted(cnt.items())), " total", sum(cnt.values()))
print("Associahedron K5 (3-dim, Tr(phi^3) 6-pt): f-vector (V,E,F) = (14, 21, 9). E_3: (5, 6, 3); a convex 3-polytope needs >= 4 facets.")
print("Associahedron of dim 6 (9-pt): facets = 9*6/2 =", 9*6//2, "; compare E_4 facets (c=5) above.")
