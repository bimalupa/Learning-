from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_version: str = "2024-02-15"
    azure_openai_deployment_name: str = "gpt-35-turbo"
    azure_openai_embedding_deployment: str = "text-embedding-3-large"

    # Fallback OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"

    # Vector Store
    chroma_db_path: str = "./data/chroma_db"
    chroma_collection_name: str = "insurance_claims"

    # App Settings
    log_level: str = "INFO"
    debug: bool = False

    # NeMo Guardrails
    guardrails_enabled: bool = True

    # Evaluation
    ragas_batch_size: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
