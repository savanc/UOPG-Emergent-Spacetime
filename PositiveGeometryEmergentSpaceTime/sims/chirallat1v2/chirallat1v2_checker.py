#!/usr/bin/env python3
"""CHIRAL-LATTICE-1 v2 locked checker (supersedes v1 sims/chirallat1/, which is never edited).
Prereg: prereg/CHIRAL-LATTICE-1v2-no-doubling-audit-2026-10-30.md. Modes: planted | broken | null | rival | live (each guarded).
Corpus (frozen, = v1 corpus): every record path r[4] of scripts/blocker_tags.py B at the v1 prereg commit 8733135,
read with `git show 8733135:path` (71 records).
Unit = clause: a record is normalised (markdown ** ` _ stripped, NFKC), split into lines, each line into clauses on
; ! ? sentence-final '.', ' — ', ' - ' bullets are kept. A clause is a CHIRAL-HIT if, after deleting non-fermion senses
(NONF: ChPT, chiral log/limit/Lagrangian/condensate/symmetry(-breaking)/expansion/EFT/..., chiral algebra/ring/primary),
it still matches FERM (chiral*, chirality, Weyl fermion/spinor/state/field, left-/right-handed).
A CHIRAL-HIT clause is a CLAIM iff it matches OUT (output verb) and none of NEG (negation), MODAL (conditional/
obligation/reopen), INPUT (input/label/assumed rep). Record label: 'c' (BITES) if >= 1 CLAIM and no un-negated ESC
clause in the record; 'e' (ESCAPED) if >= 1 CLAIM and >= 1 un-negated ESC clause; 'a' otherwise.
Verdict: ILL-DEFINED if corpus empty / record unreadable / null gate fails (any control record 'c');
else BITES if any 'c'; else ESCAPED if any 'e'; else VACUOUS. No hand adjudication."""
import json, re, subprocess, sys, unicodedata
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
from guard import guard, REPO
PREREG = 'prereg/CHIRAL-LATTICE-1v2-no-doubling-audit-2026-10-30.md'
V1_PSHA = '87331353b0e400b2b27df98a12323c7d293d4b58'
V1_FP = ['MR-2b', 'MR-3', 'MR-3b', 'FZ-1', 'FT-1', "MR-7'", 'STRUCT-1', 'STRUCT-1b', 'BRIDGE-PL-ASSOC (charge)']
CONTROL = re.compile(r"^(MR-|FT-|FZ-|LAT-|SC-|NL9|M3|OP-2|DZ-|KS-|KL-|TH-|UL-|SUB-)")   # hadron/ChPT/LS sector, + basins B1, B4
CONTROL_BASINS = ('B1', 'B4')

NONF = re.compile(r"(?i)(\bChPT\b|χPT|\bchiral[- ](perturbation|logs?\b|logarithm\w*|limit\w*|lagrangian\w*|condensate\w*|"
                  r"symmetr\w*|expansion\w*|eft\b|effective\w*|order\w*|counting|coefficient\w*|constant\w*|extrapolat\w*|"
                  r"algebra\w*|ring\w*|primar\w*|boson\w*|scal\w*|regime|point|line|fit\w*|trajector\w*|lecs?\b|"
                  r"wilson[- ]coefficient\w*|zeros?\b(?![- ]?modes?))|\bchiral[- ]?\w*[- ]breaking)")
FERM = re.compile(r"(?i)(\bchiral\w*|\bweyl[- ](fermion|spinor|state|field|particle|mode)s?\b|\b(left|right)[- ]handed\w*)")
OUT = re.compile(r"(?i)\b(produc\w*|deriv\w*|select\w*|emerg\w*|outputs?\b|predict\w*|forc(e|es|ed|ing)\b|generat(es|ed|ing)\b|"
                 r"yield\w*|fix(es|ed)\b|aris(e|es|ing)\b|arose\b|obtain\w*|reproduc\w*|realis\w*|realiz\w*|gives? rise)")
NEG = re.compile(r"(?i)(\bno\b|\bnot\b|cannot|can't|\bnever\b|\bnone\b|\bneither\b|\bnor\b|n't\b|\brul(e|es|ed|ing) out\b|≠|"
                 r"\bexclud\w*|\bnothing\b|\brefut\w*|\bfail\w*|no-go|\babsent\b|\blacks?\b)")
MODAL = re.compile(r"(?i)(\bif\b|\bwhether\b|\bwould\b|\bcould\b|\bmight\b|\bmust\b|\bshould\b|\breopen\w*|\btrigger\w*|"
                   r"\bneeds?\b|\bneeded\b|\brequire\w*|\bobligation\w*|\bfuture\b|\bplanned\b|\bconjectur\w*|\bspeculat\w*|"
                   r"\bproposal\b|\bhypothe\w*|\bfrontier-theory\b|\bwhich would\b|\bonce\b)")
INPUT = re.compile(r"(?i)(\binputs?\b|\blabel\w*|\bassum\w*|\bgiven\b|\btaken as\b|\bby hand\b|\bcolumns?\b|\brows?\b|"
                   r"\bindex\w*|\bfed\b|\bhand-added\b|\bpostulat\w*|\bimpos\w*|\brep(resentation)?s?\b|\bencod\w*)")
