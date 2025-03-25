#!/usr/bin/env sh

SCRIPT_DIR=$(dirname $(readlink -f "$0"))
ROOT_DIR=$(dirname "${SCRIPT_DIR}")
FILENAME=${ROOT_DIR}/.dmypy.json

dmypy status
if [ $? -eq 0 ]; then
  dmypy recheck
else
  dmypy run -- "$@"
fi
