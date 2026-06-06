from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "AIVAS_", "env_file": ".env"}

    # Database
    database_url: str = "postgresql+asyncpg://aivas:aivas_dev@localhost:5432/aivas"
    database_url_sync: str = "postgresql+psycopg2://aivas:aivas_dev@localhost:5432/aivas"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "aivas_dev"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # MinIO / S3
    s3_endpoint: str = "localhost:9000"
    s3_access_key: str = "aivas_admin"
    s3_secret_key: str = "aivas_dev123"
    s3_bucket: str = "aivas-artifacts"
    s3_secure: bool = False

    # LLM (Anthropic Claude API)
    llm_model: str = "claude-sonnet-4-6-20251001"
    llm_api_key: str = ""
    llm_max_tokens: int = 4096

    # App
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
