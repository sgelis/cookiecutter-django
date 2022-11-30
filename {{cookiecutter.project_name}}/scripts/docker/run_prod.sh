#!/usr/bin/env bash

set -euxo pipefail

node_modules/gulp/bin/gulp.js build
wait-for-it db:5432 --strict -- poetry run python src/manage.py migrate
poetry run python src/manage.py collectstatic --no-input
poetry run python src/manage.py compilemessages
node_modules/gulp/bin/gulp.js rmSrc
poetry run uwsgi --ini scripts/docker/uwsgi.ini
