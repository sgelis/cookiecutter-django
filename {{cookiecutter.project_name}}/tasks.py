# Third party
from invoke import task


def reset_dev_db(
    c,
    migrate=True,
    prompt="All data from the database will be lost.\nContinue? (y/N) ",
):
    response = input(prompt)
    if response.lower() != "y":
        print("DB reset canceled by user.")
        return

    c.run('sudo -u postgres psql -c "DROP DATABASE IF EXISTS {{ cookiecutter.project_slug }}"')
    c.run('sudo -u postgres psql -c "DROP DATABASE IF EXISTS {{ cookiecutter.project_slug }}_test"')
    c.run('sudo -u postgres psql -c "DROP USER IF EXISTS {{ cookiecutter.project_slug }}"')
    c.run("sudo -u postgres psql -c \"CREATE DATABASE {{ cookiecutter.project_slug }} WITH ENCODING 'UTF8'\"")
    c.run("sudo -u postgres psql -c \"CREATE USER {{ cookiecutter.project_slug }} WITH ENCRYPTED PASSWORD 'abc123'\"")
    c.run('sudo -u postgres psql -c "ALTER USER {{ cookiecutter.project_slug }} CREATEDB"')
    c.run("sudo -u postgres psql -c \"ALTER ROLE {{ cookiecutter.project_slug }} SET client_encoding TO 'utf8'\"")
    c.run(
        'sudo -u postgres psql -c "ALTER ROLE {{ cookiecutter.project_slug }} SET default_transaction_isolation TO '
        "'read committed'\""
    )
    c.run("sudo -u postgres psql -c \"ALTER ROLE {{ cookiecutter.project_slug }} SET timezone TO 'UTC'\"")
    c.run(
        'sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {{ cookiecutter.project_slug }} TO '
        '{{ cookiecutter.project_slug }}"'
    )

    if migrate:
        with c.cd("src"):
            c.run("python manage.py migrate --settings config.settings.dev")


@task
def pytest(c, settings="config.settings.dev"):
    with c.cd("src"):
        c.run(f"pytest --ds={settings}")


@task
def coverage(c, html=False, settings="config.settings.dev"):
    with c.cd("src"):
        c.run(f"DJANGO_SETTINGS_MODULE={settings} coverage run --rcfile ../pyproject.toml -m pytest")
        if html:
            c.run("coverage html --rcfile ../pyproject.toml")
            c.run('python -c \'import webbrowser; webbrowser.get("x-www-browser").open("htmlcov/index.html")\'')
        else:
            c.run("coverage report --rcfile ../pyproject.toml")


@task
def mypy(c):
    with c.cd("src"):
        c.run("mypy . --config-file ../pyproject.toml")


@task
def bandit(c):
    c.run("bandit -r src -x 'tests'")


@task
def mkdocs(c, serve=False):
    if serve:
        c.run("mkdocs serve")
    else:
        c.run("mkdocs build")


@task(mypy, bandit, pytest)
def ci(c):
    pass
