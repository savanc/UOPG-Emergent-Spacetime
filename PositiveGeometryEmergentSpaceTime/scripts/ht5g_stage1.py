"""H-T5g stage 1: route A (two top completions, two eps, two h) vs H-T5f residue ratio R_res, n=8 and n=10."""
import json, random, functools
from fractions import Fraction as F
import mpmath as mp
print = functools.partial(print, flush=True)
A = {"__name__": "a"}; exec(open("scripts/ht5g_routeA.py").read().split('\nif __name__')[0], A)
F5 = {"__name__": "f"}; exec(open("scripts/ht5f_carrier.py").read().split("out = {}")[0], F5)
tops = json.load(open("scripts/ht5g_tops.json"))
def parse(e): return tuple(int(x) if x.isdigit() else x for x in e)
out = {}; rng = random.Random(4)
def tree5(x):
    l = [(x-1+j) % 5 + 1 for j in range(5)]
    return [(l[0], 'v'), ('u', 'v'), ('w', 'v'), (l[1], 'u'), (l[2], 'u'), (l[3], 'w'), (l[4], 'w')]
trees = {4: {"((12)(34))": [(1, 'a'), (2, 'a'), ('a', 'b'), (3, 'b'), (4, 'b')], "((23)(41))": [(2, 'a'), (3, 'a'), ('a', 'b'), (4, 'b'), (1, 'b')]},
         5: {f"T{x}": tree5(x) for x in range(1, 6)}}
# H-T5f residue machinery
mp.mp.dps = 40
G10 = {"__name__": "x"}; exec(open("scripts/ht5d_spurious.py").read().split('\nif __name__')[0], G10)
G8 = {"__name__": "x"}; exec(open("scripts/ht5b_spurious.py").read().split("Zs = {")[0], G8)
name10 = {"T1": "T1", "T2": "T2", "T3": "T3", "T4": "T4", "T5": "R1b=T5"}
def R_res(k, name, tree, t):
    mp.mp.dps = 40
    if k == 5:
        net = G10["NETS"][name10[name]]
        if name == "T5": net = G10["Net"](5, tree)  # tree form of the same cell as H-T5d's R1b (zero pattern ZS[R1b=T5])
        assert sorted(map(str, net.edges)) == sorted(map(str, tree))
        cls = G10["vanishing_classes"](G10["ZS"][name10[name]]); P = G10["PAIRS"]
        m, C, Y = G10["forward"](net, t); fb = G10["fiber"](Y); x = G10["fibcoords"](fb, [m[p] for p in P])
        Ores = G10["tile_form"](fb, x, cls)[0]; Phi = G10["Phi"]; nch = 7
    else:
        net = G8["Net"](4, tree); P = G8["PAIRS"]
        m, C, Y = G8["forward"](net, t); (m0, v), _ = G8["fiber"](Y)
        i0 = next(i for i in range(6) if v[i] != 0); s = (m[P[i0]] - m0[i0]) / v[i0]
        M0 = [mp.mpf(q.numerator)/q.denominator for q in m0]; V = [mp.mpf(q.numerator)/q.denominator for q in v]
        Ores, _ = G8["residue"](M0, V, mp.mpf(s.numerator)/s.denominator); Phi = G8["Phi"]; nch = 5
    J = [mp.atanh(mp.mpf(q.numerator)/q.denominator) for q in t]
    D = F5["jac"](lambda JJ: Phi(F5["corr_mp"](net, [mp.tanh(j) for j in JJ], P)), J, nch)
    car = mp.mpf(1)
    for j in J: car *= 2*mp.coth(2*j)
    return abs(Ores / (car / mp.det(D)))
for k in (4, 5):
    M = A["Model"](k); res = []
    for name, tree in trees[k].items():
        comps = [[parse(e) for e in ex] for ex in tops[f"{k}:{name}"]["tops"]]
        for _ in range(4):
            t = [F(rng.randint(100, 900), 1000) for _ in tree]
            Jt = None
            vals = {}
            for ci, ex in enumerate(comps):
                for (dps, h, eps) in ([(80, 35, 25), (80, 25, 25), (80, 35, 30)] if ci == 0 else [(80, 35, 25)]):
                    A["setprec"](dps, h); Jt = [mp.atanh(mp.mpf(q.numerator)/q.denominator) for q in t]
                    try: vals[(ci, h, eps)] = A["J_A"](M, tree, ex, Jt, mp.mpf(10)**(-eps))
                    except ZeroDivisionError: vals[(ci, h, eps)] = mp.nan  # chart degenerate at this point
            fin = {kk: v for kk, v in vals.items() if mp.isfinite(v)}
            # consensus base: the value agreeing (rel < 1e-15) with the most other route-A evaluations
            base = max(fin.values(), key=lambda b: sum(abs(v/b - 1) < mp.mpf(10)**-15 for v in fin.values()))
            nagree = sum(abs(v/base - 1) < mp.mpf(10)**-15 for v in fin.values())
            agree = {str(key): mp.nstr(abs(v/base - 1), 3) for key, v in vals.items()}
            rr = R_res(k, name, tree, t)
            mp.mp.dps = 80
            res.append((name, base, rr, rr / base, agree))
            print(f"k={k} {name}: J_A={mp.nstr(base, 20)}  R_res/J_A={mp.nstr(rr/base, 20)}  route-A consensus {nagree}/{len(vals)} {agree}")
    ratios = [r[3] for r in res]; spread = (max(ratios) - min(ratios)) / max(ratios)
    print(f"k={k}: R_res/J_A spread {mp.nstr(spread, 3)}, mean {mp.nstr(sum(ratios)/len(ratios), 20)}")
    out[k] = dict(spread=mp.nstr(spread, 5), mean=mp.nstr(sum(ratios)/len(ratios), 25),
                  rows=[(r[0], mp.nstr(r[1], 30), mp.nstr(r[2], 25), mp.nstr(r[3], 25), r[4]) for r in res])
json.dump(out, open("scripts/ht5g_stage1.json", "w"), indent=1, default=str)
