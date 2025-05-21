from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams

router = APIRouter()


# Article Categories
@router.get("/categories/", response_model=List[schemas.ArticleCategory])
async def get_article_categories(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active article categories.
    """
    categories = await crud.article_category.get_all_active(db)
    return categories


@router.get("/categories/{category_id}", response_model=schemas.ArticleCategory)
async def get_article_category(
        category_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get article category by ID.
    """
    category = await crud.article_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article category not found",
        )
    return category


@router.post("/categories/", response_model=schemas.ArticleCategory)
async def create_article_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_in: schemas.ArticleCategoryCreate,
        current_user: schemas.User = Depends(deps.require_role(["admin", "content_manager"])),
) -> Any:
    """
    Create new article category. Only for admins and content managers.
    """
    category = await crud.article_category.create(db, obj_in=category_in)
    return category


# Article Tags
@router.get("/tags/", response_model=List[schemas.ArticleTag])
async def get_article_tags(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active article tags.
    """
    tags = await crud.article_tag.get_all_active(db)
    return tags


@router.get("/tags/{tag_id}", response_model=schemas.ArticleTag)
async def get_article_tag(
        tag_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get article tag by ID.
    """
    tag = await crud.article_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article tag not found",
        )
    return tag


@router.post("/tags/", response_model=schemas.ArticleTag)
async def create_article_tag(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        tag_in: schemas.ArticleTagCreate,
        current_user: schemas.User = Depends(deps.require_role(["admin", "content_manager"])),
) -> Any:
    """
    Create new article tag. Only for admins and content managers.
    """
    tag = await crud.article_tag.create(db, obj_in=tag_in)
    return tag


# Articles
@router.get("/", response_model=schemas.PaginatedResponse)
async def get_articles(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        search: Optional[str] = None,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag_id: Optional[int] = None,
        country_id: Optional[int] = None,
        region_id: Optional[int] = None,
) -> Any:
    """
    Search and retrieve articles with pagination and filters.
    """
    pagination_params = PaginationParams(page=page, limit=limit)

    result = await crud.article.search_articles(
        db,
        search_term=search,
        author_id=author_id,
        category_id=category_id,
        tag_id=tag_id,
        country_id=country_id,
        region_id=region_id,
        params=pagination_params
    )

    return result


@router.get("/{article_id}", response_model=schemas.ArticleWithRelations)
async def get_article(
        article_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get article by ID.
    """
    article = await crud.article.get(db, id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    # Increment view count
    await crud.article.increment_view_count(db, article_id=article_id)

    # In a real implementation, you would fetch categories and tags here
    # and populate the returned ArticleWithRelations object
    return article


@router.post("/", response_model=schemas.Article)
async def create_article(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_in: schemas.ArticleCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new article.
    """
    # Set the author_id to the current user
    article_in_dict = article_in.dict()
    article_in_dict["author_id"] = current_user.id

    article = await crud.article.create_with_relations(db, obj_in=article_in)
    return article


@router.put("/{article_id}", response_model=schemas.Article)
async def update_article(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        article_in: schemas.ArticleUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an article.
    Authors can update their own articles.
    Admins and content managers can update any article.
    """
    article = await crud.article.get(db, id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    # Check permissions
    is_author = article.author_id == current_user.id
    is_admin = current_user.role in ["admin", "content_manager"]

    if not (is_author or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this article",
        )

    article = await crud.article.update_with_relations(db, db_obj=article, obj_in=article_in)
    return article


@router.delete("/{article_id}", response_model=schemas.Article)
async def delete_article(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an article.
    Authors can delete their own articles.
    Admins and content managers can delete any article.
    """
    article = await crud.article.get(db, id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    # Check permissions
    is_author = article.author_id == current_user.id
    is_admin = current_user.role in ["admin", "content_manager"]

    if not (is_author or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this article",
        )

    article = await crud.article.remove(db, id=article_id)
    return article


# Article Comments
@router.get("/{article_id}/comments/", response_model=List[schemas.ArticleComment])
async def get_article_comments(
        article_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Get all comments for an article.
    """
    comments = await crud.article_comment.get_by_article(
        db, article_id=article_id, skip=skip, limit=limit
    )
    return comments


@router.post("/{article_id}/comments/", response_model=schemas.ArticleComment)
async def create_article_comment(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        comment_in: schemas.ArticleCommentCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new comment for an article.
    """
    # Check if article exists
    article = await crud.article.get(db, id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    # Set user_id and article_id
    comment_data = comment_in.dict()
    comment_data["user_id"] = current_user.id
    comment_data["article_id"] = article_id

    comment = await crud.article_comment.create(db, obj_in=comment_data)
    return comment


@router.put("/{article_id}/comments/{comment_id}", response_model=schemas.ArticleComment)
async def update_article_comment(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        comment_id: int,
        comment_in: schemas.ArticleCommentUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a comment.
    Users can only update their own comments.
    """
    comment = await crud.article_comment.get(db, id=comment_id)
    if not comment or comment.article_id != article_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    # Check permissions
    if comment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own comments",
        )

    comment = await crud.article_comment.update(db, db_obj=comment, obj_in=comment_in)
    return comment


@router.delete("/{article_id}/comments/{comment_id}", response_model=schemas.ArticleComment)
async def delete_article_comment(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        comment_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a comment.
    Users can delete their own comments.
    Article authors can delete any comment on their articles.
    Superusers can delete any comment.
    """
    comment = await crud.article_comment.get(db, id=comment_id)
    if not comment or comment.article_id != article_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    article = await crud.article.get(db, id=article_id)

    # Check permissions
    is_comment_author = comment.user_id == current_user.id
    is_article_author = article.author_id == current_user.id
    is_superuser = current_user.is_superuser

    if not (is_comment_author or is_article_author or is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this comment",
        )

    comment = await crud.article_comment.remove(db, id=comment_id)
    return comment


# Article Reactions
@router.post("/{article_id}/reactions/", response_model=schemas.ArticleReaction)
async def react_to_article(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        reaction_in: schemas.ArticleReactionCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    React to an article (like/bookmark/etc).
    """
    # Check if article exists
    article = await crud.article.get(db, id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    # Set user_id and article_id
    reaction_data = reaction_in.dict()
    reaction_data["user_id"] = current_user.id
    reaction_data["article_id"] = article_id

    # Check if user has already reacted
    existing_reaction = await crud.article_reaction.get_by_user_and_article(
        db, user_id=current_user.id, article_id=article_id
    )

    if existing_reaction:
        # Update existing reaction
        updated_reaction = await crud.article_reaction.update(db, db_obj=existing_reaction, obj_in=reaction_data)
        return updated_reaction

    # Create new reaction
    reaction = await crud.article_reaction.create(db, obj_in=reaction_data)
    return reaction


@router.delete("/{article_id}/reactions/{reaction_id}", response_model=schemas.ArticleReaction)
async def delete_article_reaction(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        article_id: int,
        reaction_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a reaction to an article.
    Users can only delete their own reactions.
    """
    reaction = await crud.article_reaction.get(db, id=reaction_id)
    if not reaction or reaction.article_id != article_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reaction not found",
        )

    if reaction.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reactions",
        )

    reaction = await crud.article_reaction.remove(db, id=reaction_id)
    return reaction
