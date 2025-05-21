from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin


class ArticleCategoryBase(BaseModel):
    name: str
    status: bool = True


class ArticleCategoryCreate(ArticleCategoryBase):
    pass


class ArticleCategoryUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class ArticleCategory(ArticleCategoryBase, TimestampMixin, BaseSchema):
    id: int


class ArticleTagBase(BaseModel):
    name: str
    name_code: Optional[str] = None
    status: bool = True


class ArticleTagCreate(ArticleTagBase):
    pass


class ArticleTagUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    status: Optional[bool] = None


class ArticleTag(ArticleTagBase, TimestampMixin, BaseSchema):
    id: int


class ArticleBase(BaseModel):
    author_id: int
    title: str
    title_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    content: str
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    status: bool = True


class ArticleCreate(ArticleBase):
    categories: Optional[List[int]] = None
    tags: Optional[List[int]] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    title_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    content: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    view_count: Optional[int] = None
    status: Optional[bool] = None
    categories: Optional[List[int]] = None
    tags: Optional[List[int]] = None


class Article(ArticleBase, TimestampMixin, BaseSchema):
    id: int
    view_count: int = 0


class ArticleWithRelations(Article):
    categories: List[ArticleCategory] = []
    tags: List[ArticleTag] = []


class ArticleArticleCategoryBase(BaseModel):
    article_id: int
    article_categories_id: int


class ArticleArticleTagBase(BaseModel):
    article_id: int
    article_tags_id: int


class ArticleCommentBase(BaseModel):
    user_id: int
    article_id: int
    content: str
    status: bool = True


class ArticleCommentCreate(ArticleCommentBase):
    pass


class ArticleCommentUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[bool] = None


class ArticleComment(ArticleCommentBase, TimestampMixin, BaseSchema):
    id: int


class ArticleReactionBase(BaseModel):
    user_id: int
    article_id: int
    status: bool = True


class ArticleReactionCreate(ArticleReactionBase):
    pass


class ArticleReactionUpdate(BaseModel):
    status: Optional[bool] = None


class ArticleReaction(ArticleReactionBase, TimestampMixin, BaseSchema):
    id: int
