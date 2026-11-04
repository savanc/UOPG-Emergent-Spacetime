"""H-T5g: keep only top completions whose 3 extra edges EACH give a simple pole (per-edge eps scaling test)."""
import json
exec(open("scripts/ht5g_routeA.py").read().split('\nif __name__')[0])
def tree5(x):
    l = [(x-1+j) % 5 + 1 for j in range(5)]
    return [(l[0], 'v'), ('u', 'v'), ('w', 'v'), (l[1], 'u'), (l[2], 'u'), (l[3], 'w'), (l[4], 'w')]
M = Model(5); setprec(40, 15); tops = json.load(open("scripts/ht5g_tops.json"))
for x in range(1, 6):
    tr = tree5(x); good = []; Jt = [mp.mpf(0.3)+mp.mpf(i)/10 for i in range(7)]
    for ex in find_tops(5, tr, want=60, seed=x):
        net = Net(5, tr + ex); e8, e9 = mp.mpf(10)**-8, mp.mpf(10)**-9
        base = e8**3 * M.omega(net, Jt + [e8]*3); ok = True
        for j in range(3):
            ee = [e8]*3; ee[j] = e9
            v = e8**2 * e9 * M.omega(net, Jt + ee)
            if abs(v/base - 1) > 1e-6: ok = False
        if ok: good.append(ex)
        if len(good) == 4: break
    tops[f"5:T{x}"] = {"tops": [[list(map(str, e)) for e in t] for t in good]}
json.dump(tops, open("scripts/ht5g_tops.json", "w"), indent=1)
