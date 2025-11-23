#!/bin/bash

# Script to install keepassxc on apt based systems

echo "INFO: Installing keepassxc"
#sudo apt update
#sudo apt -y install keepassxc

umask 0077
mkdir -p ~/.config/keepass

echo "INFO: Creating keyfile"
head -c 64 /dev/urandom > ~/.config/keepass/mykey.key

echo "INFO: Creating database"
keepassxc-cli db-create --set-key-file ~/.config/keepass/mykey.key --set-password ~/.config/keepass/myvault.kdbx

echo "INFO: Creating database group"
keepassxc-cli mkdir -k ~/.config/keepass/mykey.key ~/.config/keepass/myvault.kdbx "mygroup"
