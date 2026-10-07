#!/bin/sh
# Kernel check for the rank-one lemma. Not an MVP. Fails on sorry, on a
# drifted witness, or on an axiom outside the standard three. The MVP-4 card
# is not turned green by this script.
set -eu
root="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$root/mvp0/lean"

if grep -RIn --exclude-dir=.lake --exclude-dir=.git -E '\bsorry\b|\badmit\b' \
  UOPG0/RankOne.lean MainRank.lean; then
  echo "sorry or admit found in the rank-one lemma" >&2
  exit 1
fi

lake build UOPG0 rankone
out="$(lake exe rankone)"
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q 'edge 0 u=(-2, 0) v=(1, 0)'
printf '%s\n' "$out" | grep -q 'edge 1 u=(0, -2) v=(0, 1)'
printf '%s\n' "$out" | grep -q 'edge 2 u=(2, 0) v=(1, 0)'
printf '%s\n' "$out" | grep -q 'edge 3 u=(0, 2) v=(0, 1)'
printf '%s\n' "$out" | grep -q 'rescale=true'
printf '%s\n' "$out" | grep -q 'The rescaling is not a helicity.'
if printf '%s\n' "$out" | grep -q '80.4'; then
  echo "executable printed a fitted W mass; the lemma must not" >&2
  exit 1
fi

echo "---- axiom audit ----"
axioms="$(lake env lean --stdin <<'EOF'
import UOPG0
open UOPG0
#print axioms det2_outer
#print axioms outer_rescale
#print axioms exists_outer_of_det2_eq_zero
#print axioms det2_eq_zero_iff_exists_outer
#print axioms polygon_edge_outer
#print axioms polygon_edge_rescale
EOF
)"
printf '%s\n' "$axioms"
AXIOMS="$axioms" python3 - <<'PY'
import os, sys
text = os.environ["AXIOMS"]
allowed = {"propext", "Classical.choice", "Quot.sound"}
rows = [line for line in text.splitlines() if "depends on axioms" in line]
if len(rows) != 6:
    sys.exit(f"expected 6 axiom lines, got {len(rows)}")
for line in rows:
    inner = line.split("[", 1)[1].split("]", 1)[0]
    names = {part.strip() for part in inner.split(",") if part.strip()}
    bad = names - allowed
    if bad:
        sys.exit(f"unexpected axioms: {sorted(bad)}")
if "sorry" in text or "native_decide" in text or "sorryAx" in text:
    sys.exit("sorry or native_decide in the axiom audit")
PY
