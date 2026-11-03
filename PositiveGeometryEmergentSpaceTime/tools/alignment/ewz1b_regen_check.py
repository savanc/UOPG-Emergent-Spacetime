"""Phase B (2026-11-03): EW-Z1b script-level check. Regenerates the residual N from sims/ewz1b/mklean.py (code
up to `N=build()`) and compares it symbolically with the body of `def N` in lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean.
Same generator, so this checks transcription only, not the Feynman rules (SIMULATED)."""
import os, re, sys, pathlib
import sympy as S
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sims/ewz1b")); os.chdir(ROOT / "sims/ewz1b")
exec(open("mklean.py").read().split("N=build()")[0])
N = build()  # noqa: F821
lean = (ROOT / "lean/PositiveGeometryEmergentSpaceTime/EWZ1b.lean").read_text()
m = re.search(r"def N \(([^:]*): ℚ\) : ℚ :=\n\s*(.*?)\n\n", lean, re.S)
syms = {n: S.Symbol(n) for n in m.group(1).split()}
LN = S.sympify(m.group(2).replace("^", "**"), locals=syms)
NN = N.subs({x: syms[str(x)] for x in N.free_symbols})
print("free", sorted(map(str, N.free_symbols)))
ok = S.expand(NN - LN) == 0
print("DIFF_ZERO", ok); sys.exit(0 if ok else 1)
