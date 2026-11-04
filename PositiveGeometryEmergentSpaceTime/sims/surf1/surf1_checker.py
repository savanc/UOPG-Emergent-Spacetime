#!/usr/bin/env python3
"""SURF-1 locked checker (rung R2 of 3; author approved 2026-10-28).
Prereg: prereg/SURF-1-colour-sign-coherence-2026-10-28.md.  Run id SURF1-2026-10-28-r1.
Object: colour weights of the one-loop, colour-dressed cubic adjoint scalar ("Tr phi^3") for gauge group SU(N) vs U(N),
  n = 2, 3, 4 external legs (amputated; no tadpoles, no external-leg bubbles).  Double-line (index-loop) enumeration:
  vertex = sum of BOTH cyclic orientations Tr(phi_A phi_B phi_C) + Tr(phi_A phi_C phi_B), weight 1 each (d-coupling);
  propagator <phi_ij phi_kl> = delta_il delta_jk - (c/N) delta_ij delta_kl  (c = 1: SU(N); c = 0: U(N)).
  Each closed index loop gives N.  W(Gamma) = sum_orient sum_ghost (-c)^k N^(loops - k)  (exact Laurent polynomial).
Observable: K_{G,ch}(N) = W(tree_ch o G) / W(tree_ch o tree_ch): colour-summed interference of the one-loop graph G with
  the tree in channel ch (external colour summed with the same propagator).  Sign-coherent at N iff every K > 0.
  S := { integer N >= 3 : all K_{G,ch}(N) > 0 over n = 2, 3, 4 }, decided EXACTLY for all N >= 3 (Cauchy root bound).
Verdict (locked, primary): ILL-DEFINED if any gate fails (planted, broken, valid-alternative, gate self-tests);
  else SELECTS-3 if S finite and 3 in S; DISCRETE-NOT-3 if S finite, nonempty, 3 not in S; EMPTY if S empty;
  RANGE (FM-RANGE) if S contains every N >= N0 for some N0; sub-label EXCLUDES-3 / INCLUDES-3.
Planted (CITED Haber 1912.13302 eqs. (54)-(60) and trace list; must hold exactly as Laurent polynomials):
  P1 closed single propagator (bivalent trace vertex) W = N^2 - 1 (c=1), N^2 (c=0);
  P2 theta (tree3 o tree3) W = 2 (N^2-1)(N^2-4)/N;  P3 K_triangle = (N^2-12)/N;  P4 K_bubble = 2 (N^2-4)/N;
  P5 U(N) (c=0): every W has only nonnegative coefficients;  P6 f-coupling theta |W| = 2 N (N^2-1).
Broken (must be REJECTED by the planted gate): B1 ghost dropped but labelled SU(N) (c=0); B2 ghost sign flipped
  (c=-1); B3 single cyclic orientation per vertex.
Valid alternatives (must be ACCEPTED): V1 glue-order invariance W(G o T) == W(T o G) summed over channels (what makes
  full-tree interference a well-defined channel sum; full-tree K and its S reported, not verdict-bearing);
  V2 external relabelling (2,1,4,3) gives the same multiset of K polynomials; V3 propagator scaled by 2 leaves every
  sign set unchanged.
Gate self-tests (METHOD JORD-1 lesson (a)): every boolean gate the verdict reads gets a planted-true and a
  planted-false input; scale convention (vertex weight 1 per orientation; c = 1) asserted through P1.
Null (report): N1 U(N) c = 0; N2 ghost coefficient c in {0,1/4,...,2} (fixed grid), S_c on N = 3..30.
Rival (report only): R1 f-coupled cubic (vertex Tr(ABC) - Tr(ACB), times -i): |K| polynomials and whether any K
  changes sign in N >= 3 (convention-robust).
Modes: planted | broken | live.
GUARD (hardened, METHOD 2026-10-20 F-DIM-MASS): guard() inside EVERY scoring function re-verifies on EVERY call the
checker sha256 against the prereg and that the prereg commit is an ancestor of origin/main.  No pass flag; caches
keyed by origin/main sha only; `git fetch` once per process.
"""
import hashlib, itertools, json, re, subprocess, sys, time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/SURF-1-colour-sign-coherence-2026-10-28.md'
OUTDIR = HERE.parent

