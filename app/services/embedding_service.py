from openai import AzureOpenAI
from app.config import settings
from azure.core.credentials import AzureKeyCredential


client = AzureOpenAI(
    azure_endpoint=settings.azure_openai_embedding_endpoint,
    api_key=settings.azure_openai_api_key,
    api_version="2024-12-01-preview"
)


def create_embedding(text:str) -> list[float]:
    """
    Erzeugt ein Embedding für den gegebenen Text via Azure OpenAI.
    """
    response = client.embeddings.create(
        input=text,
        model=settings.azure_openai_embedding_deployment
    )
    return response.data[0].embedding


def create_embeddings_for_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Wandelt eine Liste von Text-Chunks in Embeddings um.
    """
    embeddings = []
    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)
    return embeddings

