"""
Speakers - Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class SpeakerIn(BaseModel):
    """
    Body for create amd update a speaker.
    """

    name: str
    biography: str
    twitter_url: str
    photo: Optional[str] = Field("", description="Image base64 encoded")
    event: str = Field(description="The event uuid the speakers belongs - Foregyn Key")


class SpeakerOut(SpeakerIn):
    """
    Speaker schema and response body
    """

    uuid: str
