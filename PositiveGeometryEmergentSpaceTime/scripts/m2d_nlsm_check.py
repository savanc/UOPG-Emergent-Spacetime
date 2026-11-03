"""M2d: exact sympy checks of the Tr(phi^3) -> NLSM delta-shift (arXiv:2401.05483 eq. 2),
hidden zeros (arXiv:2312.16282 sec. 3-4), Adler zero, and the LO pion scattering lengths vs data.
Pre-registration: prereg/M2d-trphi3-pions-2026-10-10.md."""
import itertools, math
import sympy as sp

d, eps = sp.symbols('delta epsilon', positive=True)
ok = {}

def Xsym(n):
    return {(i, j): sp.Symbol(f'X{i}{j}') for i in range(1, n + 1) for j in range(i + 2, n + 1) if not (i == 1 and j == n)}

def getX(X, n, i, j):
    i, j = (i - 1) % n + 1, (j - 1) % n + 1
    if i > j: i, j = j, i
    if j - i <= 1 or (i == 1 and j == n): return sp.Integer(0)
    return X[(i, j)]

def c(X, n, i, j):
    return getX(X, n, i, j) + getX(X, n, i + 1, j + 1) - getX(X, n, i, j + 1) - getX(X, n, i + 1, j)

def triangulations(n):
    chords = [(i, j) for i in range(1, n + 1) for j in range(i + 2, n + 1) if not (i == 1 and j == n)]
    cross = lambda a, b: (a[0] < b[0] < a[1] < b[1]) or (b[0] < a[0] < b[1] < a[1])
    return [T for T in itertools.combinations(chords, n - 3) if all(not cross(a, b) for a, b in itertools.combinations(T, 2))]

def A_phi3(X, n):
    return sum(1 / sp.Mul(*[X[ch] for ch in T]) for T in triangulations(n))

def shift(X, n, dd):
    return {k: v + (dd if k[0] % 2 == 0 and k[1] % 2 == 0 else -dd if k[0] % 2 == 1 and k[1] % 2 == 1 else 0) for k, v in X.items()}

def large_delta(expr, power):
    """lim_{delta->oo} delta^power * expr, plus the series in eps = 1/delta."""
    e = sp.together(sp.simplify((expr * d ** power).subs(d, 1 / eps)))
    return sp.simplify(sp.limit(e, eps, 0)), e

out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

# (a) n = 4
X4 = Xsym(4); A4 = A_phi3(X4, 4); L4, _ = large_delta(A4.subs({X4[k]: v for k, v in shift(X4, 4, d).items()}, simultaneous=True), 2)
say('(a) n=4: lim delta^2 A4(shifted) =', L4)
ok['a'] = sp.simplify(L4 + (X4[(1, 3)] + X4[(2, 4)])) == 0
say('    c13 =', c(X4, 4, 1, 3), '; A4NLSM = X13+X24 equals c13:', sp.simplify(X4[(1,3)]+X4[(2,4)] - c(X4,4,1,3)) == 0)

# (b) n = 6
X6 = Xsym(6); A6 = A_phi3(X6, 6)
say('    #planar cubic diagrams n=6:', len(triangulations(6)))
x = lambda i, j: getX(X6, 6, i, j)
def nlsm6():
    tot = 0
    for k in (0, 2, 4):
        r = lambda i: (i - 1 + k) % 6 + 1
        tot += (x(r(1), r(3)) + x(r(2), r(4))) * (x(r(1), r(5)) + x(r(4), r(6))) / x(r(1), r(4)) - x(r(1), r(3)) - x(r(2), r(4))
    return tot
A6N = nlsm6()
A6s = A6.subs({X6[k]: v for k, v in shift(X6, 6, d).items()}, simultaneous=True)
e6 = sp.together(A6s.subs(d, 1 / eps))
num, den = sp.fraction(sp.factor(e6))
# series of eps^-4 * A6 at eps -> 0: check orders delta^-1..-3 vanish
ser = sp.series(e6 / eps ** 4, eps, 0, 1).removeO()
L6 = sp.simplify(ser.coeff(eps, 0))
neg = [sp.simplify(ser.coeff(eps, -m)) for m in (1, 2, 3)]
say('(b) n=6: eps^-m coefficients of delta^4 A6, m=1,2,3 (must be 0):', neg)
sig = sp.simplify(L6 / A6N)
say('    lim delta^4 A6(shifted) / A6NLSM[eq.4.3] =', sig, '(prediction +1)')
ok['b'] = all(v == 0 for v in neg) and sig in (1, -1)
ok['b_sign_prediction'] = sig == 1

