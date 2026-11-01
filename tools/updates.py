"""Write dist/updates.json, the self-hosted update manifest both add-ons point at (update_url).

Thunderbird checks it about daily and installs a newer version from the GitHub release.
Both add-ons share one version number; the release tag is v<version>.
  tools/build.sh && python3 tools/updates.py
"""
import hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/pwelty/paper-and-honey"

def entry(folder):
    m = json.loads((ROOT / folder / "manifest.json").read_text())
    gecko = m["browser_specific_settings"]["gecko"]
    v = m["version"]
    name = f"paper-and-honey-{folder}-{v}.xpi"
    xpi = ROOT / "dist" / name
    digest = hashlib.sha256(xpi.read_bytes()).hexdigest()
    return gecko["id"], {"updates": [{
        "version": v,
        "update_link": f"{REPO}/releases/download/v{v}/{name}",
        "update_hash": f"sha256:{digest}",
        "applications": {"gecko": {"strict_min_version": gecko["strict_min_version"]}},
    }]}

addons = dict(entry(f) for f in ("theme", "reading"))
out = ROOT / "dist" / "updates.json"
out.write_text(json.dumps({"addons": addons}, indent=2) + "\n")
print(out)
