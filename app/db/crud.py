"""
Db - CRUD class.
"""

from typing import List


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

    async def create(self, data: dict) -> any:
        """
        Create a new record.

        Params:
        ------
        - data: dict - The specific instance data
        """
        entitie = await self.model.create(**data)
        return self.schema.from_tortoise_orm(entitie)

    async def read_one(self, query: dict) -> any:
        """
        Get info.
        """
        entitie = await self.model.filter(**query).first()
        return self.schema.from_tortoise_orm(entitie)

    async def read(self, query: any) -> List[any]:
        """
        Get info.
        """
        entities = await self.model.filter(query)
        entities_to_schema = []
        for ent in entities:
            entities_to_schema.append(self.schema.from_tortoise_orm(ent))
        return entities_to_schema

    async def update(self, id: str, data: dict) -> any:
        """
        Update an existing document.
        """
        entitie = await self.model.get(id=id)
        entitie.update_from_dict(data)
        await entitie.save()
        return self.schema.from_tortoise_orm(entitie)

    async def delete(self, id: str) -> any:
        """
        Delete a existing document.
        """
        entite = await self.model.get(id=id)
        entite_to_delete = entite
        await entite.delete()
        return self.schema.from_tortoise_orm(entite_to_delete)
