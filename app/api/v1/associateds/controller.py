"""
Associateds - Controller
"""

# build-in imports
from uuid import uuid4

# module imports
from auth.service import check_authorization_on_event
from utils.general import store_file
from .models import AssociatedModel
from .schemas import AssociatedIn, AssociatedOut


class AssociatedControllerModel:
    """
    Associated controller.
    """

    def __init__(self):
        self.model = AssociatedModel

    async def create(self, associated: AssociatedIn) -> AssociatedOut:
        """
        Create a new associated.
        """
        associated_data: dict = associated.dict()
        associated_data.update({"uuid": str(uuid4())})
        associated_data.update({"event": associated.event})

        logo = store_file(file_b64=associated_data["logo"])
        associated_data.update({"logo": logo})

        inserted_id = await self.model.create(associated_data)
        if not inserted_id:
            return False

        return AssociatedOut(**associated_data)

    async def read(self, associated_id: str, event_id: str = None) -> AssociatedOut:
        """
        Retrieve a existing associated or all associateds belongs
        to one event.
        """
        if event_id is not None:
            associateds_list = await self.model.find(
                query={"event": event_id}, only_one=False
            )
            return associateds_list

        query = {"uuid": associated_id}
        associated = await self.model.find(query)
        if not associated:
            return False

        return AssociatedOut(**associated)

    async def update(
        self, associated_id: str, associated_data: AssociatedIn, user: dict
    ) -> int:
        """
        Update a existing event.
        """
        associated = await self.read(associated_id)
        if not associated:
            return 404

        authorized = check_authorization_on_event(user, associated.event)
        if not authorized:
            return 403

        new_data = associated_data.dict()
        logo = store_file(file_b64=new_data["logo"])
        new_data.update({"logo": logo})

        query = {"uuid": associated_id}
        updated = await self.model.update(query, new_data)

        return updated

    async def delete(self, associated_id: str, user: dict) -> int:
        """
        Delete a existing event.
        """
        associated = await self.read(associated_id)
        if not associated:
            return 404, None

        if not check_authorization_on_event(user, associated.event):
            return 403, None

        deleted_count = await self.model.delete({"uuid": associated_id})
        return deleted_count, associated


AssociatedController = AssociatedControllerModel()
