#!/usr/bin/env python3
"""JORD-1 POST-HOC diagnostic (written 2026-10-28, after the locked live run; NOT scoring, NOT a superseding checker).
Imports the locked checker (guard passes: prereg on origin/main) and reports which F_A idempotents fail is_idempotent2,
and whether they pass when given at the 2P scale that is_idempotent2 expects."""
import importlib.util, json
spec = importlib.util.spec_from_file_location('c', 'sims/jord1/jord1_checker.py'); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
T = c.omul_table(); F = c.F4(T)
ids = c.idempotents()
bad = [n for n, v in ids if not c.is_idempotent2(v, F.C)]
print('failing:', bad)
for n, v in ids[:3]:
    w = [2*x for x in v]; print(n, 'scaled-by-2 passes:', c.is_idempotent2(w, F.C))
print('total idempotents:', len(ids), 'passing as given:', len(ids)-len(bad))
