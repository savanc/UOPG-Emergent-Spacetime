#!/usr/bin/env python3
"""STRUCT-1 locked checker. Solves perturbative anomaly-cancellation conditions over Q (sympy) for a
list of left-handed Weyl multiplets (colour dim, SU(2) dim, charge symbol) and reports the solution set
up to overall normalisation. Usage: struct1_acc.py {live|livenu|planted|broken}"""
import sys, sympy as sp
def accs(fields, use=('c3','c2','grav','cube')):
    eqs = {}
    eqs['c3'] = sum(n2 * y for (n3, n2, y) in fields if n3 == 3)            # SU(3)^2 U(1) (index 1/2 each)
    eqs['c2'] = sum(n3 * y for (n3, n2, y) in fields if n2 == 2)            # SU(2)^2 U(1)
    eqs['grav'] = sum(n3 * n2 * y for (n3, n2, y) in fields)
    eqs['cube'] = sum(n3 * n2 * y**3 for (n3, n2, y) in fields)
    return [sp.expand(eqs[k]) for k in use]
def solve(fields, norm, use=('c3','c2','grav','cube'), extra=()):
    ys = [y for *_, y in fields]
    sols = sp.solve(accs(fields, use) + [norm - 1] + list(extra), ys, dict=True)
    return sols
mode = sys.argv[1]
q, u, d, l, e, n = sp.symbols('yQ yu yd yL ye ynu')
SM = [(3,2,q),(3,1,u),(3,1,d),(1,2,l),(1,1,e)]
if mode == 'planted':   # toy: two singlets a,b with grav+cube -> must give b = -a (vector-like), unique
    a, b = sp.symbols('a b'); s = solve([(1,1,a),(1,1,b)], a, use=('grav','cube'))
    print("planted toy:", s); ok = s == [{a: 1, b: -1}]; print("recovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':    # drop SU(2)^2U(1): must NOT be unique
    s = solve(SM, q, use=('c3','grav','cube'))
    if len(s) != 2: raise SystemExit(f"REJECT: uniqueness fails without SU(2)^2U(1) ({len(s)} branches, free params)")
    print("ERROR: broken accepted", s); sys.exit(1)
if mode == 'live':      # no nu^c, yQ normalised to 1 (requires yQ != 0)
    s = solve(SM, q); print("no nu^c, yQ=1:", s)
    s0 = sp.solve(accs([(3,2,0),(3,1,u),(3,1,d),(1,2,l),(1,1,e)]), [u,d,l,e], dict=True); print("yQ=0 branch:", s0)
if mode == 'livenu':    # with nu^c: one-parameter family? test B-L direction
    F = SM + [(1,1,n)]; s = solve(F, q); print("with nu^c, yQ=1:", s)
