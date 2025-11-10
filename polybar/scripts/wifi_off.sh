#!/bin/bash
alacritty -e bash -c '
read -p "Are you sure you want to turn off Wi-Fi? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] && nmcli radio wifi off
'
