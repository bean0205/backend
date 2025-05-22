# Import và export các CRUD classes để sử dụng từ bên ngoài

# Base CRUD
from app.crud.base import CRUDBase

# User CRUD
from app.crud.user import CRUDUser, user

# Permission and Role CRUD
from app.crud.permission import CRUDPermission, permission
from app.crud.role import CRUDRole, role

# Location CRUD
from app.crud.location import (
    CRUDContinent, continent,
    CRUDCountry, country,
    CRUDRegion, region,
    CRUDDistrict, district,
    CRUDWard, ward,
    CRUDLocationCategory, location_category,
    CRUDLocation, location
)

# Accommodation CRUD
from app.crud.accommodation import (
    CRUDAccommodationCategory, accommodation_category,
    CRUDAccommodation, accommodation,
    CRUDAccommodationRoom, accommodation_room
)

# Food CRUD
from app.crud.food import (
    CRUDFoodCategory, food_category,
    CRUDFood, food,
    CRUDRating, rating
)

# Media CRUD
from app.crud.media import (
    CRUDMediaType, media_type,
    CRUDMediaCategory, media_category,
    CRUDMedia, media
)

# Article CRUD
from app.crud.article import (
    CRUDArticleCategory, article_category,
    CRUDArticleTag, article_tag,
    CRUDArticle, article,
    CRUDArticleComment, article_comment,
    CRUDArticleReaction, article_reaction
)

# Event CRUD
from app.crud.event import (
    CRUDOrganizer, organizer,
    CRUDEventCategory, event_category,
    CRUDEvent, event,
    CRUDEventAttendee, event_attendee,
    CRUDEventSponsor, event_sponsor
)

# Community Post CRUD
from app.crud.community_post import (
    CRUDCommunityPostCategory, community_post_category,
    CRUDCommunityPostTag, community_post_tag,
    CRUDCommunityPost, community_post,
    CRUDCommunityPostComment, community_post_comment,
    CRUDCommunityPostReaction, community_post_reaction
)
