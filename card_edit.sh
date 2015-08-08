#!/bin/bash

for folder in /Volumes/wulf_media/wulf_archive_autoconcat/concert_cards/curators_master/*; do
  echo "rummaging through ${folder}"
  for file in $folder/*.txt; do
    echo "oh cool, i found ${file}"
    # remove trailing ...'s
    sed -i .bak 's/\.\.\.[ \t]*$//' $file
    # removes trailing whitespace
    sed -i .bak 's/[[:blank:]]*$//' $file
    echo "replaced unwanted syntaxes. a backup was saved to ${file}.bak"
  done
done
