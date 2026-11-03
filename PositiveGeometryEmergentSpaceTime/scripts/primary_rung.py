#!/usr/bin/env python3
"""Primary-rung attribution for Lean modules (2026-10-28 deep review; replaces the hand-pinned PRIMARY_OVERRIDE list in
scripts/theorem_graph.py). Rule: a module's primary rung is the first rung record in git history that mentions it in
code context; mention counts only break ties. See primary_rungs() for which files count as records."""
import re, subprocess, collections, pathlib
RUNG_RE = re.compile(r'^([A-Z][A-Za-z0-9\-]*?(?:-[0-9a-z\']+)*?)-(result|gate|gates|prereg|full|audit|score|axioms)')
NOTE_REC = re.compile(r'^([A-Z][A-Za-z0-9\-′]*?)-(\d{4}-\d{2}-\d{2})\.md$')
NOTE_SKIP = re.compile(r'PREREG|TRAFFIC|INDEX|TRADE-SPACE|HANDOFF|BACKLOG|LEDGER|NAMING|SCAN|RANKING|METHOD|LOG')
SPAN = re.compile(r'`[^`\n]+`')
def git(R, *a): return subprocess.run(['git', '-C', str(R)] + list(a), capture_output=True, text=True).stdout
def add_times(R, path):
    """file -> (unix time, commit) of the commit that first added it (oldest A in history)."""
    out, cur, added = git(R, 'log', '--diff-filter=A', '--format=@%ct %H', '--name-only', '--', path), None, {}
    for l in out.splitlines():
        if l.startswith('@'): cur = (int(l[1:].split()[0]), l[1:].split()[1])
        elif l.strip(): added[l.strip()] = cur  # log is newest first: the last write is the oldest add
    return added
def mentions(M, t, keys):
    """Code-context mentions of module M in text t. keys = extra identifiers (unique decl short names).
    Backtick spans are tokenised in order, so a match can never straddle two spans."""
    pats = [re.compile(r'\b%s\b' % re.escape(M))] + [re.compile(r'\b%s\b' % re.escape(k)) for k in keys]
    k = sum(1 for s in SPAN.findall(t) if any(p.search(s) for p in pats))
    rest = SPAN.sub(' ', t); e = re.escape(M)
    return k + len(re.findall(r'(PositiveGeometryEmergentSpaceTime\.%s\b|(?<![\w.])%s\.lean\b|\bLean %s\b)' % (e, e, e), rest))
def primary_rungs(R, modules, decl_names):
    """Primary rung = the first rung record in git history that mentions the module (code context).
    Records: reviews/<RUNG>-{result,gate,...}*.md, plus a dated notes/<RUNG>-YYYY-MM-DD.md record only when it was
    added in the same commit that created the module's .lean file (rungs filed in notes/, e.g. R4-INDEPENDENT).
    A nested module A.B also counts mentions of A. Mention counts only break ties within one commit."""
    R = pathlib.Path(R)
    rev_add = add_times(R, 'reviews/')
    short = collections.defaultdict(set)
    for n, m in decl_names: short[n.split('.')[-1]].add(m)
    texts, out = {}, {}
    def txt(f):
        if f not in texts: texts[f] = (R / f).read_text(errors='ignore')
        return texts[f]
    for M in modules:
        keys = sorted(s for s, ms in short.items() if ms == {M} and len(s) >= 8 and '_' in s)
        names = [M] + ([M.split('.')[0]] if '.' in M else [])
        cands = []
        for f, (ts, c) in rev_add.items():
            nm = f.split('/')[-1]
            m = RUNG_RE.match(nm) or (None if re.search(r'REVIEW|AUDIT', nm) or NOTE_SKIP.search(nm) else NOTE_REC.match(nm))
            if not m or not (R / f).exists(): continue
            k = sum(mentions(x, txt(f), keys) for x in names)
            if k: cands.append((ts, -k, m.group(1), f))
        lean = R / 'lean' / 'PositiveGeometryEmergentSpaceTime' / (M.replace('.', '/') + '.lean')
        cre = git(R, 'log', '--diff-filter=A', '--format=%ct %H', '--', str(lean.relative_to(R))).split()
        if cre:
            ts, c = int(cre[-2]), cre[-1]
            for f in git(R, 'show', '--diff-filter=A', '--name-only', '--format=', c).split():
                nm = f.split('/')[-1]; m = NOTE_REC.match(nm)
                if f.startswith('notes/') and m and not NOTE_SKIP.search(nm) and (R / f).exists():
                    k = sum(mentions(x, txt(f), keys) for x in names)
                    if k: cands.append((ts, -k, m.group(1), f))
        cands.sort()
        out[M] = (cands[0][2], cands[0][3]) if cands else (None, None)
    return out
