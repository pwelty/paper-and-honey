"""Tiny Marionette client for Thunderbird.
  mn.py shot OUT.png        screenshot the main window
  mn.py js 'return ...'     run JS in the chrome context (- reads stdin)
  MN_WINDOW=<url part> picks a window (default messenger.xhtml)
  mn.py addon PATH        install an unpacked add-on temporarily (path as seen on averroes)
  mn.py reload              hot-swap theme.css + reading.css in the running TB (no restart)
"""
import socket, json, sys, base64, os
class M:
    def __init__(s, port=2828):
        s.s = socket.create_connection(("127.0.0.1", port), timeout=30); s.id = 0; s.recv()
    def recv(s):
        n = b""
        while not n.endswith(b":"): n += s.s.recv(1)
        n = int(n[:-1]); buf = b""
        while len(buf) < n: buf += s.s.recv(n - len(buf))
        return json.loads(buf)
    def cmd(s, name, params=None):
        s.id += 1; d = json.dumps([0, s.id, name, params or {}]).encode()
        s.s.sendall(str(len(d)).encode() + b":" + d); r = s.recv()
        if r[2]: raise SystemExit(f"{name}: {r[2]}")
        return r[3]
RELOAD = r"""
// Hot-swap the add-on stylesheets in every open document: arguments = {filename: css}
const files = arguments[0]; let n = 0;
function walk(doc) {
  for (const sh of InspectorUtils.getAllStyleSheets(doc)) {
    const name = sh.href?.startsWith("moz-extension://") && sh.href.split("/").pop();
    if (name && name in files) { InspectorUtils.parseStyleSheet(sh, files[name]); n++; }
  }
  for (const b of doc.querySelectorAll("browser, iframe"))
    try { if (b.contentDocument) walk(b.contentDocument); } catch (e) {}
}
for (const win of Services.wm.getEnumerator(null)) walk(win.document);
return `reloaded ${n} sheets`;
"""
m = M(); m.cmd("WebDriver:NewSession", {}); m.cmd("Marionette:SetContext", {"value": "chrome"})
# focus the main 3-pane window
for h in m.cmd("WebDriver:GetWindowHandles"):
    m.cmd("WebDriver:SwitchToWindow", {"handle": h})
    if os.environ.get("MN_WINDOW", "messenger.xhtml") in m.cmd("WebDriver:GetCurrentURL")["value"]: break
if sys.argv[1] == "shot":
    png = m.cmd("WebDriver:TakeScreenshot", {"full": False})["value"]
    open(sys.argv[2], "wb").write(base64.b64decode(png)); print("saved", sys.argv[2])
elif sys.argv[1] == "js":
    src = sys.argv[2] if sys.argv[2] != "-" else sys.stdin.read()
    print(json.dumps(m.cmd("WebDriver:ExecuteScript", {"script": src, "args": []})["value"], indent=1))
elif sys.argv[1] == "addon":
    # mn.py addon <path-on-averroes>  — install unpacked add-on temporarily (gone on restart)
    print(m.cmd("Addon:Install", {"path": sys.argv[2], "temporary": True}))
elif sys.argv[1] == "reload":
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    files = {p.name: p.read_text() for p in (root / "theme/theme.css", root / "reading/reading.css")}
    print(m.cmd("WebDriver:ExecuteScript", {"script": RELOAD, "args": [files]})["value"])
m.cmd("WebDriver:DeleteSession")
