#!/usr/bin/env bash
# (Re)start Thunderbird on averroes with Marionette + chrome access, and tunnel port 2828 here.
set -euo pipefail
ssh -o BatchMode=yes averroes '
  osascript -e "quit app \"Thunderbird\"" || true
  for i in $(seq 20); do pgrep -q -f Thunderbird.app/Contents/MacOS || break; sleep 1; done
  open --env MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1 -a Thunderbird --args --marionette
  for i in $(seq 30); do lsof -nP -iTCP:2828 -sTCP:LISTEN >/dev/null && break; sleep 1; done'
pgrep -f "L 2828:127.0.0.1:2828" >/dev/null || ssh -o BatchMode=yes -o ExitOnForwardFailure=yes -fN -L 2828:127.0.0.1:2828 averroes
echo "Ready: python3 tools/mn.py shot shots/x.png"
