#!/usr/bin/env bash

set -euxo pipefail

node_modules/gulp/bin/gulp.js dev &
npm --prefix src/frontend run watch &
find src -name '*.py' | entr -p ./scripts/python_file_watchers.sh /_
