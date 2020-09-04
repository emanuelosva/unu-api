"""
Participants - Controller
"""

# build-in imports
from uuid import uuid4

# module imports
from auth.service import check_authorization_on_event
from .models import ParticipantsModel
from .schemas import PariticipantsDir, PariticipantsDirOut


class ParticipantsControllerModel:
    """
    Agenda controller.
    """

    def __init__(self):
        self.model = ParticipantsModel

    async def create(self, event_id: str) -> PariticipantsDir:
        """
        Create a new partiipants directory for the passed event
        """
        directory = await self.model.find({"event": event_id})
        if directory:
            return 409

        event_in_list = await self.model.find_from_foregyn_key(
            collection="events",
            foregyn_keys=[event_id],
        )
        event = event_in_list[0]

        new_directory: dict = {}
        new_directory.update({"event": event_id})
        new_directory.update({"uuid": str(uuid4())})
        new_directory.update({"eventName": event["name"]})
        new_directory.update({"organization": event["organizationName"]})
        new_directory.update({"emails": []})

        new_directory = PariticipantsDir(**new_directory)
        inserted_id = await self.model.create(new_directory.dict())

        if not inserted_id:
            return None

        return new_directory

    async def register(self, event_id: str, email: str) -> int:
        """
        Register a new participant: Add the email to the emils list
        in the directory.
        """
        query = {"event": event_id}
        directory = await self.model.find(query)

        if not directory:
            return 404

        register = await self.model.add_to_set(query, "emails", email)
        return register

    async def read(self, event_id: str, user: dict) -> PariticipantsDirOut:
        """
        Return the participants directory of some specific event.
        """
        directory = await self.model.find({"event": event_id})

        if not directory:
            return 404
        if not check_authorization_on_event(user, event_id):
            return 403

        count = len(directory["emails"])
        return PariticipantsDirOut(**directory, count=count)

    async def delete(self, event_id) -> int:
        """
        Delete a participants dorectory
        """
        directory = await self.model.find({"event": event_id})

        if not directory:
            return 404

        deleted = await self.model.delete({"event": event_id})
        return deleted


ParticipantsController = ParticipantsControllerModel()
