"""
Organizations - Controller
"""

# build-in imports
from uuid import uuid4
from typing import List

# module imports
from auth.service import check_authorization_on_event
from utils.general import store_file
from .models import SpeakerModel
from .schemas import SpeakerIn, SpeakerOut


class SpeakerControllerModel:
    """
    Speaker controller.
    """

    def __init__(self):
        self.model = SpeakerModel

    async def create(self, speaker: SpeakerIn, user: dict) -> SpeakerOut:
        """
        Create a new speaker.
        """
        authorized = check_authorization_on_event(user, speaker.event)
        if not authorized:
            return 403

        query = {"event": speaker.event, "name": speaker.name}
        existing_name = await self.model.find(query)
        if existing_name:
            return 409

        speaker_data: dict = speaker.dict()
        speaker_data.update({"uuid": str(uuid4())})

        photo: str = store_file(file_b64=speaker_data["photo"])
        speaker_data.update({"photo": photo})

        new_speaker = SpeakerOut(**speaker_data)

        inserted_id = await self.model.create(new_speaker.dict())
        if not inserted_id:
            return False

        return new_speaker

    async def read(self, speaker_id: str) -> SpeakerOut:
        """
        Retrieve a existing speaker
        """
        query = {"uuid": speaker_id}
        speaker = await self.model.find(query)
        if not speaker:
            return False

        return SpeakerOut(**speaker)

    async def read_many(self, event_id: str) -> List[SpeakerOut]:
        """
        Retrieve a list of speakers thath belongs to an event.
        """
        query = {"event": event_id}
        speakers = await self.model.find(query, only_one=False)
        if not speakers:
            return []
        return speakers

    async def update(
        self, speaker_id: str, new_speaker_data: SpeakerIn, user: dict
    ) -> int:
        """
        Update a existing speaker
        """
        speaker = await self.read(speaker_id)
        if not speaker:
            return 404

        authorized = check_authorization_on_event(user, speaker.event)
        if not authorized:
            return 403

        new_data = new_speaker_data.dict()

        photo = store_file(file_b64=new_data["photo"])
        new_data.update({"photo": photo})

        query = {"uuid": speaker_id}
        updated = await self.model.update(query, new_data)

        return updated

    async def delete(self, speaker_id: str, user: dict) -> int:
        """
        Delete a existing speaker
        """
        speaker = await self.model.find({"uuid": speaker_id})
        if not speaker:
            return 404, None

        authorized = check_authorization_on_event(user, speaker["event"])
        if not authorized:
            return 403

        deleted_count = await self.model.delete({"uuid": speaker_id})
        return deleted_count, speaker["event"]


SpeakerController = SpeakerControllerModel()
