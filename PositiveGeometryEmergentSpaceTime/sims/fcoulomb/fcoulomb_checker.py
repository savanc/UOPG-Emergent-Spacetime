#!/usr/bin/env python3
"""F-COULOMB locked checker: does positivity of the 4-pt deformed amplituhedron (arXiv:2311.10814, eqs. (1),(4)-(8),
(21)-(22)) quantise dimensionless mass ratios, or leave them continuous?
GUARD (METHOD, 2026-10-20): refuses to run ANY mode unless (a) the prereg file's adding commit is an ancestor of
origin/main after `git fetch`, and (b) this file's sha256 equals the hash recorded in the prereg.
Usage: fcoulomb_checker.py {planted|broken|live}"""
import sys, subprocess, hashlib, pathlib, re
HERE = pathlib.Path(__file__).resolve()
REPO = HERE.parents[2]
PREREG = 'prereg/F-COULOMB-2026-10-20.md'

def guard():
    def git(*a):
        return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)
    if git('fetch', '-q', 'origin').returncode != 0:
        sys.exit("GUARD REFUSED: git fetch failed")
    sha = git('log', '--format=%H', '--diff-filter=A', '-n', '1', '--', PREREG).stdout.strip()
    if not sha:
        sys.exit(f"GUARD REFUSED: {PREREG} has no commit")
    if git('merge-base', '--is-ancestor', sha, 'origin/main').returncode != 0:
        sys.exit(f"GUARD REFUSED: prereg commit {sha[:9]} is not an ancestor of origin/main (not pushed)")
    text = (REPO / PREREG).read_text()
    m = re.search(r'fcoulomb_checker\.py` sha256 `([0-9a-f]{64})`', text)
    if not m:
        sys.exit("GUARD REFUSED: checker hash not found in prereg")
    if hashlib.sha256(HERE.read_bytes()).hexdigest() != m.group(1):
        sys.exit("GUARD REFUSED: checker hash does not match prereg")
    print(f"GUARD OK: prereg {sha[:9]} on origin/main; checker hash matches")

guard()

import json
import numpy as np

# Fixed zero-parameter external data: positive momentum twistors (Vandermonde, t = 1..4), <1234> > 0.
Z = np.array([[t ** k for k in range(4)] for t in (1.0, 2.0, 3.0, 4.0)])   # rows Z_1..Z_4
def br(a, b, c, d):
    return float(np.linalg.det(np.array([a, b, c, d]).T))
assert br(*Z) > 0

def line(x, y, z, w):   # eq. (6)
    A = Z[0] + x * Z[1] - y * Z[3]
    B = Z[2] + z * Z[1] + w * Z[3]
    return A, B

def deformed_ok(rho, rhot, eta, etat, x, y, z, w):
    """Shifted inequalities (1) with eqs. (4)-(5); brackets are linear in the bivector X."""
    A, B = line(x, y, z, w)
    b12, b23, b34, b14 = br(A, B, Z[0], Z[1]), br(A, B, Z[1], Z[2]), br(A, B, Z[2], Z[3]), br(A, B, Z[0], Z[3])
    b13, b24 = br(A, B, Z[0], Z[2]), br(A, B, Z[1], Z[3])
    X1h, X3h = b12 - rho * b34, b34 - rhot * b12        # <AB X^_1>, <AB X^_3>
    X2h, X4h = b23 - eta * b14, b14 - etat * b23        # <AB X^_2>, <AB X^_4>
    return X1h > 0 and X3h > 0 and X2h > 0 and X4h > 0 and b13 < 0 and b24 < 0

def witness(rho, rhot, eta, etat):
    """Explicit witness (z = 1, y = (rho + 1/rhot)/2; x = 1, w = (eta + 1/etat)/2) when products < 1."""
    y = (rho + 1.0 / rhot) / 2.0
    w = (eta + 1.0 / etat) / 2.0
    return 1.0, y, 1.0, w   # x, y, z, w

