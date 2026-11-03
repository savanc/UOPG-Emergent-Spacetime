#!/usr/bin/env python3
"""Basin / failure-mode tally (METHOD 2026-10-28, *Exploration and basin saturation*).

Reads the FM and BASIN registries in scripts/blocker_tags.py; a `Failure-mode:` line in a rung's review, when present,
overrides the registry (no review has one as of 2026-10-28). Prints per-basin counts and the two trigger forms as stated
in notes/METHOD-EXPLORATION-2026-10-28.md: basin form (>= 3 rungs in a basin with the same FM tag and no earned point; this script does not check that they were consecutive on main)
and mode form (>= 3 of the last 5 rungs with the same FM tag). Read-only; prints, writes nothing.
Usage: python3 scripts/basin_tally.py [--last RUNG,RUNG,...]   (default last-5 = the order in METHOD-EXPLORATION 4a)
"""
import collections, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import blocker_tags as T

def fm_of(rung):
    rec = R / next(r[4] for r in T.B if r[0] == rung)
    if rec.exists():
        m = re.search(r'^Failure-mode:\s*(.+)$', rec.read_text(errors='ignore'), re.M)
        if m: return re.findall(r'FM-[A-Z]+', m.group(1)), 'review'
    return T.FM.get(rung, []), 'registry'

LAST5 = ['LEAN-CERT-1', 'CASCADE-1', 'TRIALITY-WHY', 'CASCADE-1b', 'LEAN-CERT-2']
if '--last' in sys.argv: LAST5 = sys.argv[sys.argv.index('--last') + 1].split(',')
allc = collections.Counter()
for b, rungs in T.BASIN.items():
    c = collections.Counter(t for r in rungs for t in fm_of(r)[0]); allc += c
    top = c.most_common(1)
    fired = bool(top) and top[0][1] >= 3
    print('%-55s n=%d  %s  basin-form %s' % (b, len(rungs), dict(c.most_common()), 'FIRED (%s x%d)' % top[0] if fired else 'not fired'))
e = collections.Counter(t for r in T.B3_EARLIER for t in fm_of(r)[0])
print('  B3 earlier (BACKLOG class-not-point, outside the tally): %s' % dict(e))
print('All basin rungs: %s' % dict(allc.most_common()))
m = collections.Counter(t for r in LAST5 for t in fm_of(r)[0])
top = m.most_common(1)
print('Mode form over %s: %s -> %s' % (LAST5, dict(m.most_common()), 'FIRED' if top and top[0][1] >= 3 else 'not fired'))
