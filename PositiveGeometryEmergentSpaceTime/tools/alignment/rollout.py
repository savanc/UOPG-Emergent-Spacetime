"""Write notes/alignment/ROLLOUT-BLUEPRINT-2026-11-03.md from blueprint.tsv + defs_glossary.G (no hand-copying of rewordings)."""
import csv, collections, pathlib, json
from defs_glossary import G
ROOT = pathlib.Path(__file__).resolve().parents[2]; N = ROOT / "notes/alignment"
R = list(csv.DictReader(open(N / "blueprint.tsv"), delimiter="\t"))
J = ("CLAIM", "LISTING", "SCOPE", "DEF")
judged = [r for r in R if r["row_type"] in J]
cnt = collections.Counter(r["verdict"] for r in judged)
rt = collections.Counter(r["row_type"] for r in R)
rungs = sorted({r["rung"] for r in judged} - {"GENERAL"})
INDEX = [l.split("|")[1].strip() for l in (ROOT / "notes/BLOCKER-INDEX-2026-10-13.md").read_text().split("## Table", 1)[1].splitlines() if l.startswith("| ")][2:]
covered = {"H-T5 (d)": "H-T5", "CASCADE-1b": "CASCADE-1b r2", "CHIRAL-LATTICE-1 v2": "CHIRAL-LATTICE-1"}
uncovered = [x for x in INDEX if covered.get(x, x) not in rungs]
mods = {p.stem for p in (ROOT / "lean/PositiveGeometryEmergentSpaceTime").glob("*.lean")}
norm = lambda s: s.replace("-", "").replace("′", "p").replace("'", "p").replace(" ", "").upper()
modn = {norm(m): m for m in mods}
def guess(r):
    k = norm(r.split(" ")[0].split("/")[0])
    return [m for nk, m in modn.items() if nk.startswith(k) and len(k) >= 2]
st = collections.Counter(g[4] for g in G)
L = ["# Rollout: prose-to-Lean blueprint rows for every rung (2026-11-03)", "",
     "Scope (author approved 2026-11-03): blueprint rows only, every rung, plus glossary and DEF rows. No sanity theorems, no blind versions, no paper edits (edits are proposed below), no new builds.",
     "", "## What was run", "",
     "- `tools/alignment/extract.py`: parses all `lean/PositiveGeometryEmergentSpaceTime/**/*.lean` (declaration index) and the three papers (every PROVED / `\\lean` / 'Lean proves' / listing sentence) → `out/claims.json`.",
     "- `tools/alignment/verdicts.py`, `defs_glossary.py`: the judgements (one entry per claim row, DEF row and glossary term; every Lean name checked against the index).",
     "- `tools/alignment/build.py` → `blueprint.tsv`, `BLUEPRINT-ALL.md`, `GLOSSARY.md`, `out/BlueprintCheck.lean`; `rollout.py` → this file.",
     "- One batched check, `cd lean && lake env lean ../tools/alignment/out/BlueprintCheck.lean` (44 s wall, CPU, existing oleans): **all 409 cited declarations exist; 384 use only standard axioms (propext / Classical.choice / Quot.sound), 25 use none; no sorryAx, no error.** Output: `tools/alignment/out/BlueprintCheck.out`.",
     "- `lean/AxiomsAll_output.txt` unchanged: TOTAL theorems=1378 defs=798 nonstandard=0, sorry_dependent=0. No Lean file edited; `PositiveGeometryEmergentSpaceTime.lean` untouched.", "",
     "## Counts", "",
     f"- Rows: {len(R)} total = " + ", ".join(f"{k} {v}" for k, v in sorted(rt.items())) + ". PAPER and META rows are listed but not judged.",
     f"- Rungs with judged rows: {len(rungs)} (+ GENERAL rows about the whole programme): " + ", ".join(rungs) + ".",
     f"- Verdicts over the {len(judged)} judged rows: " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())) + ". UNDERSTATES 0, MISSING-LEAN 0.",
     "- By type: " + "; ".join(f"{t}: " + ", ".join(f"{k} {v}" for k, v in sorted(collections.Counter(r['verdict'] for r in judged if r['row_type'] == t).items())) for t in J) + ".",
     f"- Glossary ({len(G)} terms): " + ", ".join(f"{k} {v}" for k, v in sorted(st.items())) + ".",
     "- Pilot reuse: SURF-1′, HG-DIM-1 and RG-IR-1 rows cite `PILOT-2026-10-31.md` and the Alignment modules; no new pilot work.", "",
     "## Non-MATCH claim rows and proposed rewordings (papers not edited)", ""]
