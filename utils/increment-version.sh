#!/bin/sh
# @desc Increment version number
# @changed 2022.02.06, 23:20

test -f "./utils/config.sh" && . "./utils/config.sh"
test -f "./utils/config-local.sh" && . "./utils/config-local.sh"

# Check basic required variables...
test -f "./utils/config-check.sh" && . "./utils/config-check.sh"

# Read version from file...
VERSION_FILE="build-version.txt"
BACKUP="$VERSION_FILE.bak"

test -f "$VERSION_FILE" || echo "0.0.0" > "$VERSION_FILE"

echo "Current version: `cat $VERSION_FILE`"

# Extract patch number
PATCH_NUMBER=`cat "$VERSION_FILE" | sed "s/^\(.*\)\.\([0-9]\+\)$/\2/"`

if [ "$PATCH_NUMBER" == "" ]; then
  echo "No patch number found!"
  exit 1
fi

# Increment patch number
NEXT_PATCH_NUMBER=`expr $PATCH_NUMBER + 1`

# echo "Increment patch number ($PATCH_NUMBER -> $NEXT_PATCH_NUMBER)"

cp "$VERSION_FILE" "$BACKUP" \
  && cat "$BACKUP" \
    | sed "s/^\(.*\)\.\([0-9]\+\)$/\1.$NEXT_PATCH_NUMBER/" \
    > "$VERSION_FILE" \
  && rm "$BACKUP" \
  && echo "Updated version: `cat $VERSION_FILE`" \
  && sh "./utils/update-build-variables.sh" \
  && VERSION=`cat "$VERSION_FILE"` \
  && echo "Don't forget to update version for target project dependency (if used)"
