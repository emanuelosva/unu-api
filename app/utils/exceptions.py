"""
Custom - Exceptions
"""

from fastapi import HTTPException, status


def bad_request_400(detail: str) -> None:
    """
    Raise a 400 HTTP exception.
    """
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def unauthorized_401(detail: str) -> None:
    """
    Raise a 401 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )


def forbidden_403(detail: str) -> None:
    """
    Raise a 403 HTTP exception.
    """
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def not_fount_404(detail: str) -> None:
    """
    Raise a 404 HTTP exception.
    """
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def conflict_409(detail: str) -> None:
    """
    Raise a 409 HTTP exception.
    """
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def fail_precondition_412(detail: str) -> None:
    """
    Raise a 412 HTTP exception.
    """
    raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=detail)


def server_error_500() -> None:
    """
    Raise a 500 HTTP exception.
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error"
    )
