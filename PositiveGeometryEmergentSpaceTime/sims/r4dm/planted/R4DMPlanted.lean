import PositiveGeometryEmergentSpaceTime
open Lean Elab Command Meta

/-! R4-DM planted cases (locked, prereg/R4-DM-2026-10-20.md). NOT part of the PositiveGeometryEmergentSpaceTime library (not imported by
`PositiveGeometryEmergentSpaceTime.lean`, not counted by AxiomsAll). Toy declarations with KNOWN verdicts, exported with the SAME export block
as `sims/r4dm/R4DMExport.lean` (byte-identical; the checker verifies it) to `sims/r4dm/planted/planted_decls.jsonl`.
Module name written for these: `PositiveGeometryEmergentSpaceTime.R4DMPlanted`.
Run from `lean/`: `lake env lean ../sims/r4dm/planted/R4DMPlanted.lean`. -/

namespace PositiveGeometryEmergentSpaceTime.R4DMPlanted
open PositiveGeometryEmergentSpaceTime.IsingTiling8

/-- Planted toy "geometry → charge" map: a hypercharge read off the OG≥0(4,8) signature, `ogSignature 0 / 6`. -/
def yQgeo : ℚ := ogSignature 0 / 6

theorem yQgeo_eq : yQgeo = 1 / 6 := by
  simp [yQgeo, ogSignature]

/-- P1 GENUINE (must count, UNCONDITIONAL, PG): the geometric hypercharge is 1/6 and the SM-ratio assignment built
from it satisfies the STRUCT-1 anomaly conditions. The SM fact is the CONCLUSION; no SM input is assumed. -/
theorem planted_genuine :
    yQgeo = 1 / 6 ∧ PositiveGeometryEmergentSpaceTime.STRUCT1.ACC yQgeo (-4 * yQgeo) (2 * yQgeo) (-3 * yQgeo) (6 * yQgeo) := by
  refine ⟨yQgeo_eq, ?_⟩
  rw [yQgeo_eq]; unfold PositiveGeometryEmergentSpaceTime.STRUCT1.ACC; norm_num

/-- P2 GENUINE CONDITIONAL (must count, CONDITIONAL on a geometric hypothesis): any `y` with `6 y = ogSignature 0`
is the SM normalisation and gives an anomaly-free assignment. -/
theorem planted_conditional (y : ℚ) (h : y * 6 = ogSignature 0) :
    y = 1 / 6 ∧ PositiveGeometryEmergentSpaceTime.STRUCT1.ACC y (-4 * y) (2 * y) (-3 * y) (6 * y) := by
  have h0 : ogSignature 0 = 1 := by simp [ogSignature]
  have hy : y = 1 / 6 := by rw [h0] at h; linarith
  refine ⟨hy, ?_⟩
  rw [hy]; unfold PositiveGeometryEmergentSpaceTime.STRUCT1.ACC; norm_num

/-- S1 SMUGGLED (literal): assumes the SM charge value 1/6 as a hypothesis. Must be rejected. -/
theorem planted_smuggled_literal (y : ℚ) (_hg : y * 6 = ogSignature 0) (h : y = 1 / 6) :
    y = 1 / 6 ∧ PositiveGeometryEmergentSpaceTime.STRUCT1.ACC y (-4 * y) (2 * y) (-3 * y) (6 * y) := by
  refine ⟨h, ?_⟩
  rw [h]; unfold PositiveGeometryEmergentSpaceTime.STRUCT1.ACC; norm_num

/-- S2 SMUGGLED (SM-INPUT hypothesis): assumes the anomaly conditions themselves. Must be rejected. -/
theorem planted_smuggled_acc (yQ yu yd yL ye : ℚ) (h : PositiveGeometryEmergentSpaceTime.STRUCT1.ACC yQ yu yd yL ye)
    (hg : ogSignature 0 = 1) : PositiveGeometryEmergentSpaceTime.STRUCT1.ACC yQ yu yd yL ye ∧ ogSignature 0 = 1 :=
  ⟨h, hg⟩

/-- S3 SMUGGLED (SM-data hypothesis): assumes `N_c = 3`. Must be rejected. -/
theorem planted_smuggled_nc (N_c : ℚ) (h : N_c = 3) : N_c * ogSignature 0 = 3 := by
  rw [h]; simp [ogSignature]

/-- F1 SM-INPUT-FED: the proof uses an SM-INPUT theorem (`STRUCT1.sm_is_anomaly_free`). Must not count. -/
theorem planted_fed : ogSignature 0 = 1 ∧ PositiveGeometryEmergentSpaceTime.STRUCT1.ACC (1 / 6) (-2 / 3) (1 / 3) (-1 / 2) 1 :=
  ⟨by simp [ogSignature], PositiveGeometryEmergentSpaceTime.STRUCT1.sm_is_anomaly_free⟩

/-- N1 NON-CONSTRAINING: holds for every `yQ` (an identity in the SM datum). Must not count as DERIVED. -/
theorem planted_nonconstraining (yQ : ℚ) : yQ * ogSignature 0 = yQ := by
  simp [ogSignature]

