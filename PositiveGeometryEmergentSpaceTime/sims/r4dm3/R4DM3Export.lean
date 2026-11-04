import PositiveGeometryEmergentSpaceTime
open Lean Elab Command Meta

/-! R4-DM v3 structured exporter (locked, prereg/R4-DM3-2026-10-20.md; export block byte-identical to sims/r4dm/R4DMExport.lean). Read-only: changes no declaration.
For every user-facing `PositiveGeometryEmergentSpaceTime.*` declaration it writes one JSON line with the statement split into binders
(name, Prop-or-not, pretty type, constants, earlier binders referenced) and conclusion (pretty, constants,
binders referenced), plus type/value uses looking through auxiliary constants (as `lean/GraphExport.lean`).
Auxiliary declarations are recognised structurally (internal / implementation detail / matcher / no source
range with a `match_`/`proof_`/`eq_` component), so a user theorem whose name merely contains `match_` is kept.
Run from `lean/`: `lake env lean ../sims/r4dm3/R4DM3Export.lean` → `../graph/r4dm3_decls.jsonl`. -/

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
  r4dmExport "../graph/r4dm3_decls.jsonl" fun env n =>
    match env.getModuleIdxFor? n with
    | some idx =>
      let m := (env.header.moduleNames[idx.toNat]!).toString
      if m.startsWith "PositiveGeometryEmergentSpaceTime" then some m else none
    | none => none
