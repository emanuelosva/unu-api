"""
Common custom abstrac model.
"""

from tortoise import models, fields


class UnuBaseModel(models.Model):
    """
    Custom abstract model.
    """

    # All models have a id of uuid class.
    id = fields.UUIDField(pk=True)

    # Time metadata
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """
        No generate a table in DB.
        """

        abstract = True
