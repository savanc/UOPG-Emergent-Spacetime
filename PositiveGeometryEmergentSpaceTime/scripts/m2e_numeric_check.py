"""M2e numeric cross-check of candidate shifts, independent of the Groebner step:
evaluate delta^4 * A6(X + delta*a) directly (14 cubic diagrams, exact rationals) at random rational X for large delta,
compare with the predicted limit L, and test the Adler zero of L on each leg at a random soft point."""
import random, sympy as sp
_src = open('scripts/m2e_shift_scan.py').read(); exec(_src[:_src.index("if __name__ == '__main__':")])
random.seed(20261010)
def A6(xv):
    return sum(sp.Mul(*[1 / xv[c] for c in T]) for T in TRI)
def check(name, a):
    S = [c for c in CH if a.get(c, 0) != 0]
    U, P = numerators(S, 4)
    bsub = {B[c]: sp.nsimplify(1 / sp.Rational(a[c])) for c in S}
    Lsym = sp.cancel(P[4].subs(bsub) / sp.Mul(*[X[c] for c in U]))
    print(f'== {name}: a = {{{", ".join(f"X{c[0]}{c[1]}:{a[c]}" for c in S)}}}')
    print('   L == 0 identically:', Lsym == 0)
    for trial in range(2):
        xv = {c: sp.Rational(random.randint(1, 97), random.randint(1, 13)) for c in CH}
        Lv = Lsym.subs({X[c]: xv[c] for c in CH})
        vals = []
        for d in [10**6, 10**8]:
            vals.append(sp.Rational(d)**4 * A6({c: xv[c] + d * sp.Rational(a.get(c, 0)) for c in CH}))
        print(f'   X#{trial}: L = {float(Lv):.6g}; delta^4 A6 at 1e6 = {float(vals[0]):.6g}, at 1e8 = {float(vals[1]):.6g}')
    soft = []
    for i in range(1, 7):
        Q = sp.cancel(Lsym.subs(softmap(i), simultaneous=True))
        soft.append(Q == 0)
    print('   Adler zero per leg 1..6:', soft)
check('canonical a*', {(1,3): -1, (1,5): -1, (3,5): -1, (2,4): 1, (2,6): 1, (4,6): 1})
check('mirror (= a* rotated by one label)', {(1,3): 1, (1,5): 1, (3,5): 1, (2,4): -1, (2,6): -1, (4,6): -1})
# C1-only family on FORB + X14 (m2e_scan_k4_noC3.json, entry 1) at b46 = 2: b = (1, 2/3, 1, 2, -1, -2, 2)
b = {(1,3): 1, (1,4): sp.Rational(2,3), (1,5): 1, (2,4): 2, (2,6): -1, (3,5): -2, (4,6): 2}
check('C1-only family member (fails C3)', {c: 1 / sp.Rational(v) for c, v in b.items()})
# full support, branch (0,1,0) of the C3 analysis: a46=-a15, a26=-a13, a35=-a24, a14=a13+a24, a25=a15-a13, a36=-a15-a24
a13, a15, a24 = 1, 3, 2
check('full-support C1(<4)+C2+C3 family member (L = 0)', {(1,3): a13, (1,5): a15, (2,4): a24, (4,6): -a15, (2,6): -a13, (3,5): -a24,
      (1,4): a13 + a24, (2,5): a15 - a13, (3,6): -a15 - a24})
