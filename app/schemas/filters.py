from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventFilterParams(BaseModel):
    limit: int = Field(10, ge=1, le=100, description="Page size")
    skip: int = Field(0, ge=0, description="Offset for pagination")
    keyword: Optional[str] = Field(None, description="Search by title or description")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