def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)

_FETCH_DONE = []          # fetch once per process (NOT a pass flag)
_ANC_BY_ORIGIN = {}       # origin/main sha -> (prereg sha, is_ancestor)

def _origin_sha():
    return _git('rev-parse', '--verify', '-q', 'refs/remotes/origin/main').stdout.strip()

def guard():
    if not _FETCH_DONE:
        if _git('fetch', '-q', 'origin').returncode != 0:
            sys.exit("GUARD REFUSED: git fetch failed")
        _FETCH_DONE.append(True)
    osha = _origin_sha()
    if not osha:
        sys.exit("GUARD REFUSED: no origin/main ref")
    if osha not in _ANC_BY_ORIGIN:
        psha = _git('log', '--format=%H', '--diff-filter=A', '-n', '1', '--', PREREG).stdout.strip()
        ok = bool(psha) and _git('merge-base', '--is-ancestor', psha, osha).returncode == 0
        _ANC_BY_ORIGIN[osha] = (psha, ok)
    psha, ok = _ANC_BY_ORIGIN[osha]
    if not psha:
        sys.exit(f"GUARD REFUSED: {PREREG} has no commit")
    if not ok:
        sys.exit(f"GUARD REFUSED: prereg commit {psha[:9]} is not an ancestor of origin/main (not pushed)")
    pre = REPO / PREREG
    m = re.search(r'surf1_checker\.py` sha256 `([0-9a-f]{64})`', pre.read_text()) if pre.exists() else None
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker hash matches (re-verified on every scoring call)")

# ---------------- graphs ----------------
# A diagram: {'V': [tuple(half-edges)], 'E': [(h,h')], 'X': {leg: half-edge}}.  Half-edge names are strings.

def D(V, E, X):
    return {'V': [tuple(v) for v in V], 'E': [tuple(e) for e in E], 'X': dict(X)}

def pref(d, p):
    r = lambda h: p + h
    return D([[r(h) for h in v] for v in d['V']], [(r(a), r(b)) for a, b in d['E']], {k: r(h) for k, h in d['X'].items()})

def glue(d1, d2):
    """Closed graph: identify external leg l of d1 with leg l of d2 by one propagator."""
    a, b = pref(d1, 'L.'), pref(d2, 'R.')
    assert set(a['X']) == set(b['X'])
    return D(a['V'] + b['V'], a['E'] + b['E'] + [(a['X'][l], b['X'][l]) for l in sorted(a['X'])], {})

def closed_self(d):
    """Close a 2-leg diagram on itself (interference with the 2-pt 'tree' = identity)."""
    l1, l2 = sorted(d['X'])
    return D(d['V'], d['E'] + [(d['X'][l1], d['X'][l2])], {})

def tree3():
    return D([('1', '2', '3')], [], {1: '1', 2: '2', 3: '3'})

def tree4(ch):
    (i, j), (k, l) = ch
    return D([(f'{i}', f'{j}', 'e'), (f'{k}', f'{l}', 'f')], [('e', 'f')], {i: f'{i}', j: f'{j}', k: f'{k}', l: f'{l}'})

def bubble2():
    return D([('1', 'a', 'b'), ('2', 'b2', 'a2')], [('a', 'a2'), ('b', 'b2')], {1: '1', 2: '2'})

def triangle3(legs=(1, 2, 3)):
    x, y, z = legs
    return D([(f'{x}', 'p', 'q'), (f'{y}', 'q2', 'r'), (f'{z}', 'r2', 'p2')],
             [('p', 'p2'), ('q', 'q2'), ('r', 'r2')], {x: f'{x}', y: f'{y}', z: f'{z}'})

def box4(order):
    a, b, c, d = order
    return D([(f'{a}', 'ab', 'da2'), (f'{b}', 'bc', 'ab2'), (f'{c}', 'cd', 'bc2'), (f'{d}', 'da', 'cd2')],
             [('ab', 'ab2'), ('bc', 'bc2'), ('cd', 'cd2'), ('da', 'da2')], {k: f'{k}' for k in order})

