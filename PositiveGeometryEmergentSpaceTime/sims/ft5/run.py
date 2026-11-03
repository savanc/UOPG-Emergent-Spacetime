import random; from ft5a import *
rng=random.Random(20261013)
mus={'massless':{'u':Fr(0),'d':Fr(0),'s':Fr(0)},'equal':{'u':Fr(1),'d':Fr(1),'s':Fr(1)},'unequal':{'u':Fr(1),'d':Fr(2),'s':Fr(7)}}
def T(n,mu,f,z,trials=2):
    out=[]
    for t in range(trials):
        ff=f+[f[0]]; msq=[mu[ff[k]]+mu[ff[k+1]] for k in range(n)]
        while True:
            try:
                g=kin(n,msq,z,rng); r={op:amp(n,g,mu,ff,'exp',eps_terms=OPS[op]) for op in OPS}; break
            except ZeroDivisionError: pass
        assert all(r[op].a.iszero() for op in OPS) or z==[(0,3)] or not z  # LO zero sanity on loci (null exempt)
        out.append({op:r[op].b for op in OPS})
    return out
def st(xs,op): return 'ZERO' if all(x[op].iszero() for x in xs) else 'nonzero'
for name,mu in mus.items():
  for f in (list('udsu'),list('uuss'),list('udud')):
    r=T(4,mu,f,[(0,2)]); print('4pt',name,''.join(f),'L0',st(r,'L0'),'B',st(r,'B'),'ratio B/L0' ,[ (x['B']*x['L0'].inv()) if not x['L0'].iszero() else None for x in r])
Z6={'skinny':[(0,2),(0,3),(0,4)],'rect2x2':[(0,3),(0,4),(1,3),(1,4)],'null_pair':[(0,3)]}
for name,mu in mus.items():
  for f in ('udsuds','uuddss','ududud','ususus','uuuuus'):
    for zn,z in Z6.items():
      r=T(6,mu,list(f),z); print('6pt',name,f,zn,'L0',st(r,'L0'),'B',st(r,'B'),flush=True)
