"""MR-2: massive hidden zero at P=(1,1,2) (units M_pi^2=1). Prereg commit ca6c964.
Two-loop representation BCEGS hep-ph/9707291 eqs 4.14-4.15; b-values CGL hep-ph/0103088 eq 16.2 and BCEGS Table 3."""
import cmath, math, numpy as np
N = 16*math.pi**2; PI2 = math.pi**2
x2 = (139.57/92.4)**2
def h(s):
    s = complex(s, 1e-12); z = 1-4/s; rz = cmath.sqrt(z)
    return cmath.log((rz-1)/(rz+1))/(N*rz), z, s
def loops(s):
    hh, z, s = h(s); c = -1/(2*N**2)
    J = z*hh - 4*N*c; K1 = z*hh**2; K2 = z**2*hh**2 + 8*c
    K3 = N*z/s*hh**3 + PI2/(N*s)*hh + PI2*c
    K4 = (0.5*K1 + K3/3 + J/N + (PI2-6)*s/(12*N**2))/(s*z)
    return J, K1, K2, K3, K4
def A(s, t, u, b, order=6):
    b1,b2,b3,b4,b5,b6 = b
    Js,K1s,K2s,K3s,_ = loops(s)
    def G1(s,t): return loops(t)[0]*(14-4*s-10*t+s*t+2*t*t)/6
    F1 = Js*(s*s-1)/2
    r = x2*(s-1) + x2**2*(b1+b2*s+b3*s*s+b4*(t-u)**2 + F1+G1(s,t)+G1(s,u))
    if order < 6: return r
    F2 = Js*((503/108*s**3-929/54*s**2+887/27*s-140/9)/N + b1*(4*s-3)+b2*(s*s+4*s-4)
             + b3/3*(8*s**3-21*s**2+48*s-32) + b4/3*(16*s**3-71*s**2+112*s-48)) \
         + K1s/18*(20*s**3-119*s**2+210*s-135-9/16*PI2*(s-4)) + K2s/32*(s*PI2-24) + K3s/9*(3*s*s-17*s+9)
    def G2(s,t):
        J,K1,K2,K3,K4 = loops(t)
        return J*((412/27 - s/54*(t*t+5*t+159) - t*(267/216*t*t-727/108*t+1571/108))/N
                  + b1*(2-t) + b2/3*(t-4)*(2*t+s-5) - b3/6*(t-4)**2*(3*t+2*s-8)
                  + b4/6*(2*s*(3*t-4)*(t-4)-32*t+40*t*t-11*t**3)) \
             + K1/36*(174+8*s-10*t**3+72*t*t-185*t-PI2/16*(t-4)*(3*s-8)) + K2/9*(1+4*s+PI2/64*t*(3*s-8)) \
             + K3/9*(1+3*s*t-s+3*t*t-9*t) + 5/3*K4*(4-2*s-t)
    return r + x2**3*(b5*s**3+b6*s*(t-u)**2 + F2+G2(s,t)+G2(s,u))
def cgl_b(bb): return [bb[0]/N,bb[1]/N,bb[2]/N,bb[3]/N,bb[4]/N**2,bb[5]/N**2]
CGL = [-12.4,11.8,-0.33,0.74,3.58,2.35]; CGLe = [1.6,0.6,0.07,0.01,0.37,0.02]
S2a = [-8.63e-2,8.01e-2,-2.63e-3,4.82e-3,-0.37e-4,0.83e-4]   # mu=1 GeV
S2b = [-8.80e-2,8.31e-2,-4.34e-3,4.85e-3,0.88e-4,0.72e-4]    # mu=0.5 GeV
# validation: S-wave scattering lengths at threshold
def scl(b):
    e=1e-7; s=4+e; t=u=-e/2
    T0 = 3*A(s,t,u,b)+A(t,s,u,b)+A(u,t,s,b); T2 = A(t,s,u,b)+A(u,t,s,b)
    return (T0.real/(32*math.pi), T2.real/(32*math.pi))
grid = [(s,t,4-s-t) for s in np.linspace(0,4,41) for t in np.linspace(0,4,41) if 4-s-t >= -1e-9]
def R(Q,b,o=6): s,t,u=Q; return (A(s,t,u,b,o)/x2-(s-1)).real
def analyse(b, o=6):
    vals = np.array([R(Q,b,o) for Q in grid]); S = math.sqrt((vals**2).mean())
    Z = R((1,1,2),b,o); f = float((np.abs(vals)/S <= 1/3).mean())
    trunc = abs(R((1,1,2),b,6)-R((1,1,2),b,4))
    return dict(Z=Z, S=S, r=Z/S, f=f, trunc_r=trunc/S,
                r_thr=Z/abs(R((4,0,0),b,o)), r_ctr=Z/abs(R((4/3,4/3,4/3),b,o)))
if __name__=="__main__":
    out=[]
    def say(*a): print(*a); out.append(' '.join(map(str,a)))
    say("x2 =", round(x2,5))
    for name,b in [("S1 CGL",cgl_b(CGL)),("S2 BCEGS mu=1",S2a),("S2 BCEGS mu=0.5",S2b)]:
        a0,a2 = scl(b); say(f"[{name}] validation a0^0={a0:.4f} a0^2={a2:.5f}")
        d = analyse(b); d4 = analyse(b,4)
        say(f"[{name}] Z=R(P)={d['Z']:.5f} S=RMS={d['S']:.5f} r={d['r']:.4f} f(|R|/S<=1/3)={d['f']:.3f} trunc/S={d['trunc_r']:.4f}")
        say(f"[{name}] O(p4)-only r={d4['r']:.4f}; r_thr={d['r_thr']:.4f} r_ctr={d['r_ctr']:.4f}")
    rng = np.random.default_rng(20261012)
    for rho in [0.0, 0.8, -0.8]:
        rs=[]
        for _ in range(400):
            z = rng.standard_normal(6); z[1] = rho*z[0]+math.sqrt(1-rho**2)*z[1]
            bb = [CGL[i]+CGLe[i]*z[i] for i in range(6)]; rs.append(analyse(cgl_b(bb))['r'])
        say(f"[S1 MC rho(b1,b2)={rho}] r median={np.median(rs):.4f} sigma={np.std(rs):.4f}")
    open("scripts/mr2_massive_zero_output.txt","w").write("\n".join(out)+"\n")
