"""H-T3 (c): pull back Lee's ABJM measure (via the GP map) to Ising couplings and compare with the
carrier omega_I = prod_e dlog sinh(2J_e). Prereg + Amendment A1. mpmath, 40 digits; coarea formula."""
import mpmath as mp, itertools, random
mp.mp.dps = 40; random.seed(7)

def gp(k, m):  # m: dict (i,j) i<j -> correlation; returns k x 2k mp.matrix (GP eq. 2.4)
    C = mp.matrix(k, 2*k)
    for i in range(1, k+1):
        for j in range(1, k+1):
            if i == j: C[i-1, 2*i-2] = C[i-1, 2*i-1] = 1
            else:
                v = (-1)**(i + j + (1 if i < j else 0)) * m[(min(i, j), max(i, j))]
                C[i-1, 2*j-2] = v; C[i-1, 2*j-1] = -v
    return C
def minor(C, cols): return mp.det(mp.matrix([[C[r, c-1] for c in cols] for r in range(C.rows)]))
def gauge(C, S):
    A = mp.matrix([[C[r, c-1] for c in S] for r in range(C.rows)]); return mp.inverse(A) * C
def eta(N): return [(-1)**j for j in range(N)]  # +,-,+,- (0-based j)
def density(Jfun, k, S, jj, J):
    """Lee measure density in coupling coordinates, gauge columns S = identity, minors M_jj..M_{jj+k-1}."""
    N = 2*k; free = [c for c in range(1, N+1) if c not in S]; et = eta(N)
    def cvec(Jv):
        G = gauge(gp(k, Jfun(Jv)), S); return [G[r, c-1] for r in range(k) for c in free]
    d = len(J)
    Jac = mp.matrix(k*k, d)
    for a in range(d):
        def comp(t, a=a):
            Jv = list(J); Jv[a] = t; return cvec(Jv)
        col = [mp.diff(lambda t, i=i: comp(t)[i], J[a]) for i in range(k*k)]
        for i in range(k*k): Jac[i, a] = col[i]
    # constraint F(c) = sum_cols eta_col * C_r,col C_s,col (r<=s), with C = (I on S | c on free)
    c0 = cvec(J); cm = {(r, free[q]): c0[r*k+q] for r in range(k) for q in range(k)}
    DF = mp.matrix(k*(k+1)//2, k*k); row = 0
    for r in range(k):
        for s in range(r, k):
            for q in range(k):
                col = free[q]; e = et[col-1]
                # d/dc_{r,col}: e*c_{s,col} (+ e*c_{r,col} if r==s handled by factor)
                DF[row, r*k+q] += e * cm[(s, col)]
                DF[row, s*k+q] += e * cm[(r, col)]
            row += 1
    G = gauge(gp(k, Jfun(J)), S)
    Mprod = mp.mpf(1)
    for l in range(jj, jj+k):
        cols = [((l-1+t) % N) + 1 for t in range(k)]
        # consecutive minor with cyclic sign: columns wrap; keep as determinant in listed (wrapped) order
        Mprod *= minor(G, cols)
    return mp.sqrt(mp.det(Jac.T*Jac)) / mp.sqrt(mp.det(DF*DF.T)) / abs(Mprod)
def carrier(J): 
    p = mp.mpf(1)
    for x in J: p *= 2*mp.coth(2*x)
    return p
nets = {
    "k=2 one edge":   (2, lambda J: {(1, 2): mp.tanh(J[0])}, 1),
    "k=3 Y (star)":   (3, lambda J: (lambda t: {(1, 2): t[0]*t[1], (1, 3): t[0]*t[2], (2, 3): t[1]*t[2]})([mp.tanh(x) for x in J]), 3),
    "k=3 Delta":      (3, lambda J: (lambda u: (lambda Z: {(1, 2): (u[0]+u[1]*u[2])/Z, (1, 3): (u[1]+u[0]*u[2])/Z, (2, 3): (u[2]+u[0]*u[1])/Z})(1+u[0]*u[1]*u[2]))([mp.tanh(x) for x in J]), 3),
}
for name, (k, Jfun, d) in nets.items():
    for gname, S in [("G1 first-k", list(range(1, k+1))), ("G2 odd", list(range(1, 2*k, 2)))]:
        for jj in (1, 2):
            pts = [[mp.mpf(random.uniform(0.2, 1.5)) for _ in range(d)] for _ in range(4)]
            Rs = [density(Jfun, k, S, jj, J) / carrier(J) for J in pts]
            ratios = [R / Rs[0] for R in Rs]
            const = all(abs(r - 1) < mp.mpf(10)**-20 for r in ratios)
            print(f"{name:14s} {gname:10s} j={jj}: R = {[mp.nstr(R, 12) for R in Rs]}  constant={const}")
            if not const and k == 3:
                for J in pts[:2]:
                    t = [mp.tanh(x) for x in J]; c = [mp.tanh(2*x) for x in J]; s = [mp.sech(2*x) for x in J]
                    R = density(Jfun, k, S, jj, J) / carrier(J)
                    cand = {"1+c1c2c3": 1+c[0]*c[1]*c[2], "1-c1c2c3": 1-c[0]*c[1]*c[2], "1+s1s2s3": 1+s[0]*s[1]*s[2],
                            "1-s1s2s3": 1-s[0]*s[1]*s[2], "1+t1t2t3": 1+t[0]*t[1]*t[2], "(1+t1t2t3)^2": (1+t[0]*t[1]*t[2])**2}
                    print("      J=", [mp.nstr(x, 6) for x in J], " R/cand:", {kk: mp.nstr(R/v, 12) for kk, v in cand.items()})
