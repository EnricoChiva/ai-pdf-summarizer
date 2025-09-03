from fastapi import APIRouter, File, UploadFile
from app.services.pipeline_service import process_pdf, summarize_pdf
import uuid

from app.services.storage_service import get_all_pdf_ids



router = APIRouter()

@router.post("/pdf_upload")
async def upload_pdf_to_vector(
    file : UploadFile = File(...),
):
    """
    Nimmt eine PDF-Datei entgegen, extrahiert Text und Speichert diesen in DB.
    """

    try:
        file_bytes = await file.read()
        pdf_id = str(uuid.uuid4())
        chunks = await process_pdf(file_bytes, pdf_id, file.filename)
        return {"chunks_stored": len(chunks)}
    
    except Exception as e:
        return {"error": str(e)}
    

@router.get("/summarize")
async def summarize_document(pdf_id: str):
    """
    Erstellt eine Gesamtzusammenfassung einer PDF anhand der PDF-ID
    """
    try:
        summary = await summarize_pdf(pdf_id)
        
        return {"AI-Summary": summary}

    except Exception as e:
        return {"error": str(e)}


@router.get("/pdf_ids")
async def get_pdf_ids():
    """
    Gibt eine Liste aller PDF-IDs zurück
    """
    try:
        pdf_ids = get_all_pdf_ids()
        return {"Alle IDs": pdf_ids}
    
    except Exception as e:
        return {"error": str(e)}