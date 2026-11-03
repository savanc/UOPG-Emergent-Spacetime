"""MR-2e verdict, prereg f33e286. FLAG 2019 Table 25 (CITED), units 1e-3, mu=770 MeV."""
import numpy as np
dmu=(1/9)/(16*np.pi**2)*np.log(0.77/0.5)*1e3
rows={ # (2L6-L4, stat, sys) , (2L8-L5, stat, sys)  sys = max of asymmetric
 'HPQCD 13A':((0.22,.17,0),(-0.10,.20,0)),
 'MILC 10':((0.03,.24,.32),(-0.15,.11,.45)),
 'PACS-CS 08':((0.10,.02,0),(-0.21,.03,0)),
 'RBC/UKQCD 08':((0.00,.04,0),(0.24,.04,0))}
out=[];bands=[];npass=0
for k,(a,b) in rows.items():
    R=2*a[0]+b[0]; s=np.hypot(2*np.hypot(a[1],a[2]),np.hypot(b[1],b[2])); tr=0.3*max(abs(2*a[0]),abs(b[0]))
    band=2*np.sqrt(s**2+dmu**2+tr**2); p=abs(R)<=band; npass+=p; bands.append(band)
    out.append(f"{k}: R={R:+.2f} sigma={s:.3f} band={band:.2f} pass={p}")
rng=np.random.default_rng(1); sl=1e3/(16*np.pi**2); ss=sl/3
L5,L8=rng.normal(0,sl,(2,200000)); L4,L6=rng.normal(0,ss,(2,200000))
Rn=2*(2*L6-L4)+(2*L8-L5); mb=np.median(bands); f=np.mean(np.abs(Rn)<=mb)
# informed null (diagnostic, not prereg): each combo ~ N(0,0.3) i.e. large-Nc-small
Ri=2*rng.normal(0,.3,200000)+rng.normal(0,.3,200000); fi=np.mean(np.abs(Ri)<=mb)
out+= [f"dmu={dmu:.3f}; {npass}/4 pass -> {'PASS' if npass>=3 else 'INCONCLUSIVE' if npass==2 else 'FAIL'}",
       f"NDA null f={f:.3f} (median band {mb:.2f}); diagnostic large-Nc-informed null (combos ~N(0,0.3e-3)) f={fi:.2f}"]
print('\n'.join(out)); open('mr2e_output.txt','w').write('\n'.join(out)+'\n')
