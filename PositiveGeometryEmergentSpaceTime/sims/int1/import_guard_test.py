#!/usr/bin/env python3
"""Import-and-call test (INT-1): import the checker, call scoring functions directly.
(1) Before the prereg push every call must REFUSE.  (2) No settable pass flag: a second call re-verifies."""
import importlib.util, sys
from fractions import Fraction as Fr
from pathlib import Path
spec = importlib.util.spec_from_file_location('int1_checker', Path(__file__).with_name('int1_checker.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
outcomes = []
for call in (lambda: c.face_lattice(5, {(1, 3): Fr(1), (1, 4): Fr(1), (2, 4): Fr(1)}, {}),
             lambda: c.arrangement_forms(5), lambda: c.run_planted()):
    try:
        call()
        outcomes.append('PASSED GUARD')
    except SystemExit as e:
        outcomes.append(f'REFUSED: {e}')
print('IMPORT-AND-CALL:', outcomes)
print('pass-flag attributes present:', [n for n in dir(c) if 'GUARD_OK' in n.upper() or n.upper() == 'PASSED'])
sys.exit(2 if any(o.startswith('REFUSED') for o in outcomes) else 0)
