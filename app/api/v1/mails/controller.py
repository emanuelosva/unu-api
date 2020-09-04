"""
Mail - Controller
"""

# external imports
from fastapi import UploadFile

# module imports
from auth.service import check_authorization_on_event
from mails.service import send_special_email, send_close_event_email
from .models import MailsModel


class MailControllerModel:
    """
    Mail controller.
    """

    def __init__(self):
        self.model = MailsModel
        self._send_special = send_special_email
        self._send_alert = send_close_event_email

    async def send_special(
            self,
            event_id: str,
            subject: str,
            message: str,
            file: UploadFile,
            user: dict) -> int:
        """
        Send a special email to all participants
        registere in the passed event
        """
        # Check if directory exist
        directory = await self.model.find({"event": event_id})

        # Return status erro if an error occurs
        if not directory:
            return 404
        if not check_authorization_on_event(user, event_id):
            return 403

        # Get event info (if directory exists also the evnt)
        event = await self._get_event_data(event_id)
        mails = directory["emails"]

        self._send_special(
            event_name=event["name"],
            message=message,
            subjet=subject,
            to_list=mails,
            event_url=event["event_url"],
            image=file
        )

    async def send_alert(self, event_id: str) -> int:
        """
        Send a alerta email one day before the event.
        """
        # Check if directory exist
        directory = await self.model.find({"event": event_id})

        # Return status erro if an error occurs
        if not directory:
            return 404

        # Get event extra info
        emails = directory["emails"]
        event = await self._get_event_data(event_id)

        self._send_alert(
            event_name=event["name"],
            event_url=event["event_url"],
            to_list=emails
        )

    async def _get_event_data(self, event_id: str) -> dict:
        """
        Retrieve the event info neccessary to send a email.
        """
        event_in_list = await self.model.find_from_foregyn_key(
            collection="events",
            foregyn_keys=[event_id],
        )

        event = event_in_list[0]

        # Complete public event url
        org_url = event["organizationUrl"]
        url = event["url"]
        event_url = f"{org_url}/{url}"
        event.update({"event_url": event_url})

        return event


MailController = MailControllerModel()
