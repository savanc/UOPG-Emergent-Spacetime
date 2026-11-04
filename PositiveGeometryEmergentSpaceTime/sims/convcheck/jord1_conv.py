#!/usr/bin/env python3
"""JORD-1 convention-invariance re-check (CONV-JORD1-2026-10-30-r1; author approved (2026-10-30)).
Prereg: prereg/CONV-JORD-1-trace-scale-2026-10-30.md.  SUPERSEDES (does not edit) the F_A consistency step of the locked
sims/jord1/jord1_checker.py, whose functions are imported read-only (its own guard still runs against prereg 719e85d).
Equivalence map (refinement 1): phi_lam(v) = lam*v, lam in Q\\{0}, applied UNIFORMLY to every idempotent representative.
  Stabilisers: D(lam v) = lam D(v) for linear D, so stab(phi_lam S) = stab(S) (Lean JordConv.der_smul_eq_zero_iff).
  Idempotency: (lam x).(lam x) = lam (lam x) <=> x.x = x, i.e. P idempotent at unit scale <=> 2P satisfies the 2P-scale
  test (Lean JordConv.idem_scale_iff).  The locked checker mixed scales (E_i at unit scale, P_ij at 2P scale): not a
  single convention.
Conventions scored: CA all representatives at 2P scale (E_i -> 2E_i), checked by locked is_idempotent2;
  CB all at unit scale (P_ij -> P_ij/2, exact Fractions), checked by C(v,v) == 2v (C = locked 2x Jordan table).
Pass/flip rule: recompute the locked `consistent` formula in CA and CB with tier A/B and F_A stabilisers re-run.
  FLIPPED if consistent in CA and CB (new verdict = the locked non-ILL label); CONVENTION-ROBUST if inconsistent in both;
  ILL-DEFINED (re-check) if CA and CB disagree, or any gate fails.
Planted: PL1 stab dims of all 1326 F_A configs identical under CA, CB and lam = 3, -1/2 (equivalence holds numerically);
  PL2 locked mixed-scale list reproduces E1,E2,E3 failing (locked behaviour).  Broken (must be REJECTED by the idempotency
  test in both conventions): BR1 E1+2E2, BR2 P12(+e0) with the e0 coefficient doubled, BR3 E1 - E2.
Null: 200 random NON-uniform rescalings (each representative its own lam in {+-1,+-2,+-3,+-1/2}, seed 20261030):
  fraction passing the fixed-scale test (expected low: shows the test is scale-sensitive) and fraction with unchanged
  stab histogram (expected 1).  Rival (strong, scale-free): projective idempotency test x.x in span(x), x != 0, on the
  locked mixed list: must agree with CA/CB.
Modes: planted | broken | live."""
import importlib.util, itertools, json, random, sys, time
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path.insert(0, str(HERE.parent))
from conv_guard import guard as _g, REPO
PREREG = 'prereg/CONV-JORD-1-trace-scale-2026-10-30.md'
def guard(): return _g(PREREG, HERE)
_spec = importlib.util.spec_from_file_location('jord1_locked', REPO / 'sims/jord1/jord1_checker.py')
L = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(L)
_F = []
def F4():
    if not _F: T = L.omul_table(); _F.append((T, L.F4(T)))
    return _F[0]
def cprod(v, C):
    out = [Fraction(0)] * L.N
    for i in range(L.N):
        if not v[i]: continue
        for j in range(L.N):
            if not v[j]: continue
            for k, x in enumerate(C[i][j]):
                if x: out[k] += v[i] * v[j] * x
    return out
def idem_CA(v, C): guard(); return L.is_idempotent2(v, C)
def idem_CB(v, C): guard(); return cprod(v, C) == [2 * Fraction(x) for x in v]
def idem_proj(v, C):
    guard(); w = cprod(v, C); nz = [i for i in range(L.N) if v[i]]
    if not nz: return False
    r = Fraction(w[nz[0]]) / v[nz[0]]
    return r != 0 and all(Fraction(w[i]) == r * v[i] for i in range(L.N))
def reps(conv):
    ids = L.idempotents()  # locked: E_i unit scale, P_ij 2P scale
    out = []
    for n, v in ids:
        if conv == 'mixed': out.append((n, list(v)))
        elif conv == 'CA': out.append((n, [2 * x for x in v] if n[0] == 'E' else list(v)))
        elif conv == 'CB': out.append((n, list(v) if n[0] == 'E' else [Fraction(x, 2) for x in v]))
    return out
def stab_hist(rs):
    guard(); T, F = F4(); dims, hits = {}, []
    for r_ in (1, 2):
        for comb in itertools.combinations(rs, r_):
            h = F.stab_vecs([[Fraction(x) for x in v] for _, v in comb])
            dims[len(h)] = dims.get(len(h), 0) + 1
            if len(h) == 12 and L.sm_type(F.invariants(h)): hits.append([n for n, _ in comb])
    return dict(sorted(dims.items())), hits
