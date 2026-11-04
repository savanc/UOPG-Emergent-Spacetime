#!/usr/bin/env python3
"""Stage 2: per-rung skeletons + batched Lean check file + definition dependencies.
Reads out/{lean_index.json,claims.json} from extract.py. Writes:
  out/skeleton/<RUNG>.md   claims, cited decls (literal signatures), module theorem list (candidates)
  out/BlueprintCheck.lean  one file: `#check @name` + `#print axioms name` for every cited decl and DEF row
  out/defs.json            PositiveGeometryEmergentSpaceTime defs/structures occurring in cited headline statements (DEF-row candidates)
"""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent; OUT = HERE / 'out'
RUNG_MODULES = {
 'MR-1b': ['LSResidue'], 'H-T5': ['IsingTiling', 'IsingOG'], 'INT-1': ['IntChamber'], 'LEAN-CERT-1': ['LeanCert'],
 'BR-4': ['BR4', 'ScaleNoGo'], 'MR-3': ['MassiveLS'], 'SURF-1′': ['Surf1', 'SurfConv'], 'JORD-1': ['Jord1', 'JordConv'],
 'TRIALITY-WHY': ['TrialityWhy'], 'GRADED-POSITROID': ['GradedPositroid'], 'FL-1Z': ['FL1Z'], 'EW-Z1b': ['EWZ1b'],
 'CASCADE-1': ['Cascade1'], 'CASCADE-1b r2': ['Cascade1bR2'], 'LEAN-CERT-2': ['LeanCert2', 'LeanCertConv'],
 'RG-IR-1': ['RgIr1'], 'CHIRAL-LATTICE-1': ['ChiralLat1'], 'RP-TN-1': ['RpTn1'],
 'HG-DIM-1': ['HgDim1', 'HgDim1Mean', 'HgDim1Mean9'], 'HG-DIM-2': ['HgDim2', 'HgDim2P4', 'HgDim2P5', 'HgDim2P6'],
 'CAPPED-FORMAN-1': ['CappedForman', 'CappedFormanCerts'], 'CURV-LEAN': ['HgDim1', 'HgDim1Mean', 'HgDim1Mean9', 'HgDim2', 'CappedForman'],
 'M3': ['MassiveZero', 'Coon', 'LECRatio'], 'R4-DM': ['R4Indep'],
}
def in_mods(d, mods):
    m = d['module'].split('.')
    return len(m) > 1 and m[1] in mods
idx = json.load(open(OUT / 'lean_index.json')); C = json.load(open(OUT / 'claims.json'))
claims, notes = C['claims'], C['notes']
(OUT / 'skeleton').mkdir(exist_ok=True)
cited = set(open(OUT / 'cited.txt').read().split())
defs_used = {}
IDENT = re.compile(r"[A-Za-z_][\w.'′₀-₉]*")
def deps(sig, d):
    ns = d['name'].rsplit('.', 1)[0]
    out = set()
    for t in set(IDENT.findall(sig)):
        for cand in (t, ns + '.' + t, 'PositiveGeometryEmergentSpaceTime.' + t, d['module'] + '.' + t):
            if cand in idx and idx[cand]['kind'] in ('def', 'abbrev', 'structure', 'inductive', 'class', 'opaque') and cand != d['name']:
                out.add(cand); break
    return sorted(out)
for rung in sorted({c['rung'] for c in claims}):
    rc = [c for c in claims if c['rung'] == rung]
    mods = RUNG_MODULES.get(rung, [])
    thms = [d for d in idx.values() if in_mods(d, mods) and d['kind'] in ('theorem', 'lemma')]
    L = [f'# {rung}: skeleton (auto)', '', f'Modules: {mods}  theorems in modules: {len(thms)}', '', '## Claims']
    for c in rc:
        L.append(f"- [{c['paper']}:{c['line']}] {c['kind']}: {c['text'][:600]}  cited={c.get('resolved')}")
    L += ['', '## Notes-alignment decls', ', '.join(notes.get(rung, [])) or '-', '', '## Theorems (literal signatures)']
    for d in thms:
        s = re.sub(r'\s+', ' ', d['sig'])
        L.append(f"- `{d['name']}` ({d['file']}:{d['line']}): {s[:400]}")
        if d['name'] in cited:
            for x in deps(d['sig'], d): defs_used.setdefault(x, set()).add(d['name'])
    (OUT / 'skeleton' / f"{rung.replace(' ', '_').replace('′', 'p')}.md").write_text('\n'.join(L) + '\n')
json.dump({k: sorted(v) for k, v in defs_used.items()}, open(OUT / 'defs.json', 'w'), indent=1)
print('rungs', len({c['rung'] for c in claims}), 'defs used by cited headline thms', len(defs_used))
