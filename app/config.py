from pydantic_settings import BaseSettings
from pydantic import Field
import os

# Liest ENVIRONMENT-Variable aus, Standard: dev
env = os.getenv("ENVIRONMENT", "dev")

class Settings(BaseSettings):
    """
    App-Configuratiuon, geladen aus .env-Datei
    """

    # General Settings
    app_name: str = Field("PDF Summarizer API", description="Name der Anwendung")
    app_env: str = Field("development", description="Environment: development/production")
    debug: bool = Field(True, description="Debug-Mode aktivieren/deaktivieren")

    # Azure AI Foundry Settings 
    azure_openai_api_key: str = Field(..., description="API-Key für Azure OpenAI")

    # Azure AI Foundry o3-Settings
    azure_openai_endpoint_o3: str = Field(..., description="Endpoint für Azure OpenAI")
    azure_openai_model_o3: str = Field(..., description="Name des von Azure bereitgestellten KI-Modells")
    azure_deployment_name_o3: str = Field(..., description="Name der deployten Ressource in Foundry")
    api_version_o3: str = Field(..., description="API-Version")

    # Azure AI Foundry Maverick-Settings
    azure_openai_endpoint_maverick: str = Field(..., description="Endpoint für Azure OpenAI")
    azure_openai_model_maverick: str = Field(..., description="Name des von Azure bereitgestellten KI-Modells")
    azure_deployment_name_maverick: str = Field(..., description="Name der deployten Ressource in Foundry")
    api_version_maverick: str = Field(..., description="API-Version")

    # Azure Embedding Settings 
    azure_openai_embedding_endpoint: str = Field(..., description="Endpunkt der Azure Embedding Ressource")
    azure_openai_embedding_deployment: str = Field(..., description="Name der Deployten Ressource")

    # Azure Search-API Settings 
    search_api_endpoint: str = Field(..., description="Endpunkt der Azure AI-Search Ressource")
    search_api_key: str = Field(..., description="API-Key für Azure AI-Search Ressource")
    search_api_index: str = Field(..., description="Name des Suchindexes")


    class Config:
        env_file = f".env.{env}"
        env_file_encoding = "utf-8"
settings = Settings()
