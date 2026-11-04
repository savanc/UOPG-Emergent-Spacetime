"""M3c: Coon q-deformation of the Lovelace-Shapiro pion amplitude; epsilon(q), hidden zero, unitarity window.
Prereg: prereg/M3c-coon-2026-10-11.md (pushed before this script). alpha'=1.
M_q(s,u) = prod_{n>=0} (1-q^{n+1})(sigma tau - q^{n+1}) / ((sigma-q^{n+1})(tau-q^{n+1}))   (C = 1)
         = (q;q)_inf (q/(sigma tau);q)_inf / ((q/sigma;q)_inf (q/tau;q)_inf)
sigma = 1 + (q-1)(a0 + s), tau = 1 + (q-1)(a0 + u).  F_B: a0 = 1/(1+sqrt q);  F_A: a0 = 1/2."""
import mpmath as mp, sys, json
mp.mp.dps = 30

def a0_of(fam, q):
    return 1/(1+mp.sqrt(q)) if fam == 'B' else mp.mpf(1)/2

def M(s, u, q, a0, skip=None):
    sg = 1 + (q-1)*(a0+s); ta = 1 + (q-1)*(a0+u)
    if skip is None:
        if q > mp.mpf('0.95'):   # direct product (mpmath.qp does not converge reliably near q=1)
            N = int(mp.ceil(mp.mp.dps*mp.log(10)/(-mp.log(q)))) + 10
            tot = mp.mpf(0); qn = mp.mpf(1)
            for n in range(N):
                qn *= q
                tot += mp.log((1-qn)*(sg*ta-qn)/((sg-qn)*(ta-qn)))
            return mp.exp(tot)
        return mp.qp(q, q) * mp.qp(q/(sg*ta), q) / (mp.qp(q/sg, q) * mp.qp(q/ta, q))
    # product with the (sigma - q^{skip+1}) denominator factor removed (for residues)
    N0 = skip + 1
    if q > mp.mpf('0.95'):
        N = int(mp.ceil(mp.mp.dps*mp.log(10)/(-mp.log(q)))) + 10
        val = mp.mpf(1); qn = mp.mpf(1)
        for n in range(N):
            qn *= q
            num = (1-qn)*(sg*ta - qn); den = (ta - qn)*(1 if n == skip else (sg - qn))
            val *= num/den
        return val
    val = mp.mpf(1)
    for n in range(N0):
        qn = q**(n+1)
        num = (1-qn)*(sg*ta - qn); den = (ta - qn)*(1 if n == skip else (sg - qn))
        val *= num/den
    qs = q**(N0+1)
    val *= mp.qp(qs, q)*mp.qp(qs/(sg*ta), q)/(mp.qp(qs/sg, q)*mp.qp(qs/ta, q))
    return val

def coeffs(q, fam):
    a0 = a0_of(fam, q)
    f = lambda s, u: M(s, u, q, a0)
    g00 = f(0, 0)
    g10 = mp.diff(f, (0, 0), (1, 0))
    g10u = mp.diff(f, (0, 0), (0, 1))
    g20 = mp.diff(f, (0, 0), (2, 0))/2
    g21 = mp.diff(f, (0, 0), (1, 1))/2
    g30 = mp.diff(f, (0, 0), (3, 0))/6
    sgn = mp.sign(g10)
    return dict(g00=g00*sgn, g10=g10*sgn, g10u=g10u*sgn, g20=g20*sgn, g21=g21*sgn, g30=g30*sgn, sgn=sgn)

def mass2(n, q, a0):   # pole sigma = q^{n+1}
    return (1 - q**(n+1))/(1-q) - a0

