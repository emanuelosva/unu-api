"""
Associated - Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class AssociatedIn(BaseModel):
    """
    Body for create associateds.
    """

    name: str
    web: str
    logo: Optional[str] = ""
    event: str = Field(description="The event uuid - Foregyn key")


class AssociatedOut(AssociatedIn):
    """
    Associated out response schema.
    """

    uuid: str
