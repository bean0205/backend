from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams

router = APIRouter()


@router.get("/", response_model=List[schemas.community_post.CommunityPost])
async def get_community_posts(
        pagination: PaginationParams = Depends(),
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve community posts with pagination.
    """
    posts = await crud.community_post.get_multi(
        db, skip=pagination.skip, limit=pagination.limit
    )
    return posts


@router.post("/", response_model=schemas.community_post.CommunityPost)
async def create_community_post(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        current_user=Depends(deps.get_current_user),
        post_in: schemas.community_post.CommunityPostCreate,
) -> Any:
    """
    Create new community post.
    """
    post = await crud.community_post.create_with_owner(
        db=db, obj_in=post_in, owner_id=current_user.id
    )
    return post


@router.get("/{post_id}", response_model=schemas.community_post.CommunityPost)
async def get_community_post(
        post_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get specific community post by ID.
    """
    post = await crud.community_post.get(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community post not found"
        )
    return post
