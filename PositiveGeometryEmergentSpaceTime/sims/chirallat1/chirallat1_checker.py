#!/usr/bin/env python3
"""CHIRAL-LATTICE-1 locked checker: Nielsen-Ninomiya no-doubling audit of the basin records.
Prereg: prereg/CHIRAL-LATTICE-1-no-doubling-audit-2026-10-30.md.  Modes: planted | broken | null | live (each guarded).
Corpus (frozen): every record path r[4] of scripts/blocker_tags.py B at the prereg commit, read with `git show <prereg>:path`.
Line rule (locked): a line HITs if it matches HIT. A HIT line is (b) if it matches MECH; else (c) if it matches PROD and
not NEG; else (a) (mention only). Record = (c) if any (c) line, else (b) if any (b) line, else (a).
Verdict: VACUOUS if every record is (a); BITES if any record is (c); EVADES if no (c) and >= 1 (b); else UNCLASSIFIED;
ILL-DEFINED if the corpus is empty or a record is unreadable."""
import json, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
from guard import guard, REPO
PREREG = 'prereg/CHIRAL-LATTICE-1-no-doubling-audit-2026-10-30.md'
HIT = re.compile(r"(?i)\b(chiral\w*|weyl|fermion\w*|hypercharge\w*|generations?\b|domain[- ]wall\w*|overlap (operator|fermion|dirac)|ginsparg\w*|doubl(er|ers|ing)\b|nielsen\w*)")
MECH = re.compile(r"(?i)(domain[- ]wall|overlap (operator|fermion|dirac)|ginsparg|kaplan|neuberger|l[üu]scher|mirror fermion|wilson term|staggered)")
PROD = re.compile(r"(?i)\b(produc\w*|deriv\w*|select\w*|emerg\w*|outputs?\b|predict\w*|forc(e|es|ed|ing)\b|generat(es|ed|ing)\b|yield\w*|fix(es|ed)\b)")
NEG = re.compile(r"(?i)(\bno\b|\bnot\b|cannot|can't|\bnever\b|\bblind\b|\bfails?\b|\bfailed\b|\bwithout\b|NO-GO|\bnone\b|\bneither\b|\bnor\b|doesn't|isn't|refut\w*|\bexclude\w*)")

def line_class(line):
    if not HIT.search(line): return None
    if MECH.search(line): return 'b'
    if PROD.search(line) and not NEG.search(line): return 'c'
    return 'a'

def classify(text):
    cls = [(i + 1, line_class(l), l.strip()) for i, l in enumerate(text.splitlines())]
    hits = [c for c in cls if c[1]]
    lab = 'c' if any(c[1] == 'c' for c in hits) else 'b' if any(c[1] == 'b' for c in hits) else 'a'
    return lab, hits

def validate(text, claimed):
    return claimed == classify(text)[0]

def verdict_of(labels):
    if not labels: return 'ILL-DEFINED'
    if any(l == 'c' for l in labels): return 'BITES'
    if all(l == 'a' for l in labels): return 'VACUOUS'
    if all(l in 'ab' for l in labels): return 'EVADES'
    return 'UNCLASSIFIED'

def _git_show(psha, path):
    r = subprocess.run(['git', '-C', str(REPO), 'show', f'{psha}:{path}'], capture_output=True, text=True)
    if r.returncode != 0: raise FileNotFoundError(path)
    return r.stdout

def corpus(psha):
    src = _git_show(psha, 'scripts/blocker_tags.py')
    ns = {'__name__': 'blocker_tags_at_prereg'}
    exec(compile(src, 'blocker_tags.py', 'exec'), ns)   # repo-owned registry at the prereg commit; __main__ not run
    B, BASIN = ns['B'], ns['BASIN']
    basin_of = {r: k.split()[0] for k, v in BASIN.items() for r in v}
    basin_of.update({'JORD-1': 'B7', 'SURF-1′': 'B8', 'RG-IR-1': 'RG-IR'})   # proposed basins per LOG / this batch
    return [(r[0], basin_of.get(r[0], 'pre-basin'), r[4]) for r in B], basin_of

