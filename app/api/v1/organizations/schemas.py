"""
Organizations - Schemas
"""

from pydantic import BaseModel, Field
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from config import settings
from .models import OrganizationsModel

# Init models to get all related properties
Tortoise.init_models(settings.DB_MODELS, "models")


Organization = pydantic_model_creator(OrganizationsModel)


class OrganizationIn(BaseModel):
    """
    Pydantic schema for create a Organization.
    """

    name: str = Field(..., example="Marvel")
    url: str = Field(..., example="https://marvel.com")
    logo: str = Field(...)
