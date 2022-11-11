![Logo](src/static/{{cookiecutter.project_slug}}/img/logo.png)

# {{ cookiecutter.project_name }}

[![code style: black](res/graphics/readme_badges/black.svg)](https://github.com/psf/black)
[![mypy: type checked](res/graphics/readme_badges/mypy.svg)](https://github.com/python/mypy)
[![bandit: security](res/graphics/readme_badges/bandit.svg)](https://github.com/PyCQA/bandit)

# User requirements

- Browser
    - Firefox ≥ 74 (recommended)
    - Chrome ≥ 80
    - Edge ≥ 80
    - Safari ≥ 13.4
    - Opera ≥ 67

## Dev requirements

- Git ([Debian stable version](https://packages.debian.org/stable/git))
- Node ([latest version from NodeSource](https://github.com/nodesource/distributions/blob/master/README.md#debinstall))
- Python 3 ([Debian stable version](https://packages.debian.org/stable/python3))
- Poetry ([latest version](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions))
- PostgreSQL ([Debian stable version](https://packages.debian.org/stable/postgresql))
- PostgreSQL Client ([Debian stable version](https://packages.debian.org/stable/postgresql-client))
- libpq-dev ([Debian stable version](https://packages.debian.org/stable/libpq-dev))
- swig ([Debian stable version](https://packages.debian.org/stable/swig))

## Run locally

```sh
git clone git@github.com:{{ cookiecutter.company }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

poetry install
npm install

node_modules/gulp/bin/gulp.js ts
node_modules/gulp/bin/gulp.js sass

cp .env.template .env
# Define environment variables as required
nano .env

poetry run python src/manage.py migrate
poetry run python src/manage.py collectstatic
poetry run python src/manage.py compilemessages
poetry run python src/manage.py runserver_plus
```

### Reset database after schema modifications

```sh
poetry run invoke reset-dev-db
```

## QA

### Run tests

```sh
# Run tests without coverage report
poetry run invoke pytest
# Run tests with coverage report (CLI)
poetry run invoke coverage
# Run tests with coverage report (HTML)
poetry run invoke coverage --html
```

### Run static type-checker

```sh
poetry run invoke mypy
```

### Run static security analysis

```sh
poetry run invoke bandit
```

### Generate developer documentation

```sh
# Build docs
poetry run invoke mkdocs
# Serve docs dynamically
poetry run invoke mkdocs --serve
```

## Deploy

TBD
