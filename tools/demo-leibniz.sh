#!/usr/bin/env bash
# Start a headless demo Thunderbird on leibniz (unattended Mac with the macOS fonts) with a
# fresh profile and both add-ons, and tunnel its Marionette to local port 2829.
# Then: python3 tools/demo.py  (fills it with invented mail), and MN_PORT=2829 tools/mn.py shot …
set -euo pipefail
cd "$(dirname "$0")/.."
H=leibniz
D='Library/Caches/paper-and-honey-demo'
ssh -o BatchMode=yes $H "pkill -f '$D/profile' || true; rm -rf ~/$D && mkdir -p ~/$D/profile ~/$D/dist"
scp -q dist/paper-and-honey-theme-*.xpi dist/paper-and-honey-reading-*.xpi "$H:$D/dist/"
ssh -o BatchMode=yes $H "cat > ~/$D/profile/user.js" <<'PREFS'
user_pref("marionette.port", 2829);
user_pref("mail.threadpane.cardsview.rowcount", 2);
user_pref("mail.uidensity", 0);
user_pref("mailnews.start_page.enabled", false);
user_pref("mail.shell.checkDefaultClient", false);
user_pref("mail.provider.suppress_dialog_on_startup", true);
user_pref("datareporting.policy.dataSubmissionPolicyBypassNotification", true);
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("app.update.enabled", false);
user_pref("mailnews.mark_message_read.auto", false);
user_pref("mail.rights.version", 1);
PREFS
ssh -o BatchMode=yes $H "cd ~/$D && MOZ_HEADLESS=1 MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1 nohup /Applications/Thunderbird.app/Contents/MacOS/thunderbird -profile ~/$D/profile -no-remote --marionette --headless > tb.log 2>&1 &
  for i in \$(seq 40); do lsof -nP -iTCP:2829 -sTCP:LISTEN >/dev/null && break; sleep 1; done; lsof -nP -iTCP:2829 -sTCP:LISTEN >/dev/null && echo 'demo Thunderbird up'"
ssh -o BatchMode=yes -o ExitOnForwardFailure=yes -fN -L 2829:127.0.0.1:2829 $H 2>/dev/null || echo "(tunnel on 2829 already open)"
for x in dist/paper-and-honey-theme-*.xpi dist/paper-and-honey-reading-*.xpi; do
  python3 - "/Users/paul/$D/dist/$(basename "$x")" <<'PY'
import sys; code = open("tools/mn.py").read().split("m = M(")[0]; ns = {}; exec(code, ns)
m = ns["M"](2829); m.cmd("WebDriver:NewSession", {})
aid = m.cmd("Addon:Install", {"path": sys.argv[1], "temporary": False})["value"]
m.cmd("Marionette:SetContext", {"value": "chrome"})  # a theme installed from file isn't active until enabled
m.cmd("WebDriver:ExecuteAsyncScript", {"script": """const done = arguments[arguments.length - 1];
  const {AddonManager} = ChromeUtils.importESModule("resource://gre/modules/AddonManager.sys.mjs");
  AddonManager.getAddonByID(arguments[0]).then(a => a.enable()).then(() => done(1));""", "args": [aid]})
print("installed + enabled", aid)
m.cmd("WebDriver:DeleteSession")
PY
done
