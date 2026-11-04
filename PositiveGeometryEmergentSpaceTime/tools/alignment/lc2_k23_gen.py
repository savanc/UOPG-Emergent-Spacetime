"""Phase C (2026-11-03) LEAN-CERT-2 k=2,3 tie generator.
Formal coefficient-comparison system for N = eps * f(X), f of degree <= k in X_0..X_4:
  cyclic:   f(X_{i+1}) = f(X)        (X_i(cycP) = X_{i+1}(P))
  reversal: f(X_{3-i}) = sigma f(X)  (X_i(revP) = X_{3-i}(P), indices mod 5)
  parity rows vanish identically (eps odd, X even).
Row for target monomial u: +1 at idx(pi^{-1} u) and -sigma_g at idx(u).
Emits Lean list certificates (certL format of PositiveGeometryEmergentSpaceTime.LeanCert2.Core). Exact rationals (sympy)."""
import itertools, math, sys
from fractions import Fraction
def monos(k):
    return [c for d in range(k+1) for c in itertools.combinations_with_replacement(range(5), d)]
cycinv=lambda i:(i+4)%5
rho=lambda i:(3-i)%5
def rows(ms, pinv, sg):
    idx={m:j for j,m in enumerate(ms)}; out=[]
    for u in ms:
        r=[0]*len(ms); r[idx[tuple(sorted(pinv(i) for i in u))]]+=1; r[idx[u]]-=sg; out.append(r)
    return out
def cert(M):
    """RREF with transform T (T A = R). Kernel basis K from free columns, Q = free-column selector,
    P row pc_r = T row r (so P A + K Q = d I); scaled to integers by d."""
    m,n=len(M),len(M[0])
    A=[[Fraction(x) for x in r]+[Fraction(int(i==j)) for j in range(m)] for i,r in enumerate(M)]
    piv=[];r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]!=0),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]; pv=A[r][c]; A[r]=[x/pv for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]!=0:
                f=A[i][c]; A[i]=[x-f*y for x,y in zip(A[i],A[r])]
        piv.append(c); r+=1
    free=[c for c in range(n) if c not in piv]
    K0=[]
    for f in free:
        v=[Fraction(0)]*n; v[f]=Fraction(1)
        for i,pc in enumerate(piv): v[pc]=-A[i][f]
        K0.append(v)
    P0=[[Fraction(0)]*m for _ in range(n)]
    for i,pc in enumerate(piv): P0[pc]=A[i][n:]
    d=math.lcm(1,*[x.denominator for row in P0+K0 for x in row])
    K=[[int(x*d) for x in v] for v in K0]           # columns of K (scaled by d)
    Q=[[int(j==f) for j in range(n)] for f in free]  # Q K = d I
    P=[[int(x*d) for x in row] for row in P0]        # P A + K Q = d I
    # exact integer checks
    k=len(free)
    for j in range(k):
        assert all(sum(M[i][t]*K[j][t] for t in range(n))==0 for i in range(m))
        for a in range(k): assert sum(Q[a][t]*K[j][t] for t in range(n))==(d if a==j else 0)
    for i in range(n):
        for j in range(n):
            assert sum(P[i][t]*M[t][j] for t in range(m))+sum(K[a][i]*Q[a][j] for a in range(k))==(d if i==j else 0)
    return K,P,Q,d
def L(rows_): return "[" + ",\n  ".join("["+", ".join(str(int(x)) for x in r)+"]" for r in rows_) + "]"
res={}
for k in (2,3):
    ms=monos(k)
    for sg in (1,-1):
        M=rows(ms,cycinv,1)+rows(ms,rho,sg)
        K,P,Q,d=cert(M)
        res[(k,sg)]=(ms,M,K,P,Q,d)
        print(f"k={k} sigma={sg:+d} n={len(ms)} m={len(M)} formal_dim={len(K)} d={d}")
if __name__=="__main__" and len(sys.argv)>1:
    import json; json.dump({f"{k}{'p' if s==1 else 'm'}":dict(ms=[list(x) for x in v[0]],M=v[1],K=v[2],P=v[3],Q=v[4],d=v[5]) for (k,s),v in res.items()},open(sys.argv[1],"w"))

