FROM python:3.13-slim

WORKDIR /app

ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y curl build-essential --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --only main --no-interaction

ENV PATH="/app/.venv/bin:$PATH"


COPY . /app

EXPOSE 8000

