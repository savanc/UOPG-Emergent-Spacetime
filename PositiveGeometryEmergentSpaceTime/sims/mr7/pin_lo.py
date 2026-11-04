"""MR-7 gate: LO piN (pseudovector Born + Weinberg-Tomozawa) I=3/2 amplitude D=A+nu*B on s=M^2+Mpi^2.
Standard tree expressions (CITED from memory: Hoehler conventions; pv coupling g=gA M/F)."""
import sympy as sp
M,m,F,gA,t=sp.symbols('M m F g_A t',positive=True); g=gA*M/F
s=M**2+m**2; u=2*M**2+2*m**2-s-t; nu=(s-u)/(4*M)
Ap=g**2/M; Bp=g**2*(1/(M**2-s)-1/(M**2-u))
Am=0; Bm=g**2*(1/(M**2-s)+1/(M**2-u))-g**2/(2*M**2)+1/(2*F**2)
D32=sp.simplify((Ap-Am)+nu*(Bp-Bm))
print('D^{3/2} on line =',sp.factor(D32)); print('at t=0:',sp.simplify(D32.subs(t,0)))
