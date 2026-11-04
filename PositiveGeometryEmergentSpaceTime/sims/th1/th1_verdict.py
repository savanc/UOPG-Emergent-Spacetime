"""TH-1 verdict per prereg 4789cb3. Values: CCL hep-ph/0103088 tab:threshold col A; GKPY 1102.2183 CFD column."""
import numpy as np, json
P=json.load(open('th1_pred.json')); pred=[P['R1'],P['R2'],P['R3']]
src={'S1 CCL col A':dict(a11=(.0379,.0005),b11=(.00567,.00013),b20=(-3.55e-4,.14e-4),b22=(-3.26e-4,.12e-4),a31=(5.60e-5,.19e-5)),
     'S2 GKPY CFD':dict(a11=(38.5e-3,1.2e-3),b11=(5.07e-3,.26e-3),b20=(-4.2e-4,.3e-4),b22=(-2.8e-4,.8e-4),a31=(5.1e-5,1.3e-5))}
rng=np.random.default_rng(1); out=[]
for n,d in src.items():
    N=200000; g={k:rng.normal(*v,N) for k,v in d.items()}
    R=[g['b11']/g['a11'],g['b20']/g['b22'],g['a31']/g['a11']]
    res=[]
    for Rd,Rp in zip(R,pred):
        c=float(np.median(Rd)); s=float(np.std(Rd)); band=2*np.sqrt((0.3*Rp)**2+s**2)
        res.append((c,s,band,bool(np.sign(c)==np.sign(Rp) and abs(c-Rp)<=band)))
    k=sum(r[3] for r in res); out.append((n,res,k))
    print(n,' '.join(f"R{i+1}: data {c:.4g}±{s:.2g} pred {p:.4g} band ±{b:.2g} {'in' if ok else 'OUT'}" for i,((c,s,b,ok),p) in enumerate(zip(res,pred))),f'-> {k}/3',"PASS" if k>=2 else "FAIL")
# null per prereg: |R| log-uniform [Rp/10,10Rp], random sign; per ratio P(in band) using S1 bands
f=[]
for i,Rp in enumerate(pred):
    x=Rp*10**rng.uniform(-1,1,200000)*rng.choice([-1,1],200000); b=out[0][1][i][2]; f.append(np.mean(abs(x-Rp)<=b))
p2=f[0]*f[1]*(1-f[2])+f[0]*(1-f[1])*f[2]+(1-f[0])*f[1]*f[2]+f[0]*f[1]*f[2]
print('null per-ratio f',[round(x,3) for x in f],' f(>=2 of 3)=',round(p2,4))
