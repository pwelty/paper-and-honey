#!/usr/bin/env bash
# Package both add-ons as .xpi files in dist/ (zip of each folder, manifest at the root).
# --atn: builds for addons.thunderbird.net in dist/atn/ as *-atn.xpi, without update_url (ATN delivers
# its own updates and rejects add-ons that declare one).
set -euo pipefail
cd "$(dirname "$0")/.."
atn=""; [[ "${1:-}" == "--atn" ]] && atn=1
outdir=dist; [[ -n "$atn" ]] && outdir=dist/atn
mkdir -p "$outdir"
for a in theme reading; do
  v=$(python3 -c "import json;print(json.load(open('$a/manifest.json'))['version'])")
  out="$outdir/paper-and-honey-$a-$v${atn:+-atn}.xpi"
  rm -f "$out"
  (cd "$a" && python3 -m zipfile -c "../$out" $(ls))
  if [[ -n "$atn" ]]; then python3 - "$out" <<'PY'
import json, sys, zipfile, io
src = sys.argv[1]; buf = io.BytesIO()
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "manifest.json":
            m = json.loads(data); m["browser_specific_settings"]["gecko"].pop("update_url", None)
            data = (json.dumps(m, indent=2) + "\n").encode()
        zout.writestr(item, data)
open(src, "wb").write(buf.getvalue())
PY
  fi
  python3 - "$out" <<'PY'   # LICENSE + NOTICE (copyright, credit wording) ship in every add-on
import sys, zipfile
with zipfile.ZipFile(sys.argv[1], "a") as z:
    for f in ("LICENSE", "NOTICE"): z.write(f, f)
PY
  echo "$out"
done
