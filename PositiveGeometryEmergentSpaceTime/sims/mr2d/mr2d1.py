"""MR-2d1: one-loop SU(3)->SU(2) pi pi amplitude at P. Prereg 537bcd8."""
import math, numpy as np, sys
sys.path.insert(0,'scripts'); import mr2_massive_zero as M  # reuses validated loop functions
N=16*math.pi**2; Mpi,MK,Meta=0.13957,0.4957,0.5479
def bs(l,mu):
    l1,l2,l3,l4=l; L=math.log(Mpi**2/mu**2)/N
    return [8*l1+2*l3-2*l4+7/6*L+13/18/N, -8*l1+2*l4-2/3*L-2/9/N, 2*l1+l2/2-L/2-7/12/N, l2/2-L/6-5/36/N,0,0]
def match(Li,mu):
    L1,L2,L3,L4,L5,L6,L8=Li
    nK=(math.log(MK**2/mu**2)+1)/(2*N); ne=(math.log(Meta**2/mu**2)+1)/(2*N)
    return [4*L1+2*L3-nK/24, 4*L2-nK/12, -8*L4-4*L5+16*L6+8*L8-ne/18, 8*L4+4*L5-nK/2]
def run(Li,mu_from=0.77,mu_to=0.77):
    G=[3/32,3/16,0,1/8,3/8,11/144,5/48]
    return [x+g/N*math.log(mu_from/mu_to) for x,g in zip(Li,G)]
def r_of(Li,mu=0.77,ret=False):
    b=bs(match(run(Li,0.77,mu),mu),mu); d=M.analyse(b,4); return d if ret else d['r']
def lbar(lb):  # GL84 lbar -> l^r(mu)
    g=[1/3,2/3,-1/2,2]; return lambda mu:[gi/(2*N)*(x+math.log(Mpi**2/mu**2)) for gi,x in zip(g,lb)]
out=[]
def say(*a): print(*a); out.append(' '.join(map(str,a)))
# validation
lv=lbar([-0.4,4.3,2.9,4.4])(0.77); bv=bs(lv,0.77); say('validation a0^0,a0^2 =',M.scl(bv) if False else None)
def scl4(b):
    e=1e-7; s=4+e; t=u=-e/2; A=lambda s,t,u:M.A(s,t,u,b,4)
    return ((3*A(s,t,u)+A(t,s,u)+A(u,t,s)).real/(32*math.pi),(A(t,s,u)+A(u,t,s)).real/(32*math.pi))
say('validation one-loop a0^0,a0^2 (GL lbar):',[round(x,4) for x in scl4(bv)])
# P real/finite
say('loop J(1),J(2) at P:',M.loops(1)[0],M.loops(2)[0])
S={'BE14 p4 col6':([1.0,1.6,-3.8,0.0,1.2,0.0,0.5],[.1,.2,.3,.3,.1,.4,.2]),
   'BE14 L4=0':([.98,1.56,-3.82,0,1.23,-.11,.53],[.09,.09,.30,0,.06,.05,.13]),
   'BE14 L4=+0.3':([1.00,1.48,-3.82,.3,1.23,.14,.55],[.09,.09,.30,0,.06,.06,.12]),
   'BE14 L4=-0.3':([.95,1.64,-3.82,-.3,1.23,-.36,.50],[.09,.09,.30,0,.06,.05,.14]),
   'GL85':([.7,1.3,-4.4,-.3,1.4,-.2,.9],[.3,.7,2.5,.5,.5,.3,.3]),
   'BE14 NNLO (diag)':([.53,.81,-3.07,.3,1.01,.14,.47],[.06,.04,.20,0,.06,.05,.10])}
rng=np.random.default_rng(20261013)
res={}
for k,(v,e) in S.items():
    Li=[x*1e-3 for x in v]; d=r_of(Li,ret=True)
    rmu=[r_of(Li,mu) for mu in (0.5,0.77,1.0)]
    mc=[r_of([ (x+ee*z)*1e-3 for x,ee,z in zip(v,e,rng.standard_normal(7))]) for _ in range(300)]
    res[k]=(d['r'],np.std(mc),d['f'])
    say(f"[{k}] r={d['r']:.4f} sig_in={np.std(mc):.4f} Z={d['Z']:.5f} S={d['S']:.4f} triangle f={d['f']:.3f} mu-spread={max(rmu)-min(rmu):.1e}")
cols=[res[k][0] for k in ('BE14 L4=0','BE14 L4=+0.3','BE14 L4=-0.3')]; scan=(max(cols)-min(cols))/2
# truncation: NLO-part of r = r itself here (LO vanishes at P)
for k in ('BE14 p4 col6','GL85','BE14 NNLO (diag)'):
    r,si,f=res[k]; tr=0.08*abs(r)+0.03; sc=scan if k.startswith('BE14 p4') else 0
    sig=math.sqrt(si**2+sc**2+tr**2); P=abs(r)<=2*sig; res[k]=res[k]+(sig,P)
    say(f"VERDICT [{k}] r={r:.4f} sigma_r={sig:.4f} (in {si:.4f}, scan {sc:.4f}, trunc {tr:.4f}) band={2*sig:.4f} PASS={P}")
# NDA null
s1=1/N; s2=s1/3; rs=[]
for _ in range(2000):
    L2,L3,L5,L8=rng.normal(0,s1,4); L4,L6,dl=rng.normal(0,s2,3); L1=L2/2+dl/2
    rs.append(r_of([L1,L2,L3,L4,L5,L6,L8]))
rs=np.abs(rs)
for k in ('BE14 p4 col6','GL85'):
    say(f"NDA null f [{k} band {2*res[k][3]:.4f}] = {np.mean(rs<=2*res[k][3]):.3f}")
open('sims/mr2d/mr2d1_output.txt','w').write('\n'.join(out)+'\n')
# sensitivity (reported, not the prereg verdict): correlated refit columns individually
for k in ('BE14 L4=0','BE14 L4=+0.3','BE14 L4=-0.3'):
    r,si,f=res[k][:3]; sig=math.hypot(si,0.08*abs(r)+0.03)
    say(f"SENS [{k}] r={r:.4f} band={2*sig:.4f} pass={abs(r)<=2*sig} NDA f={np.mean(rs<=2*sig):.3f}")
open('sims/mr2d/mr2d1_output.txt','w').write('\n'.join(out)+'\n')
