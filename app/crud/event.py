from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import (
    Organizer, EventCategory, Event,
    EventAttendee, EventSponsor
)
from app.schemas.event import (
    OrganizerCreate, OrganizerUpdate,
    EventCategoryCreate, EventCategoryUpdate,
    EventCreate, EventUpdate,
    EventAttendeeCreate, EventAttendeeUpdate,
    EventSponsorCreate, EventSponsorUpdate
)
from app.schemas.base import PaginationParams


class CRUDOrganizer(CRUDBase[Organizer, OrganizerCreate, OrganizerUpdate]):
    async def get_by_user(
            self,
            db: AsyncSession,
            *,
            user_id: int
    ) -> List[Organizer]:
        """Get organizers by user ID"""
        result = await db.execute(
            select(Organizer)
            .filter(Organizer.user_id == user_id)
            .filter(Organizer.status == True)
        )
        return result.scalars().all()


class CRUDEventCategory(CRUDBase[EventCategory, EventCategoryCreate, EventCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[EventCategory]:
        """Get all active event categories"""
        result = await db.execute(
            select(EventCategory).filter(EventCategory.status == True)
        )
        return result.scalars().all()


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    async def get_by_user(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Event]:
        """Get events by user ID"""
        result = await db.execute(
            select(Event)
            .filter(Event.user_id == user_id)
            .filter(Event.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_organizer(
            self,
            db: AsyncSession,
            *,
            organizer_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Event]:
        """Get events by organizer ID"""
        result = await db.execute(
            select(Event)
            .filter(Event.organizer_id == organizer_id)
            .filter(Event.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_category(
            self,
            db: AsyncSession,
            *,
            category_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Event]:
        """Get events by category ID"""
        result = await db.execute(
            select(Event)
            .filter(Event.category_id == category_id)
            .filter(Event.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_location(
            self,
            db: AsyncSession,
            *,
            country_id: Optional[int] = None,
            region_id: Optional[int] = None,
            district_id: Optional[int] = None,
            ward_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Event]:
        """Get events by location"""
        query = select(Event).filter(Event.status == True)

        if country_id:
            query = query.filter(Event.country_id == country_id)

        if region_id:
            query = query.filter(Event.region_id == region_id)

        if district_id:
            query = query.filter(Event.district_id == district_id)

        if ward_id:
            query = query.filter(Event.ward_id == ward_id)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def search_events(
            self,
            db: AsyncSession,
            *,
            search_term: Optional[str] = None,
            category_id: Optional[int] = None,
            organizer_id: Optional[int] = None,
            country_id: Optional[int] = None,
            region_id: Optional[int] = None,
            district_id: Optional[int] = None,
            params: PaginationParams
    ) -> Dict[str, Any]:
        """Search events with filters"""
        # Base query
        query = select(Event).filter(Event.status == True)

        # Apply filters
        if search_term:
            query = query.filter(Event.name.ilike(f"%{search_term}%"))

        if category_id:
            query = query.filter(Event.category_id == category_id)

        if organizer_id:
            query = query.filter(Event.organizer_id == organizer_id)

        if country_id:
            query = query.filter(Event.country_id == country_id)

        if region_id:
            query = query.filter(Event.region_id == region_id)

        if district_id:
            query = query.filter(Event.district_id == district_id)

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination
        offset = (params.page - 1) * params.limit
        query = query.offset(offset).limit(params.limit)

        # Get paginated results
        result = await db.execute(query)
        items = result.scalars().all()

        # Calculate total pages
        total_pages = (total + params.limit - 1) // params.limit if total > 0 else 0

        return {
            "items": items,
            "total": total,
            "page": params.page,
            "limit": params.limit,
            "pages": total_pages
        }

    async def increment_view_count(self, db: AsyncSession, *, event_id: int) -> Optional[Event]:
        """Increment the view count of an event"""
        event = await self.get(db, id=event_id)
        if event:
            event.view_count = event.view_count + 1
            db.add(event)
            await db.commit()
            await db.refresh(event)
        return event


class CRUDEventAttendee(CRUDBase[EventAttendee, EventAttendeeCreate, EventAttendeeUpdate]):
    async def get_by_event(
            self,
            db: AsyncSession,
            *,
            event_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[EventAttendee]:
        """Get attendees by event ID"""
        result = await db.execute(
            select(EventAttendee)
            .filter(EventAttendee.event_id == event_id)
            .filter(EventAttendee.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[EventAttendee]:
        """Get events attended by user"""
        result = await db.execute(
            select(EventAttendee)
            .filter(EventAttendee.user_id == user_id)
            .filter(EventAttendee.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user_and_event(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            event_id: int
    ) -> Optional[EventAttendee]:
        """Check if a user is attending an event"""
        result = await db.execute(
            select(EventAttendee)
            .filter(EventAttendee.user_id == user_id)
            .filter(EventAttendee.event_id == event_id)
        )
        return result.scalars().first()

    async def count_attendees(self, db: AsyncSession, *, event_id: int) -> int:
        """Count attendees for an event"""
        result = await db.execute(
            select(func.count())
            .select_from(EventAttendee)
            .filter(EventAttendee.event_id == event_id)
            .filter(EventAttendee.status == True)
        )
        return result.scalar() or 0


class CRUDEventSponsor(CRUDBase[EventSponsor, EventSponsorCreate, EventSponsorUpdate]):
    async def get_by_event(
            self,
            db: AsyncSession,
            *,
            event_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[EventSponsor]:
        """Get sponsors by event ID"""
        result = await db.execute(
            select(EventSponsor)
            .filter(EventSponsor.event_id == event_id)
            .filter(EventSponsor.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_organizer(
            self,
            db: AsyncSession,
            *,
            organizer_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[EventSponsor]:
        """Get events sponsored by organizer"""
        result = await db.execute(
            select(EventSponsor)
            .filter(EventSponsor.organizer_id == organizer_id)
            .filter(EventSponsor.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


organizer = CRUDOrganizer(Organizer)
event_category = CRUDEventCategory(EventCategory)
event = CRUDEvent(Event)
event_attendee = CRUDEventAttendee(EventAttendee)
event_sponsor = CRUDEventSponsor(EventSponsor)
