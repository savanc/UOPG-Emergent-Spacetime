#!/usr/bin/env python3
"""STRUCT-3 / R3 locked checker (N_gen).
(a) consistency: per-generation ACC and Witten are additive in N_gen -> any N_gen passes;
(b) one-loop AF windows (CITED b0 = 11/3 C2 - 2/3 sum_Weyl T - 1/3 sum_complexscalar T):
    SU(3): b0 = 11 - (4/3) N_gen ; SU(2): b0 = 22/3 - (4/3) N_gen - 1/6 (one complex Higgs doublet, T=1/2, -1/3 T per complex scalar);
(c) KM: physical CP phases (N-1)(N-2)/2 > 0 iff N_gen >= 3 (CITED; requires CP violation as an input);
(d) discrete invariants of trunk positive geometries: does any family take the value 3 FOR EVERY member (forced)?
Usage: struct3_ngen.py {planted|broken|live}"""
import sys, math
from fractions import Fraction as F
def b_su3(N, sign=1): return sign*F(11) - F(4, 3)*N
def b_su2(N, sign=1): return sign*F(22, 3) - F(4, 3)*N - F(1, 6)
def af(N, sign=1): return b_su3(N, sign) > 0 and b_su2(N, sign) > 0
def km(N): return (N-1)*(N-2)//2
def window(sign=1): return [N for N in range(1, 30) if af(N, sign) and km(N) > 0]
FAM = {  # invariant -> (family values over its free parameter range) ; CITED closed forms
    'euler_char Gr>=0(k,n) [Galashin-Karp-Lam: closed ball]': [1 for k in range(1, 6) for n in range(k+1, 9)],
    'associahedron A_n vertices = Catalan C_{n-2}': [math.comb(2*m, m)//(m+1) for m in range(1, 12)],
    'associahedron A_n facets = n(n-3)/2': [n*(n-3)//2 for n in range(4, 15)],
    'positroid cells Gr>=0(1,n) = 2^n - 1': [2**n - 1 for n in range(1, 12)],
    'dim Gr(k,n) = k(n-k)': [k*(n-k) for k in range(1, 6) for n in range(k+1, 10)],
    'amplituhedron m (physical) = 4 ; helicity sectors k in 0..n-4': [n-3 for n in range(4, 12)],
}
mode = sys.argv[1]
if mode == 'planted':  # textbook: QCD AF <=> n_f <= 16 i.e. N_gen <= 8 ; SM SU(2) b0 = 19/6 at N_gen=3 ; KM: 1 phase at N=3
    ok = max(N for N in range(1, 30) if b_su3(N) > 0) == 8 and b_su2(3) == F(19, 6) and km(3) == 1 and km(2) == 0
    print("SU3 max N_gen", max(N for N in range(1, 30) if b_su3(N) > 0), "b_su2(3)", b_su2(3), "km(3)", km(3), "recovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':  # wrong sign of the gauge term: AF window must come out empty -> reject
    w = window(-1); print("broken window", w)
    if not w: raise SystemExit("REJECT: sign-flipped b0 gives no AF window")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'live':
    print("AF(SU3) max:", max(N for N in range(1, 30) if b_su3(N) > 0), " AF(SU2) max:", max(N for N in range(1, 30) if b_su2(N) > 0))
    print("window AF & KM:", window())
    for name, vals in FAM.items():
        print(f"{name}: forced_3={all(v == 3 for v in vals)} hits_3_at={[i for i, v in enumerate(vals) if v == 3]} sample={vals[:8]}")
