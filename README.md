# Paper & Honey

A warm theme for Thunderbird. Cream paper and brown ink in light mode, espresso in dark, honey
for the accents. A calm two-line message list, readable selection, Phosphor icons coloured by
folder role, and mail you can actually read.

Thunderbird is the right mail client: open, local, scriptable, no lock-in. It is also _so ugly_,
and most themes only recolour the toolbar. Paper & Honey themes the whole window.

## Install

1. Download both files from the [latest release](https://github.com/pwelty/paper-and-honey/releases/latest):
   - **Paper & Honey**, the theme: window, folders, message list, header, icons, light and dark.
   - **Paper & Honey Reading**, recommended: the inside of each message, set like a page.
2. In Thunderbird: **Add-ons and Themes → ⚙ → Install Add-on From File…** and pick each file.

**Why Reading is separate.** A theme can't reach the inside of a message, so that part has to be
an extension, and Thunderbird will ask you to let it "read and modify" messages as they're
displayed and composed. That's the only way to add CSS there. Reading is two CSS files and the
Charter font: no scripts, no network access, nothing collected and nothing added to mail you
send. Without it the window is Paper & Honey but the mail itself is Thunderbird's white page and
sans-serif type.

Requires Thunderbird 151 or later. Thunderbird doesn't require add-on signing, so the files install
as-is, unless your profile has been locked down to require signed add-ons. Updates arrive
automatically.

Reading carries its own Charter, so mail looks the same on every system. The window uses your
system's interface font, and the subject headline uses Charter where it's installed (every Mac)
and Georgia or another serif elsewhere.

## Recommended settings

The theme looks its best with a few built-in Thunderbird settings:

- **Two-line message cards**: message list header → display options button. (Row height is set
  by Thunderbird itself, so a theme can't do this.)
- **Compact density**: View → Density.
- **Compact message header**: on any message, More → Customize: avatar on, full address off,
  labels hidden, large subject. The theme turns the subject into a serif headline.
- **Favorites above All Folders**: folder pane ⋯ → Folder Modes. Star the folders you use daily;
  under All Folders, the collapsed account row works as a "see all" toggle.
- **Theme only, no Reading?** Settings → Fonts & Colors gets you part of the way: serif default
  font set to Charter, and "Display plain text messages in a fixed-width font" turned off.
- **Warm tag colours**: Settings → Tags. The theme tints each tagged message with that tag's
  colour, so any colours work; warm ones suit the palette.

## Known gaps

- The summary shown when you select a collapsed thread or several messages is a view
  Thunderbird never applies themes to (its own included), so it stays plain white or grey.
- Settings pages aren't themed yet.
- On macOS, right-click menus are native system menus and follow the OS.
- Menu labels keep Thunderbird's title case; the theme re-cases only the labels on screen all
  the time.

## Features

### The whole window

- Cream paper and brown ink in light mode, espresso and cream in dark. Honey is the accent
  throughout. The theme follows the system setting and switches without a restart.
- Toolbars, tabs, the spaces bar, panels and popups all share the palette. Nothing is left in
  stock grey or blue.
- The interface type is your system's own font: SF Pro on a Mac, Segoe UI on Windows.

### Folder pane

- Folder icons are coloured by role: inbox honey, sent green, archive blue, drafts plum,
  outbox teal, junk red, trash and templates muted, ordinary folders tan.
- Unread counts are soft honey badges with dark text, readable in both modes.
- Folders with unread mail are shown in honey ink, not bold.
- Rows run full width. Each nesting level indents 8px, with a 12px twisty.
- Mode headers (Favorites, All Folders) and account names are styled as quiet labels.
- Inside Favorites the account row is hidden, so the list is just your folders. Under All
  Folders, the collapsed account row works as a "see all" toggle.
- The selected folder is a deep parchment fill. Its badge stays readable on it.
- Folder suffixes, such as the address Thunderbird appends to duplicate names, stay visible.

### Message list

- Two-line cards (once that setting is on) with no frame inside a frame: each card is one
  surface with one layer of padding.
- Unread is darker ink, never bolder. Read mail steps back to secondary ink. Rows keep the same
  width and height as mail gets read.
- The read/unread dot is honey with a deeper honey outline, instead of Thunderbird's green.
- Tagged messages get a 4px edge in the tag's colour and a light tint of it across the card,
  deeper on hover. This uses Thunderbird's own tag colours, so changing a tag's colour in
  Settings changes the list.
- Selection is solid ink with cream text while the list has focus, and deep parchment with dark
  text when it doesn't. Hover never changes a selected row's colours. Buttons on a selected row
  (thread twisty, star, menu) get a cream wash instead of a tan one.
- The star is an outline at rest and filled honey when flagged.
- Replied and forwarded marks are muted. Thread children aren't indented.
- The message count reads in lowercase, for example "7,292 messages".

### Message header

- With Thunderbird's compact header settings (see Recommended settings), the header becomes a two-column grid.
  The subject comes first, set as a Charter headline at 19px in regular weight, with its tags
  beside it.

### Icons

- Phosphor icons replace Thunderbird's in the folder pane, spaces bar, toolbars, message header
  and message list.
- Most use the duotone weight: an outline with a soft fill, coloured by Thunderbird's own icon
  colours (and by folder role in the folder pane). Small or dense icons, such as plus, the menu
  dots and list views, use the plain outline weight, because duotone turned into a grey smudge
  at 16px.

### Reading (recommended companion add-on)

- Plain-text mail is set in Charter, bundled in the add-on, at 15px with 1.65 line spacing, on the same paper (or
  espresso) as the window.
- HTML mail gets those defaults only where the sender left them unset. Designed newsletters
  render exactly as sent.
- Quoted replies and signatures are set in a quieter ink.
- The compose window matches the theme's page colour, ink and link colour. This only changes
  what you see while writing; nothing is added to the mail you send.

### Labels

- Sentence case on the labels that are always on screen: "New message", "Quick filter",
  "Reply all", "Today pane".

## Design approach

- **A small reward to open.** Warmth and character, not sterile minimalism. Paper, ink and honey
  instead of white, grey and blue.
- **Reading is the point.** Mail is mostly text, so the text is set like a page of a book. HTML
  newsletters keep the design their senders gave them.
- **No bold.** Bold mushes small type together. Emphasis comes from colour and ink depth, and
  the heaviest weight anywhere is medium (500). It also stops rows changing width as mail is
  read.
- **Contrast everywhere.** Every state is checked: unread badges, selection with and without
  focus, hover over a selection, buttons on a selected row, both modes. Honey used as text is
  the deep shade (about 5:1 on the canvas); text on the selection is about 8:1.
- **One layer of spacing.** No margin around a card plus padding around the item inside it.
  Rows run full width and indents stay small, because horizontal space is precious and deep
  indents make lists harder to scan.
- **Sentence case.** Title case reads as shouting. The theme re-cases labels where CSS can
  reach. Menus keep Thunderbird's wording, since changing it would take a language pack.
- **Colour carries meaning.** Folder role, tag and unread state are each shown by colour, so the
  layout itself can stay quiet.
- **Work with Thunderbird, not against it.** The theme sets Thunderbird's own palette and
  component variables first and uses targeted rules only where no variable reaches. It uses
  Thunderbird's own settings (density, card view, header layout, tag colours) rather than
  copying them, so it keeps working as Thunderbird changes.
- **Modern add-ons only.** No `userChrome.css`, no legacy preferences, nothing to hand-edit in
  your profile. Install, enable, update like any add-on.

## How it works

Two standard add-ons, no legacy `userChrome.css`:

- `theme/` — **Paper & Honey**, a theme. `manifest.json` colours the window frame (light and
  `dark_theme`). `theme.css`, loaded via `theme_experiment`, themes everything inside: it remaps
  Thunderbird's core palette (`--layout-*`) and component variables first, and uses targeted rules
  only where no variable reaches. Colours are `light-dark()` pairs.
- `reading/` — **Paper & Honey Reading**, an extension. `reading.css` is injected into displayed
  messages (`message_display_scripts`) and `compose.css` into the compose editor
  (`compose_scripts`, page colour and default ink only; display-only, never sent). Themes can't
  reach message content, hence a separate add-on. Charter ships in `reading/fonts/`, listed as
  `web_accessible_resources` so message pages may load it.

Fonts can only be bundled in Reading. Thunderbird's own windows have a `default-src chrome:`
content security policy, so a font in the theme, embedded or not, is refused.

Icons are Phosphor duotone, applied as CSS masks over Thunderbird's own icon colours and
generated into `theme.css` by `tools/icons.py`. (Theme stylesheets resolve relative URLs against
`chrome://messenger/skin/`, and Thunderbird won't apply SVG context paint to `data:` images, so
masks are the route that works.)

## License

Paper & Honey is © 2026 Paul Welty, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (full text in `LICENSE`; copyright and credit wording in `NOTICE`;
both ship inside both add-ons). Share and adapt it freely; credit is the condition:

> "Paper & Honey" by Paul Welty (https://paulwelty.com/apps/paper-and-honey/), licensed under
> CC BY 4.0 — plus a note if you changed it.

## Credits

- Icons: [Phosphor Icons](https://phosphoricons.com) 2.1.1, © 2023 Phosphor Icons, MIT License.
  The full notice ships inside the theme as `theme/LICENSE-phosphor.txt`.
- Charter: © 1989–1992 Bitstream Inc., redistributed under Bitstream's permissive licence
  (WOFF2 files from [Practical Typography](https://practicaltypography.com/charter.html)). The
  notice ships inside Reading as `reading/LICENSE-charter.txt`. BITSTREAM CHARTER is a
  registered trademark of Bitstream Inc.

## Maintainer notes

Development runs against a live Thunderbird (on averroes, over SSH) through Marionette,
Thunderbird's automation protocol:

```sh
tools/launch-averroes.sh               # restart TB with Marionette + chrome access, tunnel :2828
python3 tools/mn.py shot shots/x.png   # screenshot the main window
python3 tools/mn.py js 'return …'      # run JS in the chrome (UI) context
python3 tools/mn.py reload             # hot-swap theme.css in the running TB, no restart
tools/dev.sh                           # temporary install of both add-ons from this folder
tools/install-averroes.sh              # build + permanent install
tools/build.sh                         # write dist/*.xpi
python3 tools/updates.py               # write dist/updates.json for the current versions
```

Marionette needs `--marionette` plus `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1` to touch the UI;
`launch-averroes.sh` sets both. `reading.css` changes need `dev.sh` (it reloads the open message).
`tools/hover.py` hovers a real pointer over an element; `tools/crop.py` enlarges part of a
screenshot.

Audits, run in the live UI:

- `python3 tools/mn.py js - < tools/audit.js` — selectors in `theme.css` that match nothing in any
  open window (expect misses only for windows/states not on screen).
- `python3 tools/mn.py js - < tools/vars.js` — variables `theme.css` sets that Thunderbird never
  reads.

### Screenshots

Taken from a headless demo Thunderbird on leibniz with invented mail, never Paul's inbox, and
never a second Thunderbird on the machine he's using:

```sh
tools/demo-leibniz.sh && python3 tools/demo.py   # fresh profile, add-ons, demo mail
# restart the demo instance once (New message picks up the account), then:
python3 tools/shots.py                            # shots/site/paper-and-honey-{light,dark,newsletter}.png
```

### Releasing

1. Bump `version` in both manifests (they share one version number).
2. `tools/build.sh`, then `python3 tools/updates.py`.
3. Create a GitHub release `vX.Y.Z` with both `.xpi` files.
4. Publish `dist/updates.json` at `https://paulwelty.com/apps/paper-and-honey/updates.json` (the
   `update_url` in both manifests). Thunderbird checks it about daily.
5. For addons.thunderbird.net: `tools/build.sh --atn` writes `dist/atn/*.xpi` without `update_url`
   (ATN rejects it and delivers its own updates). Upload each as a new version of its listing.

Thunderbird's own theme CSS, for variable names: <https://searchfox.org/comm-central/source/mail/themes/>
