"""
Custom - Exceptions
"""

from fastapi import HTTPException, status
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


def bad_request_400(detail: str) -> None:
    """
    Raise a 400 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class BadRequest(BaseModel):
    """
    Bad Request model exception.
    """
    detail: str = Field(example="Bad Request")


def unauthorized_401(detail: str) -> None:
    """
    Raise a 401 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class Unauthorized(BaseModel):
    """
    Unauthorized model exception.
    """
    detail: str = Field(example="Invalid Credential")


def forbidden_403(detail: str) -> None:
    """
    Raise a 403 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class Forbidden(BaseModel):
    """
    Forbidden model exception.
    """
    detail: str = Field(example="Action Forbidden")


def not_fount_404(detail: str) -> None:
    """
    Raise a 404 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotFound(BaseModel):
    """
    Not Found model exception.
    """
    detail: str = Field(example="Resource not found")


def conflict_409(detail: str) -> None:
    """
    Raise a 409 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail=detail)


class Conflict(BaseModel):
    """
    Conflict model exception.
    """
    detail: str = Field(example="Entitie name already exists")


def fail_precondition_412(detail: str) -> None:
    """
    Raise a 412 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED, detail=detail)


class FailPrecondition(BaseModel):
    """
    Fail Precondition model exception.
    """
    detail: str = Field(example="Fail precondition")


def server_error_500(detail: str) -> None:
    """
    Raise a 500 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class ServerError(BaseModel):
    """
    Bad Request model exception.
    """
    detail: str = Field(example="Server Error")
