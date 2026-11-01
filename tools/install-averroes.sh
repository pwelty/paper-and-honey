#!/usr/bin/env bash
# Build, copy to averroes and install permanently into the running Thunderbird.
set -euo pipefail
cd "$(dirname "$0")/.."
dest='Library/Caches/paper-and-honey-dev/dist'
ssh -o BatchMode=yes averroes "mkdir -p ~/$dest"
# Temporary dev copies (tools/dev.sh) shadow permanent installs of the same id; drop them first.
python3 -I tools/mn.py js 'const {AddonManager}=ChromeUtils.importESModule("resource://gre/modules/AddonManager.sys.mjs");
  return AddonManager.getAllAddons().then(as => Promise.all(as.filter(a => a.temporarilyInstalled && a.id.startsWith("paper-and-honey")).map(a => a.uninstall())))
  .then(r => "dropped " + r.length + " temporary copies")' 
for x in $(tools/build.sh); do
  scp -q "$x" "averroes:$dest/"
  python3 - "$x" "/Users/paul/$dest/$(basename "$x")" <<'PY'
import sys; code = open("tools/mn.py").read().split("m = M();")[0]; ns = {}; exec(code, ns)
m = ns["M"](); m.cmd("WebDriver:NewSession", {})
print(sys.argv[1], "->", m.cmd("Addon:Install", {"path": sys.argv[2], "temporary": False})["value"])
m.cmd("WebDriver:DeleteSession")
PY
done
