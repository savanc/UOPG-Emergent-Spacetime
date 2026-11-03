"""M2f: mass shift of Tr(phi^3) -> massive NLSM / Weinberg's s - M^2.
Pre-registration: prereg/M2f-mass-shift-2026-10-10.md (commit 89d9ffa, pushed before this script existed).
Conventions: mostly-minus; X_ij = (p_i+...+p_{j-1})^2, p_i^2 = M^2, Xt = X - M^2; c_ij = -2 p_i.p_j.
Exact sympy throughout (plus exact-rational large-delta evaluations as an independent check)."""
import itertools, math, json, random
from fractions import Fraction
import sympy as sp

M2 = sp.Symbol('M2')          # M^2
d, eps = sp.symbols('delta epsilon', positive=True)
out, ok = [], {}
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.append(s)

# ---------------------------------------------------------------- planar data (as M2d)
def chords(n):
    return [(i, j) for i in range(1, n + 1) for j in range(i + 2, n + 1) if not (i == 1 and j == n)]
def Xsym(n, pre='X'):
    return {ch: sp.Symbol(f'{pre}{ch[0]}{ch[1]}') for ch in chords(n)}
def getX(X, n, i, j, bdry=0):
    i, j = (i - 1) % n + 1, (j - 1) % n + 1
    if i > j: i, j = j, i
    if j - i <= 1 or (i == 1 and j == n): return sp.sympify(bdry)
    return X[(i, j)]
def cc(X, n, i, j, bdry=0):
    g = lambda a, b: getX(X, n, a, b, bdry)
    return g(i, j) + g(i + 1, j + 1) - g(i, j + 1) - g(i + 1, j)
def triangulations(n):
    ch = chords(n)
    cross = lambda a, b: (a[0] < b[0] < a[1] < b[1]) or (b[0] < a[0] < b[1] < a[1])
    return [T for T in itertools.combinations(ch, n - 3) if all(not cross(a, b) for a, b in itertools.combinations(T, 2))]
def A_phi3(Y, n):
    return sum(1 / sp.Mul(*[Y[ch] for ch in T]) for T in triangulations(n))
def astar(ch):
    i, j = ch
    return 1 if (i % 2 == 0 and j % 2 == 0) else (-1 if (i % 2 == 1 and j % 2 == 1) else 0)
def A4N(Y): return Y[(1, 3)] + Y[(2, 4)]
def A6N(Y):
    x = lambda i, j: getX(Y, 6, i, j)
    tot = 0
    for k in (0, 2, 4):
        r = lambda i: (i - 1 + k) % 6 + 1
        tot += (x(r(1), r(3)) + x(r(2), r(4))) * (x(r(1), r(5)) + x(r(4), r(6))) / x(r(1), r(4)) - x(r(1), r(3)) - x(r(2), r(4))
    return tot

X4, X6 = Xsym(4), Xsym(6)
mu4 = {ch: sp.Symbol(f'mu{ch[0]}{ch[1]}') for ch in chords(4)}
mu6 = {ch: sp.Symbol(f'mu{ch[0]}{ch[1]}') for ch in chords(6)}

# ---------------------------------------------------------------- (a) n = 4
Y4 = {ch: X4[ch] + mu4[ch] + d * astar(ch) for ch in chords(4)}
e4 = sp.together((d ** 2 * A_phi3(Y4, 4)).subs(d, 1 / eps))
L4 = sp.simplify(sp.limit(e4, eps, 0))
pred4 = -(X4[(1, 3)] + X4[(2, 4)] + mu4[(1, 3)] + mu4[(2, 4)])
say('(a) lim delta^2 A4(X + mu + delta a*) =', L4, '; prediction', pred4, ':', sp.simplify(L4 - pred4) == 0)
ser4 = sp.series(e4, eps, 0, 1).removeO()
say('    eps^-1 coefficient (must be 0):', sp.simplify(ser4.coeff(eps, -1)))
L4u = sp.expand(L4.subs({mu4[ch]: -M2 for ch in chords(4)}))
say('    uniform mass mu = -M^2:', L4u, ' (= -(Xt13+Xt24) = -c13 with X_{i,i+1}=M^2:',
    sp.simplify(L4u + cc(X4, 4, 1, 3, bdry=M2)) == 0, ')')
