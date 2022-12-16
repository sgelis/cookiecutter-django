# Third party
from invoke import task


@task
def build_frontend_assets(c):
    c.run("rm -rf src/compiled_static/*")
    c.run("node_modules/gulp/bin/gulp.js build")
    c.run("src/frontend/node_modules/@angular/cli/bin/ng.js build")
    c.run("python src/manage.py collectstatic --no-input")


@task(build_frontend_assets)
def pytest(c, settings="config.settings.dev"):
    with c.cd("src"):
        c.run(f"pytest --ds={settings}")


@task(build_frontend_assets)
def coverage(c, html=False, settings="config.settings.dev"):
    with c.cd("src"):
        c.run(f"DJANGO_SETTINGS_MODULE={settings} coverage run --rcfile ../pyproject.toml -m pytest")
        if html:
            c.run("coverage html --rcfile ../pyproject.toml")
            c.run("echo Serving coverage report at http://localhost:9000…")
            c.run("python -m http.server --directory htmlcov 9000")
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
        c.run("mkdocs serve -a 0.0.0.0:9001")
    else:
        c.run("mkdocs build")


@task(mypy, bandit, pytest)
def ci(c):
    pass
