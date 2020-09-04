"""
Agenda - Controller
"""

# build-in imports
from uuid import uuid4
from typing import List

# module imports
from auth.service import check_authorization_on_event
from .models import AgendaModel
from .schemas import Day, DayIn, DayOut, ConferenceIn, ConferenceOut


class AgendaControllerModel:
    """
    Agenda controller.
    """

    def __init__(self):
        self.model = AgendaModel

    async def create_day(
            self, day: DayIn, user: dict) -> DayOut:
        """
        Create a new day in agenda.
        """
        if not check_authorization_on_event(user, day.event):
            return 403

        query = {"event": day.event, "date": day.date}
        existing_day = await self.model.find(query)
        if existing_day:
            return 409

        day_data: dict = day.dict()
        day_data.update({"uuid": str(uuid4())})

        new_day = Day(**day_data)

        inserted_id = await self.model.create(new_day.dict())
        if not inserted_id:
            return False

        return DayOut(**new_day.dict())

    async def create_conference(
            self, day_id: str,
            conference: ConferenceIn,
            user: dict) -> ConferenceOut:
        """
        Add a new conference to one day.
        """
        query = {"uuid": day_id}
        day = await self.model.find(query)

        if not day:
            return 404
        if not check_authorization_on_event(user, day["event"]):
            return 403

        conference_data: dict = conference.dict()
        conference_data.update({"uuid": str(uuid4())})
        conference_data.update({"speakerInfo": {}})

        inserted_id = await self.model.add_to_set(
            query,
            "conferences",
            conference_data,
        )

        if not inserted_id:
            return False
        return ConferenceOut(**conference_data)

    async def read_day(self, day_id: str) -> DayOut:
        """
        Retrieve a existing day
        """
        query = {"uuid": day_id}
        day = await self.model.find(query)
        if not day:
            return False

        for i in range(len(day["conferences"])):
            speaker_info = await self.model.find_from_foregyn_key(
                "speakers",
                [day["conferences"][i]["speaker"]]
            )
            day["conferences"][i]["speakerInfo"] = speaker_info[0]

        return DayOut(**day)

    async def read_all_days(self, event_id: str) -> List[DayOut]:
        """
        Retrieve a list of days
        """
        days = await self.model.find({"event": event_id}, only_one=False)

        if len(days) == 0:
            return []

        populated_days = []
        for day in days:
            all_day_info = await self.read_day(day["uuid"])
            populated_days.append(all_day_info)

        return populated_days

    async def get_conference(self, conference_id: str) -> ConferenceOut:
        """
        Return a conference.
        """
        day = await self.model.find({"conferences.uuid": conference_id})
        if not day:
            return False

        _conferences = day["conferences"]
        _conference = [
            conf for conf in _conferences if conf["uuid"] == conference_id
        ]
        conference = _conference[0]

        speaker_info = await self.model.find_from_foregyn_key(
            "speakers",
            [conference["speaker"]]
        )
        conference["speakerInfo"] = speaker_info[0]
        return conference

    async def update_day(
            self, day_id: str,
            new_day_data: DayIn, user: dict) -> int:
        """
        Update a existing day
        """
        query = {"uuid": day_id}
        day = await self.model.find(query)

        if not day:
            return 404
        if day["event"] != new_day_data.event:
            return 412
        if not check_authorization_on_event(user, day["event"]):
            return 403

        ocuped_date = await self.model.find({"date": new_day_data.date})
        if ocuped_date["uuid"] != day_id:
            return 409

        new_data = new_day_data.dict()
        updated = await self.model.update(query, new_data)

        return updated

    async def update_conference(
            self, conference_id: str,
            conference_data: ConferenceIn,
            user: dict) -> int:
        """
        Update a existing conference.
        """
        day = await self.model.find({"conferences.uuid": conference_id})

        if not day:
            return 404
        if not check_authorization_on_event(user, day["event"]):
            return 403

        conference: dict = conference_data.dict()
        conference.update({"uuid": conference_id})
        conference.update({"speakerInfo": {}})

        query = {"uuid": day["uuid"], "conferences.uuid": conference_id}
        data = {"conferences.$": conference}
        updated = await self.model.update(query, data)

        return updated

    async def delete_conferene(self, conference_id: str, user: dict) -> int:
        """
        Remove a conference from a day
        """
        day = await self.model.find({"conferences.uuid": conference_id})

        if not day:
            return 404
        if not check_authorization_on_event(user, day["event"]):
            return 403

        query = {"uuid": day["uuid"]}
        array_name = "conferences"
        condition = {"uuid": conference_id}
        deleted = await self.model.pull_array(query, array_name, condition)

        return deleted

    async def delete_day(self, day_id: str, user: dict) -> int:
        """
        Delete a day
        """
        query = {"uuid": day_id}
        day = await self.model.find(query)

        if not day:
            return 404, None
        if not check_authorization_on_event(user, day["event"]):
            return 403, None

        deleted = await self.model.delete(query)

        day["conferences"] = []
        day = Day(**day)
        return deleted, day


AgendaController = AgendaControllerModel()
