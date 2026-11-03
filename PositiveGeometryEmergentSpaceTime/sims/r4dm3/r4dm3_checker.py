#!/usr/bin/env python3
"""R4-DM v3 derivation meter, locked checker (prereg/R4-DM3-2026-10-20.md). Supersedes the v2 checker
sims/r4dm2/r4dm2_checker.py (v2 stays as written). v2's rule, verdict order, guard and fixes D1-D3 unchanged, plus
three v3 changes (notes/NOTATION-AUDIT-2026-10-20.md H3; reviews/R4-DM2-result-2026-10-20.md §2):
  E1  charge-normalisation literals: smuggling test (c) also catches integer x6 / Y/2 hypercharge literals on a
      tier-Q SM variable, and the Y/2 fraction 4/3;
  E2  N_c-symbolic normalisation: (c) also catches 2*N_c*yQ / N_c*yQ / 1/(2*N_c) in a hypothesis;
  E3  D1 tightened: a bound SM-structure variable makes a statement SM-structure only if the conclusion reads a
      coupling/charge field (an SM-var constant), not if it merely mentions the variable.
v2 header follows (fixes kept):
  D1  field reads on a bound structure variable (x : BR5p.Inv; x.a, x.lam3) are SM data universally quantified,
      hence unconstrained unless a hypothesis references x  (v1: identities in x read as DERIVED);
  D2  Lean-generated constructor/structure lemmas (P.inj, P.injEq, P.sizeOf_spec, P.ext, P.ext_iff, P.eta with P a
      constructor or inductive) get verdict AUTO-GENERATED, kept in the denominator, never DERIVED;
  D3  a role override key k also matches suffixed names k_<...> (v1: only k and k.<...>).
Each fix is a switch in FIXES; planted mode also runs every single-fix ablation and requires that switching the fix
off changes exactly that fix's planted cases (so each fix is shown to be what changes the verdict).
Inputs (hash-locked): graph/r4dm3_decls.jsonl (sims/r4dm3/R4DM3Export.lean, export block byte-identical to v1's),
sims/r4dm3/classification.json, sims/r4dm3/planted/planted_decls.jsonl (R4DM3Planted.lean), sims/r4dm3/planted_cases.json.
Modes: planted | broken | live.  Unclassified module => UNCLASSIFIED, refuse.
GUARD as v1: guard() in EVERY scoring function, re-verified on every call; no pass flag; fetch once per process.
"""
import hashlib, json, re, subprocess, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/R4-DM3-2026-10-20.md'
CLASS = REPO / 'sims/r4dm3/classification.json'
EXPORTER = REPO / 'sims/r4dm3/R4DM3Export.lean'
EXPORTER_V1 = REPO / 'sims/r4dm/R4DMExport.lean'
PLANTED_LEAN = REPO / 'sims/r4dm3/planted/R4DM3Planted.lean'
LIVE = REPO / 'graph/r4dm3_decls.jsonl'
PLANTED = REPO / 'sims/r4dm3/planted/planted_decls.jsonl'
CASES = REPO / 'sims/r4dm3/planted_cases.json'
LOCKED = {'r4dm3_checker.py': HERE, 'classification.json': CLASS, 'R4DM3Export.lean': EXPORTER,
          'R4DM3Planted.lean': PLANTED_LEAN, 'planted_cases.json': CASES, 'R4DMExport.lean': EXPORTER_V1}
FIXES = {'D1': True, 'D2': True, 'D3': True, 'E1': True, 'E2': True, 'E3': True}   # v2 fixes + v3 changes; only planted-mode ablation switches one off
DEFLIKE = {'def', 'induct', 'ctor', 'opaque', 'axiom'}

def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)

_FETCH_DONE = []          # fetch once per process (NOT a pass flag)
_ANC_BY_ORIGIN = {}       # origin/main sha -> (prereg sha, is_ancestor)

def _origin_sha():
    return _git('rev-parse', '--verify', '-q', 'refs/remotes/origin/main').stdout.strip()

