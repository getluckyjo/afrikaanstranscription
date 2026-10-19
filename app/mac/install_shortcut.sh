#!/usr/bin/env bash
# Puts a double-click launcher for Watsejy on your Desktop.
# Run once from the project folder:   bash app/mac/install_shortcut.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET="$HOME/Desktop/Watsejy.command"

if [ ! -x "$REPO/.venv/bin/python" ]; then
  echo "No .venv found in $REPO. Create it first (see app/README.md step 5)." >&2
  exit 1
fi

cat > "$TARGET" <<EOF
#!/bin/bash
# Watsejy: dubbelklik om te begin. Maak hierdie venster toe om te stop.
cd "$REPO" || { echo "Kon nie $REPO vind nie"; read -r; exit 1; }
printf '\\033]0;Watsejy\\007'
clear
echo "  WATSEJY  ·  Wat sê jy?  ·  Jy praat. Ons tik."
echo
echo "  Die blaaier maak oop by http://127.0.0.1:7861"
echo "  Maak hierdie venster toe (of druk Ctrl+C) om te stop."
echo
exec "$REPO/.venv/bin/python" "$REPO/app/web.py"
EOF

chmod +x "$TARGET"
xattr -d com.apple.quarantine "$TARGET" 2>/dev/null || true

# Give the launcher its icon.
ICON="$REPO/app/mac/watsejy-icon.png"
set_icon_jxa() {
  local js
  js="$(mktemp -t watsejy-icon).js"
  cat > "$js" <<'JXA'
ObjC.import("AppKit");
function run(argv) {
  var img = $.NSImage.alloc.initWithContentsOfFile(argv[0]);
  if (img.isNil()) throw new Error("could not load " + argv[0]);
  var ok = $.NSWorkspace.sharedWorkspace.setIconForFileOptions(img, argv[1], 0);
  if (!ok) throw new Error("setIcon returned false");
  return "ok";
}
JXA
  osascript -l JavaScript "$js" "$ICON" "$TARGET"
  local rc=$?
  rm -f "$js"
  return $rc
}
set_icon_pyobjc() {
  "$REPO/.venv/bin/python" -c "import Cocoa" 2>/dev/null || "$REPO/.venv/bin/pip" install -q pyobjc-framework-Cocoa
  "$REPO/.venv/bin/python" - "$ICON" "$TARGET" <<'PY'
import sys
from Cocoa import NSImage, NSWorkspace
img = NSImage.alloc().initWithContentsOfFile_(sys.argv[1])
assert img is not None, "could not load icon"
ok = NSWorkspace.sharedWorkspace().setIcon_forFile_options_(img, sys.argv[2], 0)
assert ok, "setIcon returned false"
print("ok")
PY
}
if [ -f "$ICON" ]; then
  if set_icon_jxa; then
    echo "Icon applied."
  else
    echo "First method failed; trying the Python method…"
    if set_icon_pyobjc; then echo "Icon applied."; else echo "Could not apply the icon (the launcher still works)."; fi
  fi
  touch "$TARGET"
  osascript -e "tell application \"Finder\" to update (POSIX file \"$TARGET\" as alias)" >/dev/null 2>&1 || true
else
  echo "Icon file not found at $ICON (pull the latest main first)."
fi
echo "Created $TARGET"
echo "Double-click 'Watsejy' on your Desktop to start. The first time, macOS may ask to allow Terminal access to Desktop or Documents; click OK."
