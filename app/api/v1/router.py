from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, users, locations, accommodations, foods,
    ratings, media, articles, events, community_posts, test
)

api_router = APIRouter()

# Auth endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# User endpoints
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

# Location endpoints
api_router.include_router(
    locations.router,
    prefix="/locations",
    tags=["locations"]
)

# Accommodation endpoints
api_router.include_router(
    accommodations.router,
    prefix="/accommodations",
    tags=["accommodations"]
)

# Food endpoints
api_router.include_router(
    foods.router,
    prefix="/foods",
    tags=["foods"]
)

# Rating endpoints
api_router.include_router(
    ratings.router,
    prefix="/ratings",
    tags=["ratings"]
)

# Media endpoints
api_router.include_router(
    media.router,
    prefix="/media",
    tags=["media"]
)

# Article endpoints
api_router.include_router(
    articles.router,
    prefix="/articles",
    tags=["articles"]
)

# Event endpoints
api_router.include_router(
    events.router,
    prefix="/events",
    tags=["events"]
)

# Community post endpoints
api_router.include_router(
    community_posts.router,
    prefix="/community",
    tags=["community"]
)

# Test endpoints
api_router.include_router(
    test.router,
    prefix="/test",
    tags=["test"]
)
