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
  python3 - "$out" <<'PY'   # LICENSE + NOTICE (copyright, credit wording) ship in every add-on
import sys, zipfile
with zipfile.ZipFile(sys.argv[1], "a") as z:
    for f in ("LICENSE", "NOTICE"): z.write(f, f)
PY
  echo "$out"
done
