import io
import re
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extrahiert Text aus einer PDF-Datei und bereinigt Formatierungsprobleme:
    - Entfernt unnötige Zeilenumbrüche mitten im Satz.
    - Setzt Wörter zusammen, die durch Bindestrich getrennt wurden.
    - Normalisiert Leerzeichen und Absätze.
    """
    pdf_stream = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_stream)
    raw_text = ""

    # Text aus allen Seiten holen
    for page in reader.pages:
        raw_text += page.extract_text() or ""

    # 1. Bindestrich-Zeilenumbrüche reparieren
    text = re.sub(r"-\s*\n\s*", "", raw_text)

    # 2. Punkte/Leerzeichen zwischen Buchstaben entfernen (z.B. "G e s u n d" -> "Gesund")
    text = re.sub(r"(?<=\b)([A-Za-zÄÖÜäöüß])(?:\s*\.\s*|\s+)(?=[A-Za-zÄÖÜäöüß])", r"\1", text)

    # 3. Einzelne Zeilenumbrüche mitten im Satz durch Leerzeichen ersetzen
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # 4. Mehrfache Leerzeichen reduzieren
    text = re.sub(r"\s{2,}", " ", text)

    # 5. Absätze bei Doppel-Umbruch wiederherstellen
    text = re.sub(r"\n{2,}", "\n\n", text)


    return text.strip()
