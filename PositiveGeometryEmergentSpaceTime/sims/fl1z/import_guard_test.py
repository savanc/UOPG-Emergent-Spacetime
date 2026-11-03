#!/usr/bin/env python3
"""Import-and-call test (FL-1Z): import the checker, call scoring functions directly.
(1) Before the prereg push every call must REFUSE.  (2) No settable pass flag: a second call re-verifies."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('fl1z_checker', Path(__file__).with_name('fl1z_checker.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
outcomes = []
for call in (lambda: c.lepton_branches(c.Y0(c.TAU_W), __import__('random').Random(0)),
             lambda: c.observables(c.Y0(c.TAU_W), c.Ym2(c.TAU_W), 0j, 1.0, 1.0), lambda: c.run_planted()):
    try:
        call()
        outcomes.append('PASSED GUARD')
    except SystemExit as e:
        outcomes.append(f'REFUSED: {e}')
print('IMPORT-AND-CALL:', outcomes)
print('pass-flag attributes present:', [n for n in dir(c) if 'GUARD_OK' in n.upper() or n.upper() == 'PASSED'])
sys.exit(2 if any(o.startswith('REFUSED') for o in outcomes) else 0)
