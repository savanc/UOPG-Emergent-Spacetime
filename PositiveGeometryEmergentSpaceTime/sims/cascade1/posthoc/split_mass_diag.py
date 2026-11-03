#!/usr/bin/env python3
"""POST-HOC diagnostic (NOT preregistered, written after r1 live).  Imports the locked checker unchanged.
Tests hypothesis H-bug: EM-5 split failures arise because split_test eliminates on the locus c(X; m_i) with
symbolic m_i while A_X has m_i -> t_k substituted (final family), so locus and amplitude disagree on the masses.
D1: replicate locked behaviour (expect 0/10).  D2: same A_X but locus masses also mapped to final family (H-bug predicts 10/10).
D3: generic EM point off the S3 relations (mu random, m random) -> expect failures (control: split is not trivially satisfied).
D4: A_X kept in symbolic (mu,m) with mu solved by S3 relations (m free symbols) -> expect 10/10."""
import sys, json, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sympy as sp
import cascade1_checker as C

def splits_with_locus_map(kin, A_X, mapping):
    res = []
    for k in range(kin.n):
        for cp, g1, g2, el in C.SPLIT_TEMPLATES:
            cpr = C.rot(cp, k, kin.n); G1 = [C.rot(P, k, kin.n) for P in g1]; G2 = [C.rot(P, k, kin.n) for P in g2]; E = C.rot(el, k, kin.n)
            X = kin.X
            sol = sp.solve([kin.c(*cpr).subs(mapping)], [X[E]], dict=True)[0]
            Ar = sp.together(A_X.subs(sol))
            p = {X[P]: sp.Symbol(str(X[P]) + 'p') for P in G1 + G2}
            def ev(a, b):
                s = {X[P]: (p[X[P]] if a else X[P]) for P in G1}; s.update({X[P]: (p[X[P]] if b else X[P]) for P in G2})
                return Ar.subs(s, simultaneous=True)
            e = ev(0, 0) * ev(1, 1) - ev(0, 1) * ev(1, 0)
            res.append(sp.expand(sp.numer(sp.together(e))) == 0)
    return res

C.guard_banner()
s5 = C.run_stages012(5, 3)
A_y, y = s5['_A'], s5['_y']
kin = C.Kin(5, 'EM')
live = json.loads((Path(__file__).resolve().parents[1] / 'cascade1_live.json').read_text())
ff = None
for key, v in live.items():
    if isinstance(v, dict) and v.get('setting') == 'EM' and v.get('n') == 5:
        ff = v['final_family']
if ff is None:
    ff = live['cells']['EM-n5']['final_family'] if 'cells' in live else None
final = {sp.Symbol(k): sp.sympify(v) for k, v in ff.items()}
A_X = A_y.subs({y[P]: kin.X[P] - kin.mu[P] for P in kin.ch}).subs(final)
out = {}
out['D1_locked_replica'] = sum(s['ok'] for s in C.all_splits(kin, A_X))
out['D2_locus_masses_mapped'] = sum(splits_with_locus_map(kin, A_X, {kin.m[i]: final[kin.m[i]] for i in range(1, 6)}))
random.seed(20261023)
gen = {t: sp.Integer(random.randint(1, 9)) for t in kin.theta}
A_g = A_y.subs({y[P]: kin.X[P] - kin.mu[P] for P in kin.ch}).subs(gen)
out['D3_generic_off_relations'] = sum(splits_with_locus_map(kin, A_g, {kin.m[i]: gen[kin.m[i]] for i in range(1, 6)}))
musol = sp.solve([sp.sympify(r) for r in live['cells']['EM-n5']['S3']['relations']],
                 [kin.mu[P] for P in kin.ch], dict=True)[0]
A_s = A_y.subs({y[P]: kin.X[P] - kin.mu[P] for P in kin.ch}).subs(musol)
out['D4_symbolic_masses_on_S3'] = sum(splits_with_locus_map(kin, A_s, {}))
out['total_tests'] = 10
print(json.dumps(out, indent=1))
(Path(__file__).resolve().parent / 'split_mass_diag.json').write_text(json.dumps(out, indent=1))
