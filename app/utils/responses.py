"""
General - Responses.
"""

from pydantic import BaseModel, Field


##################
# Mixin Response #
##################


class EmailMsg(BaseModel):
    """Email message schema"""

    detail: str = Field(example="Email sent")


class Msg(BaseModel):
    """Any detail operation mssage schema"""

    detail: str = Field(example="Opertion successfully")


###################
# Error Responses #
###################


class BadRequest(BaseModel):
    """
    Bad Request model exception.
    """

    detail: str = Field(example="Invalid request data")


class Unauthorized(BaseModel):
    """
    Unauthorized model exception.
    """

    detail: str = Field(example="Invalid Credential")


class Forbidden(BaseModel):
    """
    Forbidden model exception.
    """

    detail: str = Field(example="Action Forbidden")


class NotFound(BaseModel):
    """
    Not Found model exception.
    """

    detail: str = Field(example="Resource not found")


class Conflict(BaseModel):
    """
    Conflict model exception.
    """

    detail: str = Field(example="Entitie name already exists")


class FailPrecondition(BaseModel):
    """
    Fail Precondition model exception.
    """

    detail: str = Field(example="Fail precondition")


class ServerError(BaseModel):
    """
    Server error model exception.
    """

    detail: str = Field(example="Server Error")
