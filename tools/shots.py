"""Pose the demo Thunderbird (tools/demo-leibniz.sh + tools/demo.py, then restart it once so
New message picks up the account) and save the website screenshots.
  python3 tools/shots.py [outdir]      (default: shots/site)
"""
import base64, json, os, sys, time

here = os.path.dirname(os.path.abspath(__file__))
code = open(os.path.join(here, "mn.py")).read().split("m = M(")[0]; ns = {}; exec(code, ns)
mn = ns["M"](int(os.environ.get("MN_PORT", "2829")))
mn.cmd("WebDriver:NewSession", {}); mn.cmd("Marionette:SetContext", {"value": "chrome"})
for h in mn.cmd("WebDriver:GetWindowHandles"):
    mn.cmd("WebDriver:SwitchToWindow", {"handle": h})
    if "messenger.xhtml" in mn.cmd("WebDriver:GetCurrentURL")["value"]: break

def js(src, *args):
    wrapped = "const done = arguments[arguments.length - 1]; (async () => {" + src + "})().then(done, e => done('ERR ' + e));"
    return mn.cmd("WebDriver:ExecuteAsyncScript", {"script": wrapped, "args": list(args)})["value"]

POSE = r"""
const [subject, dark] = arguments;
Services.prefs.setIntPref("ui.systemUsesDarkTheme", dark ? 1 : 0);
window.resizeTo(1440, 900);
const w = document.getElementById("tabmail").currentAbout3Pane;
const server = MailServices.accounts.defaultAccount.incomingServer;
w.displayFolder(server.rootFolder.getChildNamed("Inbox"));
await new Promise(r => setTimeout(r, 700));
const v = w.gDBView;
for (let i = 0; i < v.rowCount; i++) if (v.getMsgHdrAt(i).mime2DecodedSubject.includes(subject)) { w.threadTree.selectedIndex = i; break; }
w.document.querySelector('#threadTree [is="tree-view-table-body"]').focus();
await new Promise(r => setTimeout(r, 1500));
return w.gDBView.hdrForFirstSelectedMessage?.mime2DecodedSubject;
"""

out = sys.argv[1] if len(sys.argv) > 1 else "shots/site"
os.makedirs(out, exist_ok=True)
for name, subject, dark in [("light", "Field notes from Lisbon", False),
                            ("dark", "Field notes from Lisbon", True),
                            ("newsletter", "handwritten lists", False)]:
    print(name, "->", js(POSE, subject, dark))
    time.sleep(0.5)
    png = mn.cmd("WebDriver:TakeScreenshot", {"full": False})["value"]
    path = os.path.join(out, f"paper-and-honey-{name}.png")
    open(path, "wb").write(base64.b64decode(png)); print("saved", path)
js(POSE, "Field notes from Lisbon", False)
mn.cmd("WebDriver:DeleteSession")
