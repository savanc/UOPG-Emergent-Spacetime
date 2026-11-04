"""H-T5g stage 2: vertex-chain rule V and pairwise rule P on the 5 n=10 tree tiles (prereg amendment S2)."""
import itertools, random, json, functools
from fractions import Fraction as F
import mpmath as mp
print = functools.partial(print, flush=True)
FC = {"__name__": "f"}; exec(open("scripts/ht5f_carrier.py").read().split("out = {}")[0], FC)
G10 = {"__name__": "x"}; exec(open("scripts/ht5d_spurious.py").read().split('\nif __name__')[0], G10)
mp.mp.dps = 60
def inner(net): return sorted({v for e in net.edges for v in e if not isinstance(v, int)}, key=str)
def connected(net, S):
    S = set(S)
    if len(S) <= 1: return True
    adj = {x: {y for e in net.edges for y in e if x in e and y in S and y != x} for x in S}
    seen = {next(iter(S))}; st = list(seen)
    while st:
        for y in adj[st.pop()]:
            if y not in seen: seen.add(y); st.append(y)
    return seen == S
def Jrule(net, J, rule):
    tot = mp.mpf(0)
    for r in range(len(inner(net)) + 1):
        for S in itertools.combinations(inner(net), r):
            if rule == "P" and any(len(c) > 2 and connected(net, c) for c in [S]): continue
            p = mp.mpf(1)
            for i, e in enumerate(net.edges):
                if len(set(e) & set(S)) == 1: p *= mp.sech(2*J[i])
            tot += p
    return tot
def tree5(x):
    l = [(x-1+j) % 5 + 1 for j in range(5)]
    return [(l[0], 'v'), ('u', 'v'), ('w', 'v'), (l[1], 'u'), (l[2], 'u'), (l[3], 'w'), (l[4], 'w')]
nets = {f"T{x}": G10["Net"](5, tree5(x)) for x in range(1, 6)}; nets["R1b(non-tree,diag)"] = G10["NETS"]["R1b=T5"]
zs = {"T1": "T1", "T2": "T2", "T3": "T3", "T4": "T4", "T5": "R1b=T5", "R1b(non-tree,diag)": "R1b=T5"}
rng = random.Random(2026); res = {"V": [], "P": []}; out = {}
for name, net in nets.items():
    cls = G10["vanishing_classes"](G10["ZS"][zs[name]]); P = G10["PAIRS"]
    for _ in range(8):
        t = [F(rng.randint(50, 950), 1000) for _ in net.edges]
        m, C, Y = G10["forward"](net, t); fb = G10["fiber"](Y); x = G10["fibcoords"](fb, [m[p] for p in P])
        Ores = G10["tile_form"](fb, x, cls)[0]
        J = [mp.atanh(mp.mpf(q.numerator)/q.denominator) for q in t]
        D = FC["jac"](lambda JJ: G10["Phi"](FC["corr_mp"](net, [mp.tanh(j) for j in JJ], P)), J, 7, h=mp.mpf(10)**-25) if "h" in FC["jac"].__code__.co_varnames else FC["jac"](lambda JJ: G10["Phi"](FC["corr_mp"](net, [mp.tanh(j) for j in JJ], P)), J, 7)
        car = mp.mpf(1)
        for j in J: car *= 2*mp.coth(2*j)
        R = abs(Ores / (car / mp.det(D)))
        for rule in "VP": res[rule].append((name, R / Jrule(net, J, rule)))
for rule, L in res.items():
    for scope, names in [("trees", [f"T{x}" for x in range(1, 6)]), ("R1b diag", ["R1b(non-tree,diag)"])]:
        v = [r for n, r in L if n in names]; sp = (max(v)-min(v))/max(v)
        per = {n: mp.nstr(sum(r for nn, r in L if nn == n)/8, 22) for n in names}
        print(f"rule {rule} [{scope}]: spread {mp.nstr(sp, 3)}; per-tile means {per}")
        out[f"{rule}:{scope}"] = dict(spread=mp.nstr(sp, 5), means=per)
json.dump(out, open("scripts/ht5g_stage2.json", "w"), indent=1)
