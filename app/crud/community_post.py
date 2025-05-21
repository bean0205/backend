from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import (
    CommunityPost, CommunityPostCategory, CommunityPostTag,
    CommunityPostComment, CommunityPostReaction,
    CommunityPostCommunityPostTag
)
from app.schemas.community_post import (
    CommunityPostCreate, CommunityPostUpdate,
    CommunityPostCategoryCreate, CommunityPostCategoryUpdate,
    CommunityPostTagCreate, CommunityPostTagUpdate,
    CommunityPostCommentCreate, CommunityPostCommentUpdate,
    CommunityPostReactionCreate, CommunityPostReactionUpdate
)
from app.schemas.base import PaginationParams


class CRUDCommunityPostCategory(
    CRUDBase[CommunityPostCategory, CommunityPostCategoryCreate, CommunityPostCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[CommunityPostCategory]:
        """Get all active community post categories"""
        result = await db.execute(
            select(CommunityPostCategory).filter(CommunityPostCategory.status == True)
        )
        return result.scalars().all()


class CRUDCommunityPostTag(CRUDBase[CommunityPostTag, CommunityPostTagCreate, CommunityPostTagUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[CommunityPostTag]:
        """Get all active community post tags"""
        result = await db.execute(
            select(CommunityPostTag).filter(CommunityPostTag.status == True)
        )
        return result.scalars().all()

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[CommunityPostTag]:
        """Get a tag by name"""
        result = await db.execute(
            select(CommunityPostTag).filter(CommunityPostTag.name.ilike(name))
        )
        return result.scalars().first()


class CRUDCommunityPost(CRUDBase[CommunityPost, CommunityPostCreate, CommunityPostUpdate]):
    async def create_with_relations(
            self, db: AsyncSession, *, obj_in: CommunityPostCreate
    ) -> CommunityPost:
        """Create a community post with tag relations"""
        # Create the post
        db_obj = CommunityPost(
            user_id=obj_in.user_id,
            category_id=obj_in.category_id,
            title=obj_in.title,
            content=obj_in.content,
            thumbnail_url=obj_in.thumbnail_url,
            status=obj_in.status
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # Add tags
        if obj_in.tags:
            for tag_id in obj_in.tags:
                db_tag = CommunityPostCommunityPostTag(
                    community_post_id=db_obj.id,
                    community_post_tag_id=tag_id
                )
                db.add(db_tag)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_with_relations(
            self,
            db: AsyncSession,
            *,
            db_obj: CommunityPost,
            obj_in: Union[CommunityPostUpdate, Dict[str, Any]]
    ) -> CommunityPost:
        """Update a community post with its relations"""
        # Update post
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
            tags = update_data.pop("tags", None)
        else:
            update_data = obj_in.dict(exclude_unset=True)
            tags = update_data.pop("tags", None)

        # Update the basic fields
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db.add(db_obj)

        # Update tags if provided
        if tags is not None:
            # Remove all existing tags
            existing_tags = (await db.execute(
                select(CommunityPostCommunityPostTag)
                .filter(CommunityPostCommunityPostTag.community_post_id == db_obj.id)
            )).scalars().all()

            for tag in existing_tags:
                await db.delete(tag)

            # Add new tags
            for tag_id in tags:
                db_tag = CommunityPostCommunityPostTag(
                    community_post_id=db_obj.id,
                    community_post_tag_id=tag_id
                )
                db.add(db_tag)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_user(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[CommunityPost]:
        """Get posts by user ID"""
        result = await db.execute(
            select(CommunityPost)
            .filter(CommunityPost.user_id == user_id)
            .filter(CommunityPost.status == True)
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
    ) -> List[CommunityPost]:
        """Get posts by category ID"""
        result = await db.execute(
            select(CommunityPost)
            .filter(CommunityPost.category_id == category_id)
            .filter(CommunityPost.status == True)
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
    ) -> List[CommunityPost]:
        """Get posts by tag ID"""
        post_ids = await db.execute(
            select(CommunityPostCommunityPostTag.community_post_id)
            .filter(CommunityPostCommunityPostTag.community_post_tag_id == tag_id)
        )
        post_ids = post_ids.scalars().all()

        if not post_ids:
            return []

        result = await db.execute(
            select(CommunityPost)
            .filter(CommunityPost.id.in_(post_ids))
            .filter(CommunityPost.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_posts(
            self,
            db: AsyncSession,
            *,
            search_term: Optional[str] = None,
            user_id: Optional[int] = None,
            category_id: Optional[int] = None,
            tag_id: Optional[int] = None,
            params: PaginationParams
    ) -> Dict[str, Any]:
        """Search community posts with filters"""
        # Base query
        query = select(CommunityPost).filter(CommunityPost.status == True)

        # Apply filters
        if search_term:
            query = query.filter(CommunityPost.title.ilike(f"%{search_term}%"))

        if user_id:
            query = query.filter(CommunityPost.user_id == user_id)

        if category_id:
            query = query.filter(CommunityPost.category_id == category_id)

        # Tag filter
        if tag_id:
            tag_post_ids = await db.execute(
                select(CommunityPostCommunityPostTag.community_post_id)
                .filter(CommunityPostCommunityPostTag.community_post_tag_id == tag_id)
            )
            tag_post_ids = tag_post_ids.scalars().all()
            if tag_post_ids:
                query = query.filter(CommunityPost.id.in_(tag_post_ids))
            else:
                # No posts with this tag
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

    async def increment_view_count(self, db: AsyncSession, *, post_id: int) -> Optional[CommunityPost]:
        """Increment the view count of a community post"""
        post = await self.get(db, id=post_id)
        if post:
            post.view_count = post.view_count + 1
            db.add(post)
            await db.commit()
            await db.refresh(post)
        return post


class CRUDCommunityPostComment(CRUDBase[CommunityPostComment, CommunityPostCommentCreate, CommunityPostCommentUpdate]):
    async def get_by_post(
            self,
            db: AsyncSession,
            *,
            post_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[CommunityPostComment]:
        """Get comments by post ID (top level comments only)"""
        result = await db.execute(
            select(CommunityPostComment)
            .filter(CommunityPostComment.post_id == post_id)
            .filter(CommunityPostComment.parent_id == None)
            .filter(CommunityPostComment.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_parent(
            self,
            db: AsyncSession,
            *,
            parent_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[CommunityPostComment]:
        """Get replies to a comment"""
        result = await db.execute(
            select(CommunityPostComment)
            .filter(CommunityPostComment.parent_id == parent_id)
            .filter(CommunityPostComment.status == True)
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
    ) -> List[CommunityPostComment]:
        """Get comments by user ID"""
        result = await db.execute(
            select(CommunityPostComment)
            .filter(CommunityPostComment.user_id == user_id)
            .filter(CommunityPostComment.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDCommunityPostReaction(
    CRUDBase[CommunityPostReaction, CommunityPostReactionCreate, CommunityPostReactionUpdate]):
    async def get_by_post(
            self,
            db: AsyncSession,
            *,
            post_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[CommunityPostReaction]:
        """Get reactions by post ID"""
        result = await db.execute(
            select(CommunityPostReaction)
            .filter(CommunityPostReaction.post_id == post_id)
            .filter(CommunityPostReaction.comment_id == None)
            .filter(CommunityPostReaction.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_comment(
            self,
            db: AsyncSession,
            *,
            comment_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[CommunityPostReaction]:
        """Get reactions by comment ID"""
        result = await db.execute(
            select(CommunityPostReaction)
            .filter(CommunityPostReaction.comment_id == comment_id)
            .filter(CommunityPostReaction.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user_post_and_type(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            post_id: int,
            reaction_type: str = None
    ) -> Optional[CommunityPostReaction]:
        """Get a user's reaction to a post (optionally filtered by type)"""
        query = select(CommunityPostReaction) \
            .filter(CommunityPostReaction.user_id == user_id) \
            .filter(CommunityPostReaction.post_id == post_id) \
            .filter(CommunityPostReaction.comment_id == None)

        if reaction_type:
            query = query.filter(CommunityPostReaction.reaction_type == reaction_type)

        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_user_comment_and_type(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            comment_id: int,
            reaction_type: str = None
    ) -> Optional[CommunityPostReaction]:
        """Get a user's reaction to a comment (optionally filtered by type)"""
        query = select(CommunityPostReaction) \
            .filter(CommunityPostReaction.user_id == user_id) \
            .filter(CommunityPostReaction.comment_id == comment_id)

        if reaction_type:
            query = query.filter(CommunityPostReaction.reaction_type == reaction_type)

        result = await db.execute(query)
        return result.scalars().first()

    async def count_reactions_by_type(
            self,
            db: AsyncSession,
            *,
            post_id: int = None,
            comment_id: int = None,
            reaction_type: str = None
    ) -> Dict[str, int]:
        """Count reactions for a post or comment, grouped by type"""
        if not post_id and not comment_id:
            raise ValueError("Either post_id or comment_id must be provided")

        query = select(CommunityPostReaction.reaction_type, func.count().label('count')) \
            .filter(CommunityPostReaction.status == True)

        if post_id:
            query = query.filter(CommunityPostReaction.post_id == post_id)
            if comment_id is None:
                query = query.filter(CommunityPostReaction.comment_id == None)

        if comment_id:
            query = query.filter(CommunityPostReaction.comment_id == comment_id)

        if reaction_type:
            query = query.filter(CommunityPostReaction.reaction_type == reaction_type)

        query = query.group_by(CommunityPostReaction.reaction_type)
        result = await db.execute(query)

        reactions_count = {}
        for row in result:
            reactions_count[row.reaction_type] = row.count

        return reactions_count


community_post_category = CRUDCommunityPostCategory(CommunityPostCategory)
community_post_tag = CRUDCommunityPostTag(CommunityPostTag)
community_post = CRUDCommunityPost(CommunityPost)
community_post_comment = CRUDCommunityPostComment(CommunityPostComment)
community_post_reaction = CRUDCommunityPostReaction(CommunityPostReaction)
