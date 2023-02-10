FROM python:3.10.10-slim-bullseye
EXPOSE 8000 9000 9001
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION="1.2.2" \
    NODE_VERSION=18

RUN adduser --disabled-password app

COPY --chown=app:app poetry.toml poetry.lock pyproject.toml package.json package-lock.json ./
COPY --chown=app:app src/frontend/package.json src/frontend/package-lock.json src/frontend/
RUN chown app:app . && \
    apt update && \
    apt -y upgrade && \
    apt -y --no-install-recommends install build-essential entr gettext gpg libpq5 libpq-dev wait-for-it wget && \
    mkdir /etc/apt/keyrings && \
    wget -qO - 'https://deb.nodesource.com/gpgkey/nodesource.gpg.key' | gpg --dearmor | tee /etc/apt/keyrings/nodesource.gpg > /dev/null && \
    echo "Types: deb deb-src\nURIs: https://deb.nodesource.com/node_${NODE_VERSION}.x\nSuites: bullseye\nComponents: main\nSigned-By: /etc/apt/keyrings/nodesource.gpg" | tee /etc/apt/sources.list.d/nodejs.sources > /dev/null && \
    apt update && \
    apt -y --no-install-recommends install nodejs && \
    pip install --upgrade pip && \
    pip install poetry=="${POETRY_VERSION}" && \
    su app -c 'poetry --no-cache --no-interaction --no-ansi install --with dev' && \
    su app -c 'npm install' && \
    su app -c 'cd src/frontend && npm install' && \
    apt -y purge build-essential libpq-dev wget gpg && \
    apt -y autoremove && \
    apt -y purge ~c && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /home/app/.cache /home/app/.npm && \
    rm -rf src/frontend/.angular/cache && \
    mkdir -m 775 /var/log/{{ cookiecutter.project_slug }} && \
    chown app:app /var/log/{{ cookiecutter.project_slug }}

COPY --chown=app:app . ./

USER app

CMD ["scripts/docker/run_dev.sh"]