# independent Feynman-rule check of eq. 4.3 from eq. 4.2 vertices (Cayley), off-shell
# momenta as formal vectors; dot products from X's: 2 p_i.p_j = -c_ij for non-adjacent, p_i.p_{i+1} = X_{i,i+2}/2, p_i^2=0
def dot6(i, j):
    i, j = (i - 1) % 6 + 1, (j - 1) % 6 + 1
    if i == j: return sp.Integer(0)
    if i > j: i, j = j, i
    if j == i + 1 or (i == 1 and j == 6):
        a, b = (i, j) if j == i + 1 else (6, 1)
        return getX(X6, 6, a, a + 2) / 2
    return -c(X6, 6, i, j) / 2
def vdot(u, v):  # u, v: dict leg->coeff
    return sp.expand(sum(cu * cv * dot6(a, b) for a, cu in u.items() for b, cv in v.items()))
def V(moms, lam2=1):
    m = len(moms) // 2
    s = 0
    for r in range(m):
        for a in range(2 * m):
            s += vdot(moms[a], moms[(a + 2 * r + 1) % (2 * m)])
    return -sp.Rational(1, 2) * lam2 ** (m - 1) * s
leg = lambda i: {((i - 1) % 6) + 1: 1}
def P(*ls):
    dd = {}
    for l in ls:
        dd[((l - 1) % 6) + 1] = dd.get(((l - 1) % 6) + 1, 0) + 1
    return dd
neg_ = lambda u: {k: -v for k, v in u.items()}
# 4-pt check: V4 on-shell
X4d = lambda: None
amp6 = V([leg(i) for i in range(1, 7)])
for (a, b) in ((1, 4), (2, 5), (3, 6)):
    # channel X_{a,b}: legs a..b-1 on one side
    L = [leg(i) for i in range(a, b)]; R = [leg(i) for i in range(b, a + 6)]
    Pm = P(*range(a, b))
    amp6 += -V(L + [neg_(Pm)]) * V(R + [Pm]) / getX(X6, 6, a, b)
ratio = sp.simplify(sp.together(amp6) / A6N)
say('    Feynman rules (eq. 4.2, lambda=1): A6_FR / A6[eq.4.3] =', ratio)
# 4-pt normalisation with same rules: V4 on-shell vs X13+X24
V4 = sp.simplify(-sp.Rational(1, 2) * 2 * (2 * (x(1, 3) / 2 + x(2, 4) / 2)))
say('    same rules at n=4: V4 =', V4, '; [H] normalises A4 = X13+X24, so overall sign per multiplicity is convention')
ok['b_feynman'] = ratio in (1, -1)

# (c) n = 5
X5 = Xsym(5); A5 = A_phi3(X5, 5)
A5s = A5.subs({X5[k]: v for k, v in shift(X5, 5, d).items()}, simultaneous=True)
L51, _ = large_delta(A5s, 1); L52, _ = large_delta(A5s, 2)
L5pred = 1 - (X5[(1, 3)] + X5[(2, 4)]) / X5[(1, 4)] - (X5[(2, 4)] + X5[(3, 5)]) / X5[(2, 5)]
say('(c) n=5: lim delta A5 =', L51, '; lim delta^2 A5 =', sp.simplify(L52))
ok['c'] = L51 == 0 and sp.simplify(L52 - L5pred) == 0
cs5 = {(i, j): c(X5, 5, i, j) for (i, j) in ((1, 3), (1, 4), (2, 4), (2, 5), (3, 5))}
X5s = shift(X5, 5, d)
cshift = {k: sp.simplify(v.subs({X5[q]: w for q, w in X5s.items()}, simultaneous=True) - v) for k, v in cs5.items()}
say('    c shifts under delta:', cshift)
ok['c_cshift'] = all((v == 0) == (k != (1, 4)) for k, v in cshift.items())
# soft-leg scan for L5: p_i -> 0 maps X_{i,j}->X_{i+1,j}, X_{i-1,i+1}->0
def soft(X, n, expr, i):
    """p_i -> 0 in planar variables: X_{i,j} -> X_{i+1,j} for all j, X_{i-1,i+1} -> 0 (indices mod n)."""
    sub = {getX(X, n, i, j): getX(X, n, i + 1, j) for j in range(1, n + 1) if getX(X, n, i, j) != 0}
    sub[getX(X, n, i - 1, i + 1)] = 0
    return sp.simplify(sp.together(expr.subs(sub, simultaneous=True)))
