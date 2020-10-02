"""
Events - Controller
"""

# build-in imports
from uuid import uuid4
from typing import List

# module imports
from auth.service import check_authorization_on_event
from utils.general import store_file
from .models import EventsModel
from .schemas import EventsIn, EventOut, Event, EventUpdate


class EventControllerModel:
    """
    Events controller.
    """

    def __init__(self):
        self.model = EventsModel

    async def create(self, event: EventsIn, user: str) -> EventOut:
        """
        Create a new event.
        """
        new_event_data: dict = event.dict()
        new_event_data.update({"uuid": str(uuid4())})
        new_event_data.update({"user": user})

        organization_name = event.organizationUrl.replace("-", " ").capitalize()
        new_event_data.update({"organizationName": organization_name})

        new_event = Event(**new_event_data)

        inserted_id = await self.model.create(new_event.dict())
        if not inserted_id:
            return False

        return EventOut(**new_event.dict())

    async def read(self, event_id: str) -> EventOut:
        """
        Retrieve a existing event
        """
        query = {"uuid": event_id}
        event = await self.model.find(query)
        if not event:
            return False

        event["speakers"] = await self.model.find_from_foregyn_key(
            "speakers", event["speakers"]
        )
        event["agenda"] = await self.model.find_from_foregyn_key(
            "agenda", event["agenda"]
        )
        event["collaborators"] = await self.model.find_from_foregyn_key(
            "users", event["collaborators"]
        )
        event["associateds"] = await self.model.find_from_foregyn_key(
            "associateds", event["associateds"]
        )

        return EventOut(**event)

    async def get_published(self) -> List[Event]:
        """
        Retrieve a list of published events.
        """
        events = await self.model.find({"publicationStatus": True}, only_one=False)
        return events

    async def get_from_url(self, organization_url: str, url: str) -> Event:
        """
        Return the event that matches the url
        """
        query = {
            "organizationUrl": organization_url,
            "url": url,
            "publicationStatus": True,
        }
        event = await self.model.find(query)

        if not event:
            return False

        event["speakers"] = await self.model.find_from_foregyn_key(
            "speakers", event["speakers"]
        )
        event["agenda"] = await self.model.find_from_foregyn_key(
            "agenda", event["agenda"]
        )
        event["collaborators"] = await self.model.find_from_foregyn_key(
            "users", event["collaborators"]
        )

        return event

    async def update(self, event_id: str, new_event_data: EventUpdate) -> int:
        """
        Update a existing event.
        """
        event = await self.read(event_id)
        if not event:
            return 404, None

        new_data = new_event_data.dict()

        image_header = store_file(file_b64=new_data["imageHeader"])
        image_event = store_file(file_b64=new_data["imageEvent"])
        new_data.update({"imageHeader": image_header})
        new_data.update({"imageEvent": image_event})

        query = {"uuid": event_id}
        updated = await self.model.update(query, new_data)

        return updated, event.uuid

    async def update_to_field(
        self, event_id: str, field: str, uuid: str, action: str
    ) -> EventOut:
        """
        Update a existing event.
        """
        event = await self.read(event_id)
        if not event:
            return False

        query = {"uuid": event_id}
        if action == "add":
            updated = await self.model.add_to_set(query, field, uuid)
        if action == "remove":
            updated = await self.model.pull_array(query, field, uuid)

        return updated

    async def change_status(self, event_id: str, actual_status: bool) -> int:
        """
        Change the current publication status of a event
        """
        new_status = not actual_status
        query = {"uuid": event_id}
        data = {"publicationStatus": new_status}
        updated = await self.model.update(query, data)
        return updated

    async def delete(self, event_id: str, user: dict) -> int:
        """
        Delete a existing event.
        """
        event = await self.read(event_id)
        if not event:
            return 404, None

        authorized = check_authorization_on_event(user, event.uuid)
        if not authorized:
            return 403, None

        deleted_count = await self.model.delete({"uuid": event_id})
        return deleted_count, event


EventController = EventControllerModel()
