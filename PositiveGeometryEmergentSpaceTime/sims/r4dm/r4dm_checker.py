#!/usr/bin/env python3
"""R4-DM derivation meter, locked checker (prereg/R4-DM-2026-10-20.md). Supersedes the R4 separation checker
sims/r4/r4_separation.py as PositiveGeometryEmergentSpaceTime's geometry -> SM measure (R4 stays as written; see the prereg).

Question measured: of the Lean statements that ARE about Standard-Model structure, how many are DERIVED from
geometry -- proved with at least one GEOMETRY definition, no SM-INPUT declaration in the proof beyond what the
statement itself names, and no SM data smuggled in through a hypothesis?  meter = #DERIVED / #SM-structure.

Inputs (all hash-locked in the prereg):
  graph/r4dm_decls.jsonl            live export by sims/r4dm/R4DMExport.lean (binders/conclusion split)
  sims/r4dm/classification.json     module classes GEOMETRY(PG|AMP) / SM-INPUT / MIXED/TEST + roles + vocab
  sims/r4dm/planted/planted_decls.jsonl  export of sims/r4dm/planted/R4DMPlanted.lean (same export block)
  sims/r4dm/planted_cases.json      expected planted verdicts
Modes: planted | broken | live | history.
GUARD (METHOD 2026-10-20 hardened pattern, as sims/ngen/ngen_checker.py): guard() inside EVERY scoring function
re-verifies on EVERY call that the prereg commit is an ancestor of origin/main and that the checker, classification,
exporter and planted-Lean sha256 equal the prereg's; the two export blocks must be byte-identical. No pass flag;
caches keyed by origin/main sha only; `git fetch` once per process. Unclassified module => UNCLASSIFIED, refuse.
"""
import hashlib, json, re, subprocess, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/R4-DM-2026-10-20.md'
CLASS = REPO / 'sims/r4dm/classification.json'
EXPORTER = REPO / 'sims/r4dm/R4DMExport.lean'
PLANTED_LEAN = REPO / 'sims/r4dm/planted/R4DMPlanted.lean'
LIVE = REPO / 'graph/r4dm_decls.jsonl'
PLANTED = REPO / 'sims/r4dm/planted/planted_decls.jsonl'
CASES = REPO / 'sims/r4dm/planted_cases.json'
LOCKED = {'r4dm_checker.py': HERE, 'classification.json': CLASS, 'R4DMExport.lean': EXPORTER,
          'R4DMPlanted.lean': PLANTED_LEAN, 'planted_cases.json': CASES}
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
    b1, b2 = _block(EXPORTER), _block(PLANTED_LEAN)
    if b1 is None or b1 != b2:
        sys.exit("GUARD REFUSED: export block of R4DMPlanted.lean differs from R4DMExport.lean")

