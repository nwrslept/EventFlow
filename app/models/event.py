from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Table, Column, Integer
from datetime import datetime
from typing import TYPE_CHECKING, List

from app.models.base import Base

if TYPE_CHECKING:
    from .user import User

event_participants = Table(
    "event_participants",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)

    slots: Mapped[int] = mapped_column(Integer, default=100)

    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="events")

    participants: Mapped[List["User"]] = relationship(
        secondary=event_participants,
        back_populates="joined_events",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Event id={self.id} title={self.title}>"
