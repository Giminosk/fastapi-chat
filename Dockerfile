FROM python:3.12-slim

WORKDIR /src

RUN apt update -y && \
    pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false
COPY pyproject.toml .
RUN poetry install --only main

COPY /src/* .