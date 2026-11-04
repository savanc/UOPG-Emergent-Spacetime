"""H-T5f Part A POST-HOC diagnostics (not prereg verdicts): per-tile spreads and V-face J variants."""
import functools, itertools, random
exec(open("scripts/ht5f_carrier.py").read().split("out = {}")[0])
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 40
def Jvar(net, J, mode):
    inner = sorted({v for e in net.edges for v in e if not isinstance(v, int)}, key=str); tot = mp.mpf(0)
    for r in range(len(inner)+1):
        for S in itertools.combinations(inner, r):
            p = mp.mpf(1)
            for i, e in enumerate(net.edges):
                c = len(set(e) & set(S))
                if c == 0: continue
                if c == 2 and mode == "omit": continue
                p *= mp.sech(2*J[i]) ** (c if mode == "twice" else 1)
            tot += p
    return tot
G8 = {"__name__": "x"}; exec(open("scripts/ht5b_spurious.py").read().split("Zs = {")[0], G8)
Net = G8["Net"]; P8 = G8["PAIRS"]; rng = random.Random(77)
trees8 = {"((12)(34))": [(1, 'a'), (2, 'a'), ('a', 'b'), (3, 'b'), (4, 'b')], "((23)(41))": [(2, 'a'), (3, 'a'), ('a', 'b'), (4, 'b'), (1, 'b')]}
res = {m: [] for m in ("none", "once", "omit", "twice")}
for name, E in trees8.items():
    net = Net(4, E)
    for _ in range(10):
        t = [F(rng.randint(50, 950), 1000) for _ in E]
        m, C, Y = G8["forward"](net, t); (m0, v), _ = G8["fiber"](Y)
        i0 = next(i for i in range(6) if v[i] != 0); s = (m[P8[i0]] - m0[i0]) / v[i0]
        M0 = [mp.mpf(q.numerator)/q.denominator for q in m0]; V = [mp.mpf(q.numerator)/q.denominator for q in v]
        Ores, _ = G8["residue"](M0, V, mp.mpf(s.numerator)/s.denominator)
        J = [mp.atanh(mp.mpf(q.numerator)/q.denominator) for q in t]
        D = jac(lambda JJ: G8["Phi"](corr_mp(net, [mp.tanh(j) for j in JJ], P8)), J, 5)
        car = mp.mpf(1)
        for j in J: car *= 2*mp.coth(2*j)
        R = abs(Ores / (car / mp.det(D)))
        res["none"].append((name, R))
        for mode in ("once", "omit", "twice"): res[mode].append((name, R / Jvar(net, J, mode)))
for mode, L in res.items():
    vals = [x for _, x in L]; sp_ = (max(vals)-min(vals))/max(vals)
    per = {n: (lambda v: mp.nstr((max(v)-min(v))/max(v), 3))([x for nn, x in L if nn == n]) for n in trees8}
    print(f"n=8 mode {mode}: overall spread {mp.nstr(sp_,3)}, per tile {per}, mean {mp.nstr(sum(vals)/len(vals),10)}")
# ---- n = 10 test of the n=8-fitted 'omit' rule (rule fixed from n=8 before this block was run) ----
G10 = {"__name__": "x"}; exec(open("scripts/ht5d_spurious.py").read().split('\nif __name__')[0], G10)
rng = random.Random(78); res10 = {m: [] for m in ("none", "once", "omit")}
for name in ["T1", "T2", "T3", "T4", "R1b=T5"]:
    net = G10["NETS"][name]; cls = G10["vanishing_classes"](G10["ZS"][name]); PAIRS = G10["PAIRS"]
    for _ in range(6):
        t = [F(rng.randint(50, 950), 1000) for _ in net.edges]
        m, C, Y = G10["forward"](net, t); fb = G10["fiber"](Y); x = G10["fibcoords"](fb, [m[p] for p in PAIRS])
        Ores = G10["tile_form"](fb, x, cls)[0]
        J = [mp.atanh(mp.mpf(q.numerator)/q.denominator) for q in t]
        D = jac(lambda JJ: G10["Phi"](corr_mp(net, [mp.tanh(j) for j in JJ], PAIRS)), J, 7)
        car = mp.mpf(1)
        for j in J: car *= 2*mp.coth(2*j)
        R = abs(Ores / (car / mp.det(D)))
        res10["none"].append((name, R))
        for mode in ("once", "omit"): res10[mode].append((name, R / Jvar(net, J, mode)))
for mode, L in res10.items():
    vals = [x for _, x in L]
    print(f"n=10 mode {mode}: overall spread {mp.nstr((max(vals)-min(vals))/max(vals),3)}, mean {mp.nstr(sum(vals)/len(vals),12)}")
