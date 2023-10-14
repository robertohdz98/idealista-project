FROM python:3.10-slim-bullseye

RUN apt-get update --fix-missing
RUN apt-get install -y git make

ENV HOMEDIR=/app
RUN mkdir -p $HOMEDIR
COPY . $HOMEDIR
WORKDIR $HOMEDIR
ENV PYTHONPATH='$PYTHONPATH:/app'

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false && poetry install --no-dev
