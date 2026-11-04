from ewz1b import *
c=S.Symbol('c'); one={lam3:1,a:1,gs:1,lam4:1,b:1}
W=lambda i:(Epol(i),P[i])
def full(ext,**kw):
    r,ct=amp(ext,**kw); return r+c*ct
# 1) fix contact normalisation by massless gauge invariance (e1 -> p1)
z={kk:0 for kk in k}
ext=[(P[1],P[1]),W(2),W(3),W(4)]
A=S.together(full(ext).subs(one).subs(z)); num=S.expand(S.numer(A))
sol=S.solve(S.Poly(num,*[v for v in ee.values()]+[v for v in ep.values() if v is not None]).coeffs(),c); print('contact c =',sol)
cv=sol[c] if isinstance(sol,dict) else sol[0]
def A4(ext,**kw): r,ct=amp(ext,**kw); return r+cv*ct
# HZ for [1234]: c~13 = -2K1.K3 = 0 ; e1.e3=e1.p3=e3.p1=0
def HZ(expr,k13):
    # -2(p1.p3) + 2 k1 k3 = 0 -> u - m1^2 - m3^2 = 2 k1 k3  (p1.p3 =(u-m1-m3)/2)
    expr=expr.subs({ee[(1,3)]:0,ep[(1,3)]:0,ep[(3,1)]:0})
    tsol=S.solve(S.Eq(u-m2(1)-m2(3), k13),t)[0]
    return S.simplify(S.factor(expr.subs(t,tsol)))
gen=[W(1),W(2),W(3),W(4)]
print('massless YM on HZ:',HZ(A4(gen).subs(one).subs(z),0))
# 2) CGW SSB (Coulomb branch, = 5D YM), generic vevs: K-additive masses, Feynman-'t Hooft incl Goldstone/h
Assb=A4(gen).subs(one)
print('SSB generic kappa on HZ (c~13=0):',HZ(Assb,2*k[0]*k[2]))
# gauge check SSB: E1 -> K1 (5D) i.e. e1->p1 with 5th comp k1
extg=[(P[1],P[1]),W(2),W(3),W(4)]
print('SSB 5D Ward e1->K1:',S.simplify(A4(extg).subs(one)))
# 3) Proca control, uniform mass m (CGW eq 53)
m=S.Symbol('m',positive=True); km={k[0]:m,k[1]:m,k[2]:-m,k[3]:-m}
Ap=A4(gen,prop='proca',Mint=m).subs(one).subs(km)
print('Proca on HZ (c13=0 i.e. -2p1.p3=0):',HZ(Ap,0))
print('CGW eq53 target: m^2/X13~ [(e1e2)(e3e4)-(e2e3)(e1e4)], X13~=s-m^2')
# 4) deformations, generic kappa
Ad=A4(gen)
r=HZ(Ad,2*k[0]*k[2]); num=S.expand(S.numer(S.together(r)))
vars_=[v for v in ee.values()]+[v for v in ep.values() if v is not None]+[s]+list(k)
co=S.Poly(num,*vars_).coeffs()
print('WWWW deformed: solutions',S.solve(co,[lam3,a,gs,lam4,b],dict=True))
