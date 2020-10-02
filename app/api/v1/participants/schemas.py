"""
Speakers - Schemas
"""

from typing import List
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class PariticipantsDir(BaseModel):
    """
    Body for create a new participants directory.
    """

    event: str = Field(..., description="The event uuid - Foreigyn Key")
    uuid: str
    eventName: str
    organization: str
    emails: List[str]


class PariticipantsDirOut(PariticipantsDir):
    """
    Body for create a new participants directory.
    """

    count: int


class RegisterResponse(BaseModel):
    """
    Response on register a new participantt
    """

    detail: str = Field(example="Resgister Successfull")
    event: str