ESC = re.compile(r"(?i)(domain[- ]wall|overlap[- ](operator|fermion|dirac)|ginsparg|neuberger|kaplan|l[üu]scher|mirror[- ]fermion|"
                 r"\bnon-?local\w*|wilson[- ]term|staggered|not translation[- ]invariant|non-translation[- ]invariant|"
                 r"higher[- ]dimensional bulk|anomaly inflow)")
CFG0 = {'neg': True, 'nonf': True, 'input': True, 'modal': True, 'esc': True, 'norm': True}

def norm(t, cfg):
    if not cfg['norm']: return t
    t = unicodedata.normalize('NFKC', t)
    return re.sub(r"[*`]", "", t)

def clauses(text, cfg):
    out = []
    for i, line in enumerate(norm(text, cfg).splitlines()):
        for c in re.split(r"[;!?]|(?<!e\.g)(?<!i\.e)\.(?=\s|$)| — ", line):
            if c.strip(): out.append((i + 1, c.strip()))
    return out

def clause_kind(c, cfg):
    s = NONF.sub(' ', c) if cfg['nonf'] else c
    if not FERM.search(s): return None
    if not OUT.search(s): return 'mention'
    if cfg['neg'] and NEG.search(s): return 'negated'
    if cfg['modal'] and MODAL.search(s): return 'modal'
    if cfg['input'] and INPUT.search(s): return 'input'
    return 'claim'

def classify(text, cfg=CFG0):
    cl = clauses(text, cfg)
    kinds = [(n, clause_kind(c, cfg), c) for n, c in cl]
    claims = [(n, c) for n, k, c in kinds if k == 'claim']
    esc = [(n, c) for n, c in cl if cfg['esc'] and ESC.search(c) and not NEG.search(c)]
    lab = ('e' if esc else 'c') if claims else 'a'
    return lab, kinds, claims, esc

def verdict_of(labels, null_ok=True):
    if not labels or not null_ok: return 'ILL-DEFINED'
    if 'c' in labels: return 'BITES'
    if 'e' in labels: return 'ESCAPED'
    return 'VACUOUS'

def _git_show(psha, path):
    r = subprocess.run(['git', '-C', str(REPO), 'show', f'{psha}:{path}'], capture_output=True, text=True)
    if r.returncode != 0: raise FileNotFoundError(path)
    return r.stdout

def corpus():
    src = _git_show(V1_PSHA, 'scripts/blocker_tags.py')
    ns = {'__name__': 'blocker_tags_at_v1_prereg'}
    exec(compile(src, 'blocker_tags.py', 'exec'), ns)   # repo-owned registry at the v1 prereg commit; __main__ not run
    B, BASIN = ns['B'], ns['BASIN']
    basin_of = {r: k.split()[0] for k, v in BASIN.items() for r in v}
    basin_of.update({'JORD-1': 'B7', 'SURF-1′': 'B8', 'RG-IR-1': 'RG-IR'})   # same proposed basins as v1
    return [(r[0], basin_of.get(r[0], 'pre-basin'), r[4]) for r in B]

def is_control(name, basin):
    return basin in CONTROL_BASINS or bool(CONTROL.match(name.replace('′', "'")))

SYN = {   # synthetic planted records: (text, wanted record label)
 'S1_tp_claim': ("The positroid cell decomposition produces three generations of chiral fermions on a periodic lattice.", 'c'),
 'S2_tp_emerge': ("Chiral Weyl fermion content emerges from the boundary stratification of the hypersimplex.", 'c'),
 'S3_tp_esc_dw': ("The boundary yields chiral fermions as zero modes of a domain-wall construction.", 'e'),
 'S4_tp_esc_ov': ("Left-handed fermions arise from the lattice action. The Dirac operator is the overlap operator (Ginsparg-Wilson).", 'e'),
 'S5_tp_esc_negated': ("The geometry produces chiral fermions. No domain wall is used and the operator is local.", 'c'),
 'S6_neg_cannot': ("Positivity cannot produce chiral fermions.", 'a'),
 'S7_neg_rulesout': ("This rules out chiral fermions emerging from the associahedron.", 'a'),
 'S8_neg_neq': ("The derived spectrum ≠ chiral.", 'a'),
 'S9_chpt': ("The pion mass dependence is fixed by chiral perturbation theory and chiral logs.", 'a'),
 'S10_chpt2': ("The chiral condensate generates the pion mass; chiral symmetry breaking yields Goldstones.", 'a'),
 'S11_input': ("We take the 15 Weyl states as input labels and derive the moment polynomial.", 'a'),
 'S12_modal': ("Reopen trigger: a positive-geometry statement that forces the chiral field content.", 'a'),
 'S13_mention': ("Hypercharges of the chiral SM fermions are listed for reference.", 'a'),
 'S14_markdown_tp': ("**The amplituhedron `predicts` chiral fermions.**", 'c'),
 'S15_nfkc_tp': ("The geometry \ufb01xes the chiral fermion content of one generation.", 'c'),
}

