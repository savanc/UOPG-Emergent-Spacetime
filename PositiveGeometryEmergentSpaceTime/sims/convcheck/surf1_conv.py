#!/usr/bin/env python3
"""SURF-1' convention-invariance re-check (CONV-SURF1-2026-10-30-r1; author approved (2026-10-30)).
Prereg: prereg/CONV-SURF-1-coupling-norm-2026-10-30.md.  SUPERSEDES nothing in the locked sims/surf1/surf1_checker.py
(imported read-only; its own guard still runs against its prereg).
Equivalence: graph-uniform rescaling, every trivalent vertex x lam, every propagator x mu (lam in Q\\{0}, mu > 0).
  covers coupling sign / normalisation relative to the tree term (lam), T_F 1/2 vs 1 and propagator normalisation (mu),
  and the d-vertex in the f/d basis (positive rescale).  K = W(num)/W(den) picks up lam^(dV3) mu^(dE) with dV3 even
  (Lean SurfConv.pos_iff_scaled), so every sign profile and the classify() label are invariant.
Rival (not an equivalence): f-coupling / ghost-c change (different theory).  Null: random per-K sign flips of num.
Broken: per-K numerator-only factor -1 must be REJECTED by the equivalence validator.  Modes: planted | broken | live."""
import importlib.util, itertools, json, random, sys, time
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path.insert(0, str(HERE.parent))
from conv_guard import guard as _g, REPO
PREREG = 'prereg/CONV-SURF-1-coupling-norm-2026-10-30.md'
def guard(): return _g(PREREG, HERE)
_spec = importlib.util.spec_from_file_location('surf1_locked', REPO / 'sims/surf1/surf1_checker.py')
L = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(L)
LAMS = [Fraction(x) for x in (1, -1, 2, -2, Fraction(1, 2), Fraction(-1, 2))]
MUS = [Fraction(1, 2), Fraction(1), Fraction(2)]

def graphs():
    """(num_graph, den_graph) per K, mirroring locked all_K exactly."""
    guard(); G = {}
    G['n2:bubble'] = (L.closed_self(L.bubble2()), L.P1G)
    t3 = L.tree3(); G['n3:triangle'] = (L.glue(L.tree3(), L.triangle3()), L.glue(t3, t3))
    G4 = L.loop_graphs4()
    for cn, ch in L.CH.items():
        T = L.tree4(ch); TT = L.glue(T, T)
        for gn, g in G4.items(): G[f'n4:{gn}|{cn}'] = (L.glue(T, g), TT)
    return G
v3 = lambda g: sum(1 for v in g['V'] if len(v) == 3)
ne = lambda g: len(g['E'])
def factor(g, lam, mu): return lam ** v3(g) * mu ** ne(g)
def is_equiv(fnum, fden, gs, lam, mu):
    """Validator: accepted iff num/den factors equal the graph-uniform rule for every K."""
    guard()
    return all(fnum[k] == factor(n, lam, mu) and fden[k] == factor(d, lam, mu) for k, (n, d) in gs.items())
def labels(Kd):
    prof = {k: L.sign_profile(*v) for k, v in Kd.items()}
    return prof, L.classify(list(prof.values()))
def strip(p): return {k: (v.get('pos_upto_bound'), v.get('tail_positive'), v.get('den_ok')) for k, v in p.items()}

def run(mode):
    guard(); t = time.time(); gs = graphs(); K0 = L.all_K()
    assert set(gs) == set(K0)
    p0, c0 = labels(K0); out = {'base_label': c0[0], 'n_K': len(K0)}
    out['dV3'] = {k: v3(n) - 2 * 0 - v3(d) for k, (n, d) in gs.items()}
    out['dV3_all_even'] = all(x % 2 == 0 for x in out['dV3'].values())
    if mode in ('planted', 'live'):
        grid = {}
        for lam, mu in itertools.product(LAMS, MUS):
            fn = {k: factor(n, lam, mu) for k, (n, d) in gs.items()}; fd = {k: factor(d, lam, mu) for k, (n, d) in gs.items()}
            Kx = {k: (L.lsc(a, fn[k]), L.lsc(b, fd[k])) for k, (a, b) in K0.items()}
            px, cx = labels(Kx)
            grid[f'{lam},{mu}'] = {'validator': is_equiv(fn, fd, gs, lam, mu), 'label': cx[0], 'profiles_same': strip(px) == strip(p0)}
        out['grid'] = grid
        out['PLANTED_OK'] = all(v['validator'] and v['profiles_same'] and v['label'] == c0[0] for v in grid.values())
        # locked scale=2 path (mu only) must agree
        out['locked_scale2_label'] = labels(L.all_K(scale=2))[1][0]
    if mode in ('broken', 'live'):
        br = {}
        for k0 in ['n3:triangle', 'n2:bubble']:
            fn = {k: factor(n, 1, 1) for k, (n, d) in gs.items()}; fd = dict(fn); fd = {k: factor(d, 1, 1) for k, (n, d) in gs.items()}
            fn[k0] = -fn[k0]
            br[k0] = {'rejected': not is_equiv(fn, fd, gs, Fraction(1), Fraction(1))}
        out['broken'] = br; out['BROKEN_ALL_REJECTED'] = all(v['rejected'] for v in br.values())
    if mode == 'live':
        rng = random.Random(20261030); ch = 0
        for _ in range(200):
            Kx = {k: (L.lsc(a, rng.choice((1, -1))), b) for k, (a, b) in K0.items()}
            ch += labels(Kx)[1][0] != c0[0]
        out['null_random_perK_flips_label_changed'] = f'{ch}/200'
        out['rival'] = {'c=-1 (ghost sign)': labels(L.all_K(c=-1))[1][0], 'c=0': labels(L.all_K(c=0))[1][0]}
        locked = json.load(open(REPO / 'sims/surf1/live_out.json'))['VERDICT']
        out['locked_verdict'] = locked
        ok = out['PLANTED_OK'] and out['BROKEN_ALL_REJECTED'] and out['dV3_all_even']
        out['OUTCOME'] = ('CONVENTION-ROBUST' if c0[0] == locked else 'FLIPPED') if ok else 'GATE-FAIL'
    out['seconds'] = round(time.time() - t, 1)
    print(json.dumps(out, indent=1, default=str))
    (HERE.parent / f'surf1_conv_{mode}.json').write_text(json.dumps(out, indent=1, default=str))
if __name__ == '__main__': run(sys.argv[1])
