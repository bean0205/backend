from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role
from app.crud.crud_continents import continents
from app.schemas.continents import (
    ContinentCreate,
    ContinentUpdate,
    PaginatedContinentsRequest,
    ContinentOut,
)
from app.utils.role import Role
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/continent", response_model=ContinentOut,
             dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def create_continent(
        continent: ContinentCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Create a new continent.
    """
    # Check exist
    is_continent_exist = await continents.get_by_code(db=db, code=continent.code)
    if is_continent_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Continent with this code already exists"
        )
    # Create the continent
    return await continents.create(db=db, obj_in=continent)


@router.get("/continents", response_model=List[ContinentOut],
            dependencies=[Depends(
                require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_all_continents(
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get all continents.
    """
    continents_list = await continents.get_all(db=db)
    return continents_list


@router.get("/continent/{continent_code}", response_model=ContinentOut, dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_continent(
        continent_code: str,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a continent by its code.
    """
    continent = await continents.get_by_code(db=db, code=continent_code)
    if not continent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Continent not found"
        )
    return continent


@router.put("/continent/{continent_code}", response_model=ContinentOut,
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def update_continent(
        continent_code: str,
        continent: ContinentUpdate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Update a continent by its code.
    """
    # Get the continent
    db_continent = await continents.get_by_code(db=db, code=continent_code)
    if not db_continent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Continent not found"
        )
    # Update the continent
    return await continents.update(db=db, db_obj=db_continent, obj_in=continent)


@router.delete("/continent/{continent_code}",
               dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def delete_continent(
        continent_code: str,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Delete a continent by its code.
    """
    # Get the continent
    db_continent = await continents.get_by_code(db=db, code=continent_code)
    if not db_continent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Continent not found"
        )
    # Delete the continent
    await continents.delete(db=db, id=db_continent.id)
    return {"detail": "Continent deleted successfully"}


@router.get("/paginated", dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_paginated_continents(
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100),
        search_term: Optional[str] = None,
        sort_by: Optional[str] = None,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get paginated continents.
    """
    request = PaginatedContinentsRequest(
        page=page,
        size=size,
        search_term=search_term,
        sort_by=sort_by
    )
    logging.info(f"get_paginated_continents Request: {request}")
    continents_list = await continents.get_continents_by_pagination(
        db=db,
        params=request
    )
    return continents_list
