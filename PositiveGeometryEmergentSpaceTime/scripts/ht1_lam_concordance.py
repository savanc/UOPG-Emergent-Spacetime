"""H-T1 (e3): Lam 1402.6261 §5.2 Pluecker coordinates Delta_I = sum over concordant sigma of L_sigma, computed from the
definition for n = 2, 3 (positions: i-bar = 2i-1, i-tilde = 2i), then checked against the Pluecker relations."""
import sympy as sp, itertools
a, b, c = sp.symbols('a b c', positive=True)
def deltas(n, parts):  # parts: list of (sigma blocks over bars, dual blocks over tildes, L_sigma)
    out = {}
    for I in itertools.combinations(range(1, 2*n+1), n-1):
        comp = set(range(1, 2*n+1)) - set(I); tot = 0
        for sig, dual, L in parts:
            blocks = [{2*i-1 for i in blk} for blk in sig] + [{2*i for i in blk} for blk in dual]
            if all(len(blk & comp) == 1 for blk in blocks): tot += L
        out[I] = sp.expand(tot)
    return out
# n = 2: path 1 - 0 - 2 with conductances a, c
n2 = deltas(2, [([{1, 2}], [{1}, {2}], a*c), ([{1}, {2}], [{1, 2}], a + c)])
print("n=2 Deltas:", n2)
# n = 3: star with conductances a (to 1), b (to 2), c (to 3); groves: L_sigma
parts3 = [([{1, 2, 3}], [{1}, {2}, {3}], a*b*c), ([{1}, {2}, {3}], [{1, 2, 3}], a + b + c),
          ([{1, 2}, {3}], [{1}, {2, 3}], a*b), ([{2, 3}, {1}], [{2}, {1, 3}], b*c), ([{1, 3}, {2}], [{3}, {1, 2}], a*c)]
n3 = deltas(3, parts3)
print("n=3 Deltas:", n3)
D = lambda i, j: n3[(i, j)] if i < j else -n3[(j, i)]
bad = [(q, sp.expand(D(q[0], q[1])*D(q[2], q[3]) - D(q[0], q[2])*D(q[1], q[3]) + D(q[0], q[3])*D(q[1], q[2])))
       for q in itertools.combinations(range(1, 7), 4)]
print("Pluecker relations violated:", [x for x in bad if x[1] != 0])
# realise by a 2x6 matrix: column 1 = (1, 0), p2 = 0
p = sp.symbols('p3:7')
M = sp.Matrix([[1, 0] + list(p), [0] + [n3[(1, j)] for j in range(2, 7)]])
mn = lambda i, j: M[0, i-1]*M[1, j-1] - M[0, j-1]*M[1, i-1]
eqs = [sp.expand(mn(i, j) - n3[(i, j)]) for (i, j) in n3 if i != 1]
sol = sp.solve(eqs, list(p), dict=True)
print("solution:", sol)
Ms = sp.simplify(M.subs(sol[0])); print("matrix:", Ms.tolist())
print("all minors match:", all(sp.simplify(Ms[0, i-1]*Ms[1, j-1] - Ms[0, j-1]*Ms[1, i-1] - n3[(i, j)]) == 0 for (i, j) in n3))
