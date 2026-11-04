#!/usr/bin/env python3
"""Lean audit A-9 (2026-10-13): remove `simp` arguments that Lean's unusedSimpArgs linter reports.
Usage: lake build 2>&1 > build.log; python3 scripts/lean_prune_simp.py build.log
Behaviour-preserving by construction (the linter certifies the argument was not used); rerun the build after.
Post-pass for generated files such as lean/PositiveGeometryEmergentSpaceTime/ShiftForced.lean (scripts/m2e_certificates.py emits a
fixed superset simp list)."""
import re, sys, collections
log = open(sys.argv[1]).read()
hits = collections.defaultdict(list)
for m in re.finditer(r'^warning: (\S+?\.lean):(\d+):(\d+): This simp argument is unused:\n\s+(.+)$', log, re.M):
    hits[m.group(1)].append((int(m.group(2)), int(m.group(3)), m.group(4).strip()))
for f, hs in hits.items():
    path = 'lean/' + f
    lines = open(path).read().split('\n')
    for (L, C, arg) in sorted(hs, reverse=True):
        ln = lines[L - 1]
        assert ln[C:C + len(arg)] == arg, (f, L, C, arg, ln[C:C+40])
        a, b = C, C + len(arg)
        if ln[b:b + 2] == ', ': b += 2
        elif ln[b:b+1] == ',' : b += 1
        elif ln[a - 2:a] == ', ': a -= 2
        lines[L - 1] = ln[:a] + ln[b:]
    out = []
    for ln in lines:
        if re.search(r'simp only \[\s*\] at', ln):  # every argument unused: drop the no-op line
            continue
        out.append(ln)
    open(path, 'w').write('\n'.join(out))
    print(f, len(hs))
