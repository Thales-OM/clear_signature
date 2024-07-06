# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9.8
FROM python:${PYTHON_VERSION}-slim as base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.3 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # cache
    POETRY_CACHE_DIR="/mnt/cache/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry==${POETRY_VERSION}

# Activate the virtual environment
ENV VIRTUAL_ENV=/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y tk

# Use Poetry to install dependencies
RUN poetry install --no-interaction --no-root

# Copy the source code into the image
COPY . .

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
# CMD ["python","app.py"]
# CMD ["/venv/bin/activate", "&&", "python", "app.py"]
CMD ["/venv/bin/activate"]

# Switch to the non-privileged user to run the application.
USER appuser

CMD ["python", "app.py"]