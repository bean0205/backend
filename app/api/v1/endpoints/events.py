from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams

router = APIRouter()


# Organizer endpoints
@router.get("/organizers/", response_model=List[schemas.Organizer])
async def get_organizers(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve organizers created by the current user.
    """
    organizers = await crud.organizer.get_by_user(db, user_id=current_user.id)
    return organizers


@router.get("/organizers/{organizer_id}", response_model=schemas.Organizer)
async def get_organizer(
        organizer_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get organizer by ID.
    """
    organizer = await crud.organizer.get(db, id=organizer_id)
    if not organizer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer not found",
        )
    return organizer


@router.post("/organizers/", response_model=schemas.Organizer)
async def create_organizer(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        organizer_in: schemas.OrganizerCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new organizer.
    """
    # Set the user_id to the current user
    organizer_data = organizer_in.dict()
    organizer_data["user_id"] = current_user.id

    organizer = await crud.organizer.create(db, obj_in=organizer_data)
    return organizer


@router.put("/organizers/{organizer_id}", response_model=schemas.Organizer)
async def update_organizer(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        organizer_id: int,
        organizer_in: schemas.OrganizerUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an organizer.
    Users can only update their own organizers.
    Superusers can update any organizer.
    """
    organizer = await crud.organizer.get(db, id=organizer_id)
    if not organizer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer not found",
        )

    # Check permissions
    if organizer.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this organizer",
        )

    organizer = await crud.organizer.update(db, db_obj=organizer, obj_in=organizer_in)
    return organizer


# Event Categories
@router.get("/categories/", response_model=List[schemas.EventCategory])
async def get_event_categories(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active event categories.
    """
    categories = await crud.event_category.get_all_active(db)
    return categories


@router.get("/categories/{category_id}", response_model=schemas.EventCategory)
async def get_event_category(
        category_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get event category by ID.
    """
    category = await crud.event_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event category not found",
        )
    return category


@router.post("/categories/", response_model=schemas.EventCategory)
async def create_event_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_in: schemas.EventCategoryCreate,
        current_user: schemas.User = Depends(deps.require_role(["admin", "content_manager"])),
) -> Any:
    """
    Create new event category. Only for admins and content managers.
    """
    category = await crud.event_category.create(db, obj_in=category_in)
    return category


# Events
@router.get("/", response_model=schemas.PaginatedResponse)
async def get_events(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        organizer_id: Optional[int] = None,
        country_id: Optional[int] = None,
        region_id: Optional[int] = None,
        district_id: Optional[int] = None,
) -> Any:
    """
    Search and retrieve events with pagination and filters.
    """
    pagination_params = PaginationParams(page=page, limit=limit)

    result = await crud.event.search_events(
        db,
        search_term=search,
        category_id=category_id,
        organizer_id=organizer_id,
        country_id=country_id,
        region_id=region_id,
        district_id=district_id,
        params=pagination_params
    )

    return result


@router.get("/{event_id}", response_model=schemas.Event)
async def get_event(
        event_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get event by ID.
    """
    event = await crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Increment view count
    await crud.event.increment_view_count(db, event_id=event_id)

    return event


@router.post("/", response_model=schemas.Event)
async def create_event(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_in: schemas.EventCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new event.
    """
    # Check if organizer exists and belongs to current user
    organizer = await crud.organizer.get(db, id=event_in.organizer_id)
    if not organizer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer not found",
        )

    if organizer.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create events for your own organizers",
        )

    # Set the user_id to the current user
    event_data = event_in.dict()
    event_data["user_id"] = current_user.id

    event = await crud.event.create(db, obj_in=event_data)
    return event


