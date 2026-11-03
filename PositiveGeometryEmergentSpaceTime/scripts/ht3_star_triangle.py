"""H-T3 (c): Ising star-triangle and the carrier. Given star couplings L, find triangle couplings K with the same
boundary correlations; log-Jacobian of (sinh 2L) -> (sinh 2K); compare with the loop factors found in
ht3_abjm_measure.py (J_Y = 1 + prod sech 2L, J_Delta = 1 + prod tanh 2K)."""
import mpmath as mp, random
mp.mp.dps = 40; random.seed(5)
def corrY(L):
    t = [mp.tanh(x) for x in L]; return [t[0]*t[1], t[0]*t[2], t[1]*t[2]]
def corrD(K):
    u = [mp.tanh(x) for x in K]; Z = 1 + u[0]*u[1]*u[2]
    return [(u[0]+u[1]*u[2])/Z, (u[1]+u[0]*u[2])/Z, (u[2]+u[0]*u[1])/Z]   # K = (K12, K13, K23)
def y2d(L):
    m = corrY(L)
    return mp.findroot(lambda a, b, c: [x - y for x, y in zip(corrD([a, b, c]), m)], [mp.mpf(0.5)]*3)
for _ in range(4):
    L = [mp.mpf(random.uniform(0.4, 1.4)) for _ in range(3)]
    K = list(y2d(L))
    # log-Jacobian d log sinh 2K / d log sinh 2L
    def F(i, j):
        def g(x):
            Lv = list(L); Lv[j] = x; return mp.log(mp.sinh(2*y2d(Lv)[i]))
        return mp.diff(g, L[j]) / (2*mp.coth(2*L[j]))
    Jm = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3): Jm[i, j] = F(i, j)
    d = mp.det(Jm)
    JY = 1 + mp.sech(2*L[0])*mp.sech(2*L[1])*mp.sech(2*L[2])
    JD = 1 + mp.tanh(2*K[0])*mp.tanh(2*K[1])*mp.tanh(2*K[2])
    print("L=", [mp.nstr(x, 6) for x in L], "K=", [mp.nstr(x, 6) for x in K],
          " det(dlog sinh2K/dlog sinh2L) =", mp.nstr(d, 15), "  J_Y/J_Delta =", mp.nstr(JY/JD, 15))
