"""M2e: scan all linear shifts X_ij -> X_ij + delta*a_ij of the 9 hexagon chords for
C1(k): delta^k A6 -> L != 0;  C2: L has no pole at X13,X15,X24,X26,X35,X46;  C3: Adler zero on every leg.
Pre-registration: prereg/M2e-shift-forced-2026-10-10.md.  Exact (sympy, rationals)."""
import itertools, sys, json, time
import sympy as sp

CH = [(1,3),(1,4),(1,5),(2,4),(2,5),(2,6),(3,5),(3,6),(4,6)]
FORB = {(1,3),(1,5),(2,4),(2,6),(3,5),(4,6)}          # j-i even: (e,e)/(o,o)
X = {c: sp.Symbol(f'X{c[0]}{c[1]}') for c in CH}
B = {c: sp.Symbol(f'b{c[0]}{c[1]}') for c in CH}
XS = list(X.values())
cross = lambda p, q: (p[0] < q[0] < p[1] < q[1]) or (q[0] < p[0] < q[1] < p[1])
TRI = [T for T in itertools.combinations(CH, 3) if all(not cross(p, q) for p, q in itertools.combinations(T, 2))]
assert len(TRI) == 14

def getX(i, j):
    i, j = (i-1) % 6 + 1, (j-1) % 6 + 1
    if i > j: i, j = j, i
    if j - i <= 1 or (i, j) == (1, 6): return sp.Integer(0)
    return X[(i, j)]
def softmap(i):
    sub = {getX(i, j): getX(i+1, j) for j in range(1, 7) if getX(i, j) != 0}
    sub[getX(i-1, i+1)] = sp.Integer(0)
    return sub

def hcomplete(vals, r):
    if r == 0: return sp.Integer(1)
    return sp.Add(*[sp.Mul(*c) for c in itertools.combinations_with_replacement(vals, r)])

def numerators(S, mmax):
    """P_m = D_U * C_m (polynomial), m = 0..mmax, where D_U = prod of unshifted chords."""
    U = [c for c in CH if c not in S]
    P = []
    for m in range(mmax + 1):
        tot = 0
        for T in TRI:
            sh = [c for c in T if c in S]
            if m < len(sh): continue
            r = m - len(sh)
            term = (-1) ** r * sp.Mul(*[B[c] for c in sh]) * hcomplete([B[c] * X[c] for c in sh], r)
            term *= sp.Mul(*[X[c] for c in U if c not in T])
            tot += term
        P.append(sp.expand(tot))
    return U, P

def coeff_eqs(poly):
    if poly == 0: return []
    return [sp.expand(cf) for cf in sp.Poly(poly, *XS).coeffs()]

def conditions(S, k, legs=range(1, 7), use_C2=True, use_C3=True):
    U, P = numerators(S, k)
    eqs = []
    for m in range(k): eqs += coeff_eqs(P[m])
    Pk = P[k]
    Q = Pk
    if use_C2 or use_C3:
        for f in [c for c in U if c in FORB]:
            R = sp.expand(Q.subs(X[f], 0))
            if use_C2: eqs += coeff_eqs(R)
            Q = sp.expand(sp.div(sp.expand(Q - R), X[f], *XS)[0]) if use_C2 else Q
    if use_C3:
        for i in legs:
            eqs += coeff_eqs(sp.expand(Q.subs(softmap(i), simultaneous=True)))
    return U, P, Pk, eqs

import subprocess, re, os
def singular_components(eqs, bs):
    """Minimal associated primes of <eqs, t*prod(b)-1> after setting bs[0]=1 (Singular, char 0).
    Returns list of generator lists (strings), or [] if no solution with all b != 0."""
    sub0 = {bs[0]: 1}
    E = [sp.expand(e.subs(sub0)) for e in eqs]
    E = sorted({str(e) for e in E if e != 0})
    gens = [str(b) for b in bs[1:]]
    if not gens:
        return [] if E else [['(point)']]
    E.append('t*' + '*'.join(gens) + '-1')
    src = (f'LIB "primdec.lib";\nring r=0,({",".join(gens + ["t"])}),dp;\n'
           f'ideal i={",".join(e.replace("**", "^") for e in E)};\n'
           'ideal g=std(i); if (g[1]==1) {print("NOSOL");} else {list L=minAssGTZ(g); int j; for (j=1;j<=size(L);j++) {print("COMP"); print(eliminate(L[j],t));}}\nquit;\n')
    out = subprocess.run(['Singular', '-q'], input=src, capture_output=True, text=True, timeout=3600).stdout
    if 'NOSOL' in out: return []
    comps = []
    for blk in out.split('COMP')[1:]:
        comps.append([ln.strip().rstrip(',').strip() for ln in blk.strip().splitlines() if ln.strip().rstrip(',').strip() not in ('', '0')])
    return comps

def solve(S, eqs, Pk):
    bs = [B[c] for c in S]
    comps = singular_components(eqs, bs)
    res = []
    for comp in comps:
        # try to read off a point: solve the component's generators with sympy (they are simple once prime)
        gens = [sp.sympify(g.replace('^', '**')) for g in comp] if comp and comp != ['(point)'] else []
        sol = sp.solve(gens, [b for b in bs[1:]], dict=True) if gens else [{}]
        if not sol:
            res.append({'support': [f'{c[0]}{c[1]}' for c in S], 'component': comp, 'b': 'UNSOLVED-BY-SYMPY', 'free': [], 'Lk_nonzero_generic': True}); continue
        for s0 in sol:
            full = {bs[0]: sp.Integer(1), **s0}
            Lk = sp.expand(sp.numer(sp.together(Pk.subs(full))))
            res.append({'support': [f'{c[0]}{c[1]}' for c in S], 'component': comp, 'b': {str(k): str(v) for k, v in full.items()},
                        'free': [str(b) for b in bs[1:] if b not in s0], 'Lk_nonzero_generic': Lk != 0})
    return res

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--k', type=int, default=4)
    ap.add_argument('--noC2', action='store_true'); ap.add_argument('--noC3', action='store_true')
    ap.add_argument('--legs', default='123456'); ap.add_argument('--only', default='')
    A = ap.parse_args()
    legs = [int(c) for c in A.legs]
    tag = f'k{A.k}' + ('_noC2' if A.noC2 else '') + ('_noC3' if A.noC3 else '') + ('' if A.legs == '123456' else '_legs' + A.legs)
    t0 = time.time(); found = []; n = 0
    supports = [list(S) for r in range(1, 10) for S in itertools.combinations(CH, r)]
    if A.only: supports = [[c for c in CH if f'{c[0]}{c[1]}' in A.only.split(',')]]
    for S in supports:
        n += 1
        U, P, Pk, eqs = conditions(S, A.k, legs=legs, use_C2=not A.noC2, use_C3=not A.noC3)
        res = [x for x in solve(S, eqs, Pk) if x['Lk_nonzero_generic']]
        if res:
            found += res; print(tag, res, flush=True)
    print(f'{tag}: scanned {n} non-empty supports (empty support: unshifted A6, fails C1 for k>=1); '
          f'{len(found)} solution components with L != 0; {time.time()-t0:.0f}s', flush=True)
    json.dump(found, open(f'scripts/m2e_scan_{tag}.json', 'w'), indent=1)
