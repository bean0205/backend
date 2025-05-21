from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import (
    Article, ArticleCategory, ArticleTag,
    ArticleComment, ArticleReaction,
    ArticleArticleCategory, ArticleArticleTag
)
from app.schemas.article import (
    ArticleCreate, ArticleUpdate,
    ArticleCategoryCreate, ArticleCategoryUpdate,
    ArticleTagCreate, ArticleTagUpdate,
    ArticleCommentCreate, ArticleCommentUpdate,
    ArticleReactionCreate, ArticleReactionUpdate
)
from app.schemas.base import PaginationParams


class CRUDArticleCategory(CRUDBase[ArticleCategory, ArticleCategoryCreate, ArticleCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[ArticleCategory]:
        """Get all active article categories"""
        result = await db.execute(
            select(ArticleCategory).filter(ArticleCategory.status == True)
        )
        return result.scalars().all()


class CRUDArticleTag(CRUDBase[ArticleTag, ArticleTagCreate, ArticleTagUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[ArticleTag]:
        """Get all active article tags"""
        result = await db.execute(
            select(ArticleTag).filter(ArticleTag.status == True)
        )
        return result.scalars().all()

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[ArticleTag]:
        """Get a tag by name"""
        result = await db.execute(
            select(ArticleTag).filter(ArticleTag.name.ilike(name))
        )
        return result.scalars().first()

    async def get_by_name_code(self, db: AsyncSession, *, name_code: str) -> Optional[ArticleTag]:
        """Get a tag by name code"""
        result = await db.execute(
            select(ArticleTag).filter(ArticleTag.name_code == name_code)
        )
        return result.scalars().first()


class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    async def create_with_relations(
            self, db: AsyncSession, *, obj_in: ArticleCreate
    ) -> Article:
        """Create an article with category and tag relations"""
        # Create the article
        db_obj = Article(
            author_id=obj_in.author_id,
            title=obj_in.title,
            title_code=obj_in.title_code,
            description=obj_in.description,
            description_code=obj_in.description_code,
            content=obj_in.content,
            country_id=obj_in.country_id,
            region_id=obj_in.region_id,
            district_id=obj_in.district_id,
            ward_id=obj_in.ward_id,
            thumbnail_url=obj_in.thumbnail_url,
            status=obj_in.status,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # Add categories
        if obj_in.categories:
            for category_id in obj_in.categories:
                db_category = ArticleArticleCategory(
                    article_id=db_obj.id,
                    article_categories_id=category_id
                )
                db.add(db_category)

        # Add tags
        if obj_in.tags:
            for tag_id in obj_in.tags:
                db_tag = ArticleArticleTag(
                    article_id=db_obj.id,
                    article_tags_id=tag_id
                )
                db.add(db_tag)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_with_relations(
            self,
            db: AsyncSession,
            *,
            db_obj: Article,
            obj_in: Union[ArticleUpdate, Dict[str, Any]]
    ) -> Article:
        """Update an article with its relations"""
        # Update article
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
            categories = update_data.pop("categories", None)
            tags = update_data.pop("tags", None)
        else:
            update_data = obj_in.dict(exclude_unset=True)
            categories = update_data.pop("categories", None)
            tags = update_data.pop("tags", None)

        # Update the basic fields
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db.add(db_obj)

        # Update categories if provided
        if categories is not None:
            # Remove all existing categories
            await db.execute(
                select(ArticleArticleCategory)
                .filter(ArticleArticleCategory.article_id == db_obj.id)
            )
            existing_categories = (await db.execute(
                select(ArticleArticleCategory)
                .filter(ArticleArticleCategory.article_id == db_obj.id)
            )).scalars().all()

            for category in existing_categories:
                await db.delete(category)

            # Add new categories
            for category_id in categories:
                db_category = ArticleArticleCategory(
                    article_id=db_obj.id,
                    article_categories_id=category_id
                )
                db.add(db_category)

        # Update tags if provided
        if tags is not None:
            # Remove all existing tags
            existing_tags = (await db.execute(
                select(ArticleArticleTag)
                .filter(ArticleArticleTag.article_id == db_obj.id)
            )).scalars().all()

            for tag in existing_tags:
                await db.delete(tag)

            # Add new tags
            for tag_id in tags:
                db_tag = ArticleArticleTag(
                    article_id=db_obj.id,
                    article_tags_id=tag_id
                )
                db.add(db_tag)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_author(
            self,
            db: AsyncSession,
            *,
            author_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Article]:
        """Get articles by author ID"""
        result = await db.execute(
            select(Article)
            .filter(Article.author_id == author_id)
            .filter(Article.status == True)
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
    ) -> List[Article]:
        """Get articles by category ID"""
        article_ids = await db.execute(
            select(ArticleArticleCategory.article_id)
            .filter(ArticleArticleCategory.article_categories_id == category_id)
        )
        article_ids = article_ids.scalars().all()

        if not article_ids:
            return []

        result = await db.execute(
            select(Article)
            .filter(Article.id.in_(article_ids))
            .filter(Article.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_tag(
            self,
            db: AsyncSession,
            *,
            tag_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Article]:
        """Get articles by tag ID"""
        article_ids = await db.execute(
            select(ArticleArticleTag.article_id)
            .filter(ArticleArticleTag.article_tags_id == tag_id)
        )
        article_ids = article_ids.scalars().all()

        if not article_ids:
            return []

        result = await db.execute(
            select(Article)
            .filter(Article.id.in_(article_ids))
            .filter(Article.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_articles(
            self,
            db: AsyncSession,
            *,
            search_term: Optional[str] = None,
            author_id: Optional[int] = None,
            category_id: Optional[int] = None,
            tag_id: Optional[int] = None,
            country_id: Optional[int] = None,
            region_id: Optional[int] = None,
            params: PaginationParams
    ) -> Dict[str, Any]:
        """Search articles with filters"""
        # Base query
        query = select(Article).filter(Article.status == True)

        # Apply filters
        if search_term:
            query = query.filter(Article.title.ilike(f"%{search_term}%"))

        if author_id:
            query = query.filter(Article.author_id == author_id)

        if country_id:
            query = query.filter(Article.country_id == country_id)

        if region_id:
            query = query.filter(Article.region_id == region_id)

        # Category filter
        if category_id:
            category_article_ids = await db.execute(
                select(ArticleArticleCategory.article_id)
                .filter(ArticleArticleCategory.article_categories_id == category_id)
            )
            category_article_ids = category_article_ids.scalars().all()
            if category_article_ids:
                query = query.filter(Article.id.in_(category_article_ids))
            else:
                # No articles in this category
                return {
                    "items": [],
                    "total": 0,
                    "page": params.page,
                    "limit": params.limit,
                    "pages": 0
                }

        # Tag filter
        if tag_id:
            tag_article_ids = await db.execute(
                select(ArticleArticleTag.article_id)
                .filter(ArticleArticleTag.article_tags_id == tag_id)
            )
            tag_article_ids = tag_article_ids.scalars().all()
            if tag_article_ids:
                query = query.filter(Article.id.in_(tag_article_ids))
            else:
                # No articles with this tag
                return {
                    "items": [],
                    "total": 0,
                    "page": params.page,
                    "limit": params.limit,
                    "pages": 0
                }

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

    async def increment_view_count(self, db: AsyncSession, *, article_id: int) -> Optional[Article]:
        """Increment the view count of an article"""
        article = await self.get(db, id=article_id)
        if article:
            article.view_count = article.view_count + 1
            db.add(article)
            await db.commit()
            await db.refresh(article)
        return article


class CRUDArticleComment(CRUDBase[ArticleComment, ArticleCommentCreate, ArticleCommentUpdate]):
    async def get_by_article(
            self,
            db: AsyncSession,
            *,
            article_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[ArticleComment]:
        """Get comments by article ID"""
        result = await db.execute(
            select(ArticleComment)
            .filter(ArticleComment.article_id == article_id)
            .filter(ArticleComment.status == True)
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
    ) -> List[ArticleComment]:
        """Get comments by user ID"""
        result = await db.execute(
            select(ArticleComment)
            .filter(ArticleComment.user_id == user_id)
            .filter(ArticleComment.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDArticleReaction(CRUDBase[ArticleReaction, ArticleReactionCreate, ArticleReactionUpdate]):
    async def get_by_article(
            self,
            db: AsyncSession,
            *,
            article_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[ArticleReaction]:
        """Get reactions by article ID"""
        result = await db.execute(
            select(ArticleReaction)
            .filter(ArticleReaction.article_id == article_id)
            .filter(ArticleReaction.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user_and_article(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            article_id: int
    ) -> Optional[ArticleReaction]:
        """Get a user's reaction to an article"""
        result = await db.execute(
            select(ArticleReaction)
            .filter(ArticleReaction.user_id == user_id)
            .filter(ArticleReaction.article_id == article_id)
        )
        return result.scalars().first()

    async def count_reactions(self, db: AsyncSession, *, article_id: int) -> int:
        """Count reactions for an article"""
        result = await db.execute(
            select(func.count())
            .select_from(ArticleReaction)
            .filter(ArticleReaction.article_id == article_id)
            .filter(ArticleReaction.status == True)
        )
        return result.scalar() or 0


article_category = CRUDArticleCategory(ArticleCategory)
article_tag = CRUDArticleTag(ArticleTag)
article = CRUDArticle(Article)
article_comment = CRUDArticleComment(ArticleComment)
article_reaction = CRUDArticleReaction(ArticleReaction)
