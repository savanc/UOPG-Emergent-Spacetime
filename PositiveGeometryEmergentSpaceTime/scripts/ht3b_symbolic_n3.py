"""H-T3b (a): exact symbolic n = 3 loop factors and the star-triangle identity (sympy).
Lee's measure in gauge G2 (odd columns = I): C' = (I | c) with c c^T = I (eta = +,-,...), so the delta-measure is
Haar on O(3) = |det[(c^T d_a c)_{ij}]_{a,(i<j)}| up to a constant. Prereg: prereg/H-T3b-loop-factor-2026-10-12.md."""
import sympy as sp
t1, t2, t3 = sp.symbols('t1 t2 t3', positive=True)
def gp(k, m):
    C = sp.zeros(k, 2*k)
    for i in range(1, k+1):
        for j in range(1, k+1):
            if i == j: C[i-1, 2*i-2] = C[i-1, 2*i-1] = 1
            else:
                v = (-1)**(i + j + (1 if i < j else 0)) * m[(min(i, j), max(i, j))]
                C[i-1, 2*j-2] = v; C[i-1, 2*j-1] = -v
    return C
def lee_over_carrier(m, ts):
    k = 3; C = gp(k, m); A = C[:, [0, 2, 4]]; Cp = sp.simplify(A.inv() * C); c = Cp[:, [1, 3, 5]]
    assert sp.simplify(c * c.T - sp.eye(3)) == sp.zeros(3), "G2 block not orthogonal"
    rows = []
    for t in ts:
        X = sp.simplify(c.T * c.diff(t) * (1 - t**2))       # d/dL = (1 - t^2) d/dt
        rows.append([X[0, 1], X[0, 2], X[1, 2]])
    haar = sp.Matrix(rows).det()
    N = 6; M = sp.Integer(1)
    for l in (1, 2, 3):                                    # j = 1: M1 M2 M3, consecutive (cyclic) columns
        M *= Cp[:, [(l-1+q) % N for q in range(3)]].det()
    carrier = sp.prod([(1 + t**2)/t for t in ts])          # prod 2 coth 2L
    return sp.factor(sp.simplify(haar / M / carrier))
sech2 = lambda t: (1 - t**2)/(1 + t**2); tanh2 = lambda t: 2*t/(1 + t**2)
# Y network: m_ij = t_i t_j
RY = lee_over_carrier({(1, 2): t1*t2, (1, 3): t1*t3, (2, 3): t2*t3}, [t1, t2, t3])
JY = 1 + sech2(t1)*sech2(t2)*sech2(t3)
print("Y:  R_Y / (1 + prod sech 2L) =", sp.simplify(RY / JY))
# Delta network: u_ij = tanh K_ij (here t1=u12, t2=u13, t3=u23)
Z = 1 + t1*t2*t3
mD = {(1, 2): (t1 + t2*t3)/Z, (1, 3): (t2 + t1*t3)/Z, (2, 3): (t3 + t1*t2)/Z}
RD = lee_over_carrier(mD, [t1, t2, t3])
JD = 1 + tanh2(t1)*tanh2(t2)*tanh2(t3)
print("Delta: R_D / (1 + prod tanh 2K) =", sp.simplify(RD / JD))
# Star-triangle identity, parametrised by the Delta side u = (t1,t2,t3):
u = [t1, t2, t3]; m12, m13, m23 = mD[(1, 2)], mD[(1, 3)], mD[(2, 3)]
T2 = [m12*m13/m23, m12*m23/m13, m13*m23/m12]            # t_i^2 of the equivalent star
P2 = m12*m13*m23                                         # (t1 t2 t3)^2
# det(dm_Y/dt) * prod (dt/dlog sinh2L) = -2 t1t2t3 * prod t(1-t^2)/(1+t^2) = -2 P^2 prod (1-t^2)/(1+t^2)
starside = -2*P2*sp.prod([(1 - T)/(1 + T) for T in T2])
JmD = sp.Matrix([[sp.diff(mm, x) for x in u] for mm in (m12, m13, m23)]).det()
triside = JmD * sp.prod([x*(1 - x**2)/(1 + x**2) for x in u])   # det(dm_D/du) * prod du/dlog sinh2K
# det(d log sinh2K / d log sinh2L) = starside / triside
JY_u = 1 + sp.prod([(1 - T)/(1 + T) for T in T2])
identity = sp.simplify(starside/triside + JY_u/JD)
print("star-triangle: det(dlog sinh2K/dlog sinh2L) + J_Y/J_Delta =", identity)
