"""
Users - Schemas
"""

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise

from config import settings
from .models import UsersModel

Tortoise.init_models(settings.DB_MODELS, "models")

User = pydantic_model_creator(UsersModel)


class UserLogin(BaseModel):
    """
    Pydantic schema for login request.
    """

    email: str = Field(..., example="stan_lee@marvel.com")
    password: str = Field(..., example="marvelous")


class UserCreate(UserLogin):
    """
    Pydantic schema for create a user.
    """

    name: str = Field(..., exmaple="Stan Lee")


class UserUpdate(BaseModel):
    """
    Pydantic schema for create a user.
    """

    name: str = Field(..., example="Stan Lee")
    email: str = Field(..., example="stan_lee@marvel.com")
