"""
Db - CRUD class.
"""

from typing import List
from tortoise.contrib.pydantic import pydantic_queryset_creator


###################
# CRUD Operations #
###################
class CRUD:
    """
    Crud operations.

    Params:
    ------
    - model: Tortoise model class.
    - schema: Pydantic schema.
    """

    def __init__(self, model, schema):
        """
        Models injection on initialzation.
        """
        self.model = model
        self.schema = schema
        self.schema_list = pydantic_queryset_creator(model)

    async def create(self, data: dict) -> any:
        """
        Create a new record.

        Params:
        ------
        - data: dict - The specific instance data
        """
        entitie = await self.model.create(**data)
        return await self.schema.from_tortoise_orm(entitie)

    async def read_one(self, query: dict, return_db_model: bool = False) -> any:
        """
        Get info.
        """
        entitie = await self.model.filter(**query).first()
        if not entitie:
            return False
        if return_db_model:
            return entitie
        return await self.schema.from_tortoise_orm(entitie)

    async def read(self, query: any, get_related: bool = False) -> List[any]:
        """
        Get info.
        """
        entities = self.model.filter(**query)
        if get_related:
            return await self.schema_list.from_queryset(entities)
        return await entities

    async def update(self, id: str, data: dict) -> any:
        """
        Update an existing document.
        """
        entitie = await self.model.get(id=id)
        entitie.update_from_dict(data)
        await entitie.save()
        return await self.schema.from_tortoise_orm(entitie)

    async def delete(self, id: str) -> any:
        """
        Delete a existing document.
        """
        entite = await self.model.get(id=id)
        entite_to_delete = entite
        await entite.delete()
        return await self.schema.from_tortoise_orm(entite_to_delete)
