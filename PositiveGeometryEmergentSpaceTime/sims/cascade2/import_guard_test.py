#!/usr/bin/env python3
"""Import-and-call test (CASCADE-2): import the checker, call scoring functions directly.
(1) Before the prereg push every call must REFUSE.  (2) No settable pass flag: a second call re-verifies."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('cascade2_checker', Path(__file__).with_name('cascade2_checker.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
outcomes = []
for call in (lambda: c.s5_series(4, {(1, 3): 1, (2, 4): -1}), lambda: c.ratio_analysis([], [c.sp.Symbol('q')], []),
             lambda: c.p_value(1, [1]), lambda: c.s5_alone(4, [(1, 3), (2, 4)]), lambda: c.run_planted(), lambda: c.run_live()):
    try:
        call()
        outcomes.append('PASSED GUARD')
    except SystemExit as e:
        outcomes.append(f'REFUSED: {e}')
print('IMPORT-AND-CALL:', outcomes)
print('pass-flag attributes present:', [n for n in dir(c) if 'GUARD_OK' in n.upper() or n.upper() == 'PASSED'])
sys.exit(2 if any(o.startswith('REFUSED') for o in outcomes) else 0)
