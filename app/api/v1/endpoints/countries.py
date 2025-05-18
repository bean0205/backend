from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role
from app.crud.crud_countries import countries
from app.schemas.countries import (
    CountryCreate,
    CountryUpdate,
    PaginatedCountriesRequest,
    CountryOut,
)
from app.utils.role import Role
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/country", response_model=CountryOut,
             dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def create_country(
        country: CountryCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Create a new country.
    """
    # check exist
    is_country_exist = await countries.get_by_code(db=db, code=country.code);
    if is_country_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Country with this code already exists"
        )
    # Create the country
    return await countries.create(db=db, obj_in=country)


@router.get("/countries", response_model=List[CountryOut],
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def get_all_countries(
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get all countries.
    """
    countries_list = await countries.get_all(db=db)
    return countries_list


@router.get("/by-continent/{continent_id}", response_model=List[CountryOut],
            dependencies=[Depends(
                require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_countries_by_continent(
        continent_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get all countries for a specific continent.
    """
    return await countries.get_by_continent_id(db=db, continent_id=continent_id)


@router.get("/country/{country_code}", response_model=CountryOut, dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_country(
        country_code: str,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a country by its code.
    """
    country = await countries.get_by_code(db=db, code=country_code)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    return country


@router.put("/country/{country_code}", response_model=CountryOut,
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def update_country(
        country_code: str,
        country: CountryUpdate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Update a country by its code.
    """
    # Get the country
    db_country = await countries.get_by_code(db=db, code=country_code)
    if not db_country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    # Update the country
    return await countries.update(db=db, db_obj=db_country, obj_in=country)


@router.delete("/country/{country_code}",
               dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def delete_country(
        country_code: str,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Delete a country by its code.
    """
    # Get the country
    db_country = await countries.get_by_code(db=db, code=country_code)
    if not db_country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    # Delete the country
    await countries.delete(db=db, id=db_country.id)
    return {"detail": "Country deleted successfully"}


@router.get("/paginated", dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_paginated_countries(
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100),
        search_term: Optional[str] = None,
        continent_id: Optional[int] = None,
        sort_by: Optional[str] = None,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get paginated countries.
    """
    request = PaginatedCountriesRequest(
        page=page,
        size=size,
        search_term=search_term,
        continent_id=continent_id,
        sort_by=sort_by
    )
    logging.info(f"get_paginated_countries Request: {request}")
    countries_list = await countries.get_countries_by_pagination(
        db=db,
        params=request
    )
    return countries_list
