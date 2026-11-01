"""Fill a throwaway Thunderbird profile with invented mail for screenshots.

Runs against the headless demo instance on leibniz (tools/demo-leibniz.sh starts it and
tunnels Marionette to local port 2829). Never run a second Thunderbird on the machine Paul
is using: it interferes with his.
  tools/demo-leibniz.sh && python3 tools/demo.py
Everything here is fictional; addresses use reserved example domains.
"""
import json, os, subprocess, sys, base64
from datetime import datetime, timedelta, timezone

NOW = datetime(2026, 11, 1, 14, 30, tzinfo=timezone(timedelta(hours=-5)))
ME = "Robin Quill <robin@example.com>"

def at(days=0, hours=0, minutes=0):
    return (NOW - timedelta(days=days, hours=hours, minutes=minutes)).strftime("%a, %d %b %Y %H:%M:%S %z")

SLOW_POST = """<html><body style="margin:0;background:#EEF1EC;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#EEF1EC;"><tr><td align="center" style="padding:28px 12px;">
<table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:6px;font-family:Georgia,serif;color:#23302A;">
<tr><td style="background:#2F4A3A;color:#F3EBDD;padding:22px 32px;font-size:26px;letter-spacing:0.5px;">The Slow Post<div style="font-size:13px;opacity:.8;font-family:Helvetica,Arial,sans-serif;letter-spacing:1px;margin-top:4px;">ISSUE 41 &middot; LETTERS FOR UNHURRIED PEOPLE</div></td></tr>
<tr><td style="padding:28px 32px 8px;font-size:22px;">The case for handwritten lists</td></tr>
<tr><td style="padding:0 32px 18px;font-size:16px;line-height:1.6;">A list written by hand is a small promise to your future self. It is slower than an app, and that is the point: by the time you have written <em>mend the gate</em>, you have already half-decided to do it.</td></tr>
<tr><td style="padding:0 32px 24px;font-size:16px;line-height:1.6;">This week: three paper systems readers swear by, a note on pencils that survive winter, and one reader's 40-year-old grocery list, found in a cookbook.</td></tr>
<tr><td style="padding:0 32px 30px;"><a href="https://example.org/slowpost/41" style="background:#C8553D;color:#fff;text-decoration:none;padding:11px 20px;border-radius:4px;font-family:Helvetica,Arial,sans-serif;font-size:14px;">Read the issue</a></td></tr>
<tr><td style="border-top:1px solid #E3E7E1;padding:16px 32px;font-size:12px;color:#7A857E;font-family:Helvetica,Arial,sans-serif;">You subscribed at example.org. Unsubscribe any time.</td></tr>
</table></td></tr></table></body></html>"""

LISBON = """Robin,

Lisbon is louder than I remembered and kinder than I deserved. The trams still groan up the hill to Graca like old dogs who know the way home, and every bakery has decided, independently, that I need another pastel de nata.

I found the bookshop you told me about. It is smaller than a bus and older than the street. The owner wrapped my two paperbacks in brown paper and string without being asked, which felt like being handed a letter from someone who already knew me.

Tomorrow I take the train out to the coast. I mean to sit somewhere with a view, write the chapter I keep circling, and not check my mail at all. You are the exception.

More soon, and a postcard on the way.

Ana
"""

def M(folder, frm, subject, date, body, *, to=ME, html=False, tags=(), read=True, starred=False,
      msgid=None, reply_to=None, attach=None):
    return dict(folder=folder, frm=frm, to=to, subject=subject, date=date, body=body, html=html,
                tags=list(tags), read=read, starred=starred, msgid=msgid, reply_to=reply_to, attach=attach)

PDF = base64.b64encode(b"%PDF-1.4\n% chapter-3 notes (demo)\n").decode()

