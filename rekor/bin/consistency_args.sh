#!/bin/bash

checkpoint_file=$1

jq -r '.treeID,.treeSize,.rootHash' $checkpoint_file | xargs printf "--consistency --tree-id %s --tree-size %s --root-hash %s\n"
