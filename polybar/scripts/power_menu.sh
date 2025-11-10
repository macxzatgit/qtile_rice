#!/bin/bash

alacritty -e bash -c '
echo "Choose an action:"
echo "1) Shutdown"
echo "2) Restart"
echo "3) Logout"
echo "4) Cancel"
read -p "Enter choice [1-4]: " choice

case "$choice" in
    1)
        systemctl poweroff
        ;;
    2)
        systemctl reboot
        ;;
    3)
        qtile cmd-obj -o cmd -f shutdown
        ;;
    *)
        echo "Canceled."
        ;;
esac
'
