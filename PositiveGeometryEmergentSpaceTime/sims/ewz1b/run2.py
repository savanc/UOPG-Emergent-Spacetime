from ewz1b import *
import sys
one={lam3:1,a:1,gs:1,lam4:1,b:1}; z={kk:0 for kk in k}
W=lambda i:(Epol(i),P[i]); H=lambda i:(Epol(i,True),P[i])
def A4(ext,**kw): r,ct=amp(ext,**kw); return r+ct
def HZ(expr,k13,extra={}):
    expr=expr.subs({ee[(1,3)]:0,ep[(1,3)]:0,ep[(3,1)]:0}).subs(extra)
    tsol=S.solve(S.Eq(u-m2(1)-m2(3), k13),t)[0]
    return S.factor(S.simplify(expr.subs(t,tsol).subs(extra)))
gen=[W(1),W(2),W(3),W(4)]
print('CONTROL-0 massless YM on HZ:',HZ(A4(gen).subs(one),0,z))
m=S.Symbol('m',positive=True); km={k[0]:m,k[1]:m,k[2]:-m,k[3]:-m}
Ap=HZ(A4(gen,prop='proca',Mint=m).subs(one),0,km)
tgt=m**2/(s-m**2)*(ee[(1,2)]*ee[(3,4)]-ee[(2,3)]*ee[(1,4)])
print('CONTROL-1 Proca uniform-m on HZ:',Ap); print('   minus CGW eq53 (up to overall sign):',S.simplify(Ap-tgt),'|',S.simplify(Ap+tgt))
print('CONTROL-2 SSB same spectrum (k=m,m,-m,-m) on HZ:',HZ(A4(gen).subs(one),2*k[0]*k[2],km))
print('CONTROL-2b SSB generic vevs on HZ:',HZ(A4(gen).subs(one),2*k[0]*k[2]))
# massive physical h in t-channel / external: break by m_h -- not in 5D structure; skip here (see EW-Z1 scalar gate)
def solve_forced(expr,label,unknowns):
    num=S.expand(S.numer(S.together(expr)))
    vs=[v for v in ee.values()]+[v for v in ep.values() if v is not None]+[s]+list(k)+list(E5)
    co=[c for c in S.Poly(num,*vs).coeffs()]
    print(label,'nonzero-coeff eqs:',len(co),' solutions:',S.solve(co,unknowns,dict=True))
solve_forced(HZ(A4(gen),2*k[0]*k[2]),'FORCE WW->WW (generic vevs):',[a,lam4])
# WW -> hh, ordering [W1 W2 h3 h4]: k3=k4=0 => k2=-k1 ; add h^3 s-channel: a*(e1.e2)(k1-k2) * kap3*E5_3*E5_4 / s  (m_h=0)
kh={k[2]:0,k[1]:-k[0]}
ext=[W(1),W(2),H(3),H(4)]
r,ct=amp(ext); Aw=r+ct + (-1)*(a*ee[(1,2)]*(k[0]-k[1]))*kap3*E5[2]*E5[3]/s
print('WWhh SM/SSB [W W h h] on HZ:',HZ(Aw.subs(one).subs(kap3,0),0,kh))
solve_forced(HZ(Aw,0,kh),'FORCE [W W h h]:',[a,gs,b,kap3])
# ordering [W1 h2 W3 h4]: k2=k4=0, k3=-k1
kh2={k[1]:0,k[2]:-k[0]}
ext=[W(1),H(2),W(3),H(4)]
r,ct=amp(ext); Aw2=r+ct
print('WhWh SSB on HZ:',HZ(Aw2.subs(one),2*k[0]*k[2],kh2))
solve_forced(HZ(Aw2,2*k[0]*k[2],kh2),'FORCE [W h W h]:',[a,gs,b])
# neutral-boson channel (CGW toy has massless diagonal photons, no massive Z): [W1 W2 g3 g4] with k3=k4=0
ext=[W(1),W(2),W(3),W(4)]
print('WW->gamma gamma [W W g g] SSB on HZ:',HZ(A4(ext).subs(one),0,kh))
solve_forced(HZ(A4(ext),0,kh),'FORCE [W W g g]:',[a,lam4])
