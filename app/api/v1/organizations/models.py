"""
Organizations db - Model
"""

from tortoise import fields, Tortoise
from utils.abstrac_model import UnuBaseModel


class OrganizationsModel(UnuBaseModel):
    """
    Organization entitie.
    """

    name = fields.CharField(max_length=50, unique=True)
    unu_url = fields.CharField(max_length=120, unique=True)
    url = fields.CharField(max_length=256)
    logo = fields.CharField(max_length=1024)

    owner = fields.ForeignKeyField(
        "models.UsersModel", related_name="organizations", on_delete=fields.CASCADE
    )
