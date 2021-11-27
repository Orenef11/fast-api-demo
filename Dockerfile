# pull official base image
FROM python:3.10.0-alpine3.14

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV AUTH_TOKEN 80dc8410463333e3dd615b241ae8ee337700e51dc01b23276ec1ee0d9819e39e

WORKDIR /code
# copy project
COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock

# install dependencies
RUN set -eux \
    && apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps build-base curl libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --no-cache-dir --upgrade pip setuptools wheel poetry \
    && poetry install \
    && rm -rf /root/.cache/pip


COPY . /code

ENTRYPOINT ["poetry", "run", "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000"]
#ENTRYPOINT ["poetry", "run", "pytest", "tests"]
