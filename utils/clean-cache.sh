#!/bin/sh
# @desc Clean all temp files
# @since 2022.02.15, 06:01
# @changed 2022.02.23, 23:19

test -f "./utils/config.sh" && . "./utils/config.sh"
test -f "./utils/config-local.sh" && . "./utils/config-local.sh"

# NOTE: Those commands broke all searches
#   -not \( -name '*_' -prune \) \
#   -not \( -name '*~' -prune \) \

${FINDCMD} . \
  -not \( -name '.git' -prune \) \
  -not \( -name '.vscode' -prune \) \
  -not \( -name '.next' -prune \) \
  -not \( -name '.venv*' -prune \) \
  -not \( -name 'out' -prune \) \
  -not \( -name 'build*' -prune \) \
  -not \( -name '*UNUSED' -prune \) \
  -not \( -name 'publish*' -prune \) \
  -not \( -name 'node_modules' -prune \) \
  -type d \
  -name __pycache__ \
  -exec rm -Rf {} \;

rm -Rf *.py[co] \
  .*sw[op] \
  *.bak *.tmp

