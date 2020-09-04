"""
Users - Schemas
"""

# external imports
from typing import List, Optional
from pydantic import BaseModel  # pylint: disable-msg=E0611

# module imports
from api.v1.organizations.schemas import OrganizationOut


class UserLogin(BaseModel):
    """
    Body for login.
    """
    email: str
    password: str


class UserIn(UserLogin):
    """
    Body for create a user
    """
    name: str


class UserCollaborator(UserIn):
    """
    Body for add a collaborator
    """
    name: Optional[str]
    password: Optional[str]


class User(UserIn):
    """
    Json Response for user
    """
    uuid: str
    organizations: Optional[List[str]] = []
    myEvents: Optional[List[str]] = []
    myCollaborations: Optional[List[str]] = []


class UserOut(BaseModel):
    """
    Json Response for user
    """
    uuid: str
    email: str
    name: str
    organizations: List[OrganizationOut]
    myEvents: List[dict]
    myCollaborations: List[dict]


class UserOnAuth(BaseModel):
    """
    Json Response for user on auth routes
    """
    accessToken: str
    tokenType: str
    user: UserOut
