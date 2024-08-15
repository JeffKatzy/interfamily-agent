
FROM --platform=linux/amd64 python:3.12-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-dev && poetry show

COPY . /app/

EXPOSE 8080



CMD ["poetry", "run", "python", "-m", "chainlit", "run", "app.py", "-h", "--port", "8080"]