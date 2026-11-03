#!/usr/bin/env bash
# Rebuild the Lean library and re-run the axiom audits.
# Each result review in reviews/ gives the exact command for its locked checker under sims/.
set -euo pipefail
cd "$(dirname "$0")/lean"
lake exe cache get
lake build PositiveGeometryEmergentSpaceTime
lake env lean AxiomsAll.lean > AxiomsAll_output.check.txt
tail -2 AxiomsAll_output.check.txt
grep -q "TOTAL theorems=1378 defs=798 nonstandard=0" AxiomsAll_output.check.txt
grep -q "sorry_dependent=0" AxiomsAll_output.check.txt
echo "Main library axiom audit: OK"
# Alignment layer: modules outside the main import, audited by their own axiom files
lake build $(find PositiveGeometryEmergentSpaceTime/Alignment -name '*.lean' | sed 's#\.lean$##; s#/#.#g' | sort)
for f in Alignment*Axioms.lean AlignmentPhaseCAxioms/*.lean; do
  echo "== $f"; lake env lean "$f" | grep -v -E "^\s*$" | tail -3
done
