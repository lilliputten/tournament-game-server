#!/bin/sh
# @desc Update build date/time tag file with current timestamp
# @changed 2022.01.17, 21:16
# NOTE: This script updates only .txt files not properties in `package.json`.
# Use `update-build-variables.sh` script before build.

node "./utils/update-build-time.js"
