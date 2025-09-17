import logging
from typing import List, Dict

from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError

from app.config import settings
from app.models.chunk_model import ChunkModel

logger = logging.getLogger(__name__)

class StorageService:
    """Service zum Speichern und Abfragen von Chunks in Azure AI Search."""
    def __init__(self, endpoint: str = None, key: str = None, index_name: str = None):
            self.client = SearchClient(
                   endpoint=endpoint or settings.search_api_endpoint,
                   credential=AzureKeyCredential(key or settings.search_api_key),
                   index_name= index_name or settings.search_api_index
            )

    async def save_chunks(self, chunks: List[ChunkModel]) -> None:
        """
        Speichert eine Liste von Chunks in Azure AI Search (VectorDB).
        """
        try:       
            docs = [chunk.model_dump() for chunk in chunks]
            result = await self.client.upload_documents(documents=docs)
            logger.info(f"Uploaded {len(docs)} chunks, status={result[0].status_code if result else 'unknown'}")
        except AzureError as e:
             logger.exception("Fehler beim Speichern der Chunks in Azure Search")
             raise


    async def get_chunks_by_id(self, pdf_id: str, top: int = 500) -> List[dict]:
        """Holt alle Chunks für eine bestimmte PDF aus Azure Search."""
        try:
             results= await self.client.search(
                  search_text="*",
                  filter=f"pdf_id eq '{pdf_id}'",
                  top=top
            )
             return [doc async for doc in results]
        except AzureError:
             logger.exception(f"Fehler beim Abrufen der Chunks für pdf_id={pdf_id}")
        raise


    async def get_all_pdf_ids(self, top: int = 500) -> List[str]:
        """Holt alle PDF-IDs aus Azure Search."""
        try:
            results = await self.client.search(
                search_text="*",
                select="pdf_id",
                top=top
            )
            pdf_ids = [doc["pdf_id"] async for doc in results if "pdf_id" in doc]
            unique_ids = list(set(pdf_ids))
            return unique_ids
        except AzureError:
             logger.exception("Fehler beim Abrufen der PDF-IDs")
             raise

    async def delete_all_pdfs(self) -> None:
        """Löscht alle PDFs aus Azure Search.""" 
        try:
            pdf_ids = await self.get_all_pdf_ids()
            docs_to_delete = [{"pdf_id": pdf_id} for pdf_id in pdf_ids]
            if docs_to_delete:
                await self.client.delete_documents(documents=docs_to_delete)
                logger.info(f"Deleted {len(docs_to_delete)} PDFs from Azure Search")
        except AzureError:
             logger.exception("Fehler beim löschen der PDFs")
             raise
