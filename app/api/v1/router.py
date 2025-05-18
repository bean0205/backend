from fastapi import APIRouter

from app.api.v1.endpoints import countries, auth, users, regions, districts, wards, locations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(regions.router, prefix="/regions", tags=["regions"])
api_router.include_router(districts.router, prefix="/districts", tags=["districts"])
api_router.include_router(wards.router, prefix="/wards", tags=["wards"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
