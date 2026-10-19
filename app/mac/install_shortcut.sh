#!/usr/bin/env bash
# Builds a double-click launcher, Watsejy.app, on your Desktop, with its own icon.
# Run once from the project folder:   bash app/mac/install_shortcut.sh
# Safe to run again after updates; it rebuilds the app in place.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
APP="$HOME/Desktop/Watsejy.app"
ICON_PNG="$REPO/app/mac/watsejy-icon.png"

if [ ! -x "$REPO/.venv/bin/python" ]; then
  echo "No .venv found in $REPO. Create it first (see app/README.md step 5)." >&2
  exit 1
fi

# ---- bundle skeleton -------------------------------------------------------
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"

cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>Watsejy</string>
  <key>CFBundleDisplayName</key><string>Watsejy</string>
  <key>CFBundleIdentifier</key><string>za.co.watsejy.launcher</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>Watsejy</string>
  <key>CFBundleIconFile</key><string>Watsejy</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
</dict>
</plist>
PLIST

# The script Terminal runs: starts the server and keeps the window open while it runs.
cat > "$APP/Contents/Resources/run.command" <<EOF
#!/bin/bash
cd "$REPO" || { echo "Kon nie $REPO vind nie"; read -r; exit 1; }
printf '\\033]0;Watsejy\\007'
clear
echo "  WAT SÊ JY  ·  Jy praat. Ons tik."
echo
echo "  Die blaaier maak oop by http://127.0.0.1:7861"
echo "  Maak hierdie venster toe (of druk Ctrl+C) om te stop."
echo
exec "$REPO/.venv/bin/python" "$REPO/app/web.py"
EOF
chmod +x "$APP/Contents/Resources/run.command"

# The app's executable: hand the script to Terminal and exit.
cat > "$APP/Contents/MacOS/Watsejy" <<'EOF'
#!/bin/bash
HERE="$(cd "$(dirname "$0")/.." && pwd)"
open -a Terminal "$HERE/Resources/run.command"
EOF
chmod +x "$APP/Contents/MacOS/Watsejy"

# ---- icon: PNG -> .icns with the tools that ship with macOS ----------------
if [ -f "$ICON_PNG" ]; then
  ICONSET="$(mktemp -d -t watsejy)/Watsejy.iconset"
  mkdir -p "$ICONSET"
  for size in 16 32 128 256 512; do
    sips -z $size $size "$ICON_PNG" --out "$ICONSET/icon_${size}x${size}.png" >/dev/null
    double=$((size * 2))
    sips -z $double $double "$ICON_PNG" --out "$ICONSET/icon_${size}x${size}@2x.png" >/dev/null
  done
  if iconutil -c icns "$ICONSET" -o "$APP/Contents/Resources/Watsejy.icns"; then
    echo "Icon built."
  else
    echo "Could not build the icon (the app still works)."
  fi
  rm -rf "$(dirname "$ICONSET")"
else
  echo "Icon file not found at $ICON_PNG (pull the latest main first)."
fi

# ---- finishing touches ----------------------------------------------------
xattr -dr com.apple.quarantine "$APP" 2>/dev/null || true
codesign --force --deep --sign - "$APP" >/dev/null 2>&1 || true   # ad-hoc signature, if codesign exists
touch "$APP"
osascript -e "tell application \"Finder\" to update (POSIX file \"$APP\" as alias)" >/dev/null 2>&1 || true

# Remove the older .command launcher if this script made one before.
if [ -f "$HOME/Desktop/Watsejy.command" ]; then
  rm -f "$HOME/Desktop/Watsejy.command"
  echo "Removed the old Watsejy.command."
fi

echo "Created $APP"
echo "Double-click 'Watsejy' on your Desktop to start. If the icon still looks generic, run:  killall Finder"
