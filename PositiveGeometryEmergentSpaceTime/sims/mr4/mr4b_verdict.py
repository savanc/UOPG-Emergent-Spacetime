"""MR-4b: Pelaez-Rodas 2020 (2010.11222 Table tab:stparameters), prereg d6b3eaf. Reuses mr4_verdict metrics."""
import numpy as np, importlib.util, sys
src=open('mr4_verdict.py').read().split("rng=np.random.default_rng(42)")[0]; exec(src)
z=(0,0)
PRf={'C00':(1.52,.56),'C10':(.96,.11),'C01':(2.34,.05),'C11':(-.047,.006),'C20':z,'C30':z,'C02':z,'D00':(9.11,.35),'D10':(.45,.05),'D01':(.68,.02),'D20':z}
PRh=dict(PRf); PRh.update({'C10':(1.04,.11),'C11':(-.050,.006),'D00':(9.54,.38),'D10':(.38,.02),'D01':(.66,.02)})
BDMtr=dict(BDM); BDMtr.update({'C20':z,'C30':z,'C02':z,'D20':z})
rng=np.random.default_rng(42); out=[]
for name,c0 in (('S3 PR fixed-t (primary)',PRf),('S3 PR HDR (variant)',PRh),('S1 BDM truncated like S3 (diag)',BDMtr)):
    c={q:v[0] for q,v in c0.items()}; r,r0,r1,S,g0,g1=stats(c)
    mc=np.array([stats({q:v[0]+v[1]*rng.standard_normal() for q,v in c0.items()})[:3] for _ in range(4000)]); sr,s0,s1=mc.std(0)
    pas=(r-2*sr<=1/3) and (r0-2*s0<=1/3) and (r1-2*s1<=1/3)
    a=rng.uniform(-1,1,4000); b=rng.uniform(-.5,.5,4000); f=np.mean([stats(c,ai,bi)[0]<=1/3 for ai,bi in zip(a,b)])
    l=f"{name}: S={S:.3f} g0={g0:.2f} g1={g1:.3f} r={r:.3f}±{sr:.3f} r0={r0:.3f}±{s0:.3f} r1={r1:.3f}±{s1:.3f} PASS={pas} null f={f:.3f}"; print(l); out.append(l)
open('mr4b_output.txt','w').write('\n'.join(out)+'\n')
