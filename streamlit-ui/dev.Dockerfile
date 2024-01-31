FROM python:3.10-slim-bullseye

#ENV DEPENDENCIESTOEXCLUDE=

ENV HOMEDIR=/app
RUN mkdir -p $HOMEDIR

WORKDIR $HOMEDIR
COPY . $HOMEDIR

ENV PYTHONPATH='$PYTHONPATH:/app'

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry idna

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root
#RUN poetry install --no-dev --without $DEPENDENCIESTOEXCLUDE
