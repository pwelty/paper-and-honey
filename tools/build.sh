#!/usr/bin/env bash
# Package both add-ons as .xpi files in dist/ (zip of each folder, manifest at the root).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
for a in theme reading; do
  v=$(python3 -c "import json;print(json.load(open('$a/manifest.json'))['version'])")
  out="dist/paper-and-honey-$a-$v.xpi"
  rm -f "$out"
  (cd "$a" && python3 -m zipfile -c "../$out" $(ls))
  echo "$out"
done