ok['a_limit'] = sp.simplify(L4 - pred4) == 0 and sp.simplify(L4u + cc(X4, 4, 1, 3, bdry=M2)) == 0

# dressing: ordered amplitude f(x, y) = kappa (x + y - 2c), x = s_{i,i+1}, y = s_{i+1,i+2}
s, t, cpar, k = sp.symbols('s t c kappa'); u = 4 * M2 - s - t
sij = {(1, 2): s, (3, 4): s, (2, 3): t, (1, 4): t, (1, 3): u, (2, 4): u}
S = lambda a, b: sij[tuple(sorted((a, b)))]
Aord = lambda o: k * (S(o[0], o[1]) + S(o[1], o[2]) - 2 * cpar)
dl = lambda a, b: sp.Symbol(f'd{min(a,b)}{max(a,b)}')
tr4 = lambda a, b, c_, e: 2 * (dl(a, b) * dl(c_, e) - dl(a, c_) * dl(b, e) + dl(a, e) * dl(b, c_))
Mamp = sp.expand(sum(tr4(*((1,) + p)) * Aord((1,) + p) for p in itertools.permutations([2, 3, 4])))
E = [dl(1, 2) * dl(3, 4), dl(1, 3) * dl(2, 4), dl(1, 4) * dl(2, 3)]
co = [sp.factor(Mamp.coeff(e)) for e in E]
say('(a) SU(2) dressing of kappa(s12+s23-2c): coefficients of d12d34, d13d24, d14d23 =', co)
# Weinberg labels: s_W = s12 = s, t_W = s13 = u, u_W = s14 = t
ok['a_dressing'] = all(sp.simplify(x - y) == 0 for x, y in zip(co, [8 * k * (s - cpar), 8 * k * (u - cpar), 8 * k * (t - cpar)]))
say('    => A(s,t,u) = 8 kappa (s - c): Weinberg (s - M^2)/F^2 iff c = M^2; uniform offsets give c = -(mu13+mu24)/2 = M^2:',
    ok['a_dressing'])

# ---------------------------------------------------------------- (b) soft behaviour
Xt4 = Xsym(4, 'Xt'); Xt6 = Xsym(6, 'Xt')
def softmap(X, n, i):
    sub = {getX(X, n, i, j): getX(X, n, i + 1, j) for j in range(1, n + 1) if getX(X, n, i, j) != 0}
    sub[getX(X, n, i - 1, i + 1)] = 0
    return sub
b1_4 = [sp.simplify(A4N(Xt4).subs(softmap(Xt4, 4, i), simultaneous=True)) for i in range(1, 5)]
b1_6 = [sp.simplify(sp.together(A6N(Xt6).subs(softmap(Xt6, 6, i), simultaneous=True))) for i in range(1, 7)]
say('(b1) massive planar soft map (on Xt) of A4N(Xt), legs 1..4:', b1_4, '; of A6N(Xt), legs 1..6:', b1_6)
ok['b1'] = all(v == 0 for v in b1_4 + b1_6)
# (b2) naive massless soft point in physical X: X13 = X24 = 0 at n = 4
L4phys = -(X4[(1, 3)] + X4[(2, 4)] - 2 * M2)
b2_4 = L4phys.subs({X4[(1, 3)]: 0, X4[(2, 4)]: 0})
say('(b2) n=4 at s = t = 0 (X13 = X24 = 0): ordered value =', b2_4, '(prediction +2*M2); Weinberg A(0,t,u) = -M^2/F^2')
ok['b2_4'] = sp.simplify(b2_4 - 2 * M2) == 0
A6m_phys = A6N({ch: X6[ch] - M2 for ch in chords(6)})
sm = {X6[(1, 3)]: 0, X6[(2, 6)]: 0, X6[(1, 4)]: X6[(2, 4)], X6[(1, 5)]: X6[(2, 5)]}
b2_6 = sp.factor(sp.together(A6m_phys.subs(sm, simultaneous=True)))
say('(b2) n=6 naive massless soft map (leg 1) in physical X of A6N(X - M^2):', b2_6,
    '; -> 0 as M -> 0:', sp.simplify(b2_6.subs(M2, 0)) == 0)
