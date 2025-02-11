#!/bin/bash

# Set the size threshold (in bytes) for what you consider a "large" file
SIZE_THRESHOLD=100000000  # 100 MB

# List all objects and their sizes
git rev-list --objects --all |
git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
awk -v threshold=$SIZE_THRESHOLD '$3 >= threshold {print $3, $2, $4}' |
sort -nr |
awk '{print $1/1048576 " MB", $2, $3}'