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
echo "  WATSEJY  ·  Jy praat. Ons tik."
echo
echo "  Die blaaier maak oop by http://127.0.0.1:7861"
echo "  Maak hierdie venster toe (of druk Ctrl+C) om te stop."
echo
exec "$REPO/.venv/bin/python" "$REPO/app/web.py"
EOF

chmod +x "$TARGET"
xattr -d com.apple.quarantine "$TARGET" 2>/dev/null || true
echo "Created $TARGET"
echo "Double-click 'Watsejy' on your Desktop to start. The first time, macOS may ask to allow Terminal access to Desktop or Documents; click OK."
