"""H-T5g stage 1, route A: tile measure as iterated residue of the Lee measure in the Ising chart of a top network
N containing the tree (extra edges J->0); no fiber, no Y-chart. High-precision central differences."""
import itertools, functools, random, json, sys
from fractions import Fraction as F
import mpmath as mp
print = functools.partial(print, flush=True)
src = open("scripts/ht5_tiling.py").read(); head = src[:src.index("def Lam")]
g = {"__name__": "h"}; exec(head, g); Net = g["Net"]
def xing(t):
    N = len(t); ch = [(i, t[i-1]) for i in range(1, N+1) if i < t[i-1]]
    return sum(1 for (a, b), (c, d) in itertools.combinations(ch, 2) if a < c < b < d or c < a < d < b)
H = None
def setprec(dps, h): global H; mp.mp.dps = dps; H = mp.mpf(10) ** (-h)
def dmat(fun, x, nout):
    J = mp.matrix(nout, len(x))
    for a in range(len(x)):
        xp = list(x); xp[a] += H; xm = list(x); xm[a] -= H
        fp, fm = fun(xp), fun(xm)
        for r in range(nout): J[r, a] = (fp[r] - fm[r]) / (2*H)
    return J
class Model:
    def __init__(s, k):
        s.k = k; s.P = list(itertools.combinations(range(1, k+1), 2))
    def C(s, m):
        k = s.k; M = mp.matrix(k, 2*k); md = dict(zip(s.P, m))
        for i in range(1, k+1):
            for j in range(1, k+1):
                if i == j: M[i-1, 2*i-2] = M[i-1, 2*i-1] = 1
                else:
                    v = (-1) ** (i + j + (1 if i < j else 0)) * md[(min(i, j), max(i, j))]
                    M[i-1, 2*j-2] = v; M[i-1, 2*j-1] = -v
        return M
    def gauged(s, m):
        C = s.C(m); k = s.k
        A = mp.matrix([[C[r, 2*c] for c in range(k)] for r in range(k)]); return A**-1 * C
    def O(s, m):
        C = s.gauged(m); return [C[r, 2*c+1] for r in range(s.k) for c in range(s.k)]
    def rhoH(s, m):
        G = dmat(s.O, m, s.k**2); return mp.sqrt(abs(mp.det(G.T * G)))
    def PiM(s, m):
        C = s.gauged(m); k = s.k; p = mp.mpf(1)
        for i in range(k):
            cols = [(i + j) % (2*k) for j in range(k)]
            p *= mp.det(mp.matrix([[C[r, c] for c in cols] for r in range(k)]))
        return p
    def corr(s, net, J):
        t = [mp.tanh(j) for j in J]; num = {}; Z = mp.mpf(0)
        for mask, key in net.subs:
            w = mp.mpf(1)
            for i in range(len(net.edges)):
                if mask >> i & 1: w *= t[i]
            if key is None: Z += w
            else: num[key] = num.get(key, mp.mpf(0)) + w
        return [num.get(p, mp.mpf(0)) / Z for p in s.P]
    def omega(s, net, J):
        m = s.corr(net, J); D = dmat(lambda JJ: s.corr(net, JJ), J, len(s.P))
        return s.rhoH(m) * abs(mp.det(D)) / abs(s.PiM(m))
def find_tops(k, tree, want=3, seed=0):
    nodes = sorted({v for e in tree for v in e}, key=str); have = {frozenset(e) for e in tree}
    cand = [e for e in itertools.combinations(nodes, 2) if frozenset(e) not in have]
    need = k*(k-1)//2 - len(tree); found = []
    rnd = random.Random(seed); combos = list(itertools.combinations(cand, need)); rnd.shuffle(combos)
    for ex in combos:
        E = tree + list(ex)
        try: t = Net(k, E).tau()
        except Exception: continue
        if xing(t) == k*(k-1)//2: found.append(list(ex))
        if len(found) == want: break
    return found
def J_A(model, tree, extra, Jt, eps):
    net = Net(model.k, tree + extra)
    J = list(Jt) + [eps] * len(extra)
    car = mp.mpf(1)
    for j in Jt: car *= 2 * mp.coth(2*j)
    return eps ** len(extra) * model.omega(net, J) / car
if __name__ == "__main__":
    out = {}
    trees = {4: {"((12)(34))": [(1, 'a'), (2, 'a'), ('a', 'b'), (3, 'b'), (4, 'b')],
                 "((23)(41))": [(2, 'a'), (3, 'a'), ('a', 'b'), (4, 'b'), (1, 'b')]}}
    def tree5(x):
        l = [(x-1+j) % 5 + 1 for j in range(5)]
        return [(l[0], 'v'), ('u', 'v'), ('w', 'v'), (l[1], 'u'), (l[2], 'u'), (l[3], 'w'), (l[4], 'w')]
    trees[5] = {f"T{x}": tree5(x) for x in range(1, 6)}
    for k in (4, 5):
        M = Model(k)
        for name, tr in trees[k].items():
            tops = find_tops(k, tr, want=2)
            print(f"k={k} {name}: top completions found {tops}")
            out[f"{k}:{name}"] = {"tops": [[list(map(str, e)) for e in t] for t in tops]}
    json.dump(out, open("scripts/ht5g_tops.json", "w"), indent=1)
