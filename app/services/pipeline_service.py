from app.services.ai_service import combine_summaries, summarize_text
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import create_embeddings_for_chunks
from app.services.storage_service import get_chunks_by_id, save_chunks
from app.models.chunk_model import ChunkModel
import asyncio

async def process_pdf(file_bytes: bytes, pdf_id:str, file_name:str):
    text = extract_text_from_pdf(file_bytes)
    chunks = chunk_text(text)
    embeddings = create_embeddings_for_chunks(chunks)

    chunk_models = []

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_models.append(
            ChunkModel(
                pdf_id=pdf_id,
                file_name=file_name,
                page_number=None,
                chunk_index=idx,
                chunk_text=chunk,
                embedding=embedding
            )
        )

    save_chunks(chunk_models)
    return chunk_models


async def summarize_pdf(pdf_id) -> str:
    """Erstellt eine Gesamtzusammenfassung einer gespeicherten PDF."""

    # Chunks holen
    docs = get_chunks_by_id(pdf_id)
    chunks = [doc["chunk_text"] for doc in docs]

    # Summary pro Chunk erstellen
    chunk_summaries = await asyncio.gather(*(summarize_text(c) for c in chunks))

    # Gesamtsummary

    final_summary = await combine_summaries(chunk_summaries)
    return final_summary
