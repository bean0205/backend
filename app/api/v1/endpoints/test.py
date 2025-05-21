from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.error_handling import AppException, ErrorCode, raise_not_found, raise_unauthorized, raise_permission_error

router = APIRouter()


@router.get("/error/app-exception")
async def test_app_exception():
    """Test endpoint that raises an AppException"""
    raise AppException(
        message="Test error message",
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code=ErrorCode.BAD_REQUEST,
        details={"test": "value"}
    )


@router.get("/error/not-found")
async def test_not_found():
    """Test endpoint that raises a not found error"""
    raise_not_found("TestEntity", 123)


@router.get("/error/unauthorized")
async def test_unauthorized():
    """Test endpoint that raises an unauthorized error"""
    raise_unauthorized("Test unauthorized message")


@router.get("/error/forbidden")
async def test_forbidden():
    """Test endpoint that raises a permission error"""
    raise_permission_error()


@router.get("/error/database")
async def test_database_error(db: AsyncSession = Depends(deps.get_db)):
    """Test endpoint that raises a database error"""
    # Force a database error by executing invalid SQL
    await db.execute("SELECT invalid_column FROM non_existent_table")
    return {"result": "This should not be returned"}


@router.get("/health")
async def test_health():
    """Health check endpoint for testing middleware"""
    return {"status": "ok"}
