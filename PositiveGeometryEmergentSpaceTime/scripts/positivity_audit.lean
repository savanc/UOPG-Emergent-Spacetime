-- Run from savanc/UOPG-Emergent-Spacetime/mvp0/lean after `lake build UOPG0`:
--   lake env lean /path/to/positivity_audit.lean
-- For every UOPG0 theorem, it reports whether an order relation (<, ≤) appears in a hypothesis or in the conclusion, and whether an ordered-field class is assumed.
-- It also lists the UOPG0 dependencies of four core theorems.
import UOPG0
open Lean Elab Command Meta

/-- does expression mention constant c anywhere -/
def mentions (e : Expr) (cs : List Name) : Bool :=
  (e.find? fun x => match x with | .const n _ => cs.contains n | _ => false).isSome

partial def hypsMention (e : Expr) (cs : List Name) : Bool :=
  match e with
  | .forallE _ t b bi => (bi.isExplicit && mentions t cs) || (bi.isExplicit == false && false) || hypsMention b cs || (mentions t cs && !t.isSort && bi.isExplicit)
  | _ => false

elab "#pos_audit" : command => do
  let env ← getEnv
  let ord := [``LT.lt, ``LE.le]
  let ordClass := [``LinearOrder, ``PartialOrder, ``IsStrictOrderedRing, ``IsOrderedRing, ``Preorder]
  let mut lines : Array String := #[]
  let mut total := 0
  let mut hypOrd := 0
  let mut concOrd := 0
  let mut classOrd := 0
  for (name, ci) in env.constants.toList do
    if (`UOPG0).isPrefixOf name && !name.isInternal then
      if let .thmInfo ti := ci then
        total := total + 1
        let ty := ti.type
        -- split binders
        let (hyps, concl) := Id.run do
          let mut e := ty; let mut hs : Array Expr := #[]
          while e.isForall do
            hs := hs.push e.bindingDomain!; e := e.bindingBody!
          return (hs, e)
        let h := hyps.any (fun t => mentions t ord)
        let c := mentions concl ord
        let k := hyps.any (fun t => mentions t ordClass)
        if h then hypOrd := hypOrd + 1
        if c then concOrd := concOrd + 1
        if k then classOrd := classOrd + 1
        lines := lines.push s!"{name}\thypOrder={h}\tconclOrder={c}\torderedFieldClass={k}"
  let sorted := lines.qsort (· < ·)
  for l in sorted do logInfo l
  logInfo s!"TOTAL={total} hypOrder={hypOrd} conclOrder={concOrd} orderedFieldClass={classOrd}"
#pos_audit

-- dependency check: does plucker_relation's proof reach any order constant or positivity lemma?
open Lean in
partial def collectDeps (env : Environment) (n : Name) (acc : NameSet) : NameSet := Id.run do
  if acc.contains n then return acc
  let mut acc := acc.insert n
  match env.find? n with
  | some ci =>
    let mut s := ci.type.getUsedConstants.toList
    if let some v := ci.value? then s := s ++ v.getUsedConstants.toList
    for m in s do
      if (`UOPG0).isPrefixOf m then acc := collectDeps env m acc
    return acc
  | none => return acc

elab "#deps " id:ident : command => do
  let env ← getEnv
  let n := id.getId
  let ds := collectDeps env n {}
  let ci := env.find? n
  let used : List Name := match ci with
    | some c =>
        let v : Array Name := match c.value? with
          | some e => e.getUsedConstants
          | none => #[]
        (c.type.getUsedConstants ++ v).toList
    | none => []
  logInfo s!"{n}: UOPG0 deps = {ds.toList.filter (· != n)}; uses LT.lt? {used.contains ``LT.lt}; uses LE.le? {used.contains ``LE.le}"
#deps UOPG0.plucker_relation
#deps UOPG0.nullSeparation_iff
#deps UOPG0.det2_eq_zero_iff_exists_outer
#deps UOPG0.parkeTaylorCoeff_eq_inv_cyclic
