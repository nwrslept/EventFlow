from pydantic import BaseModel, ConfigDict, Field, computed_field
from datetime import datetime
from typing import Optional, List


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    date_time: datetime
    slots: int = Field(default=100, ge=1, description="Max available spots")


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    created_at: datetime
    owner_id: int
    slots: int

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def participants_count(self) -> int:
        if hasattr(self, "participants"):
             return len(self.participants)
        return 0