def _block(p):
    s = p.read_text()
    b, e = s.find('-- R4DM-EXPORT-BLOCK-BEGIN'), s.find('-- R4DM-EXPORT-BLOCK-END')
    return s[b:e] if 0 <= b < e else None

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
    text = (REPO / PREREG).read_text()
    for fname, path in LOCKED.items():
        m = re.search(re.escape(fname) + r'` sha256 `([0-9a-f]{64})`', text)
        if not m:
            sys.exit(f"GUARD REFUSED: {fname} hash not found in prereg")
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != m.group(1):
            sys.exit(f"GUARD REFUSED: {fname} hash does not match prereg")
    b0, b1, b2 = _block(EXPORTER_V1), _block(EXPORTER), _block(PLANTED_LEAN)
    if b0 is None or not (b0 == b1 == b2):
        sys.exit("GUARD REFUSED: export blocks of R4DM3Export.lean / R4DM3Planted.lean differ from v1 R4DMExport.lean")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker/classification/exporters/planted hashes match "
          f"(re-verified on every scoring call)")

# ---------------------------------------------------------------- classification

class Unclassified(Exception):
    pass

def load_class(path=CLASS, drop=None, empty=False):
    guard()
    c = json.loads(Path(path).read_text())
    if empty:
        c['modules'] = {}
    if drop:
        c['modules'].pop(drop, None)
    return c

def short(mod):
    return mod[len('PositiveGeometryEmergentSpaceTime.'):] if mod.startswith('PositiveGeometryEmergentSpaceTime.') else mod

def mod_entry(cls, mod, planted=False):
    guard()
    s = short(mod)
    e = cls['modules'].get(s)
    if e is None and planted:
        e = cls.get('planted_modules', {}).get(s)
    if e is None:
        raise Unclassified(mod)
    return e

def role(cls, d, planted=False):
    """Role of one declaration: GEOMETRY-PG | GEOMETRY-AMP | SM-INPUT | NEUTRAL."""
    guard()
    e = mod_entry(cls, d['module'], planted)
    if e['class'] == 'GEOMETRY':
        return 'GEOMETRY-' + e['sub']
    if e['class'] == 'SM-INPUT':
        return 'SM-INPUT'
    best, r = -1, e['default_role']
    for k, v in e.get('roles', {}).items():
        hit = d['name'] == k or d['name'].startswith(k + '.') or (FIXES['D3'] and d['name'].startswith(k + '_'))
        if hit and len(k) > best:
            best, r = len(k), v
    return r

def vocab(cls, d):
    guard()
    v = dict(cls['sm_vocab_global'])
    v.update(cls['sm_vocab_module'].get(short(d['module']), {}))
    return v

# ---------------------------------------------------------------- per-declaration analysis

_FRAC = re.compile(r'(?<![0-9.])(\d+)/(\d+)(?![0-9])')

def hyp_literals(cls, s):
    guard()
    t = s.replace(' ', '').replace('(', '').replace(')', '')
    lits = {x.lstrip('-') for x in cls['sm_literals_hyp'] + (cls['sm_literals_hyp_E1'] if FIXES['E1'] else [])}
    return sorted({f'{a}/{b}' for a, b in _FRAC.findall(t) if f'{a}/{b}' in lits})

_INT = re.compile(r'(?<![\w./^⁰¹²³⁴⁵⁶⁷⁸⁹])(\d+)(?![\w./])')

def hyp_int_literals(cls, s):
    """E1: standalone integer literals with |n| in sm_int_literals_hyp (not in a fraction, not an exponent,
    not glued to an identifier)."""
    guard()
    t = s.replace(' ', '').replace('(', '').replace(')', '')
    keep = {str(n) for n in cls['sm_int_literals_hyp']}
    return sorted({m for m in _INT.findall(t) if m in keep})

_SPLIT = re.compile(r'[=+<>≤≥≠∧∨↔→,¬]|(?<![*/])-')

