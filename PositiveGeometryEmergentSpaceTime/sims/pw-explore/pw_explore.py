"""PW-EXPLORE: two exploratory toy checks for the pilot-wave addendum (2026-10-28).

Run id: PWX-2026-10-28-r1. EXPLORATORY, NOT A RUNG: no prereg, no locked checker,
no verdict. Results are SIMULATED (this run id) and only motivate the DRAFT
rungs PW-1 / PW-2 in notes/TRADE-SPACE-ADDENDUM-PILOT-WAVE-2026-10-28.md.

Check A (equivariance): Bell's jump rates on a finite configuration space,
  sigma_ij = max(0, J_ij)/|psi_j|^2,  J_ij = 2 Im(conj(psi_i) H_ij psi_j)  (hbar = 1),
reproduce d|psi|^2/dt under i dpsi/dt = H psi (master equation == Schrodinger).
Check B (relaxation): one instance, n = 12, uniform rho_0, explicit Euler on the
master equation with dt = 1e-3, psi propagated exactly by expm(-i H dt);
reports D(rho || |psi|^2) at t = 0, 4, ..., 20. Repeated at dt = 2.5e-4 to see whether
the late-time floor is an Euler artefact (it should scale ~dt if so).
"""
import json, sys
import numpy as np
from scipy.linalg import expm

RUN_ID = "PWX-2026-10-28-r1"
SEED_A, SEED_B = 1, 7


def bell_generator(H, psi):
    p = np.abs(psi) ** 2
    J = 2 * np.imag(psi.conj()[:, None] * H * psi[None, :])  # probability current j -> i
    sig = np.maximum(J, 0) / p[None, :]
    np.fill_diagonal(sig, 0)
    return sig, p


def check_a(trials=200):
    rng = np.random.default_rng(SEED_A)
    worst = 0.0
    for _ in range(trials):
        n = int(rng.integers(2, 8))
        A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        H = (A + A.conj().T) / 2
        psi = rng.normal(size=n) + 1j * rng.normal(size=n)
        psi /= np.linalg.norm(psi)
        sig, p = bell_generator(H, psi)
        drho = 2 * np.real(psi.conj() * (-1j * H @ psi))
        master = sig @ p - sig.sum(0) * p
        worst = max(worst, float(np.abs(master - drho).max()))
    return {"trials": trials, "n_range": [2, 7], "max_abs_residual": worst}


def kl(r, p):
    m = r > 1e-300
    return float(np.sum(r[m] * np.log(r[m] / p[m])))


def check_b(n=12, dt=1e-3, T=20.0, every=4.0):
    rng = np.random.default_rng(SEED_B)
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    H = (A + A.conj().T) / 2
    _, V = np.linalg.eigh(H)
    c = rng.normal(size=n) + 1j * rng.normal(size=n)
    c /= np.linalg.norm(c)
    psi = V @ c
    rho = np.ones(n) / n
    U = expm(-1j * H * dt)
    steps, stride = int(round(T / dt)), int(round(every / dt))
    out = []
    for s in range(steps + 1):
        sig, p = bell_generator(H, psi)
        if s % stride == 0:
            out.append({"t": round(s * dt, 6), "KL": kl(rho, p)})
        rho = rho + dt * (sig @ rho - sig.sum(0) * rho)
        rho = np.clip(rho, 0, None)
        rho /= rho.sum()
        psi = U @ psi
    return {"n": n, "dt": dt, "T": T, "rho0": "uniform", "integrator": "explicit Euler (rho), exact expm (psi)",
            "series": out}


if __name__ == "__main__":
    res = {"run_id": RUN_ID, "seeds": {"A": SEED_A, "B": SEED_B},
           "numpy": np.__version__, "python": sys.version.split()[0],
           "check_A_equivariance": check_a(), "check_B_relaxation": check_b(),
           "check_B_dt_quarter": check_b(dt=2.5e-4)}
    print(json.dumps(res, indent=1))
