from fastapi import APIRouter, File, UploadFile, Form
from app.services.ai_service import summarize_text
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text

router = APIRouter()

@router.post("/summarize")
async def summarize_pdf(
    file : UploadFile = File(...),
    percentage : int = Form(...)
):
    """
    Nimmt eine PDF-Datei und eine Prozentangabe entgegen,
    extrahiert Text und gibt eine zusammengefasste Version zurück.
    """

    try:
        pdf_text = extract_text_from_pdf(await file.read())
        chunk_list = chunk_text(pdf_text)

        #summary = summarize_text(pdf_text)
        return {"summary": chunk_list}
    except Exception as e:
        return {"error": str(e)}