def tritree4(ch):
    """Triangle on legs (i, j, internal m) + tree vertex (k, l, m')."""
    (i, j), (k, l) = ch
    return D([(f'{i}', 'p', 'q'), (f'{j}', 'q2', 'r'), ('m2', 'r2', 'p2'), (f'{k}', f'{l}', 'm')],
             [('p', 'p2'), ('q', 'q2'), ('r', 'r2'), ('m', 'm2')], {i: f'{i}', j: f'{j}', k: f'{k}', l: f'{l}'})

def bubins4(ch):
    (i, j), (k, l) = ch
    return D([(f'{i}', f'{j}', 'a'), ('a2', 'b1', 'b2'), ('c2', 'b2x', 'b1x'), (f'{k}', f'{l}', 'c')],
             [('a', 'a2'), ('b1', 'b1x'), ('b2', 'b2x'), ('c', 'c2')], {i: f'{i}', j: f'{j}', k: f'{k}', l: f'{l}'})

CH = {'s': ((1, 2), (3, 4)), 't': ((1, 4), (2, 3)), 'u': ((1, 3), (2, 4))}

def loop_graphs4():
    G = {}
    for name, o in (('box1234', (1, 2, 3, 4)), ('box1243', (1, 2, 4, 3)), ('box1324', (1, 3, 2, 4))):
        G[name] = box4(o)
    for c, ch in CH.items():
        G[f'tri_{c}'] = tritree4(ch)
        G[f'tri_{c}_flip'] = tritree4((ch[1], ch[0]))
        G[f'bub_{c}'] = bubins4(ch)
    return G

# ---------------- index-loop enumeration ----------------
class UF:
    def __init__(s, n): s.p = list(range(n))
    def f(s, x):
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b): s.p[s.f(a)] = s.f(b)

