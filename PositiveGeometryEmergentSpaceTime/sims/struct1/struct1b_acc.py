#!/usr/bin/env python3
"""STRUCT-1b locked checker. One generation + nu^c (+ Higgs doublet H for Yukawas). Solves ACC (+ extra
conditions) over Q with yQ = 1 and reports the solution set. Usage: struct1b_acc.py {planted|broken|majorana|dirac|both}"""
import sys, sympy as sp
q,u,d,l,e,n,h = sp.symbols('yQ yu yd yL ye ynu yH')
def acc(nu=True):
    eq = [2*q+u+d, 3*q+l, 6*q+3*u+3*d+2*l+e+(n if nu else 0), 6*q**3+3*u**3+3*d**3+2*l**3+e**3+(n**3 if nu else 0)]
    return eq
YUK = [q+h+u, q-h+d, l-h+e, l+h+n]       # Q H u^c, Q H* d^c, L H* e^c, L H nu^c invariant
MAJ = [n]                                # nu^c nu^c invariant
def solve(eqs, vars_): return sp.solve(eqs + [q-1], vars_, dict=True)
mode = sys.argv[1]
if mode == 'planted':   # known answer: no nu^c (STRUCT-1) -> exactly the two SM branches
    s = solve(acc(nu=False), [q,u,d,l,e]); print("planted (no nu^c):", s)
    ok = sorted([(x[u],x[d]) for x in s]) == [(-4,2),(2,-4)] and all(x[e]==6 and x[l]==-3 for x in s)
    print("recovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':    # nu^c with no extra condition -> must be rejected as non-unique (free parameter)
    s = solve(acc(), [q,u,d,l,e,n])
    free = any(len(x) < 6 for x in s)
    if free: raise SystemExit(f"REJECT: not unique with nu^c and no extra condition ({len(s)} branches with a free parameter)")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'majorana': print("ACC + Majorana:", solve(acc()+MAJ, [q,u,d,l,e,n]))
if mode == 'dirac':    print("ACC + Dirac Yukawas:", solve(acc()+YUK, [q,u,d,l,e,n,h]))
if mode == 'both':     print("ACC + Yukawas + Majorana:", solve(acc()+YUK+MAJ, [q,u,d,l,e,n,h]))
