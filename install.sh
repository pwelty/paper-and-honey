#!/usr/bin/env bash
# Link userChrome.css / userContent.css into a Thunderbird profile and enable the pref.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"

case "$(uname)" in
  Darwin) tb_root="$HOME/Library/Thunderbird" ;;
  *)      tb_root="$HOME/.thunderbird" ;;
esac

if [[ $# -ge 1 ]]; then
  profile="$1"
else
  ini="$tb_root/profiles.ini"
  [[ -f "$ini" ]] || { echo "No $ini — is Thunderbird installed and run once?" >&2; exit 1; }
  # Prefer the [Install…] section's Default= (the profile Thunderbird actually opens).
  rel="$(awk -F= '/^\[Install/{s=1;next} /^\[/{s=0} s&&$1=="Default"{print $2; exit}' "$ini")"
  [[ -n "$rel" ]] || rel="$(awk -F= '$1=="Path"{p=$2} $1=="Default"&&$2=="1"{print p; exit}' "$ini")"
  [[ -n "$rel" ]] || { echo "Couldn't find default profile in $ini; pass one explicitly." >&2; exit 1; }
  if [[ "$rel" = /* ]]; then profile="$rel"; else profile="$tb_root/$rel"; fi
fi

[[ -d "$profile" ]] || { echo "Profile not found: $profile" >&2; exit 1; }

if pgrep -xiq thunderbird 2>/dev/null; then
  echo "Thunderbird is running — quit it first (it rewrites prefs on exit)." >&2
  exit 1
fi

mkdir -p "$profile/chrome"
for f in userChrome.css userContent.css; do
  dest="$profile/chrome/$f"
  if [[ -e "$dest" && ! -L "$dest" ]]; then
    mv "$dest" "$dest.bak"
    echo "Moved existing $f to $f.bak"
  fi
  ln -sfn "$here/$f" "$dest"
  echo "Linked $dest"
done

pref='user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'
userjs="$profile/user.js"
if ! grep -qF "$pref" "$userjs" 2>/dev/null; then
  echo "$pref" >> "$userjs"
  echo "Enabled stylesheet pref in user.js"
fi

echo "Done. Start Thunderbird."