MESSAGES = [
    # Inbox
    M("Inbox", "Ana Duarte <ana@example.net>", "Field notes from Lisbon", at(0, 1, 12), LISBON, tags=["$label3"]),
    M("Inbox", "Priya Natarajan <priya@studio.example>", "Draft chapter 3, notes attached", at(0, 2, 5),
      "Robin,\n\nNotes on chapter 3 attached. The middle drags a little; the ending is the best thing you've written.\n\nPriya\n",
      tags=["$label1"], read=False, attach="chapter-3-notes.pdf"),
    M("Inbox", "Mira Okafor <mira@example.org>", "Cabin weekend: final plan", at(0, 3, 30),
      "Friday 4pm at the trailhead lot. I'll bring the big pot and the lantern. Someone claim breakfast.\n\nMira\n",
      tags=["$label3"], msgid="cabin-1@example.org"),
    M("Inbox", "Jonah Reyes <jonah@example.net>", "Re: Cabin weekend: final plan", at(0, 3, 2),
      "Breakfast is mine. Pancakes, obviously.\n", tags=["$label3"], msgid="cabin-2@example.net", reply_to="cabin-1@example.org"),
    M("Inbox", "Mira Okafor <mira@example.org>", "Re: Cabin weekend: final plan", at(0, 2, 40),
      "Pancakes accepted. Robin, can you bring the card game?\n", tags=["$label3"], read=False,
      msgid="cabin-3@example.org", reply_to="cabin-2@example.net"),
    M("Inbox", "The Slow Post <letters@slowpost.example>", "Issue 41: The case for handwritten lists", at(0, 5), SLOW_POST,
      html=True, tags=["$label5"], read=False),
    M("Inbox", "Theo Lindqvist <theo@coop.example>", "Seed swap on Saturday", at(0, 7),
      "Bring envelopes and a pen. We're trading beans for squash this year, no exceptions.\n\nTheo\n",
      tags=["$label4"], starred=True),
    M("Inbox", "Juniper Street Bakery <orders@juniper.example>", "Your order is ready for pickup", at(0, 9),
      "One rye loaf, one dozen cardamom buns. Ready at the counter until 6pm.\n"),
    M("Inbox", "Elm Street Library <notices@library.example>", "Two books due Friday", at(1, 2),
      "The Overstory and A Field Guide to Getting Lost are due Friday. Renew online or at the desk.\n",
      tags=["$label4"]),
    M("Inbox", "Sam Whitfield <sam@trails.example>", "Trail report: Ridge Loop", at(1, 6),
      "Mud at the creek crossing, otherwise perfect. The overlook is worth the last mile.\n", tags=["$label2"]),
    M("Inbox", "Paperworks Press <hello@paperworks.example>", "Your print order has shipped", at(2, 1),
      "Your 40 letterpress cards are on their way. Tracking: PW-2026-1189.\n", tags=["$label5"]),
    M("Inbox", "Dev Patel <dev@example.com>", "Re: Borrowing the stand mixer", at(2, 4),
      "Perfect, I'll swing by Thursday. I owe you a loaf.\n"),
    M("Inbox", "Harbor Credit Union <statements@harbor.example>", "Your October statement is ready", at(3, 2),
      "Your statement is ready to view. Sign in to see it.\n"),
    M("Inbox", "Night Kitchen <menu@nightkitchen.example>", "This week's menu", at(3, 8),
      "Squash soup, braised greens, and the return of the walnut cake.\n", tags=["$label5"]),
    M("Inbox", "Lena Hart <lena@example.org>", "Book club: November pick", at(4, 3),
      "We're reading Piranesi. Meeting at mine on the 19th, bring something to share.\n", tags=["$label3"], starred=True),
    # Other folders
    M("Sent", ME, "Re: Cabin weekend: final plan", at(0, 2, 20), "Card game is packed.\n", to="Mira Okafor <mira@example.org>"),
    M("Sent", ME, "Chapter 3", at(1, 9), "Here's the draft. Be brutal.\n", to="Priya Natarajan <priya@studio.example>"),
    M("Newsletters", "Field & Fern <weekly@fieldfern.example>", "What to plant before the frost", at(1, 1), "Garlic, tulips, and patience.\n"),
    M("Newsletters", "The Slow Post <letters@slowpost.example>", "Issue 40: On mending", at(7), "Darning, glue, and second chances.\n"),
    M("Receipts", "Juniper Street Bakery <orders@juniper.example>", "Receipt for your order", at(9), "Rye loaf, cardamom buns. Total $18.50.\n"),
    M("Receipts", "Paperworks Press <hello@paperworks.example>", "Order confirmation PW-2026-1189", at(5), "40 letterpress cards. Total $64.00.\n"),
    M("Archives", "Ana Duarte <ana@example.net>", "Before I leave", at(12), "Keys under the fern. Water the basil.\n"),
    M("Garden co-op", "Theo Lindqvist <theo@coop.example>", "Plot assignments", at(20), "You have plot 7, by the rain barrel.\n"),
    M("Cabin trip", "Mira Okafor <mira@example.org>", "Packing list", at(6), "Headlamp, wool socks, the good knife.\n"),
]

def rfc822(m):
    lines = [f"From: {m['frm']}", f"To: {m['to']}", f"Subject: {m['subject']}", f"Date: {m['date']}",
             f"Message-ID: <{m['msgid'] or abs(hash(m['subject'] + m['date']))}@demo.example>" if not m["msgid"] else f"Message-ID: <{m['msgid']}>",
             "MIME-Version: 1.0"]
    if m["reply_to"]:
        lines += [f"In-Reply-To: <{m['reply_to']}>", f"References: <{m['reply_to']}>"]
    ctype = "text/html" if m["html"] else "text/plain"
    if m["attach"]:
        b = "demo-boundary-41"
        lines += [f'Content-Type: multipart/mixed; boundary="{b}"', "", f"--{b}",
                  f"Content-Type: {ctype}; charset=UTF-8", "", m["body"], f"--{b}",
                  f'Content-Type: application/pdf; name="{m["attach"]}"',
                  f'Content-Disposition: attachment; filename="{m["attach"]}"',
                  "Content-Transfer-Encoding: base64", "", PDF, f"--{b}--", ""]
    else:
        lines += [f"Content-Type: {ctype}; charset=UTF-8", "", m["body"]]
    return "\r\n".join(lines) + "\r\n"

