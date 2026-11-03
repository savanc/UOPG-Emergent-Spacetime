"""H-T5f Part B: tree-tile wall graph (from exact network degenerations) vs associahedron flip graph."""
import itertools, json, functools
print = functools.partial(print, flush=True)
src = open("scripts/ht5_tiling.py").read(); head = src[:src.index("def Lam")]
g = {"__name__": "h"}; exec(head, g); Net = g["Net"]
def xing(t):
    N = len(t); ch = [(i, t[i-1]) for i in range(1, N+1) if i < t[i-1]]
    return sum(1 for (a, b), (c, d) in itertools.combinations(ch, 2) if a < c < b < d or c < a < d < b)
def triangulations(poly):
    if len(poly) < 3: return [[]]
    if len(poly) == 3: return [[tuple(poly)]]
    a, b = poly[0], poly[-1]; out = []
    for i in range(1, len(poly)-1):
        c = poly[i]
        for L in triangulations(poly[:i+1]):
            for R in triangulations(poly[i:]): out.append(L + R + [(a, c, b)])
    return out
def tree_of(tri, k):
    # polygon vertices v_0..v_{k-1}; side i (leaf i, 1-based) joins v_{i-1}, v_i
    sides = {frozenset(((i-1) % k, i % k)): i for i in range(1, k+1)}
    E = []; T = [tuple(t) for t in tri]
    for a, t in enumerate(T):
        for e in itertools.combinations(t, 2):
            fe = frozenset(e)
            if fe in sides: E.append((sides[fe], f"t{a}"))
            else:
                for b in range(a+1, len(T)):
                    if fe <= set(T[b]): E.append((f"t{a}", f"t{b}"))
    diags = frozenset(frozenset(e) for t in T for e in itertools.combinations(t, 2) if frozenset(e) not in sides)
    return E, diags
def degens(E):
    for i, e in enumerate(E):
        yield [x for j, x in enumerate(E) if j != i]
        a, b = e
        if isinstance(a, int) and isinstance(b, int): continue
        keep, gone = (a, b) if isinstance(a, int) else ((b, a) if isinstance(b, int) else (a, b))
        yield [tuple(keep if v == gone else v for v in x) for j, x in enumerate(E) if j != i]
out = {}
for k in (4, 5, 6):
    tris = triangulations(list(range(k)))
    tiles = []
    for tri in tris:
        E, D = tree_of(tri, k); t = Net(k, E).tau(); assert xing(t) == len(E) == 2*k - 3, (k, E, xing(t))
        bd = set()
        for E2 in degens(E):
            t2 = Net(k, E2).tau()
            if xing(t2) == len(E) - 1: bd.add(t2)
        tiles.append(dict(E=E, D=D, tau=t, bd=bd))
    n = len(tiles)
    wall = {(a, b) for a, b in itertools.combinations(range(n), 2) if tiles[a]["bd"] & tiles[b]["bd"]}
    flip = {(a, b) for a, b in itertools.combinations(range(n), 2) if len(tiles[a]["D"] & tiles[b]["D"]) == k - 4}
    # boundary multiplicity: internal = shared by exactly 2
    cnt = {}
    for T in tiles:
        for b in T["bd"]: cnt[b] = cnt.get(b, 0) + 1
    internal = sum(1 for v in cnt.values() if v == 2); external = sum(1 for v in cnt.values() if v == 1)
    taus = [T["tau"] for T in tiles]
    print(f"n={2*k}: {n} tree tiles (distinct taus {len(set(taus))}); codim-1 boundaries per tile {[len(T['bd']) for T in tiles]}")
    print(f"   wall edges {len(wall)}, flip edges {len(flip)}, equal: {wall == flip}; internal walls {internal}, external {external}, max multiplicity {max(cnt.values())}")
    if k == 5:
        for T in tiles: print("   tree", T["E"], "tau", T["tau"])
    out[2*k] = dict(tiles=n, wall=sorted(wall), flip=sorted(flip), equal=wall == flip, internal=internal, external=external,
                   taus=[list(t) for t in taus])
json.dump(out, open("scripts/ht5f_adjacency.json", "w"), indent=1)
