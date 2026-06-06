FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY aivas/ aivas/

RUN pip install --no-cache-dir \
    fastapi uvicorn[standard] strawberry-graphql \
    "sqlalchemy[asyncio]>=2.0" asyncpg alembic \
    pydantic pydantic-settings redis celery \
    neo4j litellm langgraph minio python-multipart boto3

EXPOSE 8000

CMD ["python", "run.py"]
