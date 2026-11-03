#!/usr/bin/env python3
"""Import-and-call test (R4-DM v2): import the checker, call scoring functions directly.
(1) Before the prereg push every call must REFUSE.  (2) There is no settable pass flag: after a refusal, a second
call re-verifies (and refuses again) rather than reading any stored success."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('r4dm2_checker', Path(__file__).with_name('r4dm2_checker.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
outcomes = []
for call in (lambda: c.load_class(), lambda: c.hyp_literals({'sm_literals_hyp': ['1/6']}, 'y = 1 / 6'),
             lambda: c.load_class()):
    try:
        call()
        outcomes.append('PASSED GUARD')
    except SystemExit as e:
        outcomes.append(f'REFUSED: {e}')
print('IMPORT-AND-CALL:', outcomes)
print('pass-flag attributes present:', [n for n in dir(c) if 'GUARD_OK' in n.upper() or n.upper() == 'PASSED'])
sys.exit(2 if any(o.startswith('REFUSED') for o in outcomes) else 0)
