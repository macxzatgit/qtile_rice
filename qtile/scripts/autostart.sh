#!/bin/bash

# Kill any existing picom instances
pkill -x picom

# Wait until picom has been shut down
while pgrep -x picom >/dev/null; do sleep 0.1; done

# Launch picom with your config (if you have one)
CONFIG="$HOME/.config/picom/picom.conf"
if [ -f "$CONFIG" ]; then
    picom --config "$CONFIG" &
else
    picom &
fi
echo "Picom compositor launched"

# Set wallpaper (using feh as an example)
WALLPAPER="$HOME/Pictures/backgrounds/aurora2.jpg"

if [ -f "$WALLPAPER" ]; then
    feh --bg-fill "$WALLPAPER"
    echo "Wallpaper set: $WALLPAPER"
else
    echo "Wallpaper not found at $WALLPAPER"
fi

#!/bin/bash
betterlockscreen -l dimblur &
sleep 1
xset dpms force off
