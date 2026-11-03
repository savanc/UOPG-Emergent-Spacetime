"""BH-1 check (NON-BLIND: result is textbook). Exact arithmetic.
(1) coefficients of (1+y/n)^n, n=2s: C(n,l)/n^l; vanish for l>n; l!*c -> 1 (monotone, exact rationals).
(2) Kerr axis Ernst potential xi = m/(z - i a) (convention from memory, FHP-style) -> m_l = m (i a)^l,
    and the FHP-type correction combinations M_ij = m_i m_j - m_{i-1} m_{j+1} vanish (=> P_l = m_l).
(3) cross-check: exp(i a z) Taylor coefficients * l! = (i a)^l (matches Lean kerr_coeff)."""
from fractions import Fraction as F
from math import comb, factorial
import sympy as sp
ok = True
print("(1) minimal-coupling coefficients")
for s in [F(1,2),1,2,5,10,50,200]:
    n = int(2*s)
    c = [F(comb(n,l), n**l) for l in range(n+3)]
    assert c[0]==1 and (n<1 or c[1]==1) and all(x==0 for x in c[n+1:])
    r = [factorial(l)*c[l] for l in range(min(n,8)+1)]
    print(f"  s={s}: l!*c(2s,l) for l<=8:", [f"{float(x):.6f}" for x in r])
for l in range(2,7):
    seq=[factorial(l)*F(comb(n,l),n**l) for n in (10,100,1000,10000)]
    mono = all(seq[i]<seq[i+1] for i in range(3)); ok &= mono and 1-seq[-1] < F(l*l,10000)
    print(f"  l={l}: 1 - l!c(n,l) at n=1e1..1e4:", [f"{float(1-x):.2e}" for x in seq], "monotone" if mono else "NOT")
print("(2) Kerr Ernst axis potential")
z,m,a=sp.symbols('z m a',positive=True); w=sp.symbols('w')
xi = m/(z-sp.I*a)
ser = sp.series(xi.subs(z,1/w),w,0,13).removeO()
ml=[sp.simplify(ser.coeff(w,l+1)) for l in range(12)]
for l in range(12):
    good = sp.simplify(ml[l]-m*(sp.I*a)**l)==0; ok&=good
print("  m_l == m (i a)^l for l=0..11:", all(sp.simplify(ml[l]-m*(sp.I*a)**l)==0 for l in range(12)))
Mz = all(sp.simplify(ml[i]*ml[j]-ml[i-1]*ml[j+1])==0 for i in range(1,11) for j in range(0,10))
ok&=Mz; print("  M_ij = m_i m_j - m_{i-1} m_{j+1} == 0 (1<=i<=10, 0<=j<=9):", Mz)
print("  M_l = Re m_l:", [sp.re(sp.expand(x)) for x in ml[:5]], " S_l = Im m_l:", [sp.im(sp.expand(x)) for x in ml[:5]])
print("(3) exp(i a z) coefficients")
e=sp.series(sp.exp(sp.I*a*z),z,0,12).removeO()
c3 = all(sp.simplify(sp.factorial(l)*e.coeff(z,l)-(sp.I*a)**l)==0 for l in range(12)); ok&=c3
print("  l! [z^l] exp(iaz) == (ia)^l, l<=11:", c3)
print("ALL CHECKS PASS" if ok else "FAIL")
