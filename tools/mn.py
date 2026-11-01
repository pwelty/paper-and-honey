"""Tiny Marionette client: python3 mn.py shot OUT.png | python3 mn.py js 'return ...'"""
import socket, json, sys, base64
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
m = M(); m.cmd("WebDriver:NewSession", {}); m.cmd("Marionette:SetContext", {"value": "chrome"})
# focus the main 3-pane window
for h in m.cmd("WebDriver:GetWindowHandles"):
    m.cmd("WebDriver:SwitchToWindow", {"handle": h})
    if "messenger.xhtml" in m.cmd("WebDriver:GetCurrentURL")["value"]: break
if sys.argv[1] == "shot":
    png = m.cmd("WebDriver:TakeScreenshot", {"full": False})["value"]
    open(sys.argv[2], "wb").write(base64.b64decode(png)); print("saved", sys.argv[2])
elif sys.argv[1] == "js":
    src = sys.argv[2] if sys.argv[2] != "-" else sys.stdin.read()
    print(json.dumps(m.cmd("WebDriver:ExecuteScript", {"script": src, "args": []})["value"], indent=1))
m.cmd("WebDriver:DeleteSession")
