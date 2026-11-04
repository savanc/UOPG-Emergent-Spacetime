import random; from ft5b import *
rng=random.Random(20261013)
mus={'equal':{'u':Fr(1),'d':Fr(1),'s':Fr(1)},'unequal':{'u':Fr(1),'d':Fr(2),'s':Fr(7)}}
Z6={'skinny':[(0,2),(0,3),(0,4)],'rect2x2':[(0,3),(0,4),(1,3),(1,4)],'null_pair':[(0,3)]}
def T(n,mu,f,z,t,trials=2):
    out=[]
    for _ in range(trials):
        ff=f+[f[0]]; msq=[mu[ff[k]]+mu[ff[k+1]] for k in range(n)]
        while True:
            try:
                g0=kin(n,msq,z,rng); y=kin(n,shifts(n,ff,mu,t),z,rng)
                a=amplitude(n,ff,mu,g0,y,'exp',t); break
            except ZeroDivisionError: pass
        if z!=[(0,3)]: assert a.a.iszero()
        out.append(a.b)
    return out
for name,mu in mus.items():
  for f in ('udsuds','uuddss','ududud','ususus','uuuuus'):
    for zn,z in Z6.items():
      res={op:T(6,mu,list(f),z,t) for op,t in OPS5.items()}
      line=' '.join(f"{op}:{'ZERO' if all(x.iszero() for x in v) else 'nonzero'}" for op,v in res.items())
      # combination a*O5+b*O8 vanishing: ratios O8/O5 per point
      rat=[ (v8*v5.inv()) if not v5.iszero() else None for v5,v8 in zip(res['O5'],res['O8'])]
      print('6pt',name,f,zn,line,'O8/O5:',rat,flush=True)
for name,mu in mus.items():
  for f in ('udsu','uuss','udud'):
    res={op:T(4,mu,list(f),[(0,2)],t) for op,t in OPS5.items()}
    print('4pt',name,f,' '.join(f"{op}:{'ZERO' if all(x.iszero() for x in v) else 'nonzero'}" for op,v in res.items()),flush=True)
