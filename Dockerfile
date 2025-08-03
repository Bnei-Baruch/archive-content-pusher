ARG laitman_ru_url="https://test.laitman-ru.kab.sh"
ARG laitman_ru_username="username"
ARG laitman_ru_password="password"

FROM python:3.13-slim

LABEL maintainer="edoshor@gmail.com"

ARG laitman_ru_url
ARG laitman_ru_username
ARG laitman_ru_password

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential gcc mailutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (adjust version if needed)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is in PATH
ENV PATH="/root/.local/bin:$PATH"

# Disable Poetry virtualenvs (we want everything in the system Python)
ENV POETRY_VIRTUALENVS_CREATE=false

# Set workdir and copy files
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi

# set up mailutils
RUN mkdir -p /etc/postfix && touch /etc/postfix/main.cf
RUN echo "mydomain = bbdomain.org" >> /etc/postfix/main.cf
RUN echo "myhostname = app.mdb" >> /etc/postfix/main.cf
RUN echo "myorigin = \$mydomain" >> /etc/postfix/main.cf
RUN echo "relayhost = [smtp.local]" >> /etc/postfix/main.cf

COPY . .

ENV LAITMAN_RU_URL=${laitman_ru_url} \
    LAITMAN_RU_USERNAME=${laitman_ru_username} \
    LAITMAN_RU_PASSWORD=${laitman_ru_password}  

CMD ["python", "wp-autopost.py"]