def allowed(r, s, q=1.0, p=1.0):
    """Is the deformed one-loop region non-empty at rho*rhot = r, eta*etat = s, rho/rhot = q, eta/etat = p?
    Search: the explicit witness plus a random cloud (seeded)."""
    rho, rhot = np.sqrt(q * r), np.sqrt(r / q)
    eta, etat = np.sqrt(p * s), np.sqrt(s / p)
    cands = [witness(rho, rhot, eta, etat)]
    rng = np.random.default_rng(int(1e6 * r) + int(1e3 * s))
    for _ in range(400):
        cands.append(tuple(np.exp(rng.uniform(-4, 4, 4))))
    return any(deformed_ok(rho, rhot, eta, etat, *c) for c in cands)

def u_of(r):
    return (1 + r) ** 2 / (4 * r)                        # eq. (21)

def classify(pred, lo=0.0, hi=1.0):
    """Allowed set of a ratio on a refining grid: CONTINUOUS / QUANTISED / EMPTY."""
    counts = []
    for N in (64, 256):
        grid = [lo + (hi - lo) * k / N for k in range(1, N)]
        counts.append(sum(1 for g in grid if pred(g)))
    c64, c256 = counts
    if c256 == 0:
        return 'EMPTY', counts
    if c256 >= 3 * c64 and c64 >= 2:
        return 'CONTINUOUS', counts
    if c256 <= c64 + 1:
        return 'QUANTISED', counts
    return 'UNCLEAR', counts

mode = sys.argv[1]
spec = json.loads((HERE.parent / 'planted_cases.json').read_text())
if mode == 'planted':
    ok = True
    # (i) undeformed limit: x,y,z,w > 0 satisfies eq. (1) (paper, Sec. II)
    und = deformed_ok(0, 0, 0, 0, 1, 1, 1, 1); print("undeformed point in region:", und); ok &= und
    # (ii) u formula at rho*rhot = 1/4 -> 25/16
    u = u_of(spec['u_check_r']); print("u(1/4) =", u); ok &= abs(u - spec['u_check_value']) < 1e-12
    # (iii) a planted QUANTISING rule (allowed only at r = 1/4) must be classified QUANTISED
    cls, cnt = classify(lambda r: abs(r - spec['quantised_at']) < 1e-12); print("planted quantising rule ->", cls, cnt)
    ok &= cls == 'QUANTISED'
    # (iv) a planted CONTINUOUS rule (r < 1/2) must be classified CONTINUOUS
    cls2, cnt2 = classify(lambda r: r < 0.5); print("planted continuous rule ->", cls2, cnt2); ok &= cls2 == 'CONTINUOUS'
    print("recovered:", ok); sys.exit(0 if ok else 1)
if mode == 'broken':    # products >= 1: region must be empty -> classifier must say EMPTY and the run REJECTs
    cls, cnt = classify(lambda r: allowed(1.0 + r, 0.5))
    print("broken (rho*rhot in (1,2)) ->", cls, cnt)
    if cls == 'EMPTY':
        sys.exit("REJECT: deformed region empty for rho*rhot > 1 (as required)")
    print("ERROR: broken accepted"); sys.exit(1)
if mode == 'live':
    cls_r, cnt_r = classify(lambda r: allowed(r, 0.5))
    print("rho*rhot in (0,1) (eta*etat = 1/2):", cls_r, cnt_r)
    cls_q, cnt_q = classify(lambda t: allowed(0.5, 0.5, q=np.exp(8 * t - 4)))
    print("mass-ratio proxy rho/rhot = e^(8t-4), t in (0,1):", cls_q, cnt_q)
    us = sorted(u_of(k / 256) for k in range(1, 256) if allowed(k / 256, 0.5))
    print("u range sampled: [%.6f, %.3f], all > 1: %s" % (us[0], us[-1], all(x > 1 for x in us)))
    edge = [allowed(r, 0.5) for r in (0.999, 1.001)]
    print("edge rho*rhot = 0.999 / 1.001 allowed:", edge)
    verdict = 'CONTINUOUS' if (cls_r == 'CONTINUOUS' and cls_q == 'CONTINUOUS') else (
        'QUANTISED' if (cls_r == 'QUANTISED' and cls_q == 'QUANTISED') else (
        'PARTIAL' if 'QUANTISED' in (cls_r, cls_q) else ('EMPTY' if 'EMPTY' in (cls_r, cls_q) else 'UNCLASSIFIED')))
    print("verdict:", verdict)
