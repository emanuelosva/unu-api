"""
Agenga - Schema
"""

from typing import List, Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class ConferenceIn(BaseModel):
    """
    Body for create a conference.
    """

    name: str
    startHour: str
    endHour: str
    description: str
    speaker: str = Field(description="The speaker uuid - Foregyn Key")


class ConferenceOut(ConferenceIn):
    """
    Conference schema and response body.
    """

    uuid: str
    speakerInfo: dict


class DayIn(BaseModel):
    """
    Body for create a day in agenda.
    """

    event: str = Field(description="The event uuid that day belogns - Foregyn Key")
    date: str
    title: str


class Day(DayIn):
    """
    The Day schema.
    """

    uuid: str
    conferences: Optional[List[dict]] = []


class DayOut(Day):
    """
    Day response shcema.
    """

    conferences: List[ConferenceOut]