@router.put("/{event_id}", response_model=schemas.Event)
async def update_event(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_id: int,
        event_in: schemas.EventUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an event.
    Users can update their own events.
    Superusers can update any event.
    """
    event = await crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Check permissions
    if event.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this event",
        )

    # If updating organizer_id, check if the new organizer belongs to user
    if event_in.organizer_id is not None and event_in.organizer_id != event.organizer_id:
        organizer = await crud.organizer.get(db, id=event_in.organizer_id)
        if not organizer or (organizer.user_id != current_user.id and not current_user.is_superuser):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only assign your own organizers to events",
            )

    event = await crud.event.update(db, db_obj=event, obj_in=event_in)
    return event


@router.delete("/{event_id}", response_model=schemas.Event)
async def delete_event(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an event.
    Users can delete their own events.
    Superusers can delete any event.
    """
    event = await crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Check permissions
    if event.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this event",
        )

    event = await crud.event.remove(db, id=event_id)
    return event


# Event Attendees
@router.get("/{event_id}/attendees/", response_model=List[schemas.EventAttendee])
async def get_event_attendees(
        event_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Get all attendees for an event.
    """
    attendees = await crud.event_attendee.get_by_event(
        db, event_id=event_id, skip=skip, limit=limit
    )
    return attendees


@router.post("/{event_id}/attendees/", response_model=schemas.EventAttendee)
async def attend_event(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Register as an attendee for an event.
    """
    # Check if event exists
    event = await crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Check if user is already attending
    existing_attendee = await crud.event_attendee.get_by_user_and_event(
        db, user_id=current_user.id, event_id=event_id
    )

    if existing_attendee:
        if existing_attendee.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already attending this event",
            )
        else:
            # Re-attend
            existing_attendee.status = True
            db.add(existing_attendee)
            await db.commit()
            await db.refresh(existing_attendee)
            return existing_attendee

    # Check if event is full
    if event.max_attendees is not None:
        current_attendees = await crud.event_attendee.count_attendees(db, event_id=event_id)
        if current_attendees >= event.max_attendees:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is at full capacity",
            )

    # Create attendance
    attendee_data = {
        "user_id": current_user.id,
        "event_id": event_id,
        "status": True
    }

    attendee = await crud.event_attendee.create(db, obj_in=attendee_data)
    return attendee


@router.delete("/{event_id}/attendees/", response_model=schemas.EventAttendee)
async def cancel_attendance(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Cancel attendance to an event.
    """
    # Check if user is attending
    attendee = await crud.event_attendee.get_by_user_and_event(
        db, user_id=current_user.id, event_id=event_id
    )

    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not registered for this event",
        )

    # Soft delete - set status to False
    attendee_update = {"status": False}
    attendee = await crud.event_attendee.update(db, db_obj=attendee, obj_in=attendee_update)
    return attendee


# Event Sponsors
@router.get("/{event_id}/sponsors/", response_model=List[schemas.EventSponsor])
async def get_event_sponsors(
        event_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Get all sponsors for an event.
    """
    sponsors = await crud.event_sponsor.get_by_event(
        db, event_id=event_id, skip=skip, limit=limit
    )
    return sponsors


@router.post("/{event_id}/sponsors/", response_model=schemas.EventSponsor)
async def add_event_sponsor(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_id: int,
        sponsor_in: schemas.EventSponsorCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a sponsor to an event.
    User must own both the event and the organizer.
    """
    # Check if event exists and belongs to user
    event = await crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    if event.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add sponsors to this event",
        )

    # Check if organizer exists and belongs to user
    organizer = await crud.organizer.get(db, id=sponsor_in.organizer_id)
    if not organizer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer not found",
        )

    if organizer.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add your own organizers as sponsors",
        )

    # Create sponsor relationship
    sponsor_data = sponsor_in.dict()
    sponsor_data["event_id"] = event_id

    sponsor = await crud.event_sponsor.create(db, obj_in=sponsor_data)
    return sponsor


@router.delete("/{event_id}/sponsors/{sponsor_id}", response_model=schemas.EventSponsor)
async def remove_event_sponsor(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        event_id: int,
        sponsor_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a sponsor from an event.
    """
    # Check if event exists and belongs to user
    event = await crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    if event.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to remove sponsors from this event",
        )

    # Check if sponsor relationship exists
    sponsor = await crud.event_sponsor.get(db, id=sponsor_id)
    if not sponsor or sponsor.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsor relationship not found",
        )

    sponsor = await crud.event_sponsor.remove(db, id=sponsor_id)
    return sponsor