def weight_table(g, coupling='d'):
    """Exact enumeration.  Returns {(exp_N, k_ghost): integer coefficient}; W = sum coef * (-c)^k * N^exp.
    coupling: 'd' (both orientations +1), 'f' (+1, -1; overall (-i)^V applied: V must be even), 'single' (base only)."""
    guard()
    key_ = (tuple(g['V']), tuple(g['E']), coupling)
    if key_ in _WT_CACHE:          # computation memo (results only; guard() above still runs on every call)
        return dict(_WT_CACHE[key_])
    H = [h for v in g['V'] for h in v]
    assert len(H) == len(set(H)) and sorted(H) == sorted(x for e in g['E'] for x in e), 'graph not closed/simple'
    idx = {h: n for n, h in enumerate(H)}
    I = lambda h: 2 * idx[h]; O = lambda h: 2 * idx[h] + 1
    orients = []
    for v in g['V']:
        if len(v) == 2:
            orients.append([(v, 1)])
        else:
            a, b, c = v
            if coupling == 'd':
                orients.append([((a, b, c), 1), ((a, c, b), 1)])
            elif coupling == 'f':
                orients.append([((a, b, c), 1), ((a, c, b), -1)])
            elif coupling == 'single':
                orients.append([((a, b, c), 1)])
            else:
                raise ValueError(coupling)
    out = {}
    E = g['E']
    for choice in itertools.product(*orients):
        sgn = 1
        base = UF(2 * len(H))
        for (cyc, s) in choice:
            sgn *= s
            for t in range(len(cyc)):
                base.u(O(cyc[t]), I(cyc[(t + 1) % len(cyc)]))
        for mask in range(1 << len(E)):
            uf = UF(2 * len(H)); uf.p = list(base.p)
            k = 0
            for e_i, (h, h2) in enumerate(E):
                if mask >> e_i & 1:
                    k += 1; uf.u(I(h), O(h)); uf.u(I(h2), O(h2))
                else:
                    uf.u(I(h), O(h2)); uf.u(O(h), I(h2))
            comp = len({uf.f(x) for x in range(2 * len(H))})
            key = (comp - k, k)
            out[key] = out.get(key, 0) + sgn
    if coupling == 'f':
        V3 = sum(1 for v in g['V'] if len(v) == 3)
        assert V3 % 2 == 0
        ph = (-1) ** (V3 // 2)
        out = {k_: ph * v for k_, v in out.items()}
    out = {k_: v for k_, v in out.items() if v}
    _WT_CACHE[key_] = dict(out)
    return out

_WT_CACHE = {}

def laurent(tab, c):
    """Laurent polynomial in N (dict exp -> Fraction) at ghost coefficient c (Fraction)."""
    guard()
    L = {}
    for (e, k), v in tab.items():
        L[e] = L.get(e, Fraction(0)) + Fraction(v) * (-Fraction(c)) ** k
    return {e: v for e, v in L.items() if v}

def ev(L, N):
    return sum(v * Fraction(N) ** e for e, v in L.items())

def lmul(A, B):
    R = {}
    for a, x in A.items():
        for b, y in B.items():
            R[a + b] = R.get(a + b, 0) + x * y
    return {e: v for e, v in R.items() if v}

def lsc(A, s):
    return {e: v * s for e, v in A.items() if v * s}

def poly(*terms):
    """Laurent poly from (coef, exp) pairs."""
    R = {}
    for cf, e in terms:
        R[e] = R.get(e, 0) + Fraction(cf)
    return {e: v for e, v in R.items() if v}

def leq(A, B):
    return {e: v for e, v in A.items() if v} == {e: v for e, v in B.items() if v}

# ---------------- exact sign sets over all integers N >= 3 ----------------
def as_poly(L):
    lo = min(L); hi = max(L)
    return lo, [L.get(e, Fraction(0)) for e in range(lo, hi + 1)]   # coeffs low->high, times N^lo

def cauchy(coeffs):
    an = coeffs[-1]
    return 1 + max((abs(a / an) for a in coeffs[:-1]), default=Fraction(0))

def sign_profile(num, den, Nmin=3):
    """Exact: returns (positive set description).  K = num/den.  Both Laurent; sign(N^lo)>0 for N>0.
    Returns dict {'bound': B, 'pos_below': sorted N in [Nmin, B] with K>0, 'tail_positive': bool,
    'den_ok': den>0 for all N>=Nmin}."""
    guard()
    out = {}
    for nm, L in (('num', num), ('den', den)):
        if not L:
            out[nm] = None; continue
        lo, cs = as_poly(L)
        B = int(cauchy(cs)) + 1
        out[nm] = (B, cs[-1] > 0)
    if out['den'] is None or out['num'] is None:
        return {'degenerate': True}
    B = max(out['num'][0], out['den'][0], Nmin)
    pos = [N for N in range(Nmin, B + 1) if ev(num, N) * ev(den, N) > 0]
    den_ok = all(ev(den, N) > 0 for N in range(Nmin, B + 1)) and out['den'][1]
    return {'bound': B, 'pos_upto_bound': pos, 'tail_positive': out['num'][1] == out['den'][1], 'den_ok': den_ok}

def classify(profiles, Nmin=3):
    """Intersect positivity sets.  S = intersection; returns (label, finite_part, N0 or None)."""
    guard()
    if any(p.get('degenerate') for p in profiles):
        return ('DEGENERATE', [], None)
    B = max(p['bound'] for p in profiles)
    tail = all(p['tail_positive'] for p in profiles)
    S = [N for N in range(Nmin, B + 1) if all((N in p['pos_upto_bound']) if N <= p['bound'] else p['tail_positive']
                                               for p in profiles)]
    if tail:
        # S contains every N > B; find N0 = least N such that all N' >= N are in S
        N0 = B + 1
        while N0 - 1 >= Nmin and (N0 - 1) in S:
            N0 -= 1
        label = 'RANGE'
        return (label + (' INCLUDES-3' if 3 in S else ' EXCLUDES-3'), [N for N in S if N < N0], N0)
    if not S:
        return ('EMPTY', [], None)
    return ('SELECTS-3' if 3 in S else 'DISCRETE-NOT-3', S, None)

# ---------------- model evaluation ----------------
def W(g, c=1, coupling='d'):
    guard()
    return laurent(weight_table(g, coupling), c)

P1G = D([('a', 'b')], [('a', 'b')], {})

def all_K(c=1, coupling='d', relabel=None, scale=1):
    """Returns {name: (num, den)} Laurent pairs for all interference ratios at n=2,3,4."""
    guard()
    R = {}
    sc = lambda g, L: lsc(L, Fraction(scale) ** len(g['E']))
    g2 = closed_self(bubble2()); g2d = P1G
    R['n2:bubble'] = (sc(g2, W(g2, c, coupling)), sc(g2d, W(g2d, c, coupling)))
    t3 = tree3()
    gt = glue(tree3(), triangle3()); gd = glue(t3, t3)
    R['n3:triangle'] = (sc(gt, W(gt, c, coupling)), sc(gd, W(gd, c, coupling)))
    G4 = loop_graphs4()
    chs = CH if relabel is None else {k: tuple(tuple(relabel[x] for x in p) for p in v) for k, v in CH.items()}
    for cn, ch in chs.items():
        T = tree4(ch); TT = glue(T, T)
        den = sc(TT, W(TT, c, coupling))
        for gn, g in G4.items():
            gg = glue(T, g)
            R[f'n4:{gn}|{cn}'] = (sc(gg, W(gg, c, coupling)), den)
    return R

def fmt(L):
    return ' + '.join(f'({v})N^{e}' for e, v in sorted(L.items(), reverse=True)) or '0'

# ---------------- planted / broken gates ----------------
def planted_checks(c=1, coupling='d', expect_override=None):
    guard()
    N2m1 = poly((1, 2), (-1, 0)) if c == 1 else None
    exp = {
        'P1_single_loop': poly((1, 2), (-1, 0)),
        'P2_theta': lmul(lmul(poly((2, 0)), poly((1, 2), (-1, 0))), lmul(poly((1, 2), (-4, 0)), poly((1, -1)))),
        'P3_K_triangle': poly((1, 1), (-12, -1)),
        'P4_K_bubble': poly((2, 1), (-8, -1)),
    }
    if expect_override:
        exp.update(expect_override)
    got = {}
    got['P1_single_loop'] = W(P1G, c, coupling)
    th = glue(tree3(), tree3())
    got['P2_theta'] = W(th, c, coupling)
    K4 = W(glue(tree3(), triangle3()), c, coupling)
    # K = K4 / theta must equal expected: check K4 == expected * theta (exact)
    res = {}
    for k in ('P1_single_loop', 'P2_theta'):
        res[k] = leq(got[k], exp[k])
    res['P3_K_triangle'] = leq(K4, lmul(exp['P3_K_triangle'], got['P2_theta'])) and bool(got['P2_theta'])
    Kb = W(closed_self(bubble2()), c, coupling)
    res['P4_K_bubble'] = leq(Kb, lmul(exp['P4_K_bubble'], got['P1_single_loop'])) and bool(got['P1_single_loop'])
    return res, {k: fmt(v) for k, v in got.items()}

def p5_unitary_nonneg():
    guard()
    tabs = []
    for nm, (num, den) in all_K(c=0).items():
        tabs.append(all(v > 0 for v in num.values()) and all(v > 0 for v in den.values()))
    return all(tabs)

def p6_f_theta():
    guard()
    L = W(glue(tree3(), tree3()), 1, 'f')
    target = lmul(poly((2, 1)), poly((1, 2), (-1, 0)))
    return leq(L, target) or leq(L, lsc(target, -1)), fmt(L)

def planted_gate(res):
    """Boolean the verdict reads."""
    return bool(res) and all(res.values())

def gate_selftests():
    guard()
    out = {}
    out['planted_gate_true'] = planted_gate({'a': True, 'b': True}) is True
    out['planted_gate_false'] = planted_gate({'a': True, 'b': False}) is False
    out['planted_gate_empty_false'] = planted_gate({}) is False
    # planted-false input to the real planted check: wrong expected P1 = N^2 must FAIL
    r_bad, _ = planted_checks(expect_override={'P1_single_loop': poly((1, 2))})
    out['planted_check_detects_wrong_expectation'] = planted_gate(r_bad) is False
    # classify() on synthetic sign data
    def prof(L):
        return sign_profile(L, poly((1, 0)))
    tests = [
        ([poly((1, 2), (1, 0))], 'RANGE INCLUDES-3'),
        ([poly((1, 2), (-12, 0))], 'RANGE EXCLUDES-3'),
        ([poly((1, 2), (-12, 0)), poly((-1, 2), (-1, 0))], 'EMPTY'),
        ([lmul(poly((-1, 1), (3, 0)), poly((1, 1), (-6, 0)))], 'DISCRETE-NOT-3'),   # -(N-3)(N-6) > 0 : N = 4, 5
        ([lmul(poly((-1, 1), (2, 0)), poly((1, 1), (-4, 0)))], 'SELECTS-3'),        # -(N-2)(N-4) > 0 : N = 3
    ]
    for n_, (Ls, want) in enumerate(tests):
        lab = classify([prof(L) for L in Ls])[0]
        out[f'classify_{n_}_{want}'] = (lab == want)
    out['classify_discrete_set'] = classify([prof(lmul(poly((-1, 1), (3, 0)), poly((1, 1), (-6, 0))))])[1] == [4, 5]
    # scale convention asserted: vertex weight 1 per orientation, c = 1 -> single loop N^2 - 1
    out['scale_convention_P1'] = leq(W(P1G, 1), poly((1, 2), (-1, 0)))
    return out

def broken_variants():
    guard()
    out = {}
    for name, kw in (('B1_no_ghost_as_SU', {'c': 0}), ('B2_ghost_sign_flipped', {'c': -1}),
                     ('B3_single_orientation', {'coupling': 'single'})):
        res, got = planted_checks(**kw)
        out[name] = {'planted_gate': planted_gate(res), 'checks': res, 'got': got, 'rejected': not planted_gate(res)}
    return out

def valid_alternatives(Kd):
    guard()
    out = {}
    # V1 linearity: W(G o (sum of trees)) == sum_c W(G o tree_c), checked on the box1234 graph
    g = loop_graphs4()['box1234']
    full = 0
    tabsum = {}
    for cn, ch in CH.items():
        L = W(glue(tree4(ch), g))
        for e, v in L.items():
            tabsum[e] = tabsum.get(e, 0) + v
    # direct: a formal sum of trees is not a single graph; linearity is verified by recomputing each term twice
    # with independent half-edge prefixes (glue order swapped), which must agree exactly.
    tabsum2 = {}
    for cn, ch in CH.items():
        L = W(glue(g, tree4(ch)))
        for e, v in L.items():
            tabsum2[e] = tabsum2.get(e, 0) + v
    out['V1_linearity_glue_order'] = leq({e: v for e, v in tabsum.items() if v}, {e: v for e, v in tabsum2.items() if v})
    # V2 relabel (2,1,4,3)
    rel = {1: 2, 2: 1, 3: 4, 4: 3}
    Kr = all_K(relabel=rel)
    ms = lambda K: sorted(json.dumps([sorted((str(e), str(v)) for e, v in a.items()),
                                      sorted((str(e), str(v)) for e, v in b.items())]) for a, b in K.values())
    out['V2_relabel_same_multiset'] = ms(Kd) == ms(Kr)
    # V3 propagator scaled by 2: sign sets unchanged
    Ks = all_K(scale=2)
    same = True
    for k in Kd:
        a = sign_profile(*Kd[k]); b = sign_profile(*Ks[k])
        same &= (a.get('pos_upto_bound') == b.get('pos_upto_bound') and a.get('tail_positive') == b.get('tail_positive'))
    out['V3_scale_invariant_signs'] = same
    return out

# ---------------- modes ----------------
def jdump(obj, name):
    (OUTDIR / name).write_text(json.dumps(obj, indent=1, sort_keys=True, default=str) + '\n')

def run_planted():
    guard_banner(); t = time.time()
    res, got = planted_checks()
    p5 = p5_unitary_nonneg(); p6, p6got = p6_f_theta()
    res['P5_unitary_all_coeffs_positive'] = p5; res['P6_f_theta_abs'] = p6
    st = gate_selftests()
    out = {'planted': res, 'got': got, 'P6_got': p6got, 'gate_selftests': st,
           'PLANTED_ALL_OK': planted_gate(res), 'GATE_SELFTESTS_OK': all(st.values()), 'seconds': round(time.time() - t, 1)}
    print(json.dumps(out, indent=1)); jdump(out, 'planted_out.json')
    return out

def run_broken():
    guard_banner(); t = time.time()
    b = broken_variants()
    out = {'broken': b, 'BROKEN_ALL_REJECTED': all(v['rejected'] for v in b.values()), 'seconds': round(time.time() - t, 1)}
    print(json.dumps(out, indent=1)); jdump(out, 'broken_out.json')
    return out

def run_live():
    guard_banner(); t = time.time()
    pl = run_planted(); br = run_broken()
    Kd = all_K()
    prof = {k: sign_profile(*v) for k, v in Kd.items()}
    lab, finite, N0 = classify(list(prof.values()))
    va = valid_alternatives(Kd)
    # full-tree interference (valid alternative observable; report only)
    G4 = loop_graphs4(); Ts = {cn: tree4(ch) for cn, ch in CH.items()}
    denF = {}
    for a in Ts.values():
        for b in Ts.values():
            for e, v in W(glue(a, b)).items():
                denF[e] = denF.get(e, 0) + v
    denF = {e: v for e, v in denF.items() if v}
    fullK = {}
    for gn, g in G4.items():
        nm = {}
        for T in Ts.values():
            for e, v in W(glue(T, g)).items():
                nm[e] = nm.get(e, 0) + v
        fullK[gn] = ({e: v for e, v in nm.items() if v}, denF)
    full_prof = {k: sign_profile(*v) for k, v in fullK.items()}
    full_lab = classify(list(full_prof.values()) + [prof['n2:bubble'], prof['n3:triangle']])
    full_report = {'label': full_lab[0], 'finite': full_lab[1], 'N0': full_lab[2],
                   'K': {k: f'[{fmt(a)}] / [{fmt(b)}]' for k, (a, b) in fullK.items()}}
    # nulls
    nulls = {}
    for cnum in range(0, 9):
        c = Fraction(cnum, 4)
        Kc = all_K(c=c)
        S = [N for N in range(3, 31) if all(ev(a, N) * ev(b, N) > 0 for a, b in Kc.values())]
        nulls[str(c)] = {'S_3_30': S, 'large_N_all_positive': all(sign_profile(*v).get('tail_positive') for v in Kc.values())}
    # rival
    Kf = all_K(coupling='f')
    rival = {}
    for k, (a, b) in Kf.items():
        vals = [ev(a, N) / ev(b, N) if ev(b, N) else None for N in range(3, 31)]
        sg = sorted({(v > 0) - (v < 0) for v in vals if v is not None})
        rival[k] = {'K': f'[{fmt(a)}] / [{fmt(b)}]', 'signs_on_3_30': sg}
    rival_sign_change = any(len(v['signs_on_3_30']) > 1 for v in rival.values())
    gates = {'PLANTED_ALL_OK': pl['PLANTED_ALL_OK'], 'GATE_SELFTESTS_OK': pl['GATE_SELFTESTS_OK'],
             'BROKEN_ALL_REJECTED': br['BROKEN_ALL_REJECTED'], 'VALID_ALL_ACCEPTED': all(va.values()),
             'DEN_POSITIVE': all(p.get('den_ok') for p in prof.values())}
    verdict = 'ILL-DEFINED' if not all(gates.values()) else lab
    table = {k: {'K': f'[{fmt(a)}] / [{fmt(b)}]', 'K_at': {N: str(ev(a, N) / ev(b, N)) for N in (3, 4, 5, 6, 8, 12)},
                 'profile': prof[k]} for k, (a, b) in Kd.items()}
    lean = {k: {'num': {str(e): str(v) for e, v in a.items()}, 'den': {str(e): str(v) for e, v in b.items()}}
            for k, (a, b) in Kd.items()}
    res = {'run_id': 'SURF1-2026-10-28-r1', 'gates': gates, 'valid_alternatives': va, 'K_table': table,
           'S_label': lab, 'S_finite_part': finite, 'S_N0': N0, 'full_tree_report': full_report, 'nulls': nulls, 'rival_f': rival,
           'rival_f_any_sign_change_in_N': rival_sign_change, 'VERDICT': verdict, 'lean_data': lean,
           'seconds': round(time.time() - t, 1)}
    out = {k_: v for k_, v in res.items() if k_ != 'lean_data'}
    print(json.dumps(out, indent=1, default=str)); jdump(res, 'live_out.json')
    print('VERDICT:', res['VERDICT'])
    return res

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    guard()
    {'planted': run_planted, 'broken': run_broken, 'live': run_live}.get(mode, lambda: sys.exit('mode?'))()
