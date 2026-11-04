import random; from ft5b import *
rng=random.Random(7)
mu={'u':Fr(1),'d':Fr(2),'s':Fr(7)}
# LO kernel sanity: K_LO(s)=s-M0
c=mkc('exp');cb=[x.conj() for x in c]
print('k_LO(3) for ud:',k2(LO,Fr(3),Fr(1),Fr(2),c,cb),'expect 0')
for n,f in [(4,list('udsu')),(6,list('udsuds'))]:
    ff=f+[f[0]]; msq=[mu[ff[k]]+mu[ff[k+1]] for k in range(n)]
    for op,t in OPS5.items():
        while True:
            try:
                g0=kin(n,msq,[],rng); y=kin(n,shifts(n,ff,mu,t),[],rng)
                e=amplitude(n,ff,mu,g0,y,'exp',t); ca=amplitude(n,ff,mu,g0,y,'cay',t); break
            except ZeroDivisionError: pass
        print(n,op,'LO==ft2:',(e.a-amp_ft2(n,g0,mu,ff,'exp')).iszero(),'exp==cay:',(e.b-ca.b).iszero(),'T!=0:',not e.b.iszero(),flush=True)
