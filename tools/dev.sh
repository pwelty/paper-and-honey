#!/usr/bin/env bash
# Copy both add-ons to averroes and (re)install them temporarily in the running Thunderbird.
# Temporary installs vanish when Thunderbird restarts; tools/build.sh makes permanent .xpi files.
set -euo pipefail
cd "$(dirname "$0")/.."
dest='Library/Caches/paper-and-honey-dev'
ssh -o BatchMode=yes averroes "mkdir -p ~/$dest"
for a in theme reading; do
  rsync -a --delete "$a/" "averroes:$dest/$a/"
  python3 -I tools/mn.py addon "/Users/paul/$dest/$a"
done
python3 -I tools/mn.py js 'document.getElementById("tabmail").currentAboutMessage?.ReloadMessage?.(); return "message reloaded"'
