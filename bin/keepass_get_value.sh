#!/bin/bash

# Script to get value of a key pair in the keepassxc database

keyname="$1"
if [ -z "${keyname}" ]; then
	echo "ERROR: keyname cannot be blank" >&2
	exit 255
fi

keepassxc-cli show -a "Password" -s -k ~/.config/keepass/mykey.key ~/.config/keepass/myvault.kdbx "mygroup/${keyname}"