def _suite(cfg):
    guard(PREREG, HERE)
    out = {}
    for k, (t, w) in SYN.items():
        got = classify(t, cfg)[0]; out[k] = {'label': got, 'want': w, 'ok': got == w}
    for name, _, path in [r for r in corpus() if r[0] in V1_FP]:
        got = classify(_git_show(V1_PSHA, path), cfg)[0]
        out['FP_' + name] = {'label': got, 'want': 'a', 'ok': got == 'a'}
    out['V_verdicts'] = {'ok': [verdict_of(x) for x in (['a', 'a'], ['a', 'c'], ['a', 'e'], ['e', 'c'], [])] ==
                         ['VACUOUS', 'BITES', 'ESCAPED', 'BITES', 'ILL-DEFINED'] and verdict_of(['a'], null_ok=False) == 'ILL-DEFINED'}
    out['G_selftests'] = {'ok': bool(NONF.search('chiral logs')) and not NONF.search('chiral fermions')
                          and bool(FERM.search('right-handed')) and not FERM.search('fermion mass')
                          and bool(OUT.search('emerges')) and not OUT.search('listed')
                          and bool(NEG.search('rules out')) and not NEG.search('produces')
                          and bool(MODAL.search('reopen trigger')) and not MODAL.search('the geometry produces')
                          and bool(INPUT.search('as input')) and not INPUT.search('emerges')
                          and bool(ESC.search('overlap operator')) and not ESC.search('overlap region')
                          and is_control('MR-2b', 'pre-basin') and not is_control('STRUCT-1', 'pre-basin')}
    out['ALL_OK'] = all(v['ok'] for v in out.values() if isinstance(v, dict))
    return out

def planted():
    guard(PREREG, HERE)
    return _suite(CFG0)

def broken():
    guard(PREREG, HERE)
    out = {}
    for flag in ('neg', 'nonf', 'input', 'modal', 'esc', 'norm'):
        s = _suite(dict(CFG0, **{flag: False}))
        out['B_no_' + flag] = {'rejected': not s['ALL_OK'], 'failing': [k for k, v in s.items() if isinstance(v, dict) and not v['ok']]}
    out['B_empty_corpus'] = {'rejected': verdict_of([]) == 'ILL-DEFINED'}
    out['ALL_REJECTED'] = all(v['rejected'] for v in out.values())
    return out

def _run(rows):
    guard(PREREG, HERE)
    res = []
    for name, basin, path in rows:
        try: lab, kinds, claims, esc = classify(_git_show(V1_PSHA, path))
        except FileNotFoundError: return None
        res.append({'rung': name, 'basin': basin, 'record': path, 'label': lab, 'control': is_control(name, basin),
                    'n_chiral_clauses': sum(1 for k in kinds if k[1]),
                    'kinds': {x: sum(1 for k in kinds if k[1] == x) for x in ('mention', 'negated', 'modal', 'input', 'claim')},
                    'claims': [(n, c[:300]) for n, c in claims], 'esc': [(n, c[:200]) for n, c in esc]})
    return res

def null():
    guard(PREREG, HERE)
    res = _run([r for r in corpus() if is_control(r[0], r[1])])
    nc = sum(r['label'] == 'c' for r in res)
    return {'n_control': len(res), 'c_rate': nc / len(res), 'c_records': [r['rung'] for r in res if r['label'] == 'c'], 'NULL_OK': nc == 0}

def rival():
    guard(PREREG, HERE)
    v1 = json.loads((REPO / 'sims/chirallat1/chirallat1_live.json').read_text())
    return {'v1_checker_c_records': [r['rung'] for r in v1['records'] if r['label'] == 'c'], 'v1_verdict': v1['VERDICT'],
            'prior_all_a': 'VACUOUS'}

def live():
    guard(PREREG, HERE)
    rows = corpus()
    res = _run(rows)
    if res is None: return {'VERDICT': 'ILL-DEFINED', 'reason': 'unreadable record'}
    nl, rv = null(), rival()
    by = {}
    for r in res: by.setdefault(r['basin'], []).append(r['label'])
    basins = {b: ('c' if 'c' in v else 'e' if 'e' in v else 'a', len(v)) for b, v in sorted(by.items())}
    for b in ('B6', 'B9', 'B10', 'B11'): basins.setdefault(b, ('NO-RECORD', 0))
    labels = [r['label'] for r in res]
    out = {'v1_corpus_commit': V1_PSHA, 'n_records': len(res), 'counts': {x: labels.count(x) for x in 'cea'},
           'basins': basins, 'null': nl, 'rival': rv, 'records': res}
    out['VERDICT'] = verdict_of(labels, null_ok=nl['NULL_OK'])
    out['matches_prior_all_a'] = out['VERDICT'] == 'VACUOUS'
    out['matches_v1_checker'] = out['VERDICT'] == rv['v1_verdict']
    return out

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    fn = {'planted': planted, 'broken': broken, 'null': null, 'rival': rival, 'live': live}.get(mode)
    if fn is None: sys.exit('usage: chirallat1v2_checker.py planted|broken|null|rival|live')
    print(json.dumps(fn(), indent=1, ensure_ascii=False))
