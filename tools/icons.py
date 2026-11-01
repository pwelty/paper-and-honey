"""Generate the Phosphor icon masks block in theme/theme.css.

Phosphor duotone (MIT, https://phosphoricons.com) has two layers: a background shape at
opacity 0.2 and an outline drawn as a filled path. Used as a CSS mask over a box filled with
Thunderbird's --icon-color, that gives the same two-tone look as TB's own icons, in any colour.

Why masks: theme stylesheets resolve relative url()s against chrome://messenger/skin/, so
files inside the theme can't be referenced, and Thunderbird won't apply SVG context paint to
data: images. Masks need neither.

Only <path d> geometry is taken from the downloads. Re-run after changing NAMES:
  python3 -I tools/icons.py
"""
import base64, pathlib, re, urllib.request

VERSION = "2.1.1"
# name, or name:weight (default duotone). Variable is --ph-<name>[-<weight>].
NAMES = [
    "tray", "paper-plane-tilt", "archive", "trash", "fire", "note-pencil", "file-text",
    "folder-simple", "folder-simple-star", "rss", "envelope-simple", "tray-arrow-up",
    "address-book", "calendar-blank", "check-square", "chat-circle", "gear-six",
    "arrow-bend-up-left", "arrow-bend-double-up-left", "arrow-bend-up-right",
    "star", "star:fill", "paperclip",
]

PATH = re.compile(r"<path\b([^>]*)/?>")
D = re.compile(r'\bd="([MmLlHhVvCcSsQqTtAaZz0-9.,\s+-]+)"')
THEME = pathlib.Path(__file__).resolve().parent.parent / "theme" / "theme.css"
BEGIN, END = "  /* BEGIN GENERATED ICONS (tools/icons.py) */", "  /* END GENERATED ICONS */"


def mask_svg(src: str) -> str:
    paths = []
    for attrs in PATH.findall(src):
        d = D.search(attrs)
        if d:
            op = ' opacity=".2"' if 'opacity="0.2"' in attrs else ""
            paths.append(f'<path{op} d="{d.group(1)}"/>')
    if not paths:
        raise ValueError("no paths")
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">' + "".join(paths) + "</svg>"


def fetch(name: str, weight: str) -> str:
    url = f"https://cdn.jsdelivr.net/npm/@phosphor-icons/core@{VERSION}/assets/{weight}/{name}-{weight}.svg"
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode()


def main():
    lines = [BEGIN, f"  /* Phosphor {VERSION}, MIT. Masks; colour comes from --icon-color. */"]
    for entry in NAMES:
        name, _, weight = entry.partition(":")
        weight = weight or "duotone"
        var = name if weight == "duotone" else f"{name}-{weight}"
        b64 = base64.b64encode(mask_svg(fetch(name, weight)).encode()).decode()
        lines.append(f'  --ph-{var}: url("data:image/svg+xml;base64,{b64}");')
    lines.append(END)
    css = THEME.read_text()
    block = "\n".join(lines)
    if BEGIN in css:
        css = css[:css.index(BEGIN)] + block + css[css.index(END) + len(END):]
    else:
        anchor = "  /* ============================================================\n     1. CORE PALETTE"
        css = css.replace(anchor, block + "\n\n" + anchor, 1)
    THEME.write_text(css)
    print(f"wrote {len(NAMES)} icons into {THEME.name}")


if __name__ == "__main__":
    main()