def partial_waves(q, fam, nmax=8, Jmax=16):
    a0 = a0_of(fam, q); out = {}
    sgn = coeffs(q, fam)['sgn']
    for n in range(nmax+1):
        m2 = mass2(n, q, a0)
        # Res_s M at s=m2 = [M (sigma - q^{n+1})]/(q-1); spectral weight = -Res (rho convention: g^2 m^2 P_J/(m^2-s))
        R = lambda x: -sgn*M(m2, m2*(x-1)/2, q, a0, skip=n)/(q-1)
        nodes = mp.linspace(-1, 1, 3)
        for J in range(Jmax+1):
            aJ = (2*J+1)/mp.mpf(2)*mp.quad(lambda x: R(x)*mp.legendre(J, x), [-1, 0, 1])
            out[(n, J)] = aJ
    return out

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'eps'
    if mode == 'eps':
        res = {}
        print("q        fam  g00        g10        g20/g10    g21/g10    eps=1-g21/g20   Hankel g10g30-g20^2   R_full R_fam  M(s,-s)@s=0.3")
        for fam in ['B', 'A']:
            for qs in ['0.02', '0.05', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.94', '0.97', '0.99']:
                q = mp.mpf(qs); c = coeffs(q, fam)
                eps = 1 - c['g21']/c['g20']
                hk = c['g10']*c['g30'] - c['g20']**2
                full = (0 <= c['g21'] <= 2*c['g20']); famr = (c['g20'] <= c['g21'] <= 2*c['g20'])
                hz = M(mp.mpf('0.3'), mp.mpf('-0.3'), q, a0_of(fam, q))
                print(f"{qs:7s}  {fam}   {mp.nstr(c['g00'],6):>10} {mp.nstr(c['g10'],6):>10} {mp.nstr(c['g20']/c['g10'],7):>10} {mp.nstr(c['g21']/c['g10'],7):>10} {mp.nstr(eps,8):>14}   {mp.nstr(hk/c['g10']**2,6):>12}   {str(full):5s} {str(famr):5s}  {mp.nstr(hz,5)}")
                assert abs(c['g10'] - c['g10u']) < mp.mpf('1e-15')*abs(c['g10'])  # s<->u symmetry check
                res[f"{fam}:{qs}"] = dict(eps=str(eps), g20=str(c['g20']/c['g10']), g21=str(c['g21']/c['g10']), g00=str(c['g00']), hankel=str(hk/c['g10']**2))
        # LS reference (q->1): g20/g10 = 2 ln 2, eps = 0
        print("F_B exact check eps = (1-q)/(2 sqrt q) * g10/g20:")
        for qs in ['0.1','0.5','0.9']:
            q=mp.mpf(qs); c=coeffs(q,'B'); print("  q=",qs, mp.nstr(1-c['g21']/c['g20'],12), mp.nstr((1-q)/(2*mp.sqrt(q))*c['g10']/c['g20'],12))
        print("LS reference: g20/g10 = 2 ln2 =", mp.nstr(2*mp.log(2), 10))
        json.dump(res, open('scripts/m3c_eps.json', 'w'), indent=1)

def pw_fast(q, fam, nmax=6, Jmax=12, nodes=48):
    a0 = a0_of(fam, q); sgn = coeffs(q, fam)['sgn']
    xs, ws = zip(*[(x, w) for x, w in zip(*gauss_legendre(nodes))])
    out = {}
    for n in range(nmax+1):
        m2 = mass2(n, q, a0)
        Rv = [-sgn*M(m2, m2*(x-1)/2, q, a0, skip=n)/(q-1) for x in xs]
        for J in range(Jmax+1):
            out[(n, J)] = (2*J+1)/mp.mpf(2)*mp.fsum(w*r*mp.legendre(J, x) for x, w, r in zip(xs, ws, Rv))
    return out

def gauss_legendre(n):
    import numpy as np
    x, w = np.polynomial.legendre.leggauss(n)
    return [mp.mpf(float(v)) for v in x], [mp.mpf(float(v)) for v in w]

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'pw':
    for fam in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['B', 'A']):
        for qs in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['0.05', '0.1', '0.3', '0.5', '0.7', '0.8', '0.9', '0.94', '0.95', '0.97']):
            q = mp.mpf(qs); pw = pw_fast(q, fam)
            neg = [(k, v) for k, v in pw.items() if mp.re(v) < -mp.mpf('1e-12')*max(abs(mp.re(t)) for t in pw.values())]
            a0 = a0_of(fam, q)
            print(f"fam {fam} q={qs}: m_n^2 (n=0..3) = {[mp.nstr(mass2(n,q,a0),4) for n in range(4)]}, accumulation s* = {mp.nstr(1/(1-q)-a0,4)}")
            print(f"   rho (n=0,J=1) weight {mp.nstr(mp.re(pw[(0,1)]),5)}, n=0 J=0 {mp.nstr(mp.re(pw[(0,0)]),5)}, n=1 J=0 {mp.nstr(mp.re(pw[(1,0)]),5)};"
                  f" negative partial waves (n<=6, J<=12): {[(k, mp.nstr(mp.re(v),3)) for k, v in neg][:8]}{' ...' if len(neg) > 8 else ''} (count {len(neg)})")
