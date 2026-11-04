"""H-T3b (d): blind test of the pre-registered loop-factor rules C1/C2/C3 at n = 4 (k = 4, 8-pt), G2 gauge.
Reuses the H-T3 coarea density (scripts/ht3_abjm_measure.py). 40 digits."""
import mpmath as mp, itertools, random
src = open("scripts/ht3_abjm_measure.py").read().split("def carrier")[0]
exec(src)                                    # gp, minor, gauge, eta, density
mp.mp.dps = 40; random.seed(2026)
def corr(nodes, edges, n):
    def f(J):
        x = [mp.tanh(j) for j in J]; num = {(i, j): mp.mpf(0) for i in range(1, n+1) for j in range(i+1, n+1)}; Z = mp.mpf(0)
        for r in range(len(edges)+1):
            for sub in itertools.combinations(range(len(edges)), r):
                deg = {v: 0 for v in nodes}; w = mp.mpf(1)
                for e in sub: a, b = edges[e]; deg[a] += 1; deg[b] += 1; w *= x[e]
                odd = [v for v in nodes if deg[v] % 2]
                if not odd: Z += w
                elif len(odd) == 2 and all(isinstance(v, int) for v in odd): num[tuple(sorted(odd))] += w
        return {k: v/Z for k, v in num.items()}
    return f
nodes1 = [1, 2, 3, 4, 'c']; nodes2 = [1, 2, 3, 4, 'c', 'd']
nets = {
 "N1": (nodes1, [(1, 2), (2, 3), (1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')],
        # faces: (type, corners)
        [("V", [(1, 'c'), (2, 'c'), (3, 'c'), (4, 'c')]), ("F", [(1, 2), (1, 'c'), (2, 'c')]), ("F", [(2, 3), (2, 'c'), (3, 'c')])]),
 "N2": (nodes2, [(1, 'd'), (2, 'd'), ('d', 'c'), ('c', 3), ('c', 4), (2, 3)],
        [("V", [(1, 'd'), (2, 'd'), ('d', 'c')]), ("V", [('d', 'c'), ('c', 3), ('c', 4)]), ("F", [(2, 'd'), ('d', 'c'), ('c', 3), (2, 3)])]),
 "N3": (nodes2, [(1, 'd'), (2, 'd'), (2, 3), ('d', 3), ('d', 4), (3, 4)],
        [("V", [(1, 'd'), (2, 'd'), ('d', 3), ('d', 4)]), ("F", [(2, 'd'), ('d', 3), (2, 3)]), ("F", [('d', 3), (3, 4), ('d', 4)])]),
}
def weights(edges, J):
    return {e: (mp.sech(2*j), mp.tanh(2*j)) for e, j in zip(edges, J)}
def faceweight(face, W, omit=()):
    typ, cs = face; p = mp.mpf(1)
    for e in cs:
        if e in omit: continue
        p *= W[e][0] if typ == "V" else W[e][1]
    return p
def rules(faces, W):
    # adjacency: same type & share a corner -> vertex-touching; different type & share >=2 corners -> edge-adjacent
    F = len(faces); C1 = C2 = mp.mpf(0)
    for r in range(F+1):
        for S in itertools.combinations(range(F), r):
            ok = True; shared = set()
            for a, b in itertools.combinations(S, 2):
                common = set(faces[a][1]) & set(faces[b][1])
                if faces[a][0] != faces[b][0] and len(common) >= 2: ok = False
                if faces[a][0] == faces[b][0] and len(common) >= 2: ok = False   # J3-type: report
                if faces[a][0] == faces[b][0] and len(common) == 1: shared |= common
            if not ok: continue
            C1 += mp.fprod([faceweight(faces[a], W, omit=shared) for a in S]) if S else 1
            C2 += mp.fprod([faceweight(faces[a], W) for a in S]) if S else 1
    C3 = mp.fprod([1 + faceweight(f, W) for f in faces])
    return C1, C2, C3
def carrier(J): return mp.fprod([2*mp.coth(2*j) for j in J])
results = {}
for name, (nodes, edges, faces) in nets.items():
    Jf = corr(nodes, edges, 4)
    for jj in (1, 2):
        for trial in range(4):
            J = [mp.mpf(random.uniform(0.25, 1.4)) for _ in edges]
            R = density(Jf, 4, [1, 3, 5, 7], jj, J) / carrier(J); Jv = 16*R
            C1, C2, C3 = rules(faces, weights(edges, J))
            print(f"{name} j={jj}: 16R={mp.nstr(Jv, 18)}  16R/C1={mp.nstr(Jv/C1, 18)}  16R/C2={mp.nstr(Jv/C2, 10)}  16R/C3={mp.nstr(Jv/C3, 10)}")
            results.setdefault(name, []).append((J, R))
# consistency: tune N2 to N1's OG point; det(dlog sinh2J2/dlog sinh2J1) vs -/+ R1/R2
f1 = corr(nodes1, nets["N1"][1], 4); f2 = corr(nodes2, nets["N2"][1], 4)
keys = sorted(f1([mp.mpf(1)]*6))
def solve(J1):
    m = f1(J1); return mp.findroot(lambda *J2: [f2(list(J2))[k] - m[k] for k in keys], [mp.mpf(0.7)]*6)
mp.mp.dps = 30
J1 = [mp.mpf(v) for v in (0.6, 0.9, 0.7, 0.5, 0.8, 1.1)]; J2 = list(solve(J1))
Jm = mp.matrix(6, 6)
for b in range(6):
    def g(x, b=b):
        Jv = list(J1); Jv[b] = x; return [mp.log(mp.sinh(2*y)) for y in solve(Jv)]
    h = mp.mpf(10)**-8; gp_ = g(J1[b] + h); gm = g(J1[b] - h)
    for a in range(6): Jm[a, b] = (gp_[a] - gm[a])/(2*h) / (2*mp.coth(2*J1[b]))
R1 = density(f1, 4, [1, 3, 5, 7], 1, J1)/carrier(J1); R2 = density(f2, 4, [1, 3, 5, 7], 1, J2)/carrier(J2)
print("consistency N1->N2: det(dlog sinh2J2/dlog sinh2J1) =", mp.nstr(mp.det(Jm), 12), "  R1/R2 =", mp.nstr(R1/R2, 12))

# cell check (exact, reuses ht3_ising_cells): all three networks are reduced top-cell networks (xing = 6)
import fractions
_g = {}
exec(open("scripts/ht3_ising_cells.py").read().split("\nfamilies = {")[0], _g)
for name, (nodes, edges, faces) in nets.items():
    x = [fractions.Fraction(random.randint(1, 9), 10) for _ in edges]
    D = _g["plucker"](_g["gp_matrix"](4, _g["correlations"](4, nodes, edges, x)), 4, 8)
    f = _g["affine_perm"](_g["necklace"](D, 8, 4), 8); tau = {i: (f[i]-1) % 8 + 1 for i in f}
    print(name, "tau =", [tau[i] for i in range(1, 9)], "crossings =", _g["crossings"](tau, 8), "edges =", len(edges))
