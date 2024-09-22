ARG PYTHON_IMAGE_TAG=3.12-slim-bookworm

FROM python:${PYTHON_IMAGE_TAG} AS builder

ENV PIP_NO_CACHE_DIR=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_PATH=/app/.venv

WORKDIR /app

RUN pip install poetry==${POETRY_VERSION};

COPY ["./pyproject.toml", "poetry.lock", "./"]

RUN poetry install --without=dev;

FROM python:${PYTHON_IMAGE_TAG}
WORKDIR /app

RUN apt-get -y update && apt-get install -y curl

COPY --from=builder /app/.venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH

COPY ["./", "./"]

CMD ["python", "-m", "worker", "worker", "-l", "info"]
HEALTHCHECK --interval=10s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -fs http://localhost:6066 || exit 1