def hyp_nc_symbolic(cls, s):
    """E2: one multiplicative term containing an nc_vars and a charge_vars variable, or a division by an nc_vars
    variable."""
    guard()
    nc, ch = set(cls['nc_vars']), set(cls['charge_vars'])
    t = s.replace(' ', '')
    hits = []
    for v in nc:
        if re.search(r'/\(?(\d+\*)?' + re.escape(v) + r'(?![\w\'])', t):
            hits.append(f'division by {v}')
    for term in _SPLIT.split(t.replace('(', '').replace(')', '')):
        f = set(re.split(r'[*/]', term))
        if f & nc and f & ch:
            hits.append(f"term {term}")
    return sorted(set(hits))

def closure(D, seeds):
    guard()
    out, todo = set(), [n for n in seeds if n in D]
    while todo:
        n = todo.pop()
        if n in out:
            continue
        out.add(n)
        d = D[n]
        todo += [u for u in d['type_uses'] + d['value_uses'] if u in D and u not in out]
    return out

def analyse(D, R, cls, d):
    """Return dict(S, tier, verdict, detail) for one theorem d."""
    guard()
    voc = vocab(cls, d)
    svc = cls['sm_var_consts']
    bnames = {b['name'] for b in d['binders'] if not b['prop']}
    smvars = {b: voc[b] for b in bnames if b in voc}
    parents = {c.rsplit('.', 1)[0]: t for c, t in svc.items()}
    bound_struct = {}
    if FIXES['D1']:
        for b in d['binders']:
            if not b['prop']:
                hit = [parents[c] for c in b['consts'] if c in parents]
                if hit:
                    bound_struct[b['name']] = hit[0]
                    smvars[b['name']] = hit[0]
    cc = set(d['concl_consts'])
    concl_sm_input = sorted(c for c in cc if R.get(c) == 'SM-INPUT')
    concl_smv = sorted(c for c in cc if c in svc)
    concl_vars = sorted(r for r in d['concl_refs'] if r in smvars and
                        not (FIXES['E3'] and r in bound_struct and not concl_smv))
    manual = d['name'] in cls['manual_sm_structure']
    S = bool(concl_sm_input or concl_smv or concl_vars or manual)
    if not S:
        return {'S': False}
    tiers = {'Q' for _ in concl_sm_input} | {svc[c] for c in concl_smv} | {smvars[v] for v in concl_vars}
    if manual:
        tiers.add(cls['manual_sm_structure'][d['name']])
    tier = 'Q' if 'Q' in tiers else 'C'
    has_sm_symbol = bool(concl_sm_input or concl_smv or concl_vars or
                         any(r in smvars for b in d['binders'] for r in b['refs']))
    tclos = closure(D, d['type_uses'])
    vclos = closure(D, d['value_uses'])
    allc = tclos | vclos
    geo = sorted(n for n in allc if R.get(n, '').startswith('GEOMETRY') and D[n]['kind'] in DEFLIKE
                 and n not in svc)
    res = {'S': True, 'tier': tier, 'geometry_defs': len(geo)}
    if FIXES['D2']:
        par, _, last = d['name'].rpartition('.')
        if last in cls['auto_generated_suffixes'] and par in D and D[par]['kind'] in ('ctor', 'induct'):
            res.update(verdict='AUTO-GENERATED', why=f'Lean-generated lemma {last} of {par}')
            return res
    if d['name'] in cls.get('witness_exclusions', {}):
        res.update(verdict='WITNESS', why=cls['witness_exclusions'][d['name']])
        return res
    if not geo:
        res.update(verdict='NO-GEOMETRY', why='transitive closure has no GEOMETRY-role definition')
        return res
    # smuggling
    why = []
    hyps = [b for b in d['binders'] if b['prop']]
    concl_parts = {d['concl'].replace(' ', '')} | {p.replace(' ', '') for p in re.split(r' ∧ ', d['concl'])}
    for b in hyps:
        bc = set(b['consts'])
        sm_in = sorted(c for c in bc if R.get(c) == 'SM-INPUT')
        if sm_in:
            why.append(f"(a) hypothesis {b['name']} uses SM-INPUT {sm_in}")
        mentions_sm = any(r in smvars for r in b['refs']) or any(c in svc for c in bc)
        geo_c = [c for c in bc if R.get(c, '').startswith('GEOMETRY') and c not in svc]
        if mentions_sm and not geo_c and not sm_in:
            why.append(f"(b) hypothesis {b['name']} constrains SM data with no geometry: {b['type'][:80]}")
        lits = hyp_literals(cls, b['type'])
        if lits:
            why.append(f"(c) hypothesis {b['name']} contains SM literal {lits}")
        refs_q = any(smvars.get(r) == 'Q' for r in b['refs'])
        if FIXES['E1'] and refs_q:
            ints = hyp_int_literals(cls, b['type'])
            if ints:
                why.append(f"(c-E1) hypothesis {b['name']} puts integer-normalised charge literal {ints} on a tier-Q SM variable")
        if FIXES['E2']:
            sym = hyp_nc_symbolic(cls, b['type'])
            if sym:
                why.append(f"(c-E2) hypothesis {b['name']} carries the N_c-symbolic charge normalisation {sym}")
        if b['type'].replace(' ', '') in concl_parts:
            why.append(f"(d) hypothesis {b['name']} restates the conclusion")
    if why:
        res.update(verdict='SMUGGLED', why='; '.join(why))
        return res
    sm_thm = sorted(n for n in vclos - tclos if R.get(n) == 'SM-INPUT' and D[n]['kind'] == 'thm')
    sm_def = sorted(n for n in vclos - tclos if R.get(n) == 'SM-INPUT' and D[n]['kind'] != 'thm')
    if sm_thm or sm_def:
        res.update(verdict='SM-INPUT-FED', why=f'proof uses SM-INPUT {sorted(sm_thm + sm_def)[:6]}')
        return res
    hyp_sm = any(r in smvars for b in hyps for r in b['refs']) or any(c in svc for b in hyps for c in b['consts'])
    smv_bound = FIXES['D1'] and bool(concl_smv) and any(r in bound_struct for r in d['concl_refs'])
    if not has_sm_symbol or (not hyp_sm and not concl_sm_input and (not concl_smv or smv_bound)):
        res.update(verdict='NON-CONSTRAINING',
                   why='no SM symbol in the statement' if not has_sm_symbol else
                   'SM data universally quantified and unconstrained (identity/blindness)')
        return res
    pg = any(R[n] == 'GEOMETRY-PG' for n in geo)
    res.update(verdict='DERIVED', cond='CONDITIONAL' if hyps else 'UNCONDITIONAL',
               source='PG' if pg else 'AMP',
               why=f"geometry defs e.g. {geo[:4]}; hypotheses: {[b['type'][:60] for b in hyps]}")
    return res

