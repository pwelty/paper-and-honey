# Thunderbird, but lovely

Thunderbird is the right mail client: open, local, scriptable, no lock-in. It is also _so ugly_.
This project makes it something that feels like a small reward to open.

## Design intent

- **Warm paper.** Cream canvas, brown ink, honey accent. Not sterile-minimal, not Win95.
- **Reading is the point.** Message bodies in a real reading serif (Charter), generous line height.
- **Calm list.** Flat, dense message list. Unread is signalled by colour, never by weight, so
  rows don't jiggle as mail gets read.
- **Tags as colour.** Tagged messages get a coloured edge and a soft tint.
- **Personality allowed.** Rounded UI font, odd touches welcome.

## How it works

Two stylesheets, loaded by Thunderbird from the profile's `chrome/` folder:

- `userChrome.css` — the app UI (folder pane, message list, toolbars, menus, compose).
  Strategy: override Thunderbird's own CSS variables first, then target elements the
  variables don't reach.
- `userContent.css` — message bodies (and anything rendered as web content).

Thunderbird only reads these when `toolkit.legacyUserProfileCustomizations.stylesheets` is
`true`. The install script sets that.

Target: macOS (averroes). Fonts assume macOS (Charter, Iowan Old Style, Avenir Next).

## Install

```sh
./install.sh            # links into the default Thunderbird profile
./install.sh <profile>  # or a specific profile directory
```

It symlinks both files into `<profile>/chrome/`, so edits here are live after a Thunderbird
restart. Any existing non-symlinked files are moved aside as `*.bak`. It also adds the pref to
`<profile>/user.js`.

Quit Thunderbird before installing; restart to see changes.

## Iterating

Claude works against the real Thunderbird on averroes, from the Linux box, over Tailscale SSH:

```sh
tools/launch-averroes.sh                       # restart TB with Marionette, tunnel :2828
python3 tools/mn.py shot shots/now.png         # screenshot the main window
python3 tools/mn.py js 'return document.title' # run JS in the chrome (UI) context
```

Marionette needs `--marionette` plus `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1` to touch the UI.
Stylesheets reload only on restart, so each CSS change is: edit → launch → shot.
`~/Projects` on averroes is a mount of this folder, so edits here are live there.

By hand, use the Browser Toolbox to inspect the real DOM instead of guessing selectors:
**Tools → Developer Tools → Developer Toolbox** (enable `devtools.chrome.enabled` and
`devtools.debugger.remote-enabled` in the Config Editor first). The Style Editor there can
edit `userChrome.css` live.

Thunderbird's own theme CSS, for variable names: <https://searchfox.org/comm-central/source/mail/themes/>

## Known problems

Found reviewing the first (agent-built, never-inspected) pass:

- Selected messages: sender/subject stay brown on the honey background (the read/unread
  colour rules out-specify the selected-text rule). Nearly unreadable.
- Tag tints override the selection background; hover overrides it too, leaving cream text on
  a pale tint.
- `.card-layout .card-container { background: transparent }` may be hiding Thunderbird's own
  selection painting.
- `userContent.css`: `.moz-text-html body` never matches (the div is inside `<body>`), so HTML
  mail gets none of the reading styles. No compose-body rules despite the comment.
- Honey + cream text is ~3.3:1 contrast on small text (New Message, Send, badges).
- Stale/guessed selectors from pre-Supernova Thunderbird (`textbox`, `#mail-toolbox`,
  `#searchInput`, `#button-newmsg`, `.dialogBox`…). Needs a pass with the Browser Toolbox.
- Over-broad element rules (`toolbarbutton`, `button`, `input`, `menupopup`) restyle every
  dialog and settings page.
- Toolbar icons tinted with a `sepia()` filter chain; the icons are SVGs that follow `color`.
- No dark mode: in macOS dark appearance, unthemed areas go dark and clash.
- Tag colours hard-coded for the five default tags only.

## Open questions

- Ship the palette as a Thunderbird theme add-on (portable, no pref flag) and keep
  `userChrome.css` for only what themes can't reach?
- Dark mode: a warm dark variant, or force light?
