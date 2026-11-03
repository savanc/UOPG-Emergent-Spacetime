"""Import-and-call guard test (hardened guard rule): two direct calls to scoring functions must REFUSE before the prereg push."""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
m = importlib.import_module('rgir1_checker')
refused = 0
for fn in (lambda: m.evaluate(m.SM), lambda: m.planted()):
    try:
        fn(); print('CALL RAN (guard did not refuse)')
    except SystemExit as e:
        refused += 1; print("REFUSED:", e)
flags = [k for k in dir(m) if any(s in k.lower() for s in ('pass', 'ok', 'guarded', 'verified')) and not callable(getattr(m, k)) and not k.startswith('T_')]
print('pass-flag attributes present:', flags)
sys.exit(2 if refused == 2 and not flags else 0)
