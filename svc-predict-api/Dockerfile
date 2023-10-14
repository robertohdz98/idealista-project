FROM python:3.10-slim-bullseye

#ENV DEPENDENCIESTOEXCLUDE=

ENV HOMEDIR=/app
RUN mkdir -p $HOMEDIR

WORKDIR $HOMEDIR
COPY . $HOMEDIR

ENV PYTHONPATH='$PYTHONPATH:/app'

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
#RUN poetry install --no-dev --without $DEPENDENCIESTOEXCLUDE

# CHANGE: depending on component
ENTRYPOINT ["python", "src/app.py"]