SETUP_JS = r"""
const data = arguments[0];
const am = MailServices.accounts;
// A sendable account (local folders can't be the default, so New message would stay disabled).
// POP with checking off: it never touches the network.
let acct = am.accounts.find(a => a.incomingServer.type === "pop3");
if (!acct) {
  const srv = am.createIncomingServer("robin", "mail.example.com", "pop3");
  srv.loginAtStartUp = false; srv.doBiff = false;
  acct = am.createAccount(); acct.incomingServer = srv;
  const id = am.createIdentity(); id.fullName = "Robin Quill"; id.email = "robin@example.com";
  acct.addIdentity(id);
  am.defaultAccount = acct;
}
const server = acct.incomingServer;
server.prettyName = "Mail";
const root = server.rootFolder.QueryInterface(Ci.nsIMsgLocalMailFolder);
const F = Ci.nsMsgFolderFlags;
const ensure = (parent, name, flag) => {
  let f = parent.getChildNamed ? (parent.containsChildNamed(name) ? parent.getChildNamed(name) : null) : null;
  if (!f) f = parent.QueryInterface(Ci.nsIMsgLocalMailFolder).createLocalSubfolder(name);
  if (flag) f.setFlag(flag);
  return f;
};
const folders = {
  Inbox: ensure(root, "Inbox", F.Inbox), Drafts: ensure(root, "Drafts", F.Drafts), Sent: ensure(root, "Sent", F.SentMail),
  Archives: ensure(root, "Archives", F.Archive), Newsletters: ensure(root, "Newsletters"), Receipts: ensure(root, "Receipts"),
};
const projects = ensure(root, "Projects");
folders["Garden co-op"] = ensure(projects, "Garden co-op");
folders["Cabin trip"] = ensure(projects, "Cabin trip");
const warm = {"$label1":"#C74A3C","$label2":"#D4854A","$label3":"#4D8B55","$label4":"#4E9A93","$label5":"#4A7FB5"};
for (const [k,c] of Object.entries(warm)) MailServices.tags.setColorForKey(k, c);
let n = 0;
for (const m of data) {
  const f = folders[m.folder].QueryInterface(Ci.nsIMsgLocalMailFolder);
  const hdr = f.addMessage(m.raw);
  if (m.read) folders[m.folder].markMessagesRead([hdr], true);
  if (m.starred) folders[m.folder].markMessagesFlagged([hdr], true);
  if (m.tags.length) folders[m.folder].addKeywordsToMessages([hdr], m.tags.join(" "));
  n++;
}
for (const name of ["Inbox", "Newsletters", "Receipts"]) folders[name].setFlag(F.Favorite);
folders["Garden co-op"].setFlag(F.Favorite);
window.resizeTo(1440, 900);
Services.prefs.setIntPref("mail.addressDisplayFormat", 2);  // names only in the list
const w = document.getElementById("tabmail").currentAbout3Pane;
w.folderPane.activeModes = ["favorite", "all"];
await new Promise(r => setTimeout(r, 800));
for (const row of w.document.querySelectorAll('#folderTree li[data-server-type="pop3"].collapsed')) w.folderTree.expandRow(row);
const local = w.document.querySelector('#folderTree > li[data-mode="all"] li[data-server-type="none"]');
if (local && !local.classList.contains("collapsed")) w.folderTree.collapseRow(local);
w.displayFolder(folders.Inbox);
await new Promise(r => setTimeout(r, 800));
const v = w.gDBView;
for (let i = 0; i < v.rowCount; i++) if (/Lisbon/.test(v.getMsgHdrAt(i).mime2DecodedSubject)) { w.threadTree.selectedIndex = i; break; }
return {added: n, folders: Object.keys(folders), canWrite: !w.document.getElementById("folderPaneWriteMessage").disabled};
"""

if __name__ == "__main__":
    for m in MESSAGES:
        m["raw"] = rfc822(m)
    here = os.path.dirname(os.path.abspath(__file__))
    code = open(os.path.join(here, "mn.py")).read().split("m = M(")[0]; ns = {}; exec(code, ns)
    mn = ns["M"](int(os.environ.get("MN_PORT", "2829")))
    mn.cmd("WebDriver:NewSession", {}); mn.cmd("Marionette:SetContext", {"value": "chrome"})
    for h in mn.cmd("WebDriver:GetWindowHandles"):
        mn.cmd("WebDriver:SwitchToWindow", {"handle": h})
        if "messenger.xhtml" in mn.cmd("WebDriver:GetCurrentURL")["value"]: break
    js = "const done = arguments[arguments.length - 1]; (async () => {" + SETUP_JS + "})().then(done, e => done('ERR ' + e));"
    print(json.dumps(mn.cmd("WebDriver:ExecuteAsyncScript", {"script": js, "args": [MESSAGES]})["value"], indent=1))
    mn.cmd("WebDriver:DeleteSession")
