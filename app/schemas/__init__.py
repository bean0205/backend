# Import và export các schema classes để dễ dàng sử dụng từ bên ngoài

# Base schemas
from app.schemas.base import (
    BaseSchema,
    TimestampMixin,
    DateMixin,
    PaginationParams,
    PaginatedResponse
)

# User và authentication schemas
from app.schemas.user import (
    User, UserCreate, UserUpdate, UserInDB,
    Token, TokenPayload, UserRegisterResponse,
    PasswordReset, PasswordResetConfirm, PasswordChange,
    PasswordResetToken, PasswordResetTokenCreate
)

# Permission schemas
from app.schemas.permission import (
    Permission, PermissionCreate, PermissionUpdate,
    PermissionBase
)

# Role schemas
from app.schemas.role import (
    Role, RoleCreate, RoleUpdate,
    RoleBase
)

# Location schemas
from app.schemas.location import (
    Continent, ContinentCreate, ContinentUpdate,
    Country, CountryCreate, CountryUpdate,
    Region, RegionCreate, RegionUpdate,
    District, DistrictCreate, DistrictUpdate,
    Ward, WardCreate, WardUpdate,
    LocationCategory, LocationCategoryCreate, LocationCategoryUpdate,
    Location, LocationCreate, LocationUpdate
)

# Accommodation schemas
from app.schemas.accommodation import (
    AccommodationCategory, AccommodationCategoryCreate, AccommodationCategoryUpdate,
    Accommodation, AccommodationCreate, AccommodationUpdate,
    AccommodationRoom, AccommodationRoomCreate, AccommodationRoomUpdate
)

# Food schemas
from app.schemas.food import (
    FoodCategory, FoodCategoryCreate, FoodCategoryUpdate,
    Food, FoodCreate, FoodUpdate,
    Rating, RatingCreate, RatingUpdate
)

# Media schemas
from app.schemas.media import (
    MediaType, MediaTypeCreate, MediaTypeUpdate,
    MediaCategory, MediaCategoryCreate, MediaCategoryUpdate,
    Media, MediaCreate, MediaUpdate
)

# Article schemas
from app.schemas.article import (
    ArticleCategory, ArticleCategoryCreate, ArticleCategoryUpdate,
    ArticleTag, ArticleTagCreate, ArticleTagUpdate,
    Article, ArticleCreate, ArticleUpdate, ArticleWithRelations,
    ArticleComment, ArticleCommentCreate, ArticleCommentUpdate,
    ArticleReaction, ArticleReactionCreate, ArticleReactionUpdate
)

# Event schemas
from app.schemas.event import (
    Organizer, OrganizerCreate, OrganizerUpdate,
    EventCategory, EventCategoryCreate, EventCategoryUpdate,
    Event, EventCreate, EventUpdate,
    EventAttendee, EventAttendeeCreate, EventAttendeeUpdate,
    EventSponsor, EventSponsorCreate, EventSponsorUpdate
)

# Community post schemas
from app.schemas.community_post import (
    CommunityPostCategory, CommunityPostCategoryCreate, CommunityPostCategoryUpdate,
    CommunityPostTag, CommunityPostTagCreate, CommunityPostTagUpdate,
    CommunityPost, CommunityPostCreate, CommunityPostUpdate, CommunityPostWithRelations,
    CommunityPostComment, CommunityPostCommentCreate, CommunityPostCommentUpdate,
    CommunityPostReaction, CommunityPostReactionCreate, CommunityPostReactionUpdate
)
