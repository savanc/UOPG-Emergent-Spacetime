"""M1b addendum (allowed by prereg): does B1 survive every column order and sign twist of [I | X]?
For each of 24 orders x 16 column signs, the positive region is {all ordered minors of D P Pi same sign}.
Hermitian X: the Plücker vector is tau-fixed; positivity forces lambda real and y = 0 (X real symmetric), then
we test feasibility on real symmetric X by random sampling."""
import itertools, random
random.seed(1)
def minors(M):
    return {(i, j): M[0][i]*M[1][j]-M[0][j]*M[1][i] for i in range(4) for j in range(i+1, 4)}
feasible = []
samples = [(random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(20000)]
for perm in itertools.permutations(range(4)):
    for signs in itertools.product([1, -1], repeat=4):
        hit = None
        for (t, x, z) in samples:
            P = [[1, 0, t+z, x], [0, 1, x, t-z]]
            Q = [[signs[c]*P[r][perm[c]] for c in range(4)] for r in range(2)]
            m = list(minors(Q).values())
            if all(v > 0 for v in m) or all(v < 0 for v in m):
                hit = (t, x, z); break
        if hit: feasible.append((perm, signs, hit))
print(f"orders x twists with a positive real-symmetric (Hermitian, y=0) point: {len(feasible)} of 384")
for f in feasible[:8]: print("  ", f)
