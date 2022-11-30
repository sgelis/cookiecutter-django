#!/usr/bin/env bash

set -euxo pipefail

./scripts/watch_dev.sh &
wait-for-it db:5432 --strict -- poetry run python src/manage.py runserver 0.0.0.0:8000
