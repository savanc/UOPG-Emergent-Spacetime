import UOPG0.RankOne

/-!
Executable witness for the rank-one lemma. The factors are the ones proved in
`polygon_edge_outer`. The rescaling is `outer_rescale` at `t = 2`. This program
does not print a helicity, and it does not print a mass.
-/

open UOPG0

def rescaleAgrees (i : Fin 4) : Bool :=
  let p := outer (edgeFactorU i) (edgeFactorV i)
  let q := outer (fun a => (2 : ℚ) * edgeFactorU i a) (fun b => edgeFactorV i b / 2)
  p 0 0 == q 0 0 && p 0 1 == q 0 1 && p 1 0 == q 1 0 && p 1 1 == q 1 1

def showEdge (i : Fin 4) : String :=
  let p := outer (edgeFactorU i) (edgeFactorV i)
  s!"edge {i} u=({edgeFactorU i 0}, {edgeFactorU i 1}) v=({edgeFactorV i 0}, {edgeFactorV i 1}) " ++
    s!"outer=[[{p 0 0}, {p 0 1}], [{p 1 0}, {p 1 1}]] rescale={rescaleAgrees i}"

def main : IO Unit := do
  let u0 := edgeFactorU 0
  let moved := fun a => (2 : ℚ) * u0 a
  IO.println "UOPG lemma — a null edge is an outer product"
  IO.println (showEdge 0)
  IO.println (showEdge 1)
  IO.println (showEdge 2)
  IO.println (showEdge 3)
  IO.println s!"t=2 moves edge 0 u from ({u0 0}, {u0 1}) to ({moved 0}, {moved 1})"
  IO.println "A function of the momentum does not determine t."
  IO.println "The rescaling is not a helicity."
