"""M2f (d2) ablation: which subsets of the six massive skinny-rectangle zeros force the a* line (with (P)). Exact Groebner (lex)."""
import itertools, sympy as sp
exec(open('scripts/m2f_mass_shift.py').read().split('# ---------------------------------------------------------------- (a) n = 4')[0])
CH = chords(6); oe = [(1, 4), (2, 5), (3, 6)]
v = {ch: (sp.Integer(0) if ch in oe else sp.Symbol(f'v{ch[0]}{ch[1]}')) for ch in CH}
V = [v[ch] for ch in CH if ch not in oe]
Z = Xsym(6, 'Z')
def locus(conds):
    eqs_ = [cc(Z, 6, *q) for q in conds]
    for vs in itertools.combinations([Z[ch] for ch in CH if ch not in oe], len(eqs_)):
        sol = sp.solve(eqs_, vs, dict=True)
        if sol and all(sp.simplify(e.subs(sol[0])) == 0 for e in eqs_): return sol[0]
for S in ([1], [1, 2], [1, 3], [1, 4]):
    eqs = []
    for i in S:
        L = locus([(i, i + 2), (i, i + 3), (i, i + 4)])
        e = sp.numer(sp.together(A6N({ch: Z[ch] + v[ch] for ch in CH}).subs(L, simultaneous=True)))
        eqs += [c for c in sp.Poly(sp.expand(e), *Z.values()).coeffs()]
    G = sp.groebner(eqs, *V, order='lex')
    print(S, list(G.exprs))
