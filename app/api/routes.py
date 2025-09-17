from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.services.pipeline_service import PipelineService
from app.services.storage_service import StorageService
from app.services.ai_service import AIService
import uuid

# Dependency Provider
def get_storage_service() -> StorageService:
    return StorageService()

def get_pipeline_service(
        storage: StorageService = Depends(get_storage_service)
) -> PipelineService:
    ai = AIService()
    return PipelineService(ai_service=ai, storage_service=storage)

router = APIRouter()

@router.post("/pdf_upload")
async def upload_pdf_to_vector(
    file : UploadFile = File(...),
    pipeline: PipelineService = Depends(get_pipeline_service)
):
    """
    Nimmt eine PDF-Datei entgegen, extrahiert Text und Speichert diesen in DB.
    """
    try:
        file_bytes = await file.read()
        pdf_id = str(uuid.uuid4())
        chunks = await pipeline.process_pdf(file_bytes, pdf_id, file.filename)
        return {"chunks_stored": len(chunks), "PDF-ID: ": pdf_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/summarize")
async def summarize_document(
    pdf_id: str,
    pipeline: PipelineService = Depends(get_pipeline_service)
    ):
    """
    Erstellt eine Gesamtzusammenfassung einer PDF anhand der PDF-ID
    """
    try:
        summary = await pipeline.summarize_pdf(pdf_id)
        return {"AI-Summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pdf_ids")
async def get_pdf_ids(
    storage: StorageService = Depends(get_storage_service)
):
    """
    Gibt eine Liste aller PDF-IDs zurück
    """
    try:
        pdf_ids = await storage.get_all_pdf_ids()
        return {"Alle IDs": pdf_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/delete_pdf_by_id")
async def delete_pdf(
    pdf_id: str,
    storage: StorageService = Depends(get_storage_service)
):
    """
    Löscht eine PDF anhand ihrer ID
    """
    try:
        await storage.delete_pdf_by_id(pdf_id)
        return {"message": f"PDF {pdf_id} wurde geklöscht."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
