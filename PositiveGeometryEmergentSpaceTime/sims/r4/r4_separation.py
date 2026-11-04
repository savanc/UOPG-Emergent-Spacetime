#!/usr/bin/env python3
"""R4/R5 locked checker (geometry_struct_separation, ew_from_pion_geometry).
(a) Lean dependency scan of graph/raw_decls.jsonl: count declarations in STRUCT modules that use (type or value)
    any declaration of a geometry/hadron module, and vice versa. LINK iff count > 0.
(b) pi0 -> gamma gamma anomaly coefficient A = N_c (Q_u^2 - Q_d^2) with Q = T3 + Y, ACC branch yQ = -yL/N_c, yL = -1/2:
    symbolic in N_c (CITED: Bar-Wiese 2001).
Usage: r4_separation.py {planted|broken|live} [raw_decls.jsonl]"""
import sys, json, pathlib, sympy as sp
R = pathlib.Path(__file__).resolve().parents[2]
STRUCT = {'STRUCT1', 'STRUCT1b', 'STRUCT2', 'STRUCT3', 'X6'}
EXCL = {'Separation', 'AuditWitnesses'}  # bundle module (imports both by design) and audit witnesses
def mod(m): return m.split('.', 1)[1] if m.startswith('PositiveGeometryEmergentSpaceTime.') else None
def scan(decls, struct=STRUCT):
    owner = {d['name']: mod(d['module']) for d in decls}
    cross = []
    for d in decls:
        M = mod(d['module'])
        if M is None or M in EXCL: continue
        for u in d.get('type_uses', []) + d.get('value_uses', []):
            N = owner.get(u['n']) or mod(u['m'])
            if N is None or N in EXCL or N == M: continue
            if (M in struct) != (N in struct): cross.append((d['name'], u['n']))
    n_struct = sum(1 for d in decls if mod(d['module']) in struct)
    return n_struct, cross
def pi0():
    N = sp.symbols('N_c', positive=True); yQ = sp.Rational(1, 2)/N
    Qu, Qd = yQ + sp.Rational(1, 2), yQ - sp.Rational(1, 2)
    return sp.simplify(N*(Qu**2 - Qd**2)), sp.simplify(Qu.subs(N, 3)), sp.simplify(Qd.subs(N, 3))
mode = sys.argv[1]; path = sys.argv[2] if len(sys.argv) > 2 else R/'graph/raw_decls.jsonl'
decls = [json.loads(l) for l in open(path)]
if mode == 'planted':  # inject one fake STRUCT decl that uses an NLSM decl: must be detected; pi0 at N_c=3 must give SM charges 2/3,-1/3
    geo = next(d['name'] for d in decls if mod(d['module']) == 'NLSM')
    fake = {'name': 'PositiveGeometryEmergentSpaceTime.STRUCT2.fake', 'module': 'PositiveGeometryEmergentSpaceTime.STRUCT2', 'type_uses': [{'m': 'PositiveGeometryEmergentSpaceTime.NLSM', 'n': geo}], 'value_uses': []}
    n, c = scan(decls + [fake]); A, qu, qd = pi0()
    ok = any(x[0] == 'PositiveGeometryEmergentSpaceTime.STRUCT2.fake' for x in c) and qu == sp.Rational(2, 3) and qd == sp.Rational(-1, 3)
    print("planted cross:", [x for x in c if 'fake' in x[0]], "Qu,Qd(N_c=3):", qu, qd, "recovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':  # empty STRUCT set: scan is vacuous -> must reject
    n, c = scan(decls, struct={'STRUCTX'})
    if n == 0: raise SystemExit("REJECT: no STRUCT declarations found (vacuous scan)")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'live':
    n, c = scan(decls); A, _, _ = pi0()
    print("STRUCT decls:", n, " total decls:", len(decls), " cross edges geometry<->STRUCT:", len(c), c[:10])
    print("pi0 anomaly coefficient N_c(Qu^2-Qd^2) =", A, "(N_c-independent)" if not A.free_symbols else "")
