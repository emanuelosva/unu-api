"""
General - Responses.
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class Created(BaseModel):
    """
    Created response.
    """
    detail: str = Field(example="Created entitie")
    uuid: str = Field(example="d7fea47a-4fe3-4067-b7e8-53dbb724a634")


class Updated(BaseModel):
    """
    Updated response.
    """
    detail: str = Field(example="Modified success")
    modifiedCount: int = Field(example=1)


class Deleted(BaseModel):
    """
    Deleted response.
    """
    detail: str = Field(example="Deleted count: int")
