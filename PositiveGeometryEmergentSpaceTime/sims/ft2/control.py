# Negative control: naive mass term (only -1/2 M^2 phi^2, no spurion tower) must spoil zeros
import random, ft2
from ft2 import *
orig=ft2.mkc
rng=random.Random(7)
def run(tag):
    mu={'u':Fr(1),'d':Fr(2),'s':Fr(7)}; f=list('udsuds')
    for zn,z in {'skinny0':[(0,2),(0,3),(0,4)],'rect_02_13':[(0,3),(0,4),(1,3),(1,4)]}.items():
        msq=[mu[f[k]]+mu[f[(k+1)%6]] for k in range(6)]
        while True:
            try: g=kin(6,msq,z,rng); a=amp(6,g,mu,f+[f[0]],'exp'); break
            except ZeroDivisionError: pass
        print(tag,zn,'ZERO' if a.iszero() else 'nonzero')
run('spurion')
src=open('ft2.py').read()
# naive: mass vertices only at quadratic order
ft2_amp=ft2.amp
def amp_naive(n,gram,mu,f,param):
    c=orig(param)
    return None
import types
code=src.replace("cm=c[m]+cb[m]","cm=(c[m]+cb[m]) if m==2 else G(0)")
ns={}; exec(code,ns)
ft2.amp=ns['amp']; amp=ns['amp']
globals()['amp']=ns['amp']
run('naive')
