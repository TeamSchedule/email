ARG PYTHON_VERSION=3.8.10
FROM python:${PYTHON_VERSION}-slim

RUN apt-get update && pip install poetry && poetry config virtualenvs.create false

WORKDIR /email_sender
COPY . /email_sender/
COPY ./pyproject.toml       /email_sender/
COPY ./poetry.lock          /email_sender/

RUN poetry install
COPY ./email_sender /email_sender/email_sender
ENTRYPOINT poetry run python main.py
