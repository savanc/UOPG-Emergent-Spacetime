"""Generate the exact-arithmetic part of lean/PositiveGeometryEmergentSpaceTime/SliceBridge.lean from the configurations in m1b_kinematics.py."""
from fractions import Fraction as F
def q(x):
    x = F(x)
    return f"({x.numerator} : ℚ)" if x.denominator == 1 else f"({x.numerator} / {x.denominator} : ℚ)"
def vec(p): return "![" + ", ".join(q(c) for c in p) + "]"
n4 = [(5,0,0,5),(-5,-3,0,-4),(5,0,0,-5),(-5,3,0,4)]
n6 = [('5','5','0','0'),('-5','50/51','50/51','-245/51'),('3','0','0','-3'),('-4','-4/3','-8/3','-8/3'),
      ('2036/295','-4072/885','2036/885','4072/885'),('-1741/295','-691/15045','-9242/15045','88306/15045')]
lam_pos = [('1','-3'),('-1','-3'),('-4','4'),('-1','-1'),('4','3')]; lt_pos = [('-19/3','7/2'),('14/3','-5/2'),('-2','1'),('-3','-2'),('0','-1')]
lam_neg = [('-2','1'),('0','-3'),('-2','1'),('1','-4'),('-3','4')]; lt_neg = [('4','-11/2'),('-7/3','5/2'),('-3','1'),('2','0'),('0','3')]
out = []
def kin(name, ps, planar_sets):
    n = len(ps)
    out.append(f"/-- {name}: real (1,3) null momenta (mostly minus, all incoming), exact. -/")
    out.append(f"def {name} : Fin {n} → Fin 4 → ℚ := ![" + ", ".join(vec(p) for p in ps) + "]")
    out.append(f"theorem {name}_null : ∀ i, mdotQ ({name} i) ({name} i) = 0 := by\n  intro i; fin_cases i <;> norm_num [{name}, mdotQ]")
    out.append(f"theorem {name}_cons : ∀ μ, ∑ i, {name} i μ = 0 := by\n  intro μ; fin_cases μ <;> norm_num [{name}, Fin.sum_univ_succ]")
    conds = []
    for S in planar_sets:
        terms = " + ".join(f"{name} {i}" for i in S)
        conds.append(f"mdotQ ({terms}) ({terms}) < 0")
    out.append(f"theorem {name}_euclidean :\n    " + " ∧\n    ".join(conds) + f" := by\n  norm_num [{name}, mdotQ]")
kin("cfg4", n4, [(0,1),(1,2)])
kin("cfg6", n6, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,1,2),(1,2,3),(2,3,4)])
def split(name, lam, lt, sign):
    out.append(f"/-- {name}: real (2,2) spinors, n = 5, `p_i = λ_i λ̃_iᵀ`, exact. -/")
    out.append(f"def {name}L : Fin 5 → Fin 2 → ℚ := ![" + ", ".join(vec(v) for v in lam) + "]")
    out.append(f"def {name}T : Fin 5 → Fin 2 → ℚ := ![" + ", ".join(vec(v) for v in lt) + "]")
    out.append(f"theorem {name}_cons : ∀ a b : Fin 2, ∑ i, {name}L i a * {name}T i b = 0 := by\n  intro a b; fin_cases a <;> fin_cases b <;> norm_num [{name}L, {name}T, Fin.sum_univ_succ]")
    rel = "0 <" if sign > 0 else "0 >"
    conds = [f"{rel} br2 ({name}L {i}) ({name}L {(i+1)%5}) * br2 ({name}T {i}) ({name}T {(i+1)%5})" for i in range(5)]
    out.append(f"theorem {name}_planar :\n    " + " ∧\n    ".join(conds) + f" := by\n  norm_num [{name}L, {name}T, br2]")
split("splitPos", lam_pos, lt_pos, 1)
split("splitNeg", lam_neg, lt_neg, -1)
open('scripts/m1b_lean_configs.txt', 'w').write("\n\n".join(out) + "\n")
print("\n\n".join(out))
