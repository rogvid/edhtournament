FROM python:3.8.3-slim-buster as python-base

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
  && apt-get install --no-install-recommends -y netcat-openbsd

##################
#  Builder base  #
##################
FROM python-base as builder-base
RUN apt-get install --no-install-recommends -y \
      curl \
      build-essential

# Install poetry
ENV POETRY_VERSION=1.0.5
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

#################
#  Development  #
#################
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
WORKDIR /app

# COPY ./scripts/entrypoint.sh .

COPY . .

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

################
#  Production  #
################
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Create the app user directory
RUN mkdir -p api
RUN mkdir -p api/staticfiles
WORKDIR /api


# Create the app user
RUN addgroup --system user && adduser --system --no-create-home --group user
# chown all the files to the app user and change execution rights
RUN chown -R app:app /api && chmod -R 755 /api

# Add entrypoint
COPY ./scripts/entrypoint.sh /api/entrypoint.sh
RUN chmod +x /api/entrypoint.sh

# Change to non-root user
USER user

COPY . .

# run entrypoint.sh
ENTRYPOINT ["/api/scripts/entrypoint.sh"]
