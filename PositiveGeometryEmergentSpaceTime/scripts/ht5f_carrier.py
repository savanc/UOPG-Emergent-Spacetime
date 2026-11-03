"""H-T5f Part A: tile form (residue of the Lee/HW top form) vs pushforward of the pure carrier prod 2coth2J dJ,
on tree Ising networks at n=8 (1-dim fiber residue, H-T5b code) and n=10 (3-dim Grothendieck residue, H-T5d code)."""
import itertools, json, functools, random, sys
from fractions import Fraction as F
import mpmath as mp
print = functools.partial(print, flush=True)
def corr_mp(net, t, PAIRS):
    num = {}; Z = mp.mpf(0)
    for mask, key in net.subs:
        w = mp.mpf(1)
        for i in range(len(net.edges)):
            if mask >> i & 1: w *= t[i]
        if key is None: Z += w
        else: num[key] = num.get(key, mp.mpf(0)) + w
    return [num.get(p, mp.mpf(0)) / Z for p in PAIRS]
def jac(fun, x, nout, h=mp.mpf(10)**-15):
    J = mp.matrix(nout, len(x))
    for a in range(len(x)):
        xp = list(x); xp[a] += h; xm = list(x); xm[a] -= h
        fp, fm = fun(xp), fun(xm)
        for r in range(nout): J[r, a] = (fp[r] - fm[r]) / (2*h)
    return J
def JC1(net, J):
    inner = sorted({v for e in net.edges for v in e if not isinstance(v, int)}, key=str)
    tot = mp.mpf(0)
    for r in range(len(inner) + 1):
        for S in itertools.combinations(inner, r):
            es = {i for i, e in enumerate(net.edges) if set(e) & set(S)}
            p = mp.mpf(1)
            for i in es: p *= mp.sech(2*J[i])
            tot += p
    return tot
def analyse(label, rows):
    R = [r[0] for r in rows]; R1 = [r[0] / r[1] for r in rows]
    spread = lambda v: (max(abs(x) for x in v) - min(abs(x) for x in v)) / max(abs(x) for x in v)
    print(f"{label}: |R| spread {mp.nstr(spread(R), 3)} (mean |R| {mp.nstr(sum(abs(x) for x in R)/len(R), 12)}); "
          f"|R/J_C1| spread {mp.nstr(spread(R1), 3)}")
    return spread(R), spread(R1)
out = {}
mp.mp.dps = 40
# ---------------- n = 10 ----------------
G10 = {"__name__": "x"}; exec(open("scripts/ht5d_spurious.py").read().split('\nif __name__')[0], G10)
rng = random.Random(31); rows10 = []; signs10 = {}
for name in ["T1", "T2", "T3", "T4", "R1b=T5"]:
    net = G10["NETS"][name]; cls = G10["vanishing_classes"](G10["ZS"][name]); PAIRS = G10["PAIRS"]
    for _ in range(8):
        t = [F(rng.randint(50, 950), 1000) for _ in net.edges]
        m, C, Y = G10["forward"](net, t); fb = G10["fiber"](Y)
        x = G10["fibcoords"](fb, [m[p] for p in PAIRS])
        Ores = G10["tile_form"](fb, x, cls)[0]
        J = [mp.atanh(mp.mpf(q.numerator) / q.denominator) for q in t]
        D = jac(lambda JJ: G10["Phi"](corr_mp(net, [mp.tanh(j) for j in JJ], PAIRS)), J, 7)
        car = mp.mpf(1)
        for j in J: car *= 2 * mp.coth(2*j)
        Ocar = car / mp.det(D)
        rows10.append((Ores / Ocar, JC1(net, J))); signs10.setdefault(name, set()).add((int(mp.sign(Ores / Ocar)), int(mp.sign(mp.det(D))), int(mp.sign(Ores))))
s0, s1 = analyse("n=10", rows10); print("   signs (sign R, sign det dPhi/dJ, sign Omega_res):", signs10)
out["n10"] = dict(spread_R=mp.nstr(s0, 5), spread_RJ=mp.nstr(s1, 5), meanR=mp.nstr(sum(abs(r[0]) for r in rows10)/len(rows10), 20),
                  signs={k: sorted(v) for k, v in signs10.items()})
# ---------------- n = 8 ----------------
G8 = {"__name__": "x"}; exec(open("scripts/ht5b_spurious.py").read().split("Zs = {")[0], G8)
Net = G8["Net"]; PAIRS8 = G8["PAIRS"]; rows8 = []; signs8 = {}
trees8 = {"((12)(34))": [(1, 'a'), (2, 'a'), ('a', 'b'), (3, 'b'), (4, 'b')], "((23)(41))": [(2, 'a'), (3, 'a'), ('a', 'b'), (4, 'b'), (1, 'b')]}
for name, E in trees8.items():
    net = Net(4, E)
    for _ in range(8):
        t = [F(rng.randint(50, 950), 1000) for _ in E]
        m, C, Y = G8["forward"](net, t); (m0, v), _ = G8["fiber"](Y)
        # exact s with m = m0 + s v
        i0 = next(i for i in range(6) if v[i] != 0); s = (m[PAIRS8[i0]] - m0[i0]) / v[i0]
        assert all(m0[i] + s * v[i] == m[p] for i, p in enumerate(PAIRS8))
        M0 = [mp.mpf(q.numerator) / q.denominator for q in m0]; V = [mp.mpf(q.numerator) / q.denominator for q in v]
        Ores, dP = G8["residue"](M0, V, mp.mpf(s.numerator) / s.denominator)
        J = [mp.atanh(mp.mpf(q.numerator) / q.denominator) for q in t]
        D = jac(lambda JJ: G8["Phi"](corr_mp(net, [mp.tanh(j) for j in JJ], PAIRS8)), J, 5)
        car = mp.mpf(1)
        for j in J: car *= 2 * mp.coth(2*j)
        Ocar = car / mp.det(D)
        rows8.append((Ores / Ocar, JC1(net, J))); signs8.setdefault(name, set()).add((int(mp.sign(Ores / Ocar)), int(mp.sign(mp.det(D))), int(mp.sign(Ores))))
s0, s1 = analyse("n=8", rows8); print("   signs:", signs8)
out["n8"] = dict(spread_R=mp.nstr(s0, 5), spread_RJ=mp.nstr(s1, 5), meanR=mp.nstr(sum(abs(r[0]) for r in rows8)/len(rows8), 20),
                 signs={k: sorted(v) for k, v in signs8.items()})
json.dump(out, open("scripts/ht5f_carrier.json", "w"), indent=1, default=str)
