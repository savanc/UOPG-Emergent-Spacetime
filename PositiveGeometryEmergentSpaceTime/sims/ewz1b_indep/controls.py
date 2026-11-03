"""Negative controls for indep.py (run id EWZ1B-INDEP-2026-11-03-r1): the comparison must FAIL when
(i) the VVVV contact sign is flipped, (ii) the point is moved off the hidden-zero locus (ee13 != 0)."""
import random, json
from fractions import Fraction as F
import indep
args, body = indep.lean_N(); rnd = random.Random(7); R = lambda: F(rnd.randint(-9, 9), rnd.choice([1, 2, 3]))
bad1 = bad2 = 0; n = 40
for _ in range(n):
    v = {x: R() for x in args}
    for x in ('ee11', 'ee22', 'ee33', 'ee44', 'gs', 'b'): v[x] = R()
    v['e1p3'] = v['e3p1'] = v['ee13'] = F(0)
    k1, k2, k3 = v['k1'], v['k2'], v['k3']; k4 = -(k1 + k2 + k3); v['t'] = k2 * k2 + k4 * k4 - v['s'] - 2 * k1 * k3
    cpl = {x: v[x] for x in ('lam3', 'a', 'gs', 'lam4', 'b')}
    Nl = eval(body, {}, {x: v[x] for x in args})
    c2 = dict(cpl); c2['lam4'] = -cpl['lam4']
    A, (Ds, Dt) = indep.amplitude(v, c2); bad1 += (A * Ds * Dt != Nl)
    v['ee13'] = R() or F(1); A, (Ds, Dt) = indep.amplitude(v, cpl); bad2 += (A * Ds * Dt != Nl)
out = {'run_id': indep.RUN_ID, 'flip_lam4_disagree': bad1, 'off_locus_disagree': bad2, 'n': n}
print(json.dumps(out)); json.dump(out, open('controls_' + indep.RUN_ID + '.json', 'w'))
