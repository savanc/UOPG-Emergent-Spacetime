#!/usr/bin/env python3
"""Import-and-call test (F-DIM'): importing fdim2_checker and calling a scoring function directly must hit guard().
Before the prereg push it must REFUSE (SystemExit 'GUARD REFUSED'); after the push it must print GUARD OK first."""
import importlib.util, sys
from fractions import Fraction as F
from pathlib import Path
spec = importlib.util.spec_from_file_location('fdim2_checker', Path(__file__).with_name('fdim2_checker.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)          # import itself runs no scoring
try:
    c.residue_poly(('bos', F(-1)), 0)   # cheapest scoring call; must be guarded
except SystemExit as e:
    print('IMPORT-AND-CALL:', e)
    sys.exit(2)
print('IMPORT-AND-CALL: guard passed, call returned')
