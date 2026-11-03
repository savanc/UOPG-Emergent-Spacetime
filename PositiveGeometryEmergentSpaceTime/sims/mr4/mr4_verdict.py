"""MR-4 verdict per prereg 37820ee."""
import numpy as np
k=0.13957/(4*0.4957)
BDM={'C00':(2.01,1.10),'C10':(.87,.08),'C01':(2.07,.10),'C20':(.024,.006),'C11':(-.066,.010),'C30':(.0034,.0008),'C02':(.34,.03),
     'D00':(8.92,.38),'D10':(.31,.01),'D01':(.62,.06),'D20':(.0085,.0001)}
LP={'C00':(-.52,2.03),'C10':(.55,.07),'C01':(2.06,.22),'C20':(0,0),'C11':(-.04,.02),'C30':(0,0),'C02':(0,0),
    'D00':(7.31,.90),'D10':(.21,.04),'D01':(.51,.10),'D20':(0,0)}
tau=np.linspace(0,4,41); X=np.linspace(-1,1,41); TT,XX=np.meshgrid(tau,X)
def F32(c,t,x): 
    Fp=c['C00']+c['C10']*t+c['C20']*t**2+c['C30']*t**3+c['C01']*x**2+c['C11']*t*x**2+c['C02']*x**4
    Fm=x*(c['D00']+c['D10']*t+c['D20']*t**2+c['D01']*x**2)
    return Fp-Fm
def stats(c,a=0.0,b=k):
    S=np.sqrt(np.mean(F32(c,TT,XX)**2)); g=F32(c,tau,a+b*tau)
    g0=c['C00']; g1=c['C10']-k*c['D00']
    return np.sqrt(np.mean(g**2))/S, abs(g0)/S, 4*abs(g1)/S, S, g0, g1
rng=np.random.default_rng(42); out=[]
for name,src in (('S1 BDM Roy-Steiner',BDM),('S2 Lang-Porod 1978',LP)):
    c={q:v[0] for q,v in src.items()}; r,r0,r1,S,g0,g1=stats(c)
    mc=np.array([stats({q:v[0]+v[1]*rng.standard_normal() for q,v in src.items()})[:3] for _ in range(4000)])
    sr,s0,s1=mc.std(0)
    pas=(r-2*sr<=1/3) and (r0-2*s0<=1/3) and (r1-2*s1<=1/3)
    a=rng.uniform(-1,1,20000); b=rng.uniform(-.5,.5,20000)
    f=np.mean([stats(c,ai,bi)[0]<=1/3 for ai,bi in zip(a[:4000],b[:4000])])
    line=f"{name}: S={S:.3f} g0=C00+={g0:.2f} g1={g1:.3f} r={r:.3f}±{sr:.3f} r0={r0:.3f}±{s0:.3f} r1={r1:.3f}±{s1:.3f} PASS={pas} null f={f:.3f}"
    print(line); out.append(line)
open('mr4_output.txt','w').write('\n'.join(out)+'\n')
