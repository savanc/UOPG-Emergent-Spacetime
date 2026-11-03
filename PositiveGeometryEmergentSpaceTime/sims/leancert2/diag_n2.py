"""LEAN-CERT-2 post-result diagnostic (written AFTER the live run; does not change the locked verdict).
Replays the N2 corruption loop of `run_live` with the same rng (seed 20261028) on the certificates in
certs_lean.txt and classifies every accepted corruption.  An accepted corruption passes the exact
mirror check, so it is itself a valid certificate for the same k; the question is only where it sits."""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import leancert2_checker as C
from emit_lean import parse_certs

blocks = parse_certs(C.OUTDIR / 'certs_lean.txt')
order = sorted(blocks, key=lambda s: (int(s[7]), s[8] == 'm'))  # same order as run_live: k, then sigma=+1 first
rng = random.Random(20261028)
_ = C.primes_from(2**30 + 3, 20)
tot = {}; lines = []
for name in order:
    b = blocks[name]
    c = dict(Mr=b['M'], Kr=b['K'], Pr=b['P'], Qr=b['Q'], d=b['d'], m=b['m'], n=b['n'], k=b['k'],
             Kc=[[r[j] for r in b['K']] for j in range(b['k'])], rank=b['n'] - b['k'])
    acc = {'Kr': 0, 'Pr': 0, 'Qr': 0}; zero_row = 0
    for _ in range(60):
        which = rng.choice([w for w in ('Kr', 'Pr', 'Qr') if c[w] and c[w][0]])
        mat = [list(r) for r in c[which]]
        i = rng.randrange(len(mat)); j = rng.randrange(len(mat[0]))
        mat[i][j] += rng.choice((-1, 1))
        if C.mirror_check(dict(c, **{which: mat})):
            acc[which] += 1
            if which == 'Pr' and all(x == 0 for x in c['Mr'][j]): zero_row += 1
    zr = sum(1 for r in c['Mr'] if all(x == 0 for x in r))
    lines.append(f"{name}: accepted {sum(acc.values())} (K {acc['Kr']}, P {acc['Pr']}, Q {acc['Qr']}); "
                 f"P-corruptions in a zero row of M: {zero_row}; zero rows of M: {zr}/{c['m']}")
    for w in acc: tot[w] = tot.get(w, 0) + acc[w]
lines.append(f"TOTAL accepted {sum(tot.values())} = K {tot['Kr']} + P {tot['Pr']} + Q {tot['Qr']}")
print("\n".join(lines)); (C.OUTDIR / 'diag_n2.txt').write_text("\n".join(lines) + "\n")
