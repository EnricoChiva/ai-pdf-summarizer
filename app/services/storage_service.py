from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings
from app.models.chunk_model import ChunkModel


client = SearchClient(
    endpoint=settings.search_api_endpoint,
    credential=AzureKeyCredential(settings.search_api_key),
    index_name=settings.search_api_index
)

def save_chunks(chunks: list[ChunkModel]) -> None:
    """
    Speichert eine Liste von Chunks in Azure AI Search - VectorDB
    """
    docs = [chunk.model_dump() for chunk in chunks]
    client.upload_documents(documents=docs)


def get_chunks_by_id(pdf_id: str) -> list[dict]:
    """Holt alle Chunks für eine bestimmte PDF aus Azure Search."""
    results = client.search(
        search_text="*",
        filter=f"pdf_id eq '{pdf_id}'",
        top=100
    )
    return [doc for doc in results]


def get_all_pdf_ids() -> list[str]:
    """Holt alle PDF-IDs aus Azure Search."""
    results = client.search(
        search_text="*",
        select="pdf_id",
        top=100
    )

    pdf_ids = {doc["pdf_id"] for doc in results if "pdf_id" in doc}
    return list(pdf_ids)

def delete_all_pdfs():
    pdf_ids = get_all_pdf_ids()
    docs_to_delete = [{"pdf_id": pdf_id} for pdf_id in pdf_ids]
    if docs_to_delete:
        client.delete_documents(documents=docs_to_delete)
