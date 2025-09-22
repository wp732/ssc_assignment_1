#!/bin/bash

jq -r '.cert' $1 | base64 -d | openssl x509 -text -noout
