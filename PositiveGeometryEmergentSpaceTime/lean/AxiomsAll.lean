import PositiveGeometryEmergentSpaceTime
open Lean Elab Command

-- Lists every user-facing declaration in modules `PositiveGeometryEmergentSpaceTime.*` with its axioms (run: lake env lean AxiomsAll.lean).
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut rows : Array String := #[]
  let mut nThm := 0
  let mut nDef := 0
  let mut bad := 0
  let mut nAx := 0
  let mut nOpq := 0
  let mut nOther := 0
  let mut nSorry := 0
  for (n, ci) in env.constants.map₁.toList do
    let some idx := env.getModuleIdxFor? n | continue
    let m := env.header.moduleNames[idx.toNat]!
    unless m.toString.startsWith "PositiveGeometryEmergentSpaceTime" do continue
    if n.isInternal || n.isImplementationDetail then continue
    let s := n.toString
    if s.endsWith ".eq_1" || s.endsWith ".eq_def" || (s.splitOn "match_").length > 1 || (s.splitOn "proof_").length > 1 then continue
    let kind := match ci with
      | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quot" | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
    -- Audit A-10 (2026-10-13): nothing is skipped silently any more; every kind is counted and listed.
    if kind == "thm" then nThm := nThm + 1
    else if kind == "def" then nDef := nDef + 1
    else if kind == "axiom" then nAx := nAx + 1
    else if kind == "opaque" then nOpq := nOpq + 1
    else nOther := nOther + 1
    let ax ← collectAxioms n
    let std := ax.all (fun a => a == ``propext || a == ``Classical.choice || a == ``Quot.sound)
    unless std do bad := bad + 1
    if ax.contains ``sorryAx then nSorry := nSorry + 1
    rows := rows.push s!"{m} | {kind} | {n} | {ax.toList}"
  for r in rows.qsort (· < ·) do IO.println r
  IO.println s!"TOTAL theorems={nThm} defs={nDef} nonstandard={bad}"
  IO.println s!"OTHER axiom_decls={nAx} opaque_decls={nOpq} other_kinds(inductive/ctor/rec/quot)={nOther} sorry_dependent={nSorry}"
