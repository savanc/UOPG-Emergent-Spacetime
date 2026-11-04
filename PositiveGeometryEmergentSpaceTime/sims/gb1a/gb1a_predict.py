"""GB-1a: zero-parameter closed-string glueball ratios, unit sqrt(sigma). Prediction only; no lattice data read."""
from math import sqrt, pi
mpf=float

out=[]
# Model A: Nambu-Goto closed string, light-cone, D=4: m^2 = 8 pi sigma (N - (D-2)/24), N = Ntilde, leading spin J = 2N
D=4; a=mpf(D-2)/24
mA=lambda N: sqrt(8*pi*(N-a))
out.append(f"Model A intercept (D-2)/24 = {a}")
for N in [1,2,3]:
    out.append(f"A: level N={N} (leading J={2*N}++) m/sqrt(sigma) = {mA(N):.6f}")
out.append(f"A: m(4++)/m(2++) = sqrt(23/11) = {mA(2)/mA(1):.6f}; m(6++)/m(2++) = {mA(3)/mA(1):.6f}")
# Model B: LS-anchored closed trajectory. Open LS intercept alpha0=1/2 fixed by Adler zero (MR rungs);
# closed slope alpha'/2, closed intercept 2*alpha0 = 1 :  J = (alpha'/2) m^2 + 1, alpha' = 1/(2 pi sigma) => m^2 = 4 pi sigma (J-1)
mB=lambda J: sqrt(4*pi*(J-1))
for J in [2,4,6]:
    out.append(f"B: J={J}++ m/sqrt(sigma) = {mB(J):.6f}")
out.append(f"B: m(4++)/m(2++) = {mB(4)/mB(2):.6f} (= sqrt 3); m(6++)/m(2++) = {mB(6)/mB(2):.6f} (= sqrt 5)")
out.append("Both models: N-independent at this order (leading large-N string); no 1/N^2 term predicted.")
print("\n".join(out))
