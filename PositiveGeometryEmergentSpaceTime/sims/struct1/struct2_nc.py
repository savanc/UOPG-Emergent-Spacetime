#!/usr/bin/env python3
"""STRUCT-2 locked checker. One generation with N_c colours: Q (N,2,q), u^c (Nbar,1,u), d^c (Nbar,1,d), L (1,2,l), e^c (1,1,e).
Solves perturbative ACC with q = 1 for symbolic/concrete N; reports branches; Witten: #doublets = N+1 must be even.
Usage: struct2_nc.py {planted|broken|live}"""
import sys, sympy as sp
q,u,d,l,e,N = sp.symbols('yQ yu yd yL ye N')
def acc(Nv): return [2*q+u+d, Nv*q+l, 2*Nv*q+Nv*u+Nv*d+2*l+e, 2*Nv*q**3+Nv*u**3+Nv*d**3+2*l**3+e**3]
def sol(Nv): return sp.solve(acc(Nv)+[q-1], [q,u,d,l,e], dict=True)
mode = sys.argv[1]
if mode == 'planted':  # N=3 must give STRUCT-1 (u in {2,-4}, d in {-4,2}, l=-3, e=6)
    s = sol(3); print("N=3:", s); ok = sorted(x[u] for x in s) == [-4, 2] and all(x[e]==6 and x[l]==-3 for x in s)
    print("recovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':   # N=0 (no colour): must be rejected (no uniqueness / free parameter)
    s = sol(0)
    if any(len(x) < 5 for x in s) or len(s) != 2: raise SystemExit(f"REJECT: N=0 degenerate ({s})")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'live':
    print("symbolic N:", sol(N))
    for Nv in range(1, 8):
        s = sol(Nv); print(f"N={Nv}: branches={len(s)} witten_ok={(Nv+1)%2==0} sample={s[0]}")
