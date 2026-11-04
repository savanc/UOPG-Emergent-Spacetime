import numpy as np
w={1:8,2:4,3:4,4:-16,5:-8,6:32,8:16}
G={1:3/32,2:3/16,3:0,4:1/8,5:3/8,6:11/144,8:5/48}
GZ=sum(w[i]*G[i] for i in w); print('Gamma_Z',GZ)
dmu=max(abs(GZ/(16*np.pi**2)*np.log(0.77/m)) for m in (0.5,1.0))*1e3
print('Delta_mu (1e-3)',dmu)
S={'BE14 NNLO':{1:(.53,.06),2:(.81,.04),3:(-3.07,.20),4:(.3,0),5:(1.01,.06),6:(.14,.05),8:(.47,.10)},
   'BE14 p4 NLO':{1:(1.0,.1),2:(1.6,.2),3:(-3.8,.3),4:(0,.3),5:(1.2,.1),6:(0,.4),8:(.5,.2)},
   'GL85':{1:(.7,.3),2:(1.3,.7),3:(-4.4,2.5),4:(-.3,.5),5:(1.4,.5),6:(-.2,.3),8:(.9,.3)}}
rng=np.random.default_rng(0)
for k,v in S.items():
    Z=sum(w[i]*v[i][0] for i in w); sig=np.sqrt(sum((w[i]*v[i][1])**2 for i in w))
    T=sum(abs(w[i]*v[i][0]) for i in w); band=2*np.hypot(sig,dmu)
    Lr=rng.uniform(-2,2,(200000,7)); Zr=Lr@np.array([w[i] for i in w])
    f=np.mean(np.abs(Zr)<=band)
    print(f"{k}: Z={Z:.2f}e-3 sigma={sig:.2f} band={band:.2f} r=Z/S={Z/T:.3f} PASS={abs(Z)<=band} null f={f:.3f}  per-term: kin={4*(2*v[1][0]+v[2][0]+v[3][0]):.2f} L46={16*(2*v[6][0]-v[4][0]):.2f} L58={8*(2*v[8][0]-v[5][0]):.2f}")
