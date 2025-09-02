from fastapi import APIRouter, File, UploadFile, Form
from app.services.ai_service import summarize_text
from app.services.embedding_service import create_embeddings_for_chunks
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text

router = APIRouter()

@router.post("/summarize")
async def summarize_pdf(
    file : UploadFile = File(...),
):
    """
    Nimmt eine PDF-Datei entgegen, extrahiert Text und 
    gibt eine zusammengefasste Version zurück.
    """

    try:
        pdf_text = extract_text_from_pdf(await file.read())
        chunk_list = chunk_text(pdf_text)
        embeddings = create_embeddings_for_chunks(chunk_list)

        #summary = summarize_text(pdf_text)
        return {"embeddings": embeddings}
    except Exception as e:
        return {"error": str(e)}