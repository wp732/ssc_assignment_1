#!/bin/bash

# Script to add a key (username) value (password) pair to the keepassxc database

keyname="$1"
if [ -z "${keyname}" ]; then
	echo "ERROR: keyname cannot be blank" >&2
	exit 255
fi

keepassxc-cli add -k ~/.config/keepass/mykey.key ~/.config/keepass/myvault.kdbx -u $keyname -p "mygroup/${keyname}"
