"""
Users - Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import UsersModel


User = pydantic_model_creator(UsersModel)
User.Config.schema_extra = {
    "example": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2020-10-05T02:23:56.393Z",
        "updated_at": "2020-10-05T02:23:56.394Z",
        "email": "stan_Lee@marvel.com",
        "name": "Stan Lee",
        "password": "**************",
    }
}


class UserLogin(BaseModel):
    """
    Pydantic schema for login request.
    """

    email: str = Field(..., example="stan_Lee@marvel.com")
    password: str = Field(..., example="marvelous")


class UserIn(BaseModel):
    """
    Pydantic schema for create a user.
    """

    name: str = Field(..., example="Stan Lee")
    email: str = Field(..., example="stan_Lee@marvel.com")
