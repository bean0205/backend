from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Rating)
async def create_rating(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        rating_in: schemas.RatingCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new rating or update existing.
    Users can only create ratings for themselves.
    """
    # Override user_id with the current user's ID
    rating_data = rating_in.dict()
    rating_data["user_id"] = current_user.id

    # Check if the user has already rated this item
    existing_rating = await crud.rating.get_user_rating(
        db,
        user_id=current_user.id,
        reference_id=rating_in.reference_id,
        reference_type=rating_in.reference_type
    )

    if existing_rating:
        # Update existing rating
        updated_rating = await crud.rating.update(db, db_obj=existing_rating, obj_in=rating_data)
        return updated_rating

    # Create new rating
    rating = await crud.rating.create(db, obj_in=rating_data)
    return rating


@router.get("/", response_model=List[schemas.Rating])
async def get_ratings(
        db: AsyncSession = Depends(deps.get_db_session),
        reference_id: int = Query(..., description="ID of the item being rated"),
        reference_type: str = Query(..., description="Type of item being rated (location, accommodation, food)"),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Get ratings for a specific item.
    """
    ratings = await crud.rating.get_by_reference(
        db,
        reference_id=reference_id,
        reference_type=reference_type,
        skip=skip,
        limit=limit
    )
    return ratings


@router.get("/average", response_model=float)
async def get_average_rating(
        db: AsyncSession = Depends(deps.get_db_session),
        reference_id: int = Query(..., description="ID of the item being rated"),
        reference_type: str = Query(..., description="Type of item being rated (location, accommodation, food)"),
) -> Any:
    """
    Get the average rating for a specific item.
    """
    average = await crud.rating.get_average_rating(
        db,
        reference_id=reference_id,
        reference_type=reference_type
    )
    return average


@router.get("/mine", response_model=Optional[schemas.Rating])
async def get_user_rating(
        db: AsyncSession = Depends(deps.get_db_session),
        reference_id: int = Query(..., description="ID of the item being rated"),
        reference_type: str = Query(..., description="Type of item being rated (location, accommodation, food)"),
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the current user's rating for a specific item.
    """
    rating = await crud.rating.get_user_rating(
        db,
        user_id=current_user.id,
        reference_id=reference_id,
        reference_type=reference_type
    )
    return rating


@router.put("/{rating_id}", response_model=schemas.Rating)
async def update_rating(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        rating_id: int,
        rating_in: schemas.RatingUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a rating.
    Users can only update their own ratings.
    """
    rating = await crud.rating.get(db, id=rating_id)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found",
        )

    if rating.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own ratings",
        )

    rating = await crud.rating.update(db, db_obj=rating, obj_in=rating_in)
    return rating


@router.delete("/{rating_id}", response_model=schemas.Rating)
async def delete_rating(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        rating_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a rating.
    Users can only delete their own ratings.
    Superusers can delete any rating.
    """
    rating = await crud.rating.get(db, id=rating_id)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found",
        )

    if rating.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own ratings",
        )

    rating = await crud.rating.remove(db, id=rating_id)
    return rating
