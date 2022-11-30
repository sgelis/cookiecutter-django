<img alt="Logo" height="256" src="src/static/{{cookiecutter.project_slug}}/img/logo.png" width="256"/>

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

# Dev requirements

## Using Docker

- Git ([Debian stable version](https://packages.debian.org/stable/git))
- Docker ([Debian stable version](https://docs.docker.com/engine/install/debian/#install-using-the-repository))

## Not using Docker

- Git ([Debian stable version](https://packages.debian.org/stable/git))
- Node ([latest version from NodeSource](https://github.com/nodesource/distributions/blob/master/README.md#debinstall))
- Python 3 ([Debian stable version](https://packages.debian.org/stable/python3))
- Poetry ([latest version](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions))
- PostgreSQL ([Debian stable version](https://packages.debian.org/stable/postgresql))
- PostgreSQL Client ([Debian stable version](https://packages.debian.org/stable/postgresql-client))
- libpq-dev ([Debian stable version](https://packages.debian.org/stable/libpq-dev))
- swig ([Debian stable version](https://packages.debian.org/stable/swig))
- [Optional] memcache ([Debian stable version](https://packages.debian.org/stable/memcached))

# Contribute

## With Docker

```sh
git clone git@github.com:{{ cookiecutter.company }}/{{ cookiecutter.project_name }}.git
cd {{ cookiecutter.project_name }}

cp .env.template .env
# Define environment variables as required
nano .env

docker-compose build
docker-compose run --rm -d app ./scripts/watch_dev.sh
pycharm . &
```

🐍 After opening the project in PyCharm, you need to define the remote Python interpreter: the one sitting in the Python
virtual environment in the Docker container. To do so: File → Settings → Project: {{ cookiecutter.project_name }} →
Python Interpreter → Add Interpreter → On Docker Compose… → Choose service "app" → Choose "Virtualenv Environment" and
set the path to `/app/.venv/bin/python`.

🐍 PyCharm will complain about "black" and "isort" file watchers. This is due to
[PyCharm being unable to run file watchers using the remote Python interpreter](https://youtrack.jetbrains.com/issue/WEB-9724/Support-remote-external-remote-tools-for-File-Watchers).
An equivalent of these file watchers is provided by the [`python_file_watchers.sh`](scripts/python_file_watchers.sh)
script that is itself called by the main [`watch_dev.sh`](scripts/watch_dev.sh) script.

🛠 Use the following to drop in a shell interpreter into the app container:

```sh
docker-compose run --rm -p 8000:8000 -p 9000:9000 -p 9001:9001 app bash
```

🛠 Once in the shell interpreter, you can run the usual Invoke (see QA section) and Django commands, such as:

```sh
poetry run python src/manage.py migrate
```

## Without Docker

```sh
git clone git@github.com:{{ cookiecutter.company }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

poetry install --with dev
npm install

cp .env.template .env
# Define environment variables as required
nano .env

node_modules/gulp/bin/gulp.js dev &

pycharm . &
```

🐍 After opening the project in PyCharm, you need to define the local Python interpreter: the one sitting in the local
Python virtual environment. To do so: File → Settings → Project: {{ cookiecutter.project_name }} →
Python Interpreter → Add Local Interpreter… → Check "Existing" and check that the path points to
`/path/to/{{ cookiecutter.project_name }}/.venv/bin.python`.

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

# Deploy

```sh
cp .env.template
# Define environment variables as required
nano .env
docker-compose -f docker-compose.deploy.yml build
```