def guard_banner():
    guard()
    psha, _ = _ANC_BY_ORIGIN[_origin_sha()]
    print(f"GUARD OK: prereg {psha[:9]} on origin/main; checker/classification/exporter/planted hashes match "
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
        if (d['name'] == k or d['name'].startswith(k + '.')) and len(k) > best:
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
    lits = {x.lstrip('-') for x in cls['sm_literals_hyp']}
    return sorted({f'{a}/{b}' for a, b in _FRAC.findall(t) if f'{a}/{b}' in lits})

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
    cc = set(d['concl_consts'])
    concl_sm_input = sorted(c for c in cc if R.get(c) == 'SM-INPUT')
    concl_smv = sorted(c for c in cc if c in svc)
    concl_vars = sorted(r for r in d['concl_refs'] if r in smvars)
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
    if not has_sm_symbol or (not hyp_sm and not concl_sm_input and not concl_smv):
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

def mode_planted():
    """Planted declarations (sims/r4dm/planted) are injected into the live export (the library they cite) and
    scored with the same rules. Every expected verdict must match, and the planted genuine + conditional cases must
    raise n_derived by exactly 2 (they must COUNT); the others must not."""
    guard()
    cls = load_class()
    cases = json.loads(CASES.read_text())
    P = load_decls(PLANTED)
    L = load_decls(LIVE)
    rows = meter({**L, **P}, cls, planted_mods={'R4DMPlanted'})
    ok = True
    for n, exp in cases['expected'].items():
        got = rows.get(n, {'verdict': 'NOT-SM-STRUCTURE'})
        g = got['verdict'] + (f"/{got.get('cond')}/{got.get('source')}" if got['verdict'] == 'DERIVED' else '')
        hit = g == exp
        ok &= hit
        print(f"  {'PASS' if hit else 'FAIL'}  {n.split('.')[-1]:<28} expected {exp:<34} got {g}")
        if n in rows:
            print(f"        {rows[n]['why'][:200]}")
    s0 = summary({n: a for n, a in rows.items() if not n.startswith('PositiveGeometryEmergentSpaceTime.R4DMPlanted.')})
    s1 = summary(rows)
    inc = s1['n_derived'] - s0['n_derived']
    print(f"  meter without planted {s0['meter']}; with planted {s1['meter']}; n_derived increase {inc} (must be 2)")
    ok &= inc == 2
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

def _uses(x):
    return [u['n'] if isinstance(u, dict) else u for u in x]

def mode_history():
    """Coarse back-scan. (1) every graph/raw_decls.jsonl snapshot: SM-structure proxies (statement names an
    SM-INPUT-role constant, an SM-var constant, a vocab binder, or is on the manual list) whose closure reaches a
    GEOMETRY definition -> candidate list per snapshot, with appeared/disappeared names; declarations removed
    between snapshots. (2) every commit touching lean/: import-level edges GEOMETRY-module -> SM-INPUT-module."""
    guard()
    cls = load_class()
    log = _git('log', '--reverse', '--format=%h %ad', '--date=iso', '--', 'graph/raw_decls.jsonl').stdout.split('\n')
    prev_c, prev_n = None, None
    for line in filter(None, log):
        h = line.split()[0]
        raw = _git('show', f'{h}:graph/raw_decls.jsonl').stdout
        D = {}
        for l in raw.splitlines():
            if l.strip():
                d = json.loads(l)
                d['type_uses'], d['value_uses'] = _uses(d.get('type_uses', [])), _uses(d.get('value_uses', []))
                D[d['name']] = d
        R, unc = {}, set()
        for n, d in D.items():
            try:
                R[n] = role(cls, d)
            except Unclassified:
                unc.add(d['module'])
        cands = set()
        for n, d in D.items():
            if d['kind'] != 'thm' or n not in R:
                continue
            st = d['statement']
            voc = vocab(cls, d)
            s = (any(R.get(u) == 'SM-INPUT' for u in d['type_uses']) or any(u in cls['sm_var_consts'] for u in d['type_uses'])
                 or any(re.search(r'[({∀]\s*(?:[^:()]*\s)?' + re.escape(v) + r'(?:\s[^:()]*)?\s*:', st) for v in voc)
                 or n in cls['manual_sm_structure'])
            if not s:
                continue
            if any(R.get(m, '').startswith('GEOMETRY') and D[m]['kind'] in DEFLIKE for m in closure(D, d['type_uses'] + d['value_uses'])):
                cands.add(n)
        names = set(D)
        msg = f"{line.strip()[:28]}  decls {len(D):>5}  unclassified {sorted(unc) or '-'}  geo-reaching SM-structure {len(cands)}"
        if prev_c is not None:
            msg += f"  +{sorted(cands - prev_c)}  -{sorted(prev_c - cands)}  removed-decls {len(prev_n - names)}"
        print(msg)
        prev_c, prev_n = cands, names
    print("-- import edges GEOMETRY-module -> SM-INPUT-module, every commit touching lean/")
    commits = _git('log', '--reverse', '--format=%h', '--', 'lean').stdout.split()
    seen = {}
    for h in commits:
        files = _git('ls-tree', '-r', '--name-only', h, 'lean/PositiveGeometryEmergentSpaceTime').stdout.split()
        edges = set()
        for f in files:
            if not f.endswith('.lean'):
                continue
            m = Path(f).stem
            e = cls['modules'].get(m)
            if e is None:
                edges.add(f'UNCLASSIFIED {m}')
                continue
            src = _git('show', f'{h}:{f}').stdout
            for imp in re.findall(r'^import\s+PositiveGeometryEmergentSpaceTime\.(\w+)', src, re.M):
                t = cls['modules'].get(imp)
                if t is None:
                    edges.add(f'UNCLASSIFIED {imp}')
                    continue
                geo_src = e['class'] == 'GEOMETRY' or (e['class'] == 'MIXED/TEST' and e['default_role'].startswith('GEOMETRY'))
                if geo_src and (t['class'] == 'SM-INPUT' or (t['class'] == 'MIXED/TEST' and t['default_role'] == 'SM-INPUT')):
                    edges.add(f'{m} -> {imp}')
        key = tuple(sorted(edges))
        if seen.get('last') != key:
            print(f"  {h}: {sorted(edges) or 'none'}")
            seen['last'] = key
    print(f"  ({len(commits)} lean commits scanned)")

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'live'
    guard_banner()
    {'planted': mode_planted, 'broken': mode_broken, 'live': mode_live, 'history': mode_history}[mode]()