soft5 = lambda e, i: soft(X5, 5, e, i)
say('    soft scan of L5 (p_i -> 0):', {i: soft5(L5pred, i) for i in range(1, 6)})

# (d) hidden zeros
m5 = A5
zsets = [((1, 3), (1, 4)), ((2, 4), (2, 5)), ((3, 5), (1, 3)), ((1, 4), (2, 4)), ((2, 5), (3, 5))]
def locus(X, n, conds):
    """Solve the linear conditions c=0 for len(conds) planar variables; verify the solution."""
    eqs = [c(X, n, *q) for q in conds]
    for vs in itertools.combinations(list(X.values()), len(eqs)):
        sol = sp.solve(eqs, vs, dict=True)
        if sol and all(sp.simplify(e.subs(sol[0])) == 0 for e in eqs):
            return sol[0]
    raise ValueError(conds)
z5 = [(zs, sp.simplify(m5.subs(locus(X5, 5, zs)))) for zs in zsets]
say('(d) m5 on the five skinny-rectangle loci:', [v for _, v in z5])
f1 = sp.simplify(m5.subs(X5[(2, 4)], X5[(1, 4)] + X5[(2, 5)]) - (1 / X5[(1, 3)] + 1 / X5[(2, 5)]) * (1 / X5[(1, 4)] + 1 / X5[(3, 5)]))
f2 = sp.simplify(m5.subs(X5[(1, 4)], X5[(1, 3)] + X5[(2, 4)]) - (1 / X5[(1, 3)] + 1 / X5[(2, 5)]) * (1 / X5[(2, 4)] + 1 / X5[(3, 5)]))
say('    factorisation eq.3.3 (c14=0) residual:', f1, '; eq.3.5 (c13=0) residual:', f2)
zA5s = [(zs, sp.simplify(sp.together(A5s.subs(locus(X5, 5, zs))))) for zs in zsets]
say('    shifted A5 (finite delta) on loci:', [(zs, v == 0) for zs, v in zA5s])
# n = 6 skinny rectangles i: c_{i,j}=0 for j non-adjacent
z6, z6s = [], []
for i in range(1, 7):
    conds = [(i, i + 2), (i, i + 3), (i, i + 4)]
    L = locus(X6, 6, conds)
    z6.append(sp.simplify(A6N.subs(L))); z6s.append(sp.simplify(sp.together(A6s.subs(L))))
say('    A6NLSM on 6 skinny rectangles:', z6, '; shifted A6 (finite delta):', z6s)
ok['d'] = all(v == 0 for _, v in z5) and f1 == 0 and f2 == 0 and all(v == 0 for v in z6) and all(v == 0 for v in z6s) \
    and [v == 0 for _, v in zA5s] == [False, True, True, False, True]

# (e) Adler zero
soft6 = {X6[(1, 3)]: 0, X6[(2, 6)]: 0, X6[(1, 4)]: X6[(2, 4)], X6[(1, 5)]: X6[(2, 5)]}
ad6 = sp.simplify(A6N.subs(soft6, simultaneous=True))
say('(e) A6NLSM at p1 -> 0:', ad6, '; A4NLSM at p1->0: X13,X24 -> 0 gives 0')
adl = [soft(X6, 6, A6N, i) for i in range(1, 7)]
say('    A6NLSM soft in every leg (generic map):', adl)
say('    m5 (Tr phi^3) soft in leg 1 (expected NOT zero / singular):', soft5(m5, 1) if True else None)
ok['e'] = ad6 == 0 and all(v == 0 for v in adl)

