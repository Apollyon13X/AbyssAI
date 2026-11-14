#!/bin/sh
# One-time: install AbyssAI into the XFCE/app menu.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
APPDIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
ICONDIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR" "$ICONDIR"

chmod +x "$ROOT/AbyssAI.sh"

ICON_SRC=""
for c in \
  "$ROOT/nft/eye-ov-the-abyss.jpg" \
  "$ROOT/gui/public/Eye-ov-The-Abyss-launchpad.jpg" \
  "$ROOT/gui/public/favicon.svg"
do
  [ -f "$c" ] && ICON_SRC="$c" && break
done

ICON="$ICONDIR/abyssai.png"
if [ -n "$ICON_SRC" ] && command -v convert >/dev/null 2>&1; then
  convert "$ICON_SRC" -resize 256x256^ -gravity center -extent 256x256 "$ICON"
elif [ -n "$ICON_SRC" ]; then
  ICON="$ICON_SRC"
else
  ICON="utilities-terminal"
fi

cat > "$APPDIR/abyssai.desktop" << D
[Desktop Entry]
Type=Application
Version=1.0
Name=AbyssAI
GenericName=Whispers From The Void
Comment=Professor Apollyon — self-help oracle
Exec=$ROOT/AbyssAI.sh
Path=$ROOT
Icon=$ICON
Terminal=false
StartupNotify=true
Categories=Utility;Education;
Keywords=oracle;abyss;apollyon;
StartupWMClass=AbyssAI
D
chmod 644 "$APPDIR/abyssai.desktop"

command -v update-desktop-database >/dev/null 2>&1 \
  && update-desktop-database "$APPDIR" 2>/dev/null || true

echo "Installed: $APPDIR/abyssai.desktop"
echo "XFCE menu → AbyssAI"
echo "Log: ~/.local/state/abyssai/abyssai.log"
