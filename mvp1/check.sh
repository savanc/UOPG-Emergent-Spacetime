#!/bin/sh
# Kernel check for MVP-1. The Lake project is mvp0/lean, so Mathlib is not
# built a second time. Fails on sorry, on a drifted witness, or on an axiom
# outside the standard three.
set -eu
root="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$root/mvp0/lean"

if grep -RIn --exclude-dir=.lake --exclude-dir=.git -E '\bsorry\b|\badmit\b' \
  UOPG0/Canonical.lean Main1.lean; then
  echo "sorry or admit found in MVP-1 sources" >&2
  exit 1
fi

lake build uopg1
out="$(lake exe uopg1)"
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q 'x = 1/2'
printf '%s\n' "$out" | grep -q 'z = 3/2'
printf '%s\n' "$out" | grep -q 'orthant coefficient = 16/3'
printf '%s\n' "$out" | grep -q 'Parke-Taylor coefficient = -16/3'
if printf '%s\n' "$out" | grep -q '80.4'; then
  echo "executable printed a fitted W mass; MVP-1 must not" >&2
  exit 1
fi

echo "---- axiom audit ----"
axioms="$(lake env lean --stdin <<'EOF'
import UOPG0
open UOPG0
#print axioms chart_adjacentProduct
#print axioms cyclicProduct_eq_neg_adjacent
#print axioms chart_minors_pos
#print axioms gauge_mul_eq_chart
#print axioms positive_gauge_chart
#print axioms eq_gaugeMatrix
#print axioms adjacentProduct_gl_weight
#print axioms orthantCoeff_residue
#print axioms orthantCoeff_witness
#print axioms parkeTaylorCoeff_witness
#print axioms positiveExample_gauge
EOF
)"
printf '%s\n' "$axioms"
AXIOMS="$axioms" python3 - <<'PY'
import os, sys
text = os.environ["AXIOMS"]
allowed = {"propext", "Classical.choice", "Quot.sound"}
rows = [line for line in text.splitlines() if "depends on axioms" in line]
if len(rows) != 11:
    sys.exit(f"expected 11 axiom lines, got {len(rows)}")
for line in rows:
    inner = line.split("[", 1)[1].split("]", 1)[0]
    names = {part.strip() for part in inner.split(",") if part.strip()}
    bad = names - allowed
    if bad:
        sys.exit(f"unexpected axioms: {sorted(bad)}")
if "sorry" in text or "native_decide" in text or "sorryAx" in text:
    sys.exit("sorry or native_decide in the axiom audit")
PY