/-- G1 NO-GEOMETRY: an SM fact with no geometry dependency. Must not count. -/
theorem planted_nogeo : PositiveGeometryEmergentSpaceTime.STRUCT1.ACC (1 / 6) (-2 / 3) (1 / 3) (-1 / 2) 1 := by
  unfold PositiveGeometryEmergentSpaceTime.STRUCT1.ACC; norm_num

end PositiveGeometryEmergentSpaceTime.R4DMPlanted

#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_genuine
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_conditional
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_smuggled_literal
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_smuggled_acc
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_smuggled_nc
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_fed
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_nonconstraining
#print axioms PositiveGeometryEmergentSpaceTime.R4DMPlanted.planted_nogeo

-- R4DM-EXPORT-BLOCK-BEGIN
def r4dmAuxComponent (n : Name) : Bool :=
  n.components.any fun c =>
    let s := c.toString
    s.startsWith "match_" || s.startsWith "proof_" || s == "eq_1" || s == "eq_def" || s.startsWith "_"

def r4dmIsAux (env : Environment) (n : Name) : Bool :=
  n.isInternal || n.isImplementationDetail || Lean.Meta.isMatcherCore env n ||
    (r4dmAuxComponent n && (declRangeExt.find? env n).isNone)

partial def r4dmUsedThrough (env : Environment) (e : Expr) : NameSet := Id.run do
  let mut out : NameSet := {}
  let mut todo := e.getUsedConstants.toList
  let mut seen : NameSet := {}
  while !todo.isEmpty do
    let c := todo.head!
    todo := todo.tail!
    if seen.contains c then continue
    seen := seen.insert c
    if r4dmIsAux env c && (`PositiveGeometryEmergentSpaceTime).isPrefixOf c then
      if let some ci := env.find? c then
        todo := todo ++ ci.type.getUsedConstants.toList ++
          (match ci with | .thmInfo v => v.value.getUsedConstants.toList
                         | .defnInfo v => v.value.getUsedConstants.toList | _ => [])
    else out := out.insert c
  out

def r4dmEnc (s : NameSet) : Json := Json.arr (s.toList.map (fun c => Json.str c.toString)).toArray

def r4dmExport (path : String) (moduleOf : Environment → Name → Option String) : CommandElabM Unit := do
  let env ← getEnv
  let h ← IO.FS.Handle.mk path .write
  let mut k := 0
  let all := env.constants.map₁.toList ++ env.constants.map₂.toList
  for (n, ci) in all do
    let some m := moduleOf env n | continue
    unless (`PositiveGeometryEmergentSpaceTime).isPrefixOf n do continue
    if r4dmIsAux env n then continue
    let kind := match ci with
      | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quot" | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
    let (binders, cpp, cconsts, cfv) ← liftTermElabM do
      forallTelescope ci.type fun xs body => do
        let mut bs : Array Json := #[]
        let mut prev : Array (FVarId × String) := #[]
        for x in xs do
          let ld ← x.fvarId!.getDecl
          let ty ← instantiateMVars ld.type
          let isP ← Meta.isProp ty
          let pp ← ppExpr ty
          let refs := prev.filter (fun (f, _) => ty.containsFVar f) |>.map (·.2)
          bs := bs.push <| Json.mkObj [("name", ld.userName.toString), ("prop", isP), ("type", toString pp),
            ("consts", r4dmEnc (ty.getUsedConstants.foldl (·.insert ·) {})),
            ("refs", Json.arr (refs.map Json.str))]
          prev := prev.push (x.fvarId!, ld.userName.toString)
        let b ← instantiateMVars body
        let bpp ← ppExpr b
        let crefs := prev.filter (fun (f, _) => b.containsFVar f) |>.map (·.2)
        pure (bs, toString bpp, b.getUsedConstants.foldl (·.insert ·) ({} : NameSet), crefs)
    let stmt ← liftTermElabM do pure (toString (← ppExpr ci.type))
    let tUse := r4dmUsedThrough env ci.type
    let vUse := match ci with
      | .thmInfo v => r4dmUsedThrough env v.value | .defnInfo v => r4dmUsedThrough env v.value | _ => {}
    let j := Json.mkObj [("name", n.toString), ("module", m), ("kind", kind), ("statement", stmt),
      ("binders", Json.arr binders), ("concl", cpp), ("concl_consts", r4dmEnc cconsts),
      ("concl_refs", Json.arr (cfv.map Json.str)), ("type_uses", r4dmEnc tUse), ("value_uses", r4dmEnc vUse)]
    h.putStrLn j.compress
    k := k + 1
  IO.println s!"r4dm exported {k} declarations to {path}"
-- R4DM-EXPORT-BLOCK-END

#eval show CommandElabM Unit from do
  r4dmExport "../sims/r4dm/planted/planted_decls.jsonl" fun env n =>
    match env.getModuleIdxFor? n with
    | some _ => none
    | none => if (`PositiveGeometryEmergentSpaceTime.R4DMPlanted).isPrefixOf n then some "PositiveGeometryEmergentSpaceTime.R4DMPlanted" else none