ok['b2_6_reported'] = sp.simplify(b2_6.subs(M2, 0)) == 0 and sp.simplify(b2_6) != 0

# ---------------------------------------------------------------- (c1) n = 6 limit, uniform mass (symbolic) and general mu (exact rationals)
Y6u = {ch: X6[ch] - M2 + d * astar(ch) for ch in chords(6)}
e6 = sp.together((d ** 4 * A_phi3(Y6u, 6)).subs(d, 1 / eps))
num6, den6 = sp.fraction(e6)
num6 = sp.Poly(sp.expand(num6), eps); den6 = sp.Poly(sp.expand(den6), eps)
# leading behaviour: lowest eps powers; limit = ratio of eps^m coefficients at matching lowest order
lo_n = min(m for (m,) in num6.monoms()); lo_d = min(m for (m,) in den6.monoms())
L6u = sp.simplify(num6.coeff_monomial(eps ** lo_n) / den6.coeff_monomial(eps ** lo_d)) if lo_n == lo_d else None
A6m = A6N({ch: X6[ch] - M2 for ch in chords(6)})
say('(c1) uniform mass: lowest eps power num/den =', lo_n, lo_d, '; limit == A6N(X - M^2):',
    L6u is not None and sp.simplify(L6u - A6m) == 0)
ok['c1_uniform'] = L6u is not None and sp.simplify(L6u - A6m) == 0

def A6_num(Yv):
    tot = Fraction(0)
    for T in triangulations(6):
        p = Fraction(1)
        for ch in T: p *= Yv[ch]
        tot += 1 / p
    return tot
def A6N_num(Yv):
    x = lambda i, j: (lambda a, b: Yv[(min(a, b), max(a, b))])((i - 1) % 6 + 1, (j - 1) % 6 + 1)
    tot = Fraction(0)
    for kk in (0, 2, 4):
        r = lambda i: (i - 1 + kk) % 6 + 1
        tot += (x(r(1), r(3)) + x(r(2), r(4))) * (x(r(1), r(5)) + x(r(4), r(6))) / x(r(1), r(4)) - x(r(1), r(3)) - x(r(2), r(4))
    return tot
random.seed(20261010)
worst = 0.0
for trial in range(20):
    Xv = {ch: Fraction(random.randint(-50, 50), random.randint(1, 9)) or Fraction(1, 3) for ch in chords(6)}
    mv = {ch: Fraction(random.randint(-30, 30), random.randint(1, 7)) for ch in chords(6)}
    Yv = {ch: Xv[ch] + mv[ch] for ch in chords(6)}
    target = A6N_num(Yv)
    vals = []
    for D in (Fraction(10) ** 6, Fraction(10) ** 8):
        vals.append(D ** 4 * A6_num({ch: Yv[ch] + D * astar(ch) for ch in chords(6)}))
    rel = abs(float((vals[1] - target) / target))
    worst = max(worst, rel)
say('(c1) general constant offsets mu (20 random exact-rational points): max |delta^4 A6 - A6N(X+mu)|/|A6N| at delta=1e8:', f'{worst:.2e}')
ok['c1_general_numeric'] = worst < 1e-5

