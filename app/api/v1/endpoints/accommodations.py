from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams

router = APIRouter()


# Accommodation Category endpoints
@router.get("/categories/", response_model=List[schemas.AccommodationCategory])
async def get_accommodation_categories(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active accommodation categories.
    """
    categories = await crud.accommodation_category.get_all_active(db)
    return categories


@router.get("/categories/{category_id}", response_model=schemas.AccommodationCategory)
async def get_accommodation_category(
        category_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get accommodation category by ID.
    """
    category = await crud.accommodation_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation category not found",
        )
    return category


@router.post("/categories/", response_model=schemas.AccommodationCategory)
async def create_accommodation_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_in: schemas.AccommodationCategoryCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new accommodation category. Only for superusers.
    """
    category = await crud.accommodation_category.create(db, obj_in=category_in)
    return category


@router.put("/categories/{category_id}", response_model=schemas.AccommodationCategory)
async def update_accommodation_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_id: int,
        category_in: schemas.AccommodationCategoryUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an accommodation category. Only for superusers.
    """
    category = await crud.accommodation_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation category not found",
        )
    category = await crud.accommodation_category.update(db, db_obj=category, obj_in=category_in)
    return category


# Accommodation endpoints
@router.get("/", response_model=schemas.PaginatedResponse)
async def get_accommodations(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        country_id: Optional[int] = None,
        region_id: Optional[int] = None,
        district_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
) -> Any:
    """
    Search and retrieve accommodations with pagination and filters.
    """
    pagination_params = PaginationParams(page=page, limit=limit)

    result = await crud.accommodation.search_accommodations(
        db,
        search_term=search,
        category_id=category_id,
        country_id=country_id,
        region_id=region_id,
        district_id=district_id,
        min_price=min_price,
        max_price=max_price,
        params=pagination_params
    )

    return result


@router.get("/{accommodation_id}", response_model=schemas.Accommodation)
async def get_accommodation(
        accommodation_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get accommodation by ID.
    """
    accommodation = await crud.accommodation.get(db, id=accommodation_id)
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation not found",
        )
    return accommodation


@router.post("/", response_model=schemas.Accommodation)
async def create_accommodation(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        accommodation_in: schemas.AccommodationCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new accommodation.
    """
    # Set the user_id to the current user
    accommodation_in_dict = accommodation_in.dict()
    accommodation_in_dict["user_id"] = current_user.id
    accommodation = await crud.accommodation.create(db, obj_in=accommodation_in_dict)
    return accommodation


@router.put("/{accommodation_id}", response_model=schemas.Accommodation)
async def update_accommodation(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        accommodation_id: int,
        accommodation_in: schemas.AccommodationUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an accommodation.
    Owners can update their own accommodations.
    Superusers can update any accommodation.
    """
    accommodation = await crud.accommodation.get(db, id=accommodation_id)
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation not found",
        )

    # Check permissions
    if accommodation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this accommodation",
        )

    accommodation = await crud.accommodation.update(db, db_obj=accommodation, obj_in=accommodation_in)
    return accommodation


@router.delete("/{accommodation_id}", response_model=schemas.Accommodation)
async def delete_accommodation(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        accommodation_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an accommodation.
    Owners can delete their own accommodations.
    Superusers can delete any accommodation.
    """
    accommodation = await crud.accommodation.get(db, id=accommodation_id)
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation not found",
        )

    # Check permissions
    if accommodation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this accommodation",
        )

    accommodation = await crud.accommodation.remove(db, id=accommodation_id)
    return accommodation


# Room endpoints
@router.get("/{accommodation_id}/rooms/", response_model=List[schemas.AccommodationRoom])
async def get_accommodation_rooms(
        accommodation_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Get all rooms for a specific accommodation.
    """
    rooms = await crud.accommodation_room.get_by_accommodation(
        db, accommodation_id=accommodation_id, skip=skip, limit=limit
    )
    return rooms


@router.get("/{accommodation_id}/rooms/{room_id}", response_model=schemas.AccommodationRoom)
async def get_accommodation_room(
        accommodation_id: int,
        room_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get a specific room by ID.
    """
    room = await crud.accommodation_room.get(db, id=room_id)
    if not room or room.accommodation_id != accommodation_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return room


@router.post("/{accommodation_id}/rooms/", response_model=schemas.AccommodationRoom)
async def create_accommodation_room(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        accommodation_id: int,
        room_in: schemas.AccommodationRoomCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new room for an accommodation.
    Accommodation owners can create rooms for their own accommodations.
    Superusers can create rooms for any accommodation.
    """
    # Check if accommodation exists and user has permission
    accommodation = await crud.accommodation.get(db, id=accommodation_id)
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation not found",
        )

    if accommodation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add rooms to this accommodation",
        )

    # Set the accommodation_id
    room_in_dict = room_in.dict()
    room_in_dict["accommodation_id"] = accommodation_id
    room = await crud.accommodation_room.create(db, obj_in=room_in_dict)
    return room


@router.put("/{accommodation_id}/rooms/{room_id}", response_model=schemas.AccommodationRoom)
async def update_accommodation_room(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        accommodation_id: int,
        room_id: int,
        room_in: schemas.AccommodationRoomUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a room.
    Accommodation owners can update rooms in their own accommodations.
    Superusers can update any room.
    """
    # Check if accommodation exists and user has permission
    accommodation = await crud.accommodation.get(db, id=accommodation_id)
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation not found",
        )

    if accommodation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update rooms in this accommodation",
        )

    # Check if room exists and belongs to the accommodation
    room = await crud.accommodation_room.get(db, id=room_id)
    if not room or room.accommodation_id != accommodation_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    room = await crud.accommodation_room.update(db, db_obj=room, obj_in=room_in)
    return room


@router.delete("/{accommodation_id}/rooms/{room_id}", response_model=schemas.AccommodationRoom)
async def delete_accommodation_room(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        accommodation_id: int,
        room_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a room.
    Accommodation owners can delete rooms in their own accommodations.
    Superusers can delete any room.
    """
    # Check if accommodation exists and user has permission
    accommodation = await crud.accommodation.get(db, id=accommodation_id)
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accommodation not found",
        )

    if accommodation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete rooms in this accommodation",
        )

    # Check if room exists and belongs to the accommodation
    room = await crud.accommodation_room.get(db, id=room_id)
    if not room or room.accommodation_id != accommodation_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    room = await crud.accommodation_room.remove(db, id=room_id)
    return room
