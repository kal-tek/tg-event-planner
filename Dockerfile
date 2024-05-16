# `python-base` sets up all our shared environment variables
FROM python:3.11 as python-base

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
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# set env type to distinguish between production and non-production envs
ARG ENV_TYPE=development
ENV ENVIRONMENT=${ENV_TYPE}


####################################################
# Build builder
####################################################
FROM python-base as builder-base

# If you change the installed packages, don't forget to update this:
# .github/workflows/update-dependencies.yaml:jobs.docker-dependencies.strategy.matrix
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl=7.88.1-10+deb12u5 \
        wget=1.21.3-1+b2 \
        # deps for building python deps
        build-essential=12.9

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --only main


####################################################
# Build runtime stage
####################################################
FROM python-base as runtime
ENV ENVIRONMENT=development

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
WORKDIR $PYSETUP_PATH
RUN poetry install

# Conditional block for non-production envs. Install if ENV_TYPE is staging or development.
# hadolint ignore=DL3003
RUN if [ "${ENV_TYPE}" != "production" ]; then \
    cd "$PYSETUP_PATH" && \
    poetry install ; \
    fi

COPY ./manage.py /app/
COPY ./Procfile.sh /app/
COPY ./event_planner /app/event_planner
RUN find /app -name tests -type d -prune -exec rm -rf {} \;

WORKDIR /app
CMD ["bash", "Procfile.sh"]