# D1: SU(2) dressing of ordered A(1234) = k (s12 + s23)
s, t = sp.symbols('s t'); u = -s - t; k = sp.Symbol('kappa')
sij = {(1, 2): s, (3, 4): s, (2, 3): t, (1, 4): t, (1, 3): u, (2, 4): u}
S = lambda a, b: sij[tuple(sorted((a, b)))]
Aord = lambda o: k * (S(o[0], o[1]) + S(o[1], o[2]))
dlt = lambda a, b: sp.Symbol(f'd{min(a,b)}{max(a,b)}')
def tr4(a, b, cc, dd):  # Tr(sigma sigma sigma sigma) in terms of delta structures (legs labels)
    return 2 * (dlt(a, b) * dlt(cc, dd) - dlt(a, cc) * dlt(b, dd) + dlt(a, dd) * dlt(b, cc))
M = 0
for perm in itertools.permutations([2, 3, 4]):
    o = (1,) + perm
    M += tr4(*o) * Aord(o)
M = sp.expand(M)
E1, E2, E3 = dlt(1, 2) * dlt(3, 4), dlt(1, 3) * dlt(2, 4), dlt(1, 4) * dlt(2, 3)
co = [sp.factor(M.coeff(E)) for E in (E1, E2, E3)]
say('D1: coefficients of d12d34, d13d24, d14d23:', co)
# Weinberg labels (all incoming): s_W = s12 = s, t_W = s13 = u (here), u_W = s14 = t (here)
ok['D1'] = sp.simplify(co[0] / s - co[1] / u) == 0 and sp.simplify(co[0] / s - co[2] / t) == 0
say('    => M = (', sp.simplify(co[0] / s), ') [s12 d12d34 + s13 d13d24 + s14 d14d23] = Weinberg chiral-limit form A(s,t,u) ∝ s')

# D2: LO scattering lengths (Weinberg mass insertion = INPUT), CGL inputs
Mpi, Fpi = 139.57, 92.4
Mw, Fw, sw, tw, uw = sp.symbols('M F s t u')
Aw = lambda s_, t_, u_: (s_ - Mw ** 2) / Fw ** 2
thr = {sw: 4 * Mw ** 2, tw: 0, uw: 0}
T0 = (3 * Aw(sw, tw, uw) + Aw(tw, sw, uw) + Aw(uw, tw, sw)).subs(thr)
T2 = (Aw(tw, sw, uw) + Aw(uw, tw, sw)).subs(thr)
a00 = sp.simplify(T0 / (32 * sp.pi)); a20 = sp.simplify(T2 / (32 * sp.pi))
say('D2: a0^0 =', a00, ', a0^2 =', a20)
v00 = float(a00.subs({Mw: Mpi, Fw: Fpi})); v20 = float(a20.subs({Mw: Mpi, Fw: Fpi}))
meas = {'a00': (0.2220, math.sqrt(0.0128**2 + 0.0050**2 + 0.0037**2)), 'a20': (-0.0432, math.sqrt(0.0086**2 + 0.0034**2 + 0.0028**2))}
cgl = {'a00': (0.220, 0.005), 'a20': (-0.0444, 0.0010)}
for key, lo in (('a00', v00), ('a20', v20)):
    m, e = meas[key]
    rel = (lo - m) / abs(m)
    say(f'    {key}: LO = {lo:.4f}; NA48/2 Ke4 = {m} +- {e:.4f}; rel dev = {100*rel:+.1f}%; pull = {(lo-m)/e:+.2f} sigma; CGL = {cgl[key]}; within 30%: {abs(rel) <= 0.30}')
    ok['D2_' + key] = abs(rel) <= 0.30
say(f'    ratio a0^2/a0^0: LO = {v20/v00:.4f} (=-2/7); NA48/2 = {meas["a20"][0]/meas["a00"][0]:.4f} (not graded)')

say('RESULTS:', ok)
say('VERDICT:', 'PASS' if all(v for kk, v in ok.items() if kk != 'b_sign_prediction') else 'FAIL',
    '(sign prediction sigma=+1:', 'hit' if ok['b_sign_prediction'] else 'MISS', ')')
open(__file__.replace('.py', '_output.txt'), 'w').write('\n'.join(out) + '\n')