def load_decls(path):
    guard()
    return {d['name']: d for d in (json.loads(l) for l in Path(path).read_text().splitlines() if l.strip())}

def meter(D, cls, planted_mods=()):
    guard()
    R = {}
    for n, d in D.items():
        R[n] = role(cls, d, planted=short(d['module']) in planted_mods)   # raises Unclassified
    rows = {}
    for n, d in sorted(D.items()):
        if d['kind'] != 'thm':
            continue
        a = analyse(D, R, cls, d)
        if a['S']:
            rows[n] = a
    return rows

def summary(rows):
    guard()
    S = len(rows)
    der = {n: a for n, a in rows.items() if a['verdict'] == 'DERIVED'}
    out = {'n_sm_structure': S, 'n_derived': len(der), 'meter': f'{len(der)}/{S}',
           'verdicts': dict(Counter(a['verdict'] for a in rows.values()))}
    for t in ('Q', 'C'):
        St = [n for n, a in rows.items() if a['tier'] == t]
        Dt = [n for n in St if n in der]
        out[f'meter_{t}'] = f'{len(Dt)}/{len(St)}'
    for s in ('PG', 'AMP'):
        out[f'derived_{s}'] = sorted(n for n, a in der.items() if a['source'] == s)
    out['derived_unconditional'] = sorted(n for n, a in der.items() if a['cond'] == 'UNCONDITIONAL')
    return out

def print_rows(rows):
    guard()
    for n, a in sorted(rows.items(), key=lambda x: (x[1]['verdict'], x[0])):
        extra = f" [{a.get('cond')}, {a.get('source')}]" if a['verdict'] == 'DERIVED' else ''
        print(f"  {a['verdict']:<17} tier {a['tier']}  {n}{extra}\n      {a['why'][:220]}")

