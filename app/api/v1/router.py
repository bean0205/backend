from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth_router, users_router, locations_router, accommodations_router, foods_router,
    ratings_router, media_router, articles_router, events_router, community_posts_router, test_router
)

api_router = APIRouter()

# Auth endpoints
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["authentication"]
)

# User endpoints
api_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)

# Locations endpoints
api_router.include_router(
    locations_router,
    prefix="/locations",
    tags=["locations"]
)

# Accommodations endpoints
api_router.include_router(
    accommodations_router,
    prefix="/accommodations",
    tags=["accommodations"]
)

# Foods endpoints
api_router.include_router(
    foods_router,
    prefix="/foods",
    tags=["foods"]
)

# Ratings endpoints
api_router.include_router(
    ratings_router,
    prefix="/ratings",
    tags=["ratings"]
)

# Media endpoints
api_router.include_router(
    media_router,
    prefix="/media",
    tags=["media"]
)

# Articles endpoints
api_router.include_router(
    articles_router,
    prefix="/articles",
    tags=["articles"]
)

# Events endpoints
api_router.include_router(
    events_router,
    prefix="/events",
    tags=["events"]
)

# Community posts endpoints
api_router.include_router(
    community_posts_router,
    prefix="/community-posts",
    tags=["community-posts"]
)

# Test endpoints
api_router.include_router(
    test_router,
    prefix="/test",
    tags=["test"]
)
