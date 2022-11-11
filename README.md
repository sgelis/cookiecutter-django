# Use

- Make sure `cookiecutter` is installed on your computer (either globally or in a virtual environment, including this 
project's virtual environment):

```sh
cookiecutter -V
```

If not, install it in this project's virtual environment:

```sh
poetry install
```

OR as per [the official documentation](https://cookiecutter.readthedocs.io/en/stable/installation.html).

- Bake a new cake from this cookiecutter:

```sh
poetry run cookiecutter git@github.com:sgelis/cookiecutter-django.git

> project_name [FooProject]: 
> project_slug [fooproject]: 
> company [EvilCorp] : 
> python_interpreter [/usr/bin/python3]: 
```

- Make sure all dev requirements are installed on your system (listed on
[the project's README]({{cookiecutter.project_name}}/README.md)).
- Start developing:

```sh
cd FooProject
poetry install
npm install
pycharm . &
```

# Contribute

- Make sure `Poetry` is installed on your computer:

```sh
poetry -V
```

If not, install it as per [the official documentation](https://python-poetry.org/docs/#installation).

- Clone this repository and install its dependencies:

```sh
git clone git@github.com:sgelis/cookiecutter-django.git
cd cookiecutter-django
poetry install
```

- Have fun! But before considering opening a PR, please run the CI and make sure everything is fine:

```sh
invoke ci
```
