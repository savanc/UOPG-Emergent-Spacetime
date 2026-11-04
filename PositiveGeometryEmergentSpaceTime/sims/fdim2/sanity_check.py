import importlib.util
from fractions import Fraction as F
spec=importlib.util.spec_from_file_location('c',__import__('pathlib').Path(__file__).with_name('fdim2_checker.py')); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
m=('ls',F(1,2))
for N in (2,3,40):
    p=c.residue_poly(m,N); g=c.geg_coeffs(p,4)
    print(N,'deg',len(p)-1,'nonzero',sum(1 for x in g if x!=0),'signs',set((x>0)-(x<0) for x in g),'min|c|',float(min(abs(x) for x in g if x!=0)))
print('level2 D4 x128 (sigma=-1):',[str(-128*x) for x in c.geg_coeffs(c.residue_poly(m,2),4)])
