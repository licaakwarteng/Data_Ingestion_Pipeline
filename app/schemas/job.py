from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    source_url: HttpUrl

class JobResponse(BaseModel):
    id: int
    source_url: str
    status: str
    filename: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True