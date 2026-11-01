// For each selector in theme/theme.css, count matches across every open chrome document.
// State pseudo-classes are stripped so :hover/.selected-style rules still count.
const hits = new Map(), docs = [];
function walk(doc) {
  docs.push(doc.documentURI);
  for (const sh of InspectorUtils.getAllStyleSheets(doc)) {
    if (!/^(jar|file|moz-extension):.*[\/!]theme\.css$/.test(sh.href || "")) continue;
    for (const r of sh.cssRules) {
      if (!r.selectorText) continue;
      for (const part of r.selectorText.split(/,(?![^(]*\))/)) {
        const sel = part.trim();
        const probe = sel.replace(/:(hover|focus|focus-within|focus-visible|active|checked|disabled)(?![\w-])/g, "")
                         .replace(/::?[\w-]+(\([^)]*\))?$/, "") || "*";
        let n = 0; try { n = doc.querySelectorAll(probe).length; } catch (e) { n = -1; }
        hits.set(sel, (hits.get(sel) || 0) + Math.max(n, 0));
      }
    }
  }
  for (const b of doc.querySelectorAll("browser, iframe"))
    try { if (b.contentDocument) walk(b.contentDocument); } catch (e) {}
}
for (const win of Services.wm.getEnumerator(null)) walk(win.document);
return { docs, unmatched: [...hits].filter(([, n]) => n === 0).map(([s]) => s) };