def emit(path):
    def LL(rows_): return "[" + ",\n    ".join("["+", ".join(str(int(x)) for x in r)+"]" for r in rows_) + "]"
    def T(rows_, ncols): return [[r[j] for r in rows_] for j in range(ncols)]
    out=[]
    for k in (2,3):
        ms=res[(k,1)][0]
        out.append(f"/-- Monomials of degree ≤ {k} in `X₀..X₄`, in the column order of `rank_count.py`. -/\n"
                   f"def ms{k} : List (List (Fin 5)) := [" + ", ".join("["+", ".join(map(str,m))+"]" for m in ms) + "]\n")
        for sg in (1,-1):
            _,M,K,P,Q,d=res[(k,sg)]; n=len(ms); m=len(M); kk=len(K); t=f"k{k}{'p' if sg==1 else 'm'}"
            Kr=[[K[j][i] for j in range(kk)] for i in range(n)] if kk else []
            Qc=[[Q[a][i] for a in range(kk)] for i in range(n)] if kk else []
            sgs="1" if sg==1 else "-1"
            blk=f"""-- {t}: m = {m}, n = {n}, kernel dimension {kk}
def {t}_Mr : List (List ℤ) := {LL(M)}
def {t}_Mc : List (List ℤ) := {LL(T(M,n))}
def {t}_Kr : List (List ℤ) := {LL(Kr)}
def {t}_Kc : List (List ℤ) := {LL(K)}
def {t}_Pr : List (List ℤ) := {LL(P)}
def {t}_Qr : List (List ℤ) := {LL(Q)}
def {t}_Qc : List (List ℤ) := {LL(Qc)}
def {t}_d : ℤ := {d}

/-- The {t} rows are exactly the coefficient comparison generated from `ms{k}` (cyclic, then reversal with σ = {sgs}). -/
theorem {t}_rows_gen : fRows ms{k} cycInv 1 ++ fRows ms{k} rho ({sgs}) = {t}_Mr := by decide +kernel

/-- Kernel check of the list certificate (`certL {m} {n} {kk}`). -/
theorem {t}_cert : certL {m} {n} {kk} {t}_Mr {t}_Mc {t}_Kr {t}_Kc {t}_Pr {t}_Qr {t}_Qc {t}_d = true := by
  decide +kernel

/-- **Formal dimension {kk}** for k = {k}, σ = {sgs} (the value `rank_count.py` prints for the 40 sampled points). -/
theorem {t}_finrank : Module.finrank ℚ (LinearMap.ker
    (cq (rowsM {m} {n} (fRows ms{k} cycInv 1 ++ fRows ms{k} rho ({sgs})))).mulVecLin) = {kk} := by
  rw [{t}_rows_gen]; exact finrank_of_certL {t}_cert
"""
            out.append(blk)
            if kk:
                pats=" | ".join(["rfl"]*kk)
                out.append(f"""/-- Every certified kernel vector for {t} is a cyclic-invariant polynomial with reversal sign σ = {sgs}. -/
theorem {t}_inv : ∀ c ∈ {t}_Kc, (∀ x : Fin 5 → R, evalPoly c ms{k} (fun i => x (i + 1)) = evalPoly c ms{k} x) ∧
    (∀ x : Fin 5 → R, evalPoly c ms{k} (fun i => x (3 - i)) = ({sgs}) * evalPoly c ms{k} x) := by
  intro c hc
  simp only [{t}_Kc, List.mem_cons, List.not_mem_nil, or_false] at hc
  rcases hc with {pats} <;>
    refine ⟨fun x => ?_, fun x => ?_⟩ <;>
    simp [evalPoly, ms{k}] <;> ring

/-- **Tie ({t})**: each certified kernel vector gives `N = eps·f(X)` whose cyclic, reversal and parity rows
  vanish at every point with momentum conservation (not only the 40 sampled points). -/
theorem {t}_N_rows (c : List ℤ) (hc : c ∈ {t}_Kc) (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    NN c ms{k} P2 P3 P4 (-(P1 + P2 + P3 + P4)) - NN c ms{k} P1 P2 P3 P4 = 0 ∧
    NN c ms{k} (-(P1 + P2 + P3 + P4)) P4 P3 P2 - ({sgs}) * NN c ms{k} P1 P2 P3 P4 = 0 ∧
    NN c ms{k} P1ᵀ P2ᵀ P3ᵀ P4ᵀ + NN c ms{k} P1 P2 P3 P4 = 0 :=
  N_rows_of_inv c ms{k} _ ({t}_inv c hc).1 ({t}_inv c hc).2 P1 P2 P3 P4
""")
    open(path,"w").write(HEADER + "\n".join(out) + FOOTER)

