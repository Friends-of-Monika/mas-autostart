#!/bin/sh

# Builds a package with the submod.
# Usage: $ scripts/build PACKAGE_NAME

dir="$(dirname "$(CDPATH="" cd -- "$(dirname -- "$0")" && pwd)")"
temp="$(mktemp -d)"

mkdir -p "$temp/game/Submods"
cp -r "$dir/mod" "$temp/game/Submods/MAS Autostart Mod"
(cd "$temp" || exit 1; find game | zip -9@ "$dir/$1" && rm -rf "$temp")