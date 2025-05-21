# Import các router từ các endpoint modules

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.locations import router as locations_router
from app.api.v1.endpoints.accommodations import router as accommodations_router
from app.api.v1.endpoints.foods import router as foods_router
from app.api.v1.endpoints.ratings import router as ratings_router
from app.api.v1.endpoints.media import router as media_router
from app.api.v1.endpoints.articles import router as articles_router
from app.api.v1.endpoints.events import router as events_router
from app.api.v1.endpoints.community_posts import router as community_posts_router
from app.api.v1.endpoints.test import router as test_router

# Export tất cả các router để có thể import từ module này
__all__ = [
    "auth", "users", "locations", "accommodations", "foods",
    "ratings", "media", "articles", "events", "community_posts", "test"
]

# Gán router cho các biến để dễ sử dụng
auth = auth_router
users = users_router
locations = locations_router
accommodations = accommodations_router
foods = foods_router
ratings = ratings_router
media = media_router
articles = articles_router
events = events_router
community_posts = community_posts_router
test = test_router
