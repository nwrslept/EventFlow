from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.event import Event
from app.models.user import User
from app.schemas.filters import EventFilterParams
from typing import List
from sqlalchemy import or_


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

    @staticmethod
    async def get_multi(
            db: AsyncSession,
            filters: EventFilterParams
    ) -> List[Event]:
        """
        Get list of events with filtering and pagination.
        """
        query = select(Event).options(selectinload(Event.participants))

        if filters.keyword:
            search = f"%{filters.keyword}%"
            query = query.filter(
                or_(
                    Event.title.ilike(search),
                    Event.description.ilike(search)
                )
            )

        if filters.start_date:
            query = query.filter(Event.date_time >= filters.start_date)

        if filters.end_date:
            query = query.filter(Event.date_time <= filters.end_date)

        query = query.order_by(Event.date_time.asc())

        query = query.offset(filters.skip).limit(filters.limit)

        result = await db.execute(query)
        return result.scalars().all()