def run_planted():
    guard(); T, F = F4(); res = {}
    base = stab_hist(reps('CA'))
    for lab, rs in (('CB', reps('CB')), ('lam3', [(n, [3 * Fraction(x) for x in v]) for n, v in reps('CA')]),
                    ('lam-1/2', [(n, [Fraction(-1, 2) * x for x in v]) for n, v in reps('CA')])):
        res[f'PL1_{lab}_same_hist'] = stab_hist(rs) == base
    res['PL2_mixed_fail'] = sorted(n for n, v in reps('mixed') if not idem_CA(v, F.C)) == ['E1', 'E2', 'E3']
    res['PLANTED_ALL_OK'] = all(res.values()); print(json.dumps(res)); return res
def broken_cases():
    E = L.E; e1, e2 = E(0), E(1); p = dict(reps('CA'))['P12(+e0)']
    br1 = [a + 2 * b for a, b in zip(e1, e2)]; br2 = list(p); k = [i for i, x in enumerate(p) if x][-1]; br2[k] *= 2
    br3 = [a - b for a, b in zip(e1, e2)]
    return {'BR1': br1, 'BR2': br2, 'BR3': br3}
def run_broken():
    guard(); T, F = F4(); res = {}
    for n, v in broken_cases().items():
        res[n] = {'CA': idem_CA([2 * x for x in v] if n != 'BR2' else v, F.C),
                  'CB': idem_CB([Fraction(x) for x in v] if n != 'BR2' else [Fraction(x, 2) for x in v], F.C)}
    res['BROKEN_ALL_REJECTED'] = not any(x for r in res.values() for x in r.values())
    print(json.dumps(res)); return res
def run_live():
    psha = guard(); t0 = time.time(); T, F = F4(); res = {'run_id': 'CONV-JORD1-2026-10-30-r1', 'prereg_commit': psha}
    pl = run_planted(); br = run_broken()
    s1 = F.stab_vecs([L.E(0)]); g = F.intersect(s1, F.setstab(L.sub_idx(L.KUNITS['C']))); cl = F.closure(g)
    vA = ('POSITIVITY-CLOSED' if len(cl) == len(g) else
          'NOT-POSITIVITY-CLOSED' if len(cl) > len(g) and L.rank(g + cl, F.dim) == len(cl) else 'UNCLASSIFIED')
    k = sum(L.sm_type(F.invariants(h)) for _, h in L.family_B(F))
    lab = 'CHOICE-UNIQUE' if k == 1 else ('CHOICE-NONE' if k == 0 else f'CHOICE-AMONG-{k}')
    res.update(tierA=vA, tierB_smtype=k, tierB_label=lab)
    for conv, test in (('CA', idem_CA), ('CB', idem_CB)):
        rs = reps(conv); allid = all(test(v, F.C) for _, v in rs); hist, hits = stab_hist(rs)
        cons = not (vA == 'NOT-POSITIVITY-CLOSED' and hits) and allid and k >= 1
        res[conv] = dict(all_idempotent=allid, stab_hist=hist, smtype_hits=hits, consistent=cons)
    res['rival_projective_all_idempotent_on_mixed'] = all(idem_proj(v, F.C) for _, v in reps('mixed'))
    rng = random.Random(20261030); lams = [1, -1, 2, -2, 3, -3, Fraction(1, 2), Fraction(-1, 2)]
    base = res['CA']['stab_hist']; npass = nsame = 0; NT = 200
    singles = {n: len(F.stab_vecs([[Fraction(x) for x in v]])) for n, v in reps('CA')}
    for _ in range(NT):
        rs = [(n, [rng.choice(lams) * Fraction(x) for x in v]) for n, v in reps('CA')]
        npass += all(idem_CA(v, F.C) for _, v in rs)
        nsame += all(len(F.stab_vecs([v])) == singles[n] for n, v in rs)
    res['null_nonuniform_pass_fixed_scale'] = f'{npass}/{NT}'
    res['null_nonuniform_single_stab_unchanged'] = f'{nsame}/{NT}'
    gates = pl['PLANTED_ALL_OK'] and br['BROKEN_ALL_REJECTED']
    a, b = res['CA']['consistent'], res['CB']['consistent']
    newv = f"{vA} / {lab}" + (' / NO-GO' if vA == 'NOT-POSITIVITY-CLOSED' else '')
    res['OUTCOME'] = ('ILL-DEFINED' if not gates or a != b else ('FLIPPED' if a else 'CONVENTION-ROBUST'))
    res['NEW_VERDICT'] = newv if res['OUTCOME'] == 'FLIPPED' else ('ILL-DEFINED' if res['OUTCOME'] == 'CONVENTION-ROBUST' else None)
    res['seconds'] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1, default=str)); (HERE.parent / 'jord1_conv_live.json').write_text(json.dumps(res, indent=1, default=str) + '\n')
    print('OUTCOME:', res['OUTCOME'], '|', res['NEW_VERDICT']); return res
if __name__ == '__main__':
    guard()
    {'planted': run_planted, 'broken': run_broken, 'live': run_live}.get(sys.argv[1] if len(sys.argv) > 1 else '', lambda: sys.exit('mode?'))()
