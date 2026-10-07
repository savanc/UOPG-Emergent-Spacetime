#!/bin/sh
# Kernel check for MVP-0. Fails if a proof uses sorry or admit, if the build fails,
# or if the executable witness does not reproduce the proved minors.
set -eu
cd "$(dirname "$0")/lean"

if grep -RIn --exclude-dir=.lake --exclude-dir=.git -E '\bsorry\b|\badmit\b' UOPG0 UOPG0.lean Main.lean; then
  echo "sorry or admit found in MVP-0 sources" >&2
  exit 1
fi

lake build
out="$(lake exe uopg0)"
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q 'P01 = 1'
printf '%s\n' "$out" | grep -q 'P23 = 1'
if printf '%s\n' "$out" | grep -q '80.4'; then
  echo "executable printed a fitted W mass; MVP-0 must not" >&2
  exit 1
fi

echo "---- axiom audit ----"
lake env lean --stdin <<'EOF'
import UOPG0
open UOPG0
#print axioms plucker_relation
#print axioms plucker_gl_weight_det
#print axioms plucker_specialLinear_invariant
#print axioms positiveExample_minors_pos
#print axioms pairing_graph
#print axioms nullSeparation_iff
#print axioms singular_iff_exists_kernel
#print axioms edgeMomentum_det_eq_zero
#print axioms edgeMomentum_sum_eq_zero
#print axioms edge_nullSeparation
EOF

echo "---- geometry shadow ----"
cd ..
python3 viz/geometry.py --check