def planted():
    guard(PREREG, HERE)
    T = {'T1_claim': ("This construction derives chiral fermions in three generations from the geometry.", 'c'),
         'T2_mechanism': ("Chiral fermions arise on a domain-wall (Kaplan) defect.", 'b'),
         'T3_mention': ("Hypercharge assignments are taken as input from STRUCT-1.", 'a'),
         'T4_negated': ("Positivity cannot produce chirality.", 'a'),
         'T5_nohit': ("The LS amplitude depends on alpha' and the pion mass.", 'a')}
    out = {k: {'label': classify(t)[0], 'want': w, 'ok': classify(t)[0] == w} for k, (t, w) in T.items()}
    out['V_verdicts'] = {'ok': [verdict_of(x) for x in (['a', 'a'], ['a', 'c'], ['a', 'b'], [])] == ['VACUOUS', 'BITES', 'EVADES', 'ILL-DEFINED']}
    out['G_selftests'] = {'ok': bool(HIT.search('Weyl')) and not HIT.search('pion') and bool(MECH.search('overlap operator'))
                          and not MECH.search('overlap region') and bool(PROD.search('selects')) and not PROD.search('pion mass')
                          and bool(NEG.search('does not')) and not NEG.search('derives')}
    out['ALL_OK'] = all(v['ok'] for v in out.values())
    return out

def broken():
    guard(PREREG, HERE)
    out = {'B1_nonfermion_marked_c': not validate("The LS amplitude depends on the pion mass only.", 'c'),
           'B2_claim_marked_a': not validate("The geometry predicts chiral fermions.", 'a'),
           'B3_empty_corpus': verdict_of([]) == 'ILL-DEFINED'}
    out['ALL_REJECTED'] = all(out.values())
    return out

def _run(psha, rows):
    res = []
    for name, basin, path in rows:
        try: lab, hits = classify(_git_show(psha, path))
        except FileNotFoundError: return None
        res.append({'rung': name, 'basin': basin, 'record': path, 'label': lab, 'n_hits': len(hits),
                    'c_lines': [(n, l[:300]) for n, c, l in hits if c == 'c'], 'b_lines': [(n, l[:300]) for n, c, l in hits if c == 'b']})
    return res

def null():
    psha = guard(PREREG, HERE)
    rows, _ = corpus(psha)
    ctrl = [r for r in rows if r[1] in ('B1', 'B4')]
    res = _run(psha, ctrl)
    return {'control_basins': ['B1', 'B4'], 'n': len(res), 'c_rate': sum(r['label'] == 'c' for r in res) / len(res),
            'c_records': [r['rung'] for r in res if r['label'] == 'c']}

def live():
    psha = guard(PREREG, HERE)
    rows, _ = corpus(psha)
    res = _run(psha, rows)
    if res is None: return {'VERDICT': 'ILL-DEFINED', 'reason': 'unreadable record'}
    by = {}
    for r in res: by.setdefault(r['basin'], []).append(r['label'])
    basins = {b: ('c' if 'c' in v else 'b' if 'b' in v else 'a', len(v)) for b, v in sorted(by.items())}
    for b in ('B6', 'B9', 'B10', 'B11'): basins.setdefault(b, ('NO-RECORD', 0))
    out = {'prereg_commit': psha, 'n_records': len(res), 'basins': basins, 'records': res,
           'rival_all_a_matches': all(r['label'] == 'a' for r in res), 'null': null()}
    out['VERDICT'] = verdict_of([r['label'] for r in res])
    return out

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    fn = {'planted': planted, 'broken': broken, 'null': null, 'live': live}.get(mode)
    if fn is None: sys.exit('usage: chirallat1_checker.py planted|broken|null|live')
    print(json.dumps(fn(), indent=1, ensure_ascii=False))
