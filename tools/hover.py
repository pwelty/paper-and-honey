"""Hover a real pointer over an element in about:3pane and report colours of it and its kids.
  python3 tools/hover.py '<css selector in about:3pane>' [shot.png]
"""
import sys, json, time, base64
code = open(__file__.replace("hover.py", "mn.py")).read().split("m = M();")[0]; ns = {}; exec(code, ns)
m = ns["M"](); m.cmd("WebDriver:NewSession", {}); m.cmd("Marionette:SetContext", {"value": "chrome"})
for h in m.cmd("WebDriver:GetWindowHandles"):
    m.cmd("WebDriver:SwitchToWindow", {"handle": h})
    if "messenger.xhtml" in m.cmd("WebDriver:GetCurrentURL")["value"]: break
js = lambda src, *a: m.cmd("WebDriver:ExecuteScript", {"script": src, "args": list(a)})["value"]
pt = js('''const tm=document.getElementById("tabmail"), br=tm.currentTabInfo.chromeBrowser.getBoundingClientRect();
  const e=tm.currentAbout3Pane.document.querySelector(arguments[0]); if(!e) return null; e.scrollIntoView({block:"nearest"});
  const r=e.getBoundingClientRect(); return [Math.round(br.x+r.x+r.width/2), Math.round(br.y+r.y+r.height/2)];''', sys.argv[1])
if not pt: sys.exit("no element: " + sys.argv[1])
m.cmd("WebDriver:PerformActions", {"actions": [{"type": "pointer", "id": "m", "parameters": {"pointerType": "mouse"},
      "actions": [{"type": "pointerMove", "x": pt[0], "y": pt[1], "origin": "viewport"}]}]})
time.sleep(0.5)
print(json.dumps(js('''const w=document.getElementById("tabmail").currentAbout3Pane, e=w.document.querySelector(arguments[0]);
  const d = x => { const cs=w.getComputedStyle(x); return {el: x.localName+"."+String(x.className).split(" ").slice(0,3).join("."), hover: x.matches(":hover"), color: cs.color, bg: cs.backgroundColor, fill: cs.fill, stroke: cs.stroke}; };
  return [d(e), ...[...e.querySelectorAll("*")].slice(0,4).map(d)];''', sys.argv[1]), indent=1))
if len(sys.argv) > 2:
    open(sys.argv[2], "wb").write(base64.b64decode(m.cmd("WebDriver:TakeScreenshot", {"full": False})["value"]))
m.cmd("WebDriver:ReleaseActions", {}); m.cmd("WebDriver:DeleteSession")
