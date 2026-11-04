import random,sys; from ft2 import *
rng=random.Random(20261013)
def test(n,mu,f,zeros,trials=3):
    out=[]
    for t in range(trials):
        msq=[mu[f[k]]+mu[f[(k+1)%n]] for k in range(n)]
        while True:
          try:
            g=kin(n,msq,zeros,rng)
            a=amp(n,g,mu,f+[f[0]],'exp'); b=amp(n,g,mu,f+[f[0]],'cay'); break
          except ZeroDivisionError: pass
        assert (a-b).iszero(), ("param mismatch",a,b)
        out.append(a)
    return out
mus={'equal':{'u':Fr(1),'d':Fr(1),'s':Fr(1)},'unequal':{'u':Fr(1),'d':Fr(2),'s':Fr(7)},'massless':{'u':0,'d':0,'s':0}}
# 4 point: zero c_{1,3}: p1.p3? in mesh language skinny zero at 4pt: c_{0,2}=0 <-> p0.p2=0
for name,mu in mus.items():
  for f in (['u','d','s','u'],['u','s','d','s'],['u','d','u','d'],['u','u','s','s']):
    r=test(4,mu,f,[(0,2)]); g=test(4,mu,f,[],1)
    print('4pt',name,f,'zero(p0.p2=0):',all(x.iszero() for x in r),'generic nonzero:',not g[0].iszero())
# 6 point zeros (mesh): skinny rectangle c_{0,j}=0 j=2,3,4 ; and 2x2 type: {(0,2),(0,3),(1,3)...}
Z6={'skinny0':[(0,2),(0,3),(0,4)],'rect_02_13':[(0,3),(0,4),(1,3),(1,4)],'rect':[(0,2),(0,3),(1,3)],'pair_only':[(0,3)]}
for name,mu in mus.items():
  for f in (['u','d','s','u','d','s'],['u','u','d','d','s','s'],['u','d','u','d','u','d'],['u','s','u','s','u','s'],['u','u','u','u','u','s']):
    for zn,z in Z6.items():
      r=test(6,mu,f,z,2)
      print('6pt',name,''.join(f),zn,'ZERO' if all(x.iszero() for x in r) else 'nonzero')
    sys.stdout.flush()
