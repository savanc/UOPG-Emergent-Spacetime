#!/usr/bin/env python3
"""HG-DIM-1 addendum: exact combinatorial cross-check of the mean-curvature closed form.
Does NOT call the curvature solver. kappa_e = (2 - p_e)/(n - 2) is used as the (paper-proved) per-edge formula.
Method A (n <= BRUTE_MAX): enumerate all triangulations, compute p for every (T, d) by finding the two apexes.
Method B (all n): quadrilateral sum  sum_{a<b<c<e} 2 * prod C(gap-1) * #(gaps >= 2)  (2 = choice of diagonal).
Method C (all n): closed form (2n-12) C_{n-2} + 2n C_{n-3}  (ear identity) and mean (10-n)/((n-2)(2n-5)).
Compares with the locked live run sims/hgdim1/hgdim1_live.json (n = 6..11) and the planted pentagon (n = 5, 1/3)."""
import json, sys, time, hashlib, platform
from fractions import Fraction as F
from itertools import combinations
from math import comb
NMIN, NMAX, BRUTE_MAX = 4, 16, 12
def C(m): return comb(2*m, m)//(m+1)
def is_side(n, u, v): u, v = min(u, v), max(u, v); return v == u+1 or (u == 0 and v == n-1)
def tris(n):
    D = [(i, j) for i in range(n) for j in range(i+2, n) if not (i == 0 and j == n-1)]
    def cr(p, q): return (p[0] < q[0] < p[1] < q[1]) or (q[0] < p[0] < q[1] < p[1])
    out = []
    def rec(k, acc):
        if len(acc) == n-3: out.append(frozenset(acc)); return
        for t in range(k, len(D)):
            if len(D)-t < n-3-len(acc): break
            if all(not cr(D[t], q) for q in acc): rec(t+1, acc+[D[t]])
    rec(0, []); return out
def brute(n):
    S = 0; ears = 0; npairs = 0; per_T_ok = True; Ts = tris(n)
    for T in Ts:
        E = lambda u, v: is_side(n, u, v) or (min(u, v), max(u, v)) in T
        sp = 0
        for (a, c) in T:
            x = [v for v in range(a+1, c) if E(a, v) and E(v, c)]
            y = [v for v in list(range(c+1, n))+list(range(0, a)) if E(a, v) and E(v, c)]
            assert len(x) == 1 and len(y) == 1
            p = sum(not is_side(n, u, v) for u, v in [(a, x[0]), (x[0], c), (a, y[0]), (y[0], c)])
            sp += p; npairs += 1
        e = sum(1 for v in range(n) if (min((v-1) % n, (v+1) % n), max((v-1) % n, (v+1) % n)) in T)
        ears += e; per_T_ok &= (sp == 2*n-12+2*e); S += sp
    return dict(N=len(Ts), pairs=npairs, sum_p=S, sum_ears=ears, per_T_identity=per_T_ok)
def quad_sum(n):
    S = 0
    for q in combinations(range(n), 4):
        gaps = [q[1]-q[0], q[2]-q[1], q[3]-q[2], n-q[3]+q[0]]
        w = 1
        for g in gaps: w *= C(g-1)
        S += 2*w*sum(g >= 2 for g in gaps)
    return S
t0 = time.time()
live = json.load(open('../hgdim1/hgdim1_live.json'))
live_mean = {int(r['n']): F(r['kmean']) for r in live['rows']}
live_psum = {int(r['n']): 2*sum(int(k)*v for k, v in r['p_hist'].items()) for r in live['rows']}  # each edge = 2 (T, d) pairs
live_mean[5] = F(1, 3)  # planted PL5 (pentagon C_5), all edges 1/3
rows = []; ok = True
for n in range(NMIN, NMAX+1):
    pairs = (n-3)*C(n-2); closed = (2*n-12)*C(n-2) + 2*n*C(n-3)
    qs = quad_sum(n); mean = (2 - F(qs, pairs))/(n-2); conj = F(10-n, (n-2)*(2*n-5))
    r = dict(n=n, catalan=C(n-2), pairs=pairs, sum_p_quad=qs, sum_p_closed=closed, mean_kappa=str(mean), conj=str(conj),
             Ep=str(F(qs, pairs)), Ep_conj=str(F(5*(n-4), 2*n-5)))
    good = qs == closed and mean == conj
    if n <= BRUTE_MAX:
        b = brute(n); r.update(brute=b)
        good &= b['sum_p'] == qs and b['N'] == C(n-2) and b['pairs'] == pairs and b['per_T_identity'] and b['sum_ears'] == n*C(n-3)
    if n in live_mean: r['live_mean'] = str(live_mean[n]); good &= live_mean[n] == mean
    if n in live_psum: r['live_sum_p_pairs'] = live_psum[n]; good &= live_psum[n] == qs
    r['ok'] = good; ok &= good; rows.append(r)
    print(n, r['catalan'], qs, closed, mean, conj, r.get('live_mean', '-'), 'brute' if n <= BRUTE_MAX else '', good, flush=True)
run_id = 'HGDIM1-MEAN-' + time.strftime('%Y%m%dT%H%M%S')
out = dict(run_id=run_id, all_ok=ok, rows=rows, python=platform.python_version(), elapsed_s=round(time.time()-t0, 2))
json.dump(out, open('mean_check.json', 'w'), indent=1)
print('ALL_OK', ok, run_id)
