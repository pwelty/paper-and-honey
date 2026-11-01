# Paper & Honey

Thunderbird is the right mail client: open, local, scriptable, no lock-in. It is also _so ugly_,
and the user-made themes are uglier. This project makes it something that feels like a small
reward to open.

## Design intent

- **Warm paper.** Cream canvas, brown ink, honey accent. Espresso in dark mode. Not
  sterile-minimal, not Win95.
- **Reading is the point.** Message bodies in a real reading serif (Charter), generous leading.
- **Calm list.** Flat, two-line message list. Unread is darker ink, never bolder, so rows don't
  jiggle as mail gets read.
- **No bold.** It mushes small type. Emphasis is colour; the heaviest weight is medium.
- **Tags as colour.** Tagged messages get a coloured edge and a soft tint.
- **Personality allowed.** Rounded UI font, odd touches welcome.

## What's in here

Two add-ons, both standard Thunderbird extensions (no legacy `userChrome.css`, no profile hacks):

- `theme/` — **Paper & Honey**, a theme.
  - `manifest.json` colours the window frame (toolbar, tabs, search, popups, folder tree), with a
    `dark_theme` block Thunderbird switches to in dark mode.
  - `theme.css` themes everything inside, loaded via `theme_experiment`. It remaps
    Thunderbird's core palette (`--layout-*`) and component variables first, and uses targeted
    rules only where no variable reaches. Colours are `light-dark()` pairs.
- `reading/` — **Paper & Honey Reading**, an extension that injects `reading.css` into every
  displayed message (`message_display_scripts`). Themes can't reach message content, hence
  a separate add-on. Plain text gets the full reading treatment; HTML mail only gets inherited
  defaults, so designed newsletters stay intact.

Icons are Phosphor duotone (MIT), applied as CSS masks over Thunderbird's own icon colours
and generated into `theme.css` by `tools/icons.py`. (Theme stylesheets resolve relative URLs
against `chrome://messenger/skin/`, and TB won't apply SVG context paint to `data:` images,
so masks are the route that works.) Folder icons are coloured by role via `--folder-color-*`.

Requires Thunderbird 151+. Thunderbird doesn't require add-on signing, so the `.xpi` files install
as-is.

### Thunderbird settings the design relies on

Set once in Thunderbird (they're preferences, not CSS):

- Message list: card view, **two rows** (`mail.threadpane.cardsview.rowcount = 2`). Row height is
  fixed by Thunderbird's JS, so CSS can't do this.
- Tag colours: warm palette, set in Settings → Tags. The CSS reads each tag's colour, so custom
  tags just work.
- Density: Compact (View → Density).
- Folder pane: All Folders mode. Account rows are styled as section labels.
- Start page off (`mailnews.start_page.enabled = false`).

## Install

`tools/build.sh` writes `dist/*.xpi`. In Thunderbird: Add-ons and Themes → ⚙ → Install Add-on
From File… → pick each `.xpi`.

## Working on it

Claude works against the real Thunderbird on averroes from the Linux box, over Tailscale SSH,
through Marionette (Thunderbird's automation protocol):

```sh
tools/launch-averroes.sh            # restart TB with Marionette + chrome access, tunnel :2828
python3 tools/mn.py shot shots/x.png   # screenshot the main window
python3 tools/mn.py js 'return …'      # run JS in the chrome (UI) context
python3 tools/mn.py reload             # hot-swap theme.css in the running TB, no restart
tools/dev.sh                        # temporary install of both add-ons from this folder
tools/install-averroes.sh           # build + permanent install
```

Marionette needs `--marionette` plus `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1` to touch the UI;
`launch-averroes.sh` sets both. `reading.css` changes need `dev.sh` (it reloads the open message).

Audits, run in the live UI:

- `python3 tools/mn.py js - < tools/audit.js` — selectors in `theme.css` that match nothing in
  any open window (expect misses only for windows/states not on screen).
- `python3 tools/mn.py js - < tools/vars.js` — variables `theme.css` sets that Thunderbird never
  reads.

By hand: Tools → Developer Tools → Developer Toolbox. Thunderbird's own theme CSS, for names:
<https://searchfox.org/comm-central/source/mail/themes/>
