#!/usr/bin/env python3
"""Import-and-call test (JORD-1): import the checker, call scoring functions directly.
(1) Before the prereg push every call must REFUSE.  (2) There is no settable pass flag: after a refusal, a second
call re-verifies (and refuses again) rather than reading any stored success."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('jord1_checker', Path(__file__).with_name('jord1_checker.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
outcomes = []
for call in (lambda: c.table_ok(c.omul_table()), lambda: c.F4(c.omul_table())):
    try:
        call()
        outcomes.append('PASSED GUARD')
    except SystemExit as e:
        outcomes.append(f'REFUSED: {e}')
print('IMPORT-AND-CALL:', outcomes)
print('pass-flag attributes present:', [n for n in dir(c) if 'GUARD_OK' in n.upper() or n.upper() == 'PASSED'])
sys.exit(2 if any(o.startswith('REFUSED') for o in outcomes) else 0)
