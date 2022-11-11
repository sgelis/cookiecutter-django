# Third party
from invoke import task


@task
def mypy(c):
    with c.cd("{{cookiecutter.project_name}}/src"):
        c.run("mypy . --config-file ../pyproject.toml")


@task
def bandit(c):
    with c.cd("{{cookiecutter.project_name}}"):
        c.run("bandit -r src -x 'tests'")


@task(mypy, bandit)
def ci(c):
    pass
