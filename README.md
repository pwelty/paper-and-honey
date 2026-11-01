# Paper & Honey

A warm theme for Thunderbird. Cream paper and brown ink in light mode, espresso in dark, honey
for the accents. A calm two-line message list, readable selection, Phosphor icons coloured by
folder role, and mail you can actually read.

Thunderbird is the right mail client: open, local, scriptable, no lock-in. It is also _so ugly_,
and most themes only recolour the toolbar. Paper & Honey themes the whole window.

## Install

1. Download both `.xpi` files from the [latest release](https://github.com/pwelty/paper-and-honey/releases/latest):
   - **Paper & Honey** — the theme
   - **Paper & Honey Reading** — typography for message bodies and the compose window
2. In Thunderbird: **Add-ons and Themes → ⚙ → Install Add-on From File…** and pick each file.

Requires Thunderbird 151 or later. Thunderbird doesn't require add-on signing, so the files install
as-is, unless your profile has been locked down to require signed add-ons. Updates arrive
automatically.

The type assumes macOS fonts (SF Pro Rounded, Charter); elsewhere it falls back gracefully.

## Recommended settings

The theme looks its best with a few built-in Thunderbird settings:

- **Two-line message cards**: message list header → display options button. (Row height is set
  by Thunderbird itself, so a theme can't do this.)
- **Compact density**: View → Density.
- **Compact message header**: on any message, More → Customize: avatar on, full address off,
  labels hidden, large subject. The theme turns the subject into a serif headline.
- **Favorites above All Folders**: folder pane ⋯ → Folder Modes. Star the folders you use daily;
  under All Folders, the collapsed account row works as a "see all" toggle.
- **Warm tag colours**: Settings → Tags. The theme tints each tagged message with that tag's
  colour, so any colours work; warm ones suit the palette.

## Known gaps

- The summary shown when you select a collapsed thread or several messages is a view
  Thunderbird never applies themes to (its own included), so it stays plain white or grey.
- Settings pages aren't themed yet.
- On macOS, right-click menus are native system menus and follow the OS.
- Menu labels keep Thunderbird's title case; the theme re-cases only the labels on screen all
  the time.

## Design

- **Warm paper.** Cream canvas, brown ink, honey accent; espresso in dark mode.
- **Reading is the point.** Plain-text mail in Charter with generous leading. HTML newsletters
  keep their own design.
- **Calm list.** Unread is darker ink, never bolder, so rows don't jiggle as mail gets read.
- **No bold.** It mushes small type. Emphasis is colour; the heaviest weight is medium.
- **One layer of spacing.** Full-width rows, small indents, no padding stacked on padding.
- **Sentence case** where the theme can reach it.

## How it works

Two standard add-ons, no legacy `userChrome.css`:

- `theme/` — **Paper & Honey**, a theme. `manifest.json` colours the window frame (light and
  `dark_theme`). `theme.css`, loaded via `theme_experiment`, themes everything inside: it remaps
  Thunderbird's core palette (`--layout-*`) and component variables first, and uses targeted rules
  only where no variable reaches. Colours are `light-dark()` pairs.
- `reading/` — **Paper & Honey Reading**, an extension. `reading.css` is injected into displayed
  messages (`message_display_scripts`) and `compose.css` into the compose editor
  (`compose_scripts`, page colour and default ink only; display-only, never sent). Themes can't
  reach message content, hence a separate add-on.

Icons are Phosphor duotone, applied as CSS masks over Thunderbird's own icon colours and
generated into `theme.css` by `tools/icons.py`. (Theme stylesheets resolve relative URLs against
`chrome://messenger/skin/`, and Thunderbird won't apply SVG context paint to `data:` images, so
masks are the route that works.)

## License

Paper & Honey is © 2026 Paul Welty, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (full text in `LICENSE`, which also ships
inside both add-ons). Share and adapt it freely; credit is the condition:

> "Paper & Honey" by Paul Welty (https://paulwelty.com/apps/paper-and-honey/), licensed under
> CC BY 4.0 — plus a note if you changed it.

## Credits

- Icons: [Phosphor Icons](https://phosphoricons.com) 2.1.1, © 2023 Phosphor Icons, MIT License.
  The full notice ships inside the theme as `theme/LICENSE-phosphor.txt`.
- Fonts are referenced, not bundled: Charter, Iowan Old Style and SF Pro Rounded come with macOS.

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

### Releasing

1. Bump `version` in both manifests (they share one version number).
2. `tools/build.sh`, then `python3 tools/updates.py`.
3. Create a GitHub release `vX.Y.Z` with both `.xpi` files.
4. Publish `dist/updates.json` at `https://paulwelty.com/apps/paper-and-honey/updates.json` (the
   `update_url` in both manifests). Thunderbird checks it about daily.

Thunderbird's own theme CSS, for variable names: <https://searchfox.org/comm-central/source/mail/themes/>
