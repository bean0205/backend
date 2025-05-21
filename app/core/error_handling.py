from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import traceback
from typing import Dict, Any, Optional


class AppException(Exception):
    def __init__(
            self,
            message: str,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code: str = "INTERNAL_ERROR",
            details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


async def app_exception_handler(request: Request, exc: AppException):
    """Handler for custom application exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for request validation errors"""
    errors = []
    for error in exc.errors():
        error_detail = {
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", "")
        }
        errors.append(error_detail)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Dữ liệu không hợp lệ",
            "details": {"errors": errors}
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler for SQLAlchemy errors"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DATABASE_ERROR",
            "message": "Lỗi cơ sở dữ liệu",
            "details": {"error": str(exc)}
        }
    )


async def pydantic_validation_handler(request: Request, exc: ValidationError):
    """Handler for Pydantic validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "SCHEMA_ERROR",
            "message": "Lỗi xác thực dữ liệu mô hình",
            "details": {"errors": exc.errors()}
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Fallback handler for all other exceptions"""
    # In production, we would want to log the full traceback
    trace = traceback.format_exc()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Đã xảy ra lỗi hệ thống",
            "details": {"error": str(exc)}
        }
    )


# Common error codes
class ErrorCode:
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# Helper functions for raising consistent errors
def raise_not_found(entity: str, entity_id: Any = None):
    details = {"entity": entity}
    if entity_id:
        details["id"] = str(entity_id)

    message = f"{entity} không tìm thấy"
    if entity_id:
        message += f" với ID: {entity_id}"

    raise AppException(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code=ErrorCode.NOT_FOUND,
        details=details
    )


def raise_permission_error(message: str = "Không có quyền thực hiện hành động này"):
    raise AppException(
        message=message,
        status_code=status.HTTP_403_FORBIDDEN,
        error_code=ErrorCode.FORBIDDEN
    )


def raise_bad_request(message: str, details: Optional[Dict[str, Any]] = None):
    raise AppException(
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code=ErrorCode.BAD_REQUEST,
        details=details
    )


def raise_unauthorized(message: str = "Chưa xác thực"):
    raise AppException(
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_code=ErrorCode.UNAUTHORIZED
    )
