# Base Python
FROM python:3.13-slim as python-base

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Adiciona Poetry e virtualenv ao PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Cria diretório de trabalho
WORKDIR $PYSETUP_PATH

# Copia pyproject.toml e gera o lockfile
COPY pyproject.toml ./
RUN /opt/poetry/bin/poetry lock

# Instala dependências do projeto sem dev
RUN /opt/poetry/bin/poetry install --no-dev

# Copia o restante do projeto
WORKDIR /app
COPY . /app/

# Exposição da porta do Django
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