HEADER='''/-
Copyright (c) 2026 Savan Chhaniyara. All rights reserved.
Released under MIT license as described in the file LICENSE.
Authors: Savan Chhaniyara

ALIGNMENT PHASE C (2026-11-03) — LEAN-CERT-2 ties for k = 2, 3 (D173).
Generated by tools/alignment/lc2_k23_gen.py. Not part of `import PositiveGeometryEmergentSpaceTime`; nothing in the original edited.
-/
import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LeanCert2Sanity

/-!
# LEAN-CERT-2 ties for k = 2, 3

`rank_count.py` uses the basis `eps(P₁..P₄)·∏X` (monomials of degree ≤ k in the five cyclic invariants
`X_i = det(P_i + P_{i+1})`) and samples 40 points. Symbolically:

* `Xv_cyc`, `Xv_rev`, `Xv_par`: under the cyclic shift `X_i ↦ X_{i+1}`, under reversal `X_i ↦ X_{3−i}`
  (indices mod 5), under parity `X` is unchanged. With `eps_cyc`, `eps_rev`, `eps_par` (k = 0 module) the parity
  row vanishes identically and the other two rows become the coefficient comparison
  `f(X∘cyc) = f(X)`, `f(X∘ρ) = σ f(X)`.
* `kNs_finrank`: that formal comparison system (`fRows`, generated in Lean from the monomial list) has kernel
  dimension 5, 0, 10, 2 for (k, σ) = (2, +), (2, −), (3, +), (3, −) — the values the script prints.
* `kNs_N_rows`: every certified kernel vector gives `N = eps·f(X)` with all three rows zero at every
  momentum-conserving point, so the script's solution space contains these.
* Not proved here: that the 40 sampled points add no extra solutions beyond the formal ones (the script's
  rank equals the formal rank there; that step is SIMULATED).
-/

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LeanCert2K23
open Matrix PositiveGeometryEmergentSpaceTime.LeanCert PositiveGeometryEmergentSpaceTime.LeanCert2 PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LeanCert2Sanity

variable {R : Type*} [CommRing R]

/-- Cyclic invariants `X_i = det(P_i + P_{i+1})`, with `P₅ = −(P₁+P₂+P₃+P₄)`. -/
def Xv (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) : Fin 5 → R := fun i =>
  match i with
  | 0 => (P1 + P2).det
  | 1 => (P2 + P3).det
  | 2 => (P3 + P4).det
  | 3 => (P4 + -(P1 + P2 + P3 + P4)).det
  | 4 => (-(P1 + P2 + P3 + P4) + P1).det

theorem Xv_cyc (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    Xv P2 P3 P4 (-(P1 + P2 + P3 + P4)) = fun i => Xv P1 P2 P3 P4 (i + 1) := by
  funext i; fin_cases i <;>
    simp [Xv, Matrix.det_fin_two, Matrix.add_apply, Matrix.neg_apply]

theorem Xv_rev (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    Xv (-(P1 + P2 + P3 + P4)) P4 P3 P2 = fun i => Xv P1 P2 P3 P4 (3 - i) := by
  funext i; fin_cases i <;>
    simp [Xv, Matrix.det_fin_two, Matrix.add_apply, Matrix.neg_apply] <;> ring

theorem Xv_par (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    Xv P1ᵀ P2ᵀ P3ᵀ P4ᵀ = Xv P1 P2 P3 P4 := by
  funext i; fin_cases i <;>
    simp [Xv, Matrix.det_fin_two, Matrix.add_apply, Matrix.neg_apply] <;> ring

/-- `f(x) = Σ c_m ∏_{i∈m} x_i` for a coefficient list `c` over the monomial list `ms`. -/
def evalPoly (c : List ℤ) (ms : List (List (Fin 5))) (x : Fin 5 → R) : R :=
  (List.zipWith (fun (a : ℤ) (m : List (Fin 5)) => (a : R) * (m.map x).prod) c ms).sum

/-- `N = eps · f(X)`. -/
def NN (c : List ℤ) (ms : List (List (Fin 5))) (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) : R :=
  eps P1 P2 P3 P4 * evalPoly c ms (Xv P1 P2 P3 P4)

/-- Rows from invariance: if `f` is cyclic-invariant with reversal sign `sg`, all three rows of `N` vanish. -/
theorem N_rows_of_inv (c : List ℤ) (ms : List (List (Fin 5))) (sg : R)
    (hc : ∀ x : Fin 5 → R, evalPoly c ms (fun i => x (i + 1)) = evalPoly c ms x)
    (hr : ∀ x : Fin 5 → R, evalPoly c ms (fun i => x (3 - i)) = sg * evalPoly c ms x)
    (P1 P2 P3 P4 : Matrix (Fin 2) (Fin 2) R) :
    NN c ms P2 P3 P4 (-(P1 + P2 + P3 + P4)) - NN c ms P1 P2 P3 P4 = 0 ∧
    NN c ms (-(P1 + P2 + P3 + P4)) P4 P3 P2 - sg * NN c ms P1 P2 P3 P4 = 0 ∧
    NN c ms P1ᵀ P2ᵀ P3ᵀ P4ᵀ + NN c ms P1 P2 P3 P4 = 0 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [NN, NN, eps_cyc, Xv_cyc, hc]; ring
  · rw [NN, NN, eps_rev, Xv_rev, hr]; ring
  · rw [NN, NN, eps_par, Xv_par]; ring

/-- Insertion sort for monomials. -/
def srt (m : List (Fin 5)) : List (Fin 5) := m.insertionSort (· ≤ ·)

/-- Inverse cyclic shift on indices and the reversal involution `i ↦ 3 − i` (mod 5). -/
def cycInv (i : Fin 5) : Fin 5 := i + 4
def rho (i : Fin 5) : Fin 5 := 3 - i

/-- Coefficient-comparison rows: for each target monomial `u`, `+1` at `π⁻¹u` and `−sg` at `u`. -/
def fRows (ms : List (List (Fin 5))) (pinv : Fin 5 → Fin 5) (sg : ℤ) : List (List ℤ) :=
  ms.map fun u => (List.range ms.length).map fun j =>
    (if j = ms.idxOf (srt (u.map pinv)) then 1 else 0) - sg * (if j = ms.idxOf u then 1 else 0)

/-- Monomial-list check: sorted, length ≤ k, no duplicates, and `C(k+5,5)` of them (so all monomials). -/
def monoOK (k : ℕ) (ms : List (List (Fin 5))) : Bool :=
  ms.all (fun m => decide (m.length ≤ k) && decide (srt m = m)) && decide ms.Nodup &&
    decide (ms.length = Nat.choose (k + 5) 5)

'''
FOOTER='''
theorem ms2_ok : monoOK 2 ms2 = true := by decide +kernel
theorem ms3_ok : monoOK 3 ms3 = true := by decide +kernel

/-- Planted: the single monomial `X₀` (degree 1, inside `ms2`) is not cyclic-invariant. -/
theorem planted_X0_not_cyclic :
    evalPoly (R := ℚ) [0, 1] ms2 (fun i => (fun j : Fin 5 => if j = 0 then (1 : ℚ) else 0) (i + 1)) ≠
      evalPoly [0, 1] ms2 (fun j : Fin 5 => if j = 0 then (1 : ℚ) else 0) := by
  simp [evalPoly, ms2]

end PositiveGeometryEmergentSpaceTime.Alignment.Sanity.LeanCert2K23
'''
