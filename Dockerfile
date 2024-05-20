FROM python:3.11-slim as builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes


FROM python:3.11-slim as dev

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder requirements.dev.txt ./

RUN apt update -y && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.dev.txt

COPY /src/* .

EXPOSE 8000