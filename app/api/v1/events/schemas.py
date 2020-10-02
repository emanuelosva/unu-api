"""
Events - Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class EventsIn(BaseModel):
    """
    Body for create events.
    """

    name: str
    template: str
    url: str
    startDate: str
    utc: str
    organizationUrl: str = Field(
        ..., description="The organization owner unuUrl field - Foregyn key"
    )


class EventUpdate(BaseModel):
    """
    Body for update a event.
    """

    name: str
    template: str
    url: str
    startDate: str
    utc: str
    titleHeader: str = ""
    shortDescription: str = ""
    description: str = ""
    imageHeader: str = ""
    imageEvent: str = ""
    titleHeader: str = ""


class Event(EventUpdate, EventsIn):
    """
    Event schema.
    """

    uuid: str
    organizationName: str
    publicationStatus: Optional[bool] = False
    associateds: Optional[List[str]] = []
    speakers: Optional[List[str]] = []
    agenda: Optional[List[str]] = []
    collaborators: Optional[List[str]] = []
    user: str = Field(..., description="The user owner uuid - Foregyn Key")


class EventOut(Event):
    """
    Event response schema.
    """

    publicationStatus: bool
    associateds: List[dict]
    speakers: List[dict]
    agenda: List[dict]
    collaborators: List[dict]
