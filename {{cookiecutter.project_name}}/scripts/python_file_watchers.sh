#!/usr/bin/env bash

set -euxo pipefail

poetry run isort "$1"
poetry run black "$1"
