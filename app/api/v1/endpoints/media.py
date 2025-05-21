from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


# Media Types
@router.get("/types/", response_model=List[schemas.MediaType])
async def get_media_types(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active media types.
    """
    types = await crud.media_type.get_all_active(db)
    return types


@router.get("/types/{type_id}", response_model=schemas.MediaType)
async def get_media_type(
        type_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get media type by ID.
    """
    media_type = await crud.media_type.get(db, id=type_id)
    if not media_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media type not found",
        )
    return media_type


@router.post("/types/", response_model=schemas.MediaType)
async def create_media_type(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        type_in: schemas.MediaTypeCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new media type. Only for superusers.
    """
    media_type = await crud.media_type.create(db, obj_in=type_in)
    return media_type


# Media Categories
@router.get("/categories/", response_model=List[schemas.MediaCategory])
async def get_media_categories(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active media categories.
    """
    categories = await crud.media_category.get_all_active(db)
    return categories


@router.get("/categories/{category_id}", response_model=schemas.MediaCategory)
async def get_media_category(
        category_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get media category by ID.
    """
    category = await crud.media_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media category not found",
        )
    return category


@router.post("/categories/", response_model=schemas.MediaCategory)
async def create_media_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_in: schemas.MediaCategoryCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new media category. Only for superusers.
    """
    category = await crud.media_category.create(db, obj_in=category_in)
    return category


# Media files
@router.get("/", response_model=List[schemas.Media])
async def get_media_files(
        db: AsyncSession = Depends(deps.get_db_session),
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = None,
        type_id: Optional[int] = None,
        category_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve media files with various filters.
    """
    if reference_id and reference_type:
        media = await crud.media.get_by_reference(
            db, reference_id=reference_id, reference_type=reference_type,
            skip=skip, limit=limit
        )
    elif type_id:
        media = await crud.media.get_by_type(db, type_id=type_id, skip=skip, limit=limit)
    elif category_id:
        media = await crud.media.get_by_category(db, category_id=category_id, skip=skip, limit=limit)
    else:
        media = await crud.media.get_multi(db, skip=skip, limit=limit)

    return media


@router.get("/{media_id}", response_model=schemas.Media)
async def get_media(
        media_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get media file by ID.
    """
    media = await crud.media.get(db, id=media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found",
        )
    return media


@router.post("/", response_model=schemas.Media)
async def create_media(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        media_in: schemas.MediaCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new media file.
    Note: In a real implementation, this would handle file uploads and storage.
    """
    # Check media type and category exist
    media_type = await crud.media_type.get(db, id=media_in.type_id)
    if not media_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media type not found",
        )

    media_category = await crud.media_category.get(db, id=media_in.category_id)
    if not media_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media category not found",
        )

    media = await crud.media.create(db, obj_in=media_in)
    return media


@router.put("/{media_id}", response_model=schemas.Media)
async def update_media(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        media_id: int,
        media_in: schemas.MediaUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a media file.
    """
    media = await crud.media.get(db, id=media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found",
        )

    media = await crud.media.update(db, db_obj=media, obj_in=media_in)
    return media


@router.delete("/{media_id}", response_model=schemas.Media)
async def delete_media(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        media_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a media file.
    """
    media = await crud.media.get(db, id=media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found",
        )

    # In a real implementation, you would also delete the actual file from storage
    media = await crud.media.remove(db, id=media_id)
    return media