for r in judged:
    if r["row_type"] != "DEF" and r["verdict"] != "MATCH":
        L += [f"### {r['paper:line']} — {r['rung']} — {r['verdict']}", "", f"- Reason: {r['note']}", f"- Lean: {r['lean_decls'][:300]}", f"- Proposed rewording: {r['proposed_rewording']}", ""]
L += ["MISSING-LEAN: none. Every prose PROVED / `\\lean` claim the extractor found resolves to existing, axiom-clean declarations; the gaps are in what the prose says those declarations mean.", "",
      "## DEF rows not MATCH (hidden-definition risk)", "",
      "NAME-ONLY means a headline theorem is about this Lean object, and its identification with the object the paper names is in a name, docstring or generating script only.", ""]
for r in judged:
    if r["row_type"] == "DEF" and r["verdict"] != "MATCH":
        L.append(f"- `{r['lean_decls']}` ({r['rung']}, {r['paper:line']}): {r['note']}")
L += ["", "Proposed treatment (no new Lean): say once per affected rung, next to the PROVED tag, that the object is entered by hand / by script, e.g. HG-DIM-1: 'closed neighbourhoods listed by hand and checked against the flip graph by script'; FL-1Z: 'the matrix of Eq. (D.3) of [2502.12662] transcribed at τ=ω'; EW-Z1b: 'residual generated from the Feynman rules by `sims/ewz1b/mklean.py`'. A cheap Lean fix for HG-DIM-1 (`NA_neg = closed nbhd of 2` by `decide`) belongs to the sanity-theorem step.", "",
      "## Glossary edits (MISSING-IN-PAPER and MISMATCH)", ""]
for term, key, plain, defs, status, note in G:
    if status != "DEFINED": L.append(f"- **{term}** — {status}: {note}")
L += ["", "## Rungs with no blueprint row", "",
      f"{len(uncovered)} of the {len(INDEX)} rungs in `notes/BLOCKER-INDEX-2026-10-13.md` carry no PROVED / Lean claim in the three papers, so they have no blueprint row. "
      "Where a Lean module with a matching name exists it is shown (name match only, not checked against the rung record); 'not located' means no module name matches.", "",
      "| rung | Lean module by name |", "|---|---|"]
for u in uncovered:
    g = guess(u); L.append(f"| {u} | {', '.join(g) if g else 'not located'} |")
L += ["", "Also judged but not in the blocker index: MR-1b, BR-4, CURV-LEAN (curvature paper Lean section).", "",
      "## Cost estimate for the sanity-theorem step (next, not done)", "",
      "Pilot (2026-10-31): 3 rungs, 113 sanity/equivalence theorems, about 6–7 agent-hours plus one large CPU build. Proposed scope: the 9 OVERSTATES rungs' headline theorems plus the 7 NAME-ONLY DEF rows, i.e. about 10–12 rungs with 3–6 theorems each (known value, planted wrong case, non-vacuity, and for DEF rows one tie theorem such as `NA_neg = closedNbhd 2`).",
      "Estimate: about 1.5–2 agent-hours per rung, so roughly 15–24 agent-hours in total, using the same CPU box (8 CPUs, 15 GB). Use one batched `lake build` of a single new `Alignment/Sanity2` module per batch of rungs; with existing oleans that is minutes per batch. Do not rebuild Mathlib. The largest risk is kernel time for `decide` on the HG-DIM n=9 data; reuse the pilot's HgKernel split.", ""]
(N / "ROLLOUT-BLUEPRINT-2026-11-03.md").write_text("\n".join(L) + "\n")
print(len(uncovered), sum(1 for u in uncovered if not guess(u)))
