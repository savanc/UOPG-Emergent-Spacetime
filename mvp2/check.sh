#!/bin/sh
# Kernel check for MVP-2. The Lake project is mvp0/lean, so Mathlib is not
# built a second time. Fails on sorry, on a drifted witness, or on an axiom
# outside the standard three.
set -eu
root="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$root/mvp0/lean"

if grep -RIn --exclude-dir=.lake --exclude-dir=.git -E '\bsorry\b|\badmit\b' \
  UOPG0/Boundary.lean Main2.lean; then
  echo "sorry or admit found in MVP-2 sources" >&2
  exit 1
fi

lake build UOPG0 uopg2
out="$(lake exe uopg2)"
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q 'drop x = 8/3'
printf '%s\n' "$out" | grep -q 'drop y = 8/3'
printf '%s\n' "$out" | grep -q 'drop z = 8'
printf '%s\n' "$out" | grep -q 'drop w = 8/3'
printf '%s\n' "$out" | grep -q 'P13 on the x = 0 face = 3/4'
printf '%s\n' "$out" | grep -q 'column shift P23 = 0'
if printf '%s\n' "$out" | grep -q '80.4'; then
  echo "executable printed a fitted W mass; MVP-2 must not" >&2
  exit 1
fi

echo "---- axiom audit ----"
axioms="$(lake env lean --stdin <<'EOF'
import UOPG0
open UOPG0
#print axioms chart_adjacentProduct_eq_zero_iff
#print axioms chart_pole_iff_adjacent_minor
#print axioms residue_drop_x
#print axioms residue_drop_y
#print axioms residue_drop_z
#print axioms residue_drop_w
#print axioms nonadjacent_zero_off_chamber
#print axioms face_x_P13_pos
#print axioms face_y_P13_pos
#print axioms face_z_P13_pos
#print axioms face_w_P13_pos
#print axioms witness_columnShift_P23
#print axioms witness_columnShift_quadric
#print axioms witness_columnShift_leaves_positive
#print axioms residue_drop_x_witness
#print axioms residue_drop_z_witness
#print axioms face_x_P13_witness
EOF
)"
printf '%s\n' "$axioms"
AXIOMS="$axioms" python3 - <<'PY'
import os, sys
text = os.environ["AXIOMS"]
allowed = {"propext", "Classical.choice", "Quot.sound"}
rows = [line for line in text.splitlines() if "depends on axioms" in line]
if len(rows) != 17:
    sys.exit(f"expected 17 axiom lines, got {len(rows)}")
for line in rows:
    inner = line.split("[", 1)[1].split("]", 1)[0]
    names = {part.strip() for part in inner.split(",") if part.strip()}
    bad = names - allowed
    if bad:
        sys.exit(f"unexpected axioms: {sorted(bad)}")
if "sorry" in text or "native_decide" in text or "sorryAx" in text:
    sys.exit("sorry or native_decide in the axiom audit")
PY
