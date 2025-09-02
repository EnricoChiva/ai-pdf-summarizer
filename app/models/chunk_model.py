from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class ChunkModel(BaseModel):
    chunk_id: str = str(uuid.uuid4())
    pdf_id: str
    file_name: Optional[str] = None
    page_number: Optional[int] = None
    chunk_index: int
    chunk_text: str
    embedding: Optional[List[float]] = None
    source_url: Optional[str] = None
    created_at: datetime = datetime.now(tz=None)
    tags: Optional[List[str]] = []
