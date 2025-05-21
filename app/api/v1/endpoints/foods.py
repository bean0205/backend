from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams

router = APIRouter()


# Food Category endpoints
@router.get("/categories/", response_model=List[schemas.FoodCategory])
async def get_food_categories(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active food categories.
    """
    categories = await crud.food_category.get_all_active(db)
    return categories


@router.get("/categories/{category_id}", response_model=schemas.FoodCategory)
async def get_food_category(
        category_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get food category by ID.
    """
    category = await crud.food_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food category not found",
        )
    return category


@router.post("/categories/", response_model=schemas.FoodCategory)
async def create_food_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_in: schemas.FoodCategoryCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new food category. Only for superusers.
    """
    category = await crud.food_category.create(db, obj_in=category_in)
    return category


@router.put("/categories/{category_id}", response_model=schemas.FoodCategory)
async def update_food_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_id: int,
        category_in: schemas.FoodCategoryUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a food category. Only for superusers.
    """
    category = await crud.food_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food category not found",
        )
    category = await crud.food_category.update(db, db_obj=category, obj_in=category_in)
    return category


# Food endpoints
@router.get("/", response_model=schemas.PaginatedResponse)
async def get_foods(
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
    Search and retrieve foods with pagination and filters.
    """
    pagination_params = PaginationParams(page=page, limit=limit)

    result = await crud.food.search_foods(
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


@router.get("/{food_id}", response_model=schemas.Food)
async def get_food(
        food_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get food item by ID.
    """
    food = await crud.food.get(db, id=food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )
    return food


@router.post("/", response_model=schemas.Food)
async def create_food(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        food_in: schemas.FoodCreate,
        current_user: schemas.User = Depends(deps.require_role(["admin", "content_manager"])),
) -> Any:
    """
    Create new food item. Only for admins and content managers.
    """
    food = await crud.food.create(db, obj_in=food_in)
    return food


@router.put("/{food_id}", response_model=schemas.Food)
async def update_food(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        food_id: int,
        food_in: schemas.FoodUpdate,
        current_user: schemas.User = Depends(deps.require_role(["admin", "content_manager"])),
) -> Any:
    """
    Update a food item. Only for admins and content managers.
    """
    food = await crud.food.get(db, id=food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )
    food = await crud.food.update(db, db_obj=food, obj_in=food_in)
    return food


@router.delete("/{food_id}", response_model=schemas.Food)
async def delete_food(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        food_id: int,
        current_user: schemas.User = Depends(deps.require_role(["admin", "content_manager"])),
) -> Any:
    """
    Delete a food item. Only for admins and content managers.
    """
    food = await crud.food.get(db, id=food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )
    food = await crud.food.remove(db, id=food_id)
    return food
