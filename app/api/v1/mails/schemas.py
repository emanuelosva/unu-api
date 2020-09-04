"""
Mails - Schemas
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class MailResponse(BaseModel):
    """
    Response mail schema
    """
    detail: str = Field(example="Email sended")
    target: str = Field(example="Event/Email: str")