# ---------------------------------------------------------------- (c2) Feynman rules, Cayley parametrisation, with mass term
# U = (1+i Phi)(1-i Phi)^{-1} = -1 + 2 sum_k (i Phi)^k ;  F^2 = 1/2 so Phi = phi^a T^a, Tr(T^aT^b)=delta^ab, canonical.
# L = (F^2/4) Tr(dU dU^dag) + (F^2 M^2/4) Tr(U + U^dag - 2)
I = sp.I
def kinetic_words(nf):
    """Tr(dU dU^dag) terms with nf fields: dict word(tuple of 0/1, 1 = derivative field) -> coefficient (times F^2/4 * 4)."""
    W = {}
    for kk in range(1, nf):
        ll = nf - kk
        for j in range(kk):
            for jp in range(ll):
                w = tuple([0] * j + [1] + [0] * (kk - 1 - j) + [0] * jp + [1] + [0] * (ll - 1 - jp))
                W[w] = W.get(w, 0) + (I ** kk) * ((-I) ** ll)
    Fsq = sp.Rational(1, 2)
    return {w: sp.nsimplify(sp.expand(Fsq / 4 * 4 * cf)) for w, cf in W.items()}
def mass_words(nf):
    Fsq = sp.Rational(1, 2)
    if nf % 2: return {}
    return {tuple([0] * nf): Fsq * M2 / 4 * 4 * (-1) ** (nf // 2)}
def dotv(u, v, dot):
    return sp.expand(sum(cu * cv * dot(a, b) for a, cu in u.items() for b, cv in v.items()))
def vertex(moms, dot):
    """Ordered vertex (Lagrangian coefficient, Feynman rule = i*V) for cyclically ordered legs with incoming momenta moms."""
    nf = len(moms); tot = 0
    for W in (kinetic_words(nf), mass_words(nf)):
        for w, cf in W.items():
            for r in range(nf):
                legs = [moms[(p + r) % nf] for p in range(nf)]
                pos = [p for p in range(nf) if w[p] == 1]
                fac = -dotv(legs[pos[0]], legs[pos[1]], dot) if len(pos) == 2 else 1
                tot += cf * fac
    return sp.expand(tot)
def make_dot(n, Xt):
    def dot(i, j):
        i, j = (i - 1) % n + 1, (j - 1) % n + 1
        if i == j: return M2
        a, b = min(i, j), max(i, j)
        if b == a + 1: return (getX(Xt, n, a, a + 2) - M2) / 2
        if a == 1 and b == n: return (getX(Xt, n, n, n + 2) - M2) / 2
        return -cc(Xt, n, a, b) / 2
    return dot
leg = lambda n, i: {((i - 1) % n) + 1: 1}
def P(n, ls):
    dd = {}
    for l in ls: dd[((l - 1) % n) + 1] = dd.get(((l - 1) % n) + 1, 0) + 1
    return dd
neg = lambda u_: {kk: -v for kk, v in u_.items()}
dot4 = make_dot(4, Xt4)
A4FR = sp.simplify(vertex([leg(4, i) for i in range(1, 5)], dot4))
rho4 = sp.simplify(A4FR / A4N(Xt4))
say('(c2) Cayley + mass term: A4_FR =', sp.factor(A4FR), '; rho4 = A4_FR/(Xt13+Xt24) =', rho4)
dot6 = make_dot(6, Xt6)
A6FR = vertex([leg(6, i) for i in range(1, 7)], dot6)
for (a, b) in ((1, 4), (2, 5), (3, 6)):
    Lg = [leg(6, i) for i in range(a, b)]; Rg = [leg(6, i) for i in range(b, a + 6)]
    Pm = P(6, range(a, b))
    A6FR += -vertex(Lg + [neg(Pm)], dot6) * vertex(Rg + [Pm], dot6) / getX(Xt6, 6, a, b)
rho6 = sp.simplify(sp.together(A6FR) / A6N(Xt6))
say('    A6_FR / A6N(Xt) =', rho6, '; prediction rho6 = -rho4^2 =', sp.simplify(-rho4 ** 2))
ok['c2'] = rho4.free_symbols == set() and rho6.free_symbols == set() and sp.simplify(rho6 + rho4 ** 2) == 0
# contact-term check: the 6-pt contact vertex depends on M2 (parametrisation-dependent pieces), the total does not
V6c = vertex([leg(6, i) for i in range(1, 7)], dot6)
say('    (info) 6-pt contact vertex M2-coefficient (nonzero => mass enters vertices, cancels in total):', sp.factor(sp.diff(V6c, M2)))
# naive mass term only (no Tr(U+U^dag) potential, just -M^2 Tr Phi^2 /2): expect hidden zero spoiled
def vertex_naive(moms, dot):
    nf = len(moms); tot = 0
    for w, cf in kinetic_words(nf).items():
        for r in range(nf):
            legs = [moms[(p + r) % nf] for p in range(nf)]
            pos = [p for p in range(nf) if w[p] == 1]
            tot += cf * (-dotv(legs[pos[0]], legs[pos[1]], dot))
    return sp.expand(tot)
A4naive = sp.factor(vertex_naive([leg(4, i) for i in range(1, 5)], dot4))
say('    (info) Cayley, naive mass term only: A4 =', A4naive, '(not proportional to c13 = Xt13+Xt24 unless M=0)')

# ---------------------------------------------------------------- (d) uniqueness of constant offsets
lam = sp.Symbol('lambda')
v6 = {ch: sp.Symbol(f'v{ch[0]}{ch[1]}') for ch in chords(6)}
Z6 = Xsym(6, 'Z')
# (d0) unobservable direction
d0_6 = sp.simplify(sp.together(A6N({ch: Z6[ch] + lam * astar(ch) for ch in chords(6)}) - A6N(Z6)))
Z4 = Xsym(4, 'Z')
d0_4 = sp.simplify(A4N({ch: Z4[ch] + lam * astar(ch) for ch in chords(4)}) - A4N(Z4))
say('(d0) A6N(Z + lambda a*) - A6N(Z) =', d0_6, '; A4N likewise:', d0_4)
ok['d0'] = d0_6 == 0 and d0_4 == 0
def coeff_eqs(expr, vars_):
    num = sp.numer(sp.together(expr))
    return [e for e in sp.Poly(sp.expand(num), *vars_).coeffs() if e != 0]
# (d1) with (P): v_oe = 0 ; require A6N(Z + v) = A6N(Z)
oe = [(1, 4), (2, 5), (3, 6)]
vP = {ch: (0 if ch in oe else v6[ch]) for ch in chords(6)}
eqs = coeff_eqs(A6N({ch: Z6[ch] + vP[ch] for ch in chords(6)}) - A6N(Z6), list(Z6.values()))
unk = [v6[ch] for ch in chords(6) if ch not in oe]
sol_d1 = sp.solve(eqs, unk, dict=True)
say('(d1) with (P) [v_oe = 0]: #equations', len(eqs), '; solutions:', sol_d1)
def is_astar_line(sol, chs):
    # all solutions are of the form v = lambda * a*  (one free parameter)
    if len(sol) != 1: return False
    vec = {ch: sp.sympify(vP[ch]).subs(sol[0]) if ch not in oe else 0 for ch in chs}
    free = set().union(*[sp.sympify(x).free_symbols for x in vec.values()])
    if len(free) != 1: return False
    f = free.pop()
    return all(sp.simplify(vec[ch] - (-f if False else 0) - sp.diff(vec[ch], f) * f) == 0 for ch in chs) and \
        len({sp.simplify(sp.diff(vec[ch], f) * astar(ch)) for ch in chs if astar(ch) != 0}) == 1
ok['d1'] = is_astar_line(sol_d1, chords(6))
say('    => v = lambda * a* (uniform mass up to delta-reparametrisation):', ok['d1'])
# (d1') without (P): all nine v free; numerators after clearing (Z14+v14) etc.
eqs_full = coeff_eqs(A6N({ch: Z6[ch] + v6[ch] for ch in chords(6)}) - A6N(Z6), list(Z6.values()))
sol_full = sp.solve(eqs_full, list(v6.values()), dict=True)
say("(d1') without (P), all nine offsets free: solutions:", sol_full)
ok['d1_noP_reported'] = True
# (d2) hidden zeros with (P): L = A6N(Xt + v) must vanish on the six skinny-rectangle loci c(Xt) = 0
def locus(X, n, conds):
    eqs_ = [cc(X, n, *q) for q in conds]
    for vs in itertools.combinations(list(X.values()), len(eqs_)):
        sol = sp.solve(eqs_, vs, dict=True)
        if sol and all(sp.simplify(e.subs(sol[0])) == 0 for e in eqs_):
            return sol[0]
    raise ValueError(conds)
eqs_d2 = []
for i in range(1, 7):
    Lc = locus(Xt6, 6, [(i, i + 2), (i, i + 3), (i, i + 4)])
    expr = A6N({ch: Xt6[ch] + vP[ch] for ch in chords(6)}).subs(Lc, simultaneous=True)
    eqs_d2 += coeff_eqs(expr, list(Xt6.values()))
sol_d2 = sp.solve(eqs_d2, unk, dict=True)
say('(d2) hidden zeros on all six loci, with (P): solutions:', sol_d2)
ok['d2'] = is_astar_line(sol_d2, chords(6))
say('    => same set as (d1):', ok['d2'])

# (d2') hidden zeros WITHOUT (P): all nine offsets free (reported, not graded)
eqs_d2f = []
for i in range(1, 7):
    Lc = locus(Xt6, 6, [(i, i + 2), (i, i + 3), (i, i + 4)])
    expr = A6N({ch: Xt6[ch] + v6[ch] for ch in chords(6)}).subs(Lc, simultaneous=True)
    eqs_d2f += coeff_eqs(expr, list(Xt6.values()))
sol_d2f = sp.solve(eqs_d2f, list(v6.values()), dict=True)
say("(d2') hidden zeros on all six loci, all nine offsets free (no (P)): solutions:", sol_d2f)
G_d2f = sp.groebner(eqs_d2f, *[v6[ch] for ch in chords(6)], order='lex')
G_d1f = sp.groebner(eqs_full, *[v6[ch] for ch in chords(6)], order='lex')
say("    Groebner bases (lex) — d2' (hidden zeros, no P):", list(G_d2f.exprs), "; d1' (target, no P):", list(G_d1f.exprs))
ok['d_groebner_linear'] = all(sp.Poly(g, *v6.values()).total_degree() == 1 for g in list(G_d2f.exprs) + list(G_d1f.exprs))
say('    all Groebner generators linear (so the solution sets above are complete, no extra branches):', ok['d_groebner_linear'])
# (d2') n=4: L4 = -(X13+X24+mu13+mu24) vanishing on c13 = X13 + X24 - 2M^2 = 0
m13, m24 = mu4[(1, 3)], mu4[(2, 4)]
d2_4 = sp.solve(sp.Poly(sp.expand(pred4.subs(X4[(2, 4)], 2 * M2 - X4[(1, 3)])), X4[(1, 3)]).coeffs(), [m13], dict=True)
say('(d2) n=4 hidden zero c13 = 0 forces:', d2_4, ' i.e. c = -(mu13+mu24)/2 = M^2')
ok['d2_4'] = d2_4 == [{m13: -2 * M2 - m24}]
# (d3) n=6 family with (P) and a free c: mu_oo = -c + l, mu_ee = -c - l, mu_oe = -M^2: check it is a consistent function
cfam = sp.Symbol('c')
Yf = {ch: X6[ch] + (-M2 if ch in oe else -cfam) for ch in chords(6)}
Lf = A6N(Yf)
res14 = sp.factor(sp.simplify(sp.together(Lf * (X6[(1, 4)] - M2)).subs(X6[(1, 4)], M2)))
say('(d3) n=6 family (P), oo/ee offsets -c: residue at X14 = M^2:', res14,
    '; = product of two n=4 family amplitudes (X13+X24-2c)(X15+X46-2c):',
    sp.simplify(res14 - (X6[(1, 3)] + X6[(2, 4)] - 2 * cfam) * (X6[(1, 5)] + X6[(4, 6)] - 2 * cfam)) == 0)
hz = sp.simplify(Lf.subs({ch: v + M2 for ch, v in locus(Xsym(6), 6, [(1, 3), (1, 4), (1, 5)]).items()} if False else {}, simultaneous=True))
# hidden zero of the family on locus 1 (c in physical X; boundary M^2)
Lc1 = locus(Xt6, 6, [(1, 3), (1, 4), (1, 5)])
fam_on_locus = sp.factor(sp.together(A6N({ch: Xt6[ch] + (0 if ch in oe else M2 - cfam) for ch in chords(6)}).subs(Lc1, simultaneous=True)))
say('    family on skinny rectangle 1 (in Xt):', fam_on_locus, '-> zero iff c = M^2')

# ---------------------------------------------------------------- (e) data
Mpi = 139.57039; fpi = 130.2; Fpdg = fpi / math.sqrt(2); Fcgl = 92.4
meas = {'a00': (0.2220, math.sqrt(0.0128 ** 2 + 0.0050 ** 2 + 0.0037 ** 2)), 'a20': (-0.0432, math.sqrt(0.0086 ** 2 + 0.0034 ** 2 + 0.0028 ** 2))}
Mw, Fw = sp.symbols('M F', positive=True)
Aw = lambda s_, t_, u_: (s_ - cpar) / Fw ** 2
thr = (4 * Mw ** 2, 0, 0)
T0 = 3 * Aw(*thr) + Aw(thr[1], thr[0], thr[2]) + Aw(thr[2], thr[1], thr[0])
T2 = Aw(thr[1], thr[0], thr[2]) + Aw(thr[2], thr[1], thr[0])
a00c = sp.simplify(T0 / (32 * sp.pi)); a20c = sp.simplify(T2 / (32 * sp.pi))
say('(e) general c: a0^0 =', a00c, ', a0^2 =', a20c, '; at c = M^2:', sp.simplify(a00c.subs(cpar, Mw ** 2)), ',', sp.simplify(a20c.subs(cpar, Mw ** 2)))
ok['e_formulae'] = sp.simplify(a00c.subs(cpar, Mw ** 2) - 7 * Mw ** 2 / (32 * sp.pi * Fw ** 2)) == 0 and \
    sp.simplify(a20c.subs(cpar, Mw ** 2) + Mw ** 2 / (16 * sp.pi * Fw ** 2)) == 0
res = {}
for lab, F_ in (('PDG2024', Fpdg), ('CGL', Fcgl)):
    for key, ex in (('a00', a00c), ('a20', a20c)):
        v = float(ex.subs({cpar: Mw ** 2}).subs({Mw: Mpi, Fw: F_}))
        m, e = meas[key]; rel = (v - m) / abs(m); pull = (v - m) / e
        res[(lab, key)] = (v, rel, pull)
        say(f'    [{lab}: M={Mpi}, F={F_:.3f}] {key}: LO = {v:.4f}; NA48/2 = {m} +- {e:.4f}; rel dev = {100*rel:+.1f}%; pull = {pull:+.2f} sigma; within 30%: {abs(rel) <= 0.30}')
ok['e_PDG'] = all(abs(res[('PDG2024', kk)][1]) <= 0.30 for kk in ('a00', 'a20'))
ratio_LO = sp.simplify(a00c / a20c)
say('    ratio a0^0/a0^2 (general c) =', ratio_LO, '; at c = M^2:', sp.simplify(ratio_LO.subs(cpar, Mw ** 2)),
    f'; NA48/2: {meas["a00"][0]/meas["a20"][0]:.3f} (reported, not graded)')
csol = sp.solve(sp.Eq(ratio_LO.subs(Mw, 1), meas['a00'][0] / meas['a20'][0]), cpar)
say(f'    (info) the c that would reproduce the measured ratio at LO: c/M^2 = {[float(x) for x in csol]} (NOT used; LO is not accurate enough)')

say('RESULTS:', ok)
graded = ['a_limit', 'a_dressing', 'c1_uniform', 'c2', 'd1', 'e_PDG']
say('GRADED (script side):', {g: ok[g] for g in graded}, '->', 'all hold' if all(ok[g] for g in graded) else 'MISS')
open(__file__.replace('.py', '_output.txt'), 'w').write('\n'.join(out) + '\n')
