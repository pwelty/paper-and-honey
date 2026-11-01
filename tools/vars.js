// Which custom properties set in theme/theme.css are actually read by Thunderbird's own CSS?
const used = new Set(), ours = new Set(), seen = new Set();
function scanSheet(sh) {
  if (!sh || seen.has(sh)) return; seen.add(sh);
  let rules; try { rules = sh.cssRules; } catch (e) { return; }
  const mine = /^(jar|file|moz-extension):.*[\/!]theme\.css$/.test(sh.href || "");
  const visit = list => { for (const r of list) {
    if (r.styleSheet) scanSheet(r.styleSheet);
    if (r.cssRules) visit(r.cssRules);
    if (!r.style) continue;
    for (let i = 0; i < r.style.length; i++) {
      const p = r.style[i], v = r.style.getPropertyValue(p);
      if (mine && p.startsWith("--") && !p.startsWith("--warm-")) ours.add(p);
    }
    if (!mine) for (const m of r.style.cssText.matchAll(/var\((--[\w-]+)/g)) used.add(m[1]);
  }};
  visit(rules);
}
function walk(root) {
  const doc = root.ownerDocument || root;
  for (const sh of InspectorUtils.getAllStyleSheets(doc)) scanSheet(sh);
  for (const el of root.querySelectorAll("*")) {
    if (el.shadowRoot) { for (const sh of el.shadowRoot.styleSheets) scanSheet(sh); walk(el.shadowRoot); }
    if (/^(browser|iframe)$/.test(el.localName)) try { if (el.contentDocument) walk(el.contentDocument); } catch (e) {}
  }
}
for (const win of Services.wm.getEnumerator(null)) walk(win.document);
return { dead: [...ours].filter(v => !used.has(v)), live: [...ours].filter(v => used.has(v)).length,
         candidates: [...used].filter(v => /panel|menu|tag|tree-card|treeitem|sidebar|toolbar|button|search|tab|input|layout-|header/.test(v)).sort() };
