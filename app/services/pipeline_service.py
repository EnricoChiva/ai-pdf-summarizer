import asyncio
import logging
from typing import List

from app.services.ai_service import AIService
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import create_embeddings_for_chunks
from app.services.storage_service import StorageService
from app.models.chunk_model import ChunkModel

logger = logging.getLogger(__name__)
class PipelineService:
    """
    Service für die Verarbeitung von PDFs und Erstellung von Summaries.
    """

    def __init__(self, ai_service: AIService, storage_service: StorageService):
        self.ai = ai_service
        self.storage = storage_service
        pass

    async def process_pdf(self, file_bytes: bytes, pdf_id: str, file_name: str) -> List[ChunkModel]:
        """
        Extrahiert Text, erstellt Chunks + Embeddings und speichert sie.
        """
        try:
            text = extract_text_from_pdf(file_bytes)
            chunks = chunk_text(text)
            embeddings = create_embeddings_for_chunks(chunks)

            chunk_models = [
                ChunkModel(
                    pdf_id=pdf_id,
                    file_name=file_name,
                    page_number=None,
                    chunk_index=idx,
                    chunk_text=chunk,
                    embedding=embedding
                )
                for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings))
            ]

            self.storage.save_chunks(chunk_models)
            return chunk_models
        except Exception:
            logger.exception("process_pdf failed")
            raise


    async def summarize_pdf(self, pdf_id) -> str:
        """
        Erstellt eine Gesamtzusammenfassung einer gespeicherten PDF.
        """
        try:
            docs = await self.storage.get_chunks_by_id(pdf_id)
            chunks = [doc["chunk_text"] for doc in docs]

            # Chunk-Summaries mit Limit für gleichzeitige Requests
            chunk_summaries = await self.ai.pre_summarize_many(chunks, concurrency=4)

            # Gesamtsummary
            final_summary = await self.ai.combine_summaries(chunk_summaries)
            return final_summary
        except Exception as e:
            logger.exception("summarize_pdf failed")
            raise