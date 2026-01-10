from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.event import Event
from app.models.user import User

class EventService:
    @staticmethod
    async def join_event(db: AsyncSession, event_id: int, user_id: int) -> Event:
        """
        Adds a user to the event participants list.
        Checks for existence, double booking, and available slots.
        """
        query = (
            select(Event)
            .where(Event.id == event_id)
            .options(selectinload(Event.participants))
        )
        result = await db.execute(query)
        event = result.scalar_one_or_none()

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        if len(event.participants) >= event.slots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is fully booked"
            )

        for participant in event.participants:
            if participant.id == user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already joined this event"
                )

        user_query = select(User).where(User.id == user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalar_one_or_none()

        if not user:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        event.participants.append(user)
        await db.commit()
        await db.refresh(event)

        return event
