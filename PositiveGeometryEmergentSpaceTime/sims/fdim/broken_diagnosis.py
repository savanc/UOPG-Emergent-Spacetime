import sys; sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('c','<local path>'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
from fractions import Fraction as F
m=('bos',F(0))
for N in range(0,6):
    p=c.residue_poly(m,N)
    print(N,[str(x) for x in p])
    for D in (26,27):
        print('  D',D,[str(x) for x in c.geg_coeffs(p,D)])
print('---')
for D in (20,26,27,30):
    bad=[(N,j,float(x)) for N in range(13) for j,x in enumerate(c.geg_coeffs(c.residue_poly(m,N),D)) if x>0]
    print(D, bad[:4])
# real string for comparison
mb=('bos',F(-1))
for D in (26,27):
    bad=[(N,j,float(x)) for N in range(13) for j,x in enumerate(c.geg_coeffs(c.residue_poly(mb,N),D)) if x>0]
    print('m2=-1',D,bad[:4])
