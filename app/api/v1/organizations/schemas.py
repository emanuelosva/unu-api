"""
Organizations - Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class OrganizationIn(BaseModel):
    """
    Body for create organization.
    """
    name: str
    oficialUrl: Optional[str] = ""
    logo: Optional[str] = ""


class Organization(OrganizationIn):
    """
    Organization schema.
    """
    uuid: str
    unuUrl: str
    events: Optional[List[str]] = []
    user: str = Field(..., description="The uuid of user owner - Foregyn key")


class OrganizationOut(Organization):
    """
    Organization schema.
    """
    unuUrl: str
    events: List[str]
