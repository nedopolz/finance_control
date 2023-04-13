FROM python:latest

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .
