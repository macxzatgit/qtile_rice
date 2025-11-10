#!/bin/bash

alacritty -e bash -c '
echo "Available Wi-Fi Networks:"
nmcli device wifi list
echo
read -p "Enter SSID: " ssid
read -s -p "Enter password: " password
echo
nmcli device wifi connect "$ssid" password "$password"
read -p "Press Enter to close..."
'
