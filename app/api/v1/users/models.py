"""
User db - Model
"""

from tortoise import fields
from utils.abstrac_model import UnuBaseModel


class UsersModel(UnuBaseModel):
    """
    Users entitie.
    """

    email = fields.CharField(max_length=50, unique=True)
    name = fields.CharField(max_length=40)
    password = fields.CharField(max_length=120)

    class Meta:
        """
        Meta properties.
        """

        table = "users"
