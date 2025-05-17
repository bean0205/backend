from fastapi import APIRouter

from app.api.v1.endpoints import countries, auth, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
