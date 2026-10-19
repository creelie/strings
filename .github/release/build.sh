#!/usr/bin/env bash
# Build the release assets of "Which String Vibrations Become Which Generations on the Dwork
# Quintic": the PDF, the LaTeX source with the figures as PNG (tex.zip) and the arXiv package with
# the checks, the engine record and the Lean file in anc/ (tar.gz).
#
# Usage: build.sh <version> <output directory>
# Needs pdflatex with revtex4-2, pdfinfo (poppler), zip and gzip.
set -euo pipefail

version=$1
mkdir -p "$2"
out=$(cd "$2" && pwd)
root=$(cd "$(dirname "$0")/../.." && pwd)
src=$root/paper
pdf=$root/preprintDworkGenerations/DworkGenerations.pdf
name=DworkGenerations-v$version
stamp=$(git -C "$root" log -1 --format=%cI)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

mkdir -p "$work/tex/figures" "$work/arxiv/anc/checks" "$work/arxiv/anc/bllm" "$work/arxiv/anc/lean"
cp "$src/main.tex" "$work/tex/"
cp "$src"/figures/*.png "$work/tex/figures/"
cp -r "$work/tex/." "$work/arxiv/"
cp "$root"/code/checks/* "$work/arxiv/anc/checks/"
cp "$root"/code/run_checks.sh "$work/arxiv/anc/"
cp "$root"/code/bllm/*.py "$root"/code/bllm/out/* "$work/arxiv/anc/bllm/"
cp "$root"/lean/{Strings.lean,lean-toolchain,axioms.txt} "$work/arxiv/anc/lean/"

# The source has to compile from these files alone, with no BibTeX pass and no shell escape, to
# the same number of pages as the committed PDF, with no undefined reference and no overfull box.
cp -r "$work/tex" "$work/build"
(
  cd "$work/build"
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex > /dev/null
  done
  pages() { pdfinfo "$1" | awk '/^Pages:/ {print $2}'; }
  test "$(pages main.pdf)" = "$(pages "$pdf")"
  if grep -iE 'undefined|overfull' main.log; then exit 1; fi
)

find "$work/tex" "$work/arxiv" -exec touch -h -d "$stamp" {} +
cp "$pdf" "$out/$name.pdf"
(cd "$work/tex" && find . -type f | LC_ALL=C sort | sed 's|^\./||' | TZ=UTC zip -X -q -9 "$out/$name-tex.zip" -@)
(cd "$work/arxiv" && tar --sort=name --mtime="$stamp" --owner=0 --group=0 --numeric-owner -cf - \
  main.tex figures anc | gzip -n -9 > "$out/$name-arxiv.tar.gz")
ls -l "$out"
