from pydantic_settings import BaseSettings
from pydantic import Field
import os

# Liest ENVIRONMENT-Variable aus, Standard: dev
env = os.getenv("ENVIRONMENT", "dev")

class Settings(BaseSettings):
    """
    App-Configuratiuon, geladen aus .env-Datei
    """
    app_name: str = Field("PDF Summarizer API", description="Name der Anwendung")
    app_env: str = Field("development", description="Environment: development/production")
    debug: bool = Field(True, description="Debug-Mode aktivieren/deaktivieren")

    azure_openai_endpoint: str = Field(..., description="Endpoint für Azure OpenAI")
    azure_openai_api_key: str = Field(..., description="API-Key für Azure OpenAI")
    azure_openai_model: str = Field(..., description="Name des von Azure bereitgestellten KI-Modells")
    azure_deployment_name: str = Field(..., description="Name der deployten Ressource in Foundry")

    azure_openai_embedding_endpoint: str = Field(..., description="Endpunkt der Azure Embedding Ressource")
    azure_openai_embedding_deployment: str = Field(..., description="Name der Deployten Ressource")


    class Config:
        env_file = f".env.{env}"
        env_file_encoding = "utf-8"
settings = Settings()