# ---------------------------------------------------------------- modes

def _planted_rows():
    guard()
    cls = load_class()
    D = {**load_decls(LIVE), **load_decls(PLANTED)}
    return meter(D, cls, planted_mods={'R4DM3Planted', 'R4DM3PlantedMixed'})

def _label(rows, n):
    guard()
    got = rows.get(n, {'verdict': 'NOT-SM-STRUCTURE'})
    return got['verdict'] + (f"/{got.get('cond')}/{got.get('source')}" if got['verdict'] == 'DERIVED' else '')

def mode_planted():
    """Planted declarations injected into the live export, all fixes on: every expected verdict must match, and
    n_derived must rise by exactly cases['n_derived_increase']. Then each fix alone is switched off: the labels of
    exactly that fix's planted cases (cases['fix_cases'][fix]) must change, and no other planted label may change."""
    guard()
    cases = json.loads(CASES.read_text())
    rows = _planted_rows()
    ok = True
    for n, exp in cases['expected'].items():
        g = _label(rows, n)
        hit = g == exp
        ok &= hit
        print(f"  {'PASS' if hit else 'FAIL'}  {n.split('R4DM3Planted.')[-1]:<28} expected {exp:<30} got {g}")
        if n in rows:
            print(f"        {rows[n]['why'][:200]}")
    pre = 'PositiveGeometryEmergentSpaceTime.R4DM3Planted.'
    s0 = summary({n: a for n, a in rows.items() if not n.startswith(pre)})
    s1 = summary(rows)
    inc = s1['n_derived'] - s0['n_derived']
    print(f"  meter without planted {s0['meter']}; with planted {s1['meter']}; n_derived increase {inc} "
          f"(must be {cases['n_derived_increase']})")
    ok &= inc == cases['n_derived_increase']
    base = {n: _label(rows, n) for n in cases['expected']}
    for fix, members in cases['fix_cases'].items():
        FIXES[fix] = False
        try:
            r = _planted_rows()
        finally:
            FIXES[fix] = True
        changed = sorted(n for n in cases['expected'] if _label(r, n) != base[n])
        hit = changed == sorted(members)
        ok &= hit
        print(f"  {'PASS' if hit else 'FAIL'}  ablation {fix} off: changed {[c.split(pre)[-1] + ' -> ' + _label(r, c) for c in changed]}"
              f" (expected exactly {[m.split(pre)[-1] for m in members]})")
    print('PLANTED:', 'PASS' if ok else 'FAIL')
    return ok

def mode_broken():
    guard()
    L = load_decls(LIVE)
    ok = True
    for label, kw in (('empty classification', {'empty': True}), ('module STRUCT1 removed', {'drop': 'STRUCT1'}),
                      ('module EWZ1b removed', {'drop': 'EWZ1b'})):
        cls = load_class(**kw)
        try:
            meter(L, cls)
            print(f"  FAIL  {label}: checker produced a meter")
            ok = False
        except Unclassified as e:
            print(f"  PASS  {label}: UNCLASSIFIED {e} -> refused")
    print('BROKEN:', 'PASS' if ok else 'FAIL')
    return ok

def mode_live():
    guard()
    cls = load_class()
    L = load_decls(LIVE)
    mods = Counter(d['module'] for d in L.values())
    print(f"live export: {len(L)} declarations, {len(mods)} modules, "
          f"{sum(1 for d in L.values() if d['kind'] == 'thm')} theorems")
    cl = Counter(mod_entry(cls, m)['class'] + ('-' + mod_entry(cls, m).get('sub', '') if mod_entry(cls, m)['class'] == 'GEOMETRY' else '') for m in mods)
    print('module classes:', dict(cl))
    rows = meter(L, cls)
    print_rows(rows)
    print('SUMMARY:', json.dumps(summary(rows), indent=1))
    return rows

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    {'planted': mode_planted, 'broken': mode_broken, 'live': mode_live}[mode]()
