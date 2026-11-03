#!/usr/bin/env python3
"""Import-and-call test (CASCADE-1b r2): import the v3 checker, call scoring functions directly.
(1) Before the prereg push every call must REFUSE.  (2) No settable pass flag: a second call re-verifies."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('cascade1b_checker', Path(__file__).with_name('cascade1b_checker_v3.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
outcomes = []
for call in (lambda: c.run_stages012(4, 1), lambda: c.cone_dim(c.sp.Matrix([[1], [1]])), lambda: c.offsets(c.Kin(4, 'E0')),
             lambda: c.components(c.sp.Integer(1), []), lambda: c.V_D(4, 1/c.sp.Symbol('y13') + 1/c.sp.Symbol('y24'), {(1, 3): c.sp.Symbol('y13'), (2, 4): c.sp.Symbol('y24')}, [(1, 3)]), lambda: c.run_planted(), lambda: c.run_live()):
    try:
        call()
        outcomes.append('PASSED GUARD')
    except SystemExit as e:
        outcomes.append(f'REFUSED: {e}')
print('IMPORT-AND-CALL:', outcomes)
print('pass-flag attributes present:', [n for n in dir(c) if 'GUARD_OK' in n.upper() or n.upper() == 'PASSED'])
sys.exit(2 if any(o.startswith('REFUSED') for o in outcomes) else 0)
