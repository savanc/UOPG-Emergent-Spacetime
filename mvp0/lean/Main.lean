import UOPG0.Basic

/-!
Executable witness for the positive chamber. The numbers below are the minors
already proved in `UOPG0.Positive`. This program does not fit a mass.
-/

open UOPG0

def main : IO Unit := do
  IO.println "UOPG MVP-0 — Gr+(2,4) positive witness"
  IO.println s!"P01 = {plucker positiveExample 0 1}"
  IO.println s!"P02 = {plucker positiveExample 0 2}"
  IO.println s!"P03 = {plucker positiveExample 0 3}"
  IO.println s!"P12 = {plucker positiveExample 1 2}"
  IO.println s!"P13 = {plucker positiveExample 1 3}"
  IO.println s!"P23 = {plucker positiveExample 2 3}"
  IO.println "Each polygon edge has det = 0 by edgeMomentum_det_eq_zero."
  IO.println "Sum of the four edge momenta is 0 by edgeMomentum_sum_eq_zero."
  IO.println "No fitted scale. A GeV mass is not a theorem of MVP-0."
