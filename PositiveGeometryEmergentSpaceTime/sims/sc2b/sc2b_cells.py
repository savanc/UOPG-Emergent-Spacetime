#!/usr/bin/env python3
"""SC-2b locked checker. For a cone of the Feynman (g-vector) fan given by its g-vectors:
 (I1) cone Jacobian |det g|  (2309.15913 eq.22 measure);
 (I2) Lebesgue volume of the projective slice {rho>=0, sum rho = 1} in coords (rho_1..rho_{E-1}) = 1/(E-1)!;
 (I3) for E=2 the bubble F/U moment int_0^1 x(1-x) dx.
Compares with SC-2 geometric factors (triangle 1/2, bubble 1/6). Usage: sc2b_cells.py {live|planted|broken}"""
import sys, sympy as sp, itertools
x = sp.symbols('x')
def jac(gs): return abs(sp.Matrix(gs).det())
def slice_vol(E):
    v = sp.symbols(f'r1:{E}'); expr = sp.Integer(1); lim = 1
    # iterated integral over simplex sum v <= 1
    res = sp.Integer(1)
    for i in reversed(range(E-1)):
        res = sp.integrate(res, (v[i], 0, 1 - sum(v[:i])))
    return sp.nsimplify(res)
mode = sys.argv[1]
if mode == 'planted':   # 5-pt tree fan, 2309.15913 eq.81: five cones, all unimodular
    g = {'13':(1,0),'14':(0,1),'24':(-1,1),'25':(-1,0),'35':(0,-1)}
    cones = [('13','14'),('14','24'),('24','25'),('25','35'),('35','13')]
    ds = [jac([g[a],g[b]]) for a,b in cones]
    print("planted 5pt tree cone jacobians:", ds, "all_unimodular=", all(d==1 for d in ds))
    sys.exit(0 if all(d==1 for d in ds) else 1)
if mode == 'broken':
    d = jac([(1,0),(1,2)])
    if d != 1: raise SystemExit(f"REJECT: non-unimodular cone, |det|={d} - not a Feynman-fan cone")
    print("ERROR: broken input accepted"); sys.exit(1)
if mode == 'live':
    bubble_cone = [(0,-1),(-1,0)]            # 2309.15913 eq.101: S1, S2 (bubble diagram cone)
    tri_cone = [(1,0,0),(0,1,0),(0,0,1)]     # triangulation T (one-peak curves, g = e_i, eq.78) at 3pt 1-loop
    T_geo, S_geo = sp.Rational(1,2), sp.Rational(1,6)   # SC-2 geometric factors (simplex area, int x(1-x))
    I1T, I1S = jac(tri_cone), jac(bubble_cone)
    I2T, I2S = slice_vol(3), slice_vol(2)
    I3S = sp.integrate(x*(1-x), (x,0,1))
    print(f"triangle: I1 jac={I1T} I2 slice={I2T}  SC-2 factor={T_geo}  matches: I1={I1T==T_geo} I2={I2T==T_geo}")
    print(f"bubble:   I1 jac={I1S} I2 slice={I2S} I3 moment={I3S}  SC-2 factor={S_geo}  matches: I1={I1S==S_geo} I2={I2S==S_geo} I3={I3S==S_geo}")
    tv = (I1T==T_geo) or (I2T==T_geo); sv = (I1S==S_geo) or (I2S==S_geo)
    print("VERDICT:", "PASS" if tv and sv else "PARTIAL" if tv != sv else "FAIL")
