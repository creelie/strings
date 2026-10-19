#!/usr/bin/env bash
# Runs every independent check of the paper and prints one summary line.
#   C          checks/labels.c     the 101 labels, their characters, the couplings
#                                  allowed by the group, the mass map (Theorems A, B)
#   C++        checks/hessian.cpp  the Hessian by its 120 permutations, Table I
#   Python     checks/verify.py    socle, Hessian, Seifert form, Fermat norms
#   Python     checks/weighted.py  the weighted Fermat pencils: labels, characters,
#                                  mass map, three families on free quotients
#   Julia      checks/fermat.jl    the Fermat norms from a Lanczos Gamma, Table II
#   Macaulay2  checks/socle.m2     the Jacobian ring and its socle
#   Macaulay2  checks/weighted.m2  the Jacobian rings of the weighted pencils
#   Lean 4     ../lean/Strings.lean the finite counts and the moved-point rule
# Tools are taken from PATH, or from CC, CXX, PYTHON, JULIA, M2, LEAN.
# A tool that is missing is reported and its checks are skipped.
set -u
cd "$(dirname "$0")"
CC=${CC:-gcc}; CXX=${CXX:-g++}; PYTHON=${PYTHON:-python3}
JULIA=${JULIA:-julia}; M2=${M2:-M2}; LEAN=${LEAN:-lean}
BUILD=$(mktemp -d); trap 'rm -rf "$BUILD"' EXIT
LOG="$BUILD/all.log"; : > "$LOG"
skipped=()

run() {   # run <name> <command...>
  local name=$1; shift
  echo "== $name" | tee -a "$LOG"
  "$@" 2>&1 | tee -a "$LOG"
  return "${PIPESTATUS[0]}"
}
have() { command -v "$1" >/dev/null 2>&1; }

status=0
if have "$CC"; then
  "$CC" -O2 -o "$BUILD/labels" checks/labels.c && run "C: labels and couplings" "$BUILD/labels" || status=1
else skipped+=("C"); fi
if have "$CXX"; then
  "$CXX" -O2 -std=c++17 -o "$BUILD/hessian" checks/hessian.cpp && run "C++: Hessian" "$BUILD/hessian" || status=1
else skipped+=("C++"); fi
if have "$PYTHON"; then
  run "Python: socle, Hessian, Seifert form, Fermat norms" "$PYTHON" checks/verify.py || status=1
  run "Python: weighted Fermat pencils" "$PYTHON" checks/weighted.py || status=1
else skipped+=("Python"); fi
if have "$JULIA"; then
  run "Julia: Fermat norms" "$JULIA" --startup-file=no checks/fermat.jl || status=1
else skipped+=("Julia"); fi
if have "$M2"; then
  run "Macaulay2: Jacobian ring" "$M2" --script checks/socle.m2 || status=1
  run "Macaulay2: weighted Jacobian rings" "$M2" --script checks/weighted.m2 || status=1
else skipped+=("Macaulay2"); fi
if have "$LEAN"; then
  echo "== Lean 4: ../lean/Strings.lean" | tee -a "$LOG"
  ( cd ../lean && "$LEAN" Strings.lean ) > "$BUILD/lean.out" 2>&1 || status=1
  cat "$BUILD/lean.out" | tee -a "$LOG"
  nthm=$(grep -c '^theorem ' ../lean/Strings.lean)
  nok=$(grep -cE "does not depend on any axioms|depends on axioms: \[propext\]$" "$BUILD/lean.out")
  if [ "$nthm" = "$nok" ] && ! grep -q error "$BUILD/lean.out"; then
    echo "PASS Lean: $nthm theorems, each axiom-free or on propext only" | tee -a "$LOG"
  else
    echo "FAIL Lean: $nok of $nthm theorems checked" | tee -a "$LOG"; status=1
  fi
else skipped+=("Lean"); fi

pass=$(grep -c '^PASS' "$LOG"); fail=$(grep -c '^FAIL' "$LOG")
[ ${#skipped[@]} -gt 0 ] && echo "skipped (tool not found): ${skipped[*]}"
echo "$pass checks passed, $fail failed"
[ "$fail" = 0 ] && [ "$status" = 0 ]
