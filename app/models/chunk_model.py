from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class ChunkModel(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    pdf_id: str
    file_name: Optional[str] = None
    page_number: Optional[int] = None
    chunk_index: int
    chunk_text: str
    embedding: Optional[List[float]] = None
    source_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)
