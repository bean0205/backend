from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin


class CommunityPostCategoryBase(BaseModel):
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    status: bool = True


class CommunityPostCategoryCreate(CommunityPostCategoryBase):
    pass


class CommunityPostCategoryUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    status: Optional[bool] = None


class CommunityPostCategory(CommunityPostCategoryBase, TimestampMixin, BaseSchema):
    id: int


class CommunityPostTagBase(BaseModel):
    name: str
    status: bool = True


class CommunityPostTagCreate(CommunityPostTagBase):
    pass


class CommunityPostTagUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class CommunityPostTag(CommunityPostTagBase, TimestampMixin, BaseSchema):
    id: int


class CommunityPostBase(BaseModel):
    user_id: int
    category_id: int
    title: str
    content: str
    thumbnail_url: Optional[str] = None
    status: bool = True


class CommunityPostCreate(CommunityPostBase):
    tags: Optional[List[int]] = None


class CommunityPostUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    thumbnail_url: Optional[str] = None
    view_count: Optional[int] = None
    status: Optional[bool] = None
    tags: Optional[List[int]] = None


class CommunityPost(CommunityPostBase, TimestampMixin, BaseSchema):
    id: int
    view_count: int = 0


class CommunityPostWithRelations(CommunityPost):
    tags: List[CommunityPostTag] = []


class CommunityPostCommentBase(BaseModel):
    user_id: int
    post_id: int
    content: str
    parent_id: Optional[int] = None
    status: bool = True


class CommunityPostCommentCreate(CommunityPostCommentBase):
    pass


class CommunityPostCommentUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[bool] = None


class CommunityPostComment(CommunityPostCommentBase, TimestampMixin, BaseSchema):
    id: int


class CommunityPostReactionBase(BaseModel):
    user_id: int
    post_id: int
    reaction_type: str
    comment_id: Optional[int] = None
    status: bool = True


class CommunityPostReactionCreate(CommunityPostReactionBase):
    pass


class CommunityPostReactionUpdate(BaseModel):
    reaction_type: Optional[str] = None
    status: Optional[bool] = None


class CommunityPostReaction(CommunityPostReactionBase, TimestampMixin, BaseSchema):
    id: int


class CommunityPostCommunityPostTagBase(BaseModel):
    community_post_id: int
    community_post_tag_id: int


class CommunityPostCommunityPostTagCreate(CommunityPostCommunityPostTagBase):
    pass


class CommunityPostCommunityPostTag(CommunityPostCommunityPostTagBase, BaseSchema):
    id: int
