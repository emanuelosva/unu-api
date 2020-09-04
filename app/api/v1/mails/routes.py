"""
Mails - Routes.
"""
# build-in modules
from typing import Optional

# external imports
from fastapi import APIRouter, Form, UploadFile, Depends

# module imports
from auth.service import get_current_user
from utils import exceptions
from .schemas import MailResponse
from .controller import MailController


router = APIRouter()


###########################################
##          Send a special email         ##
###########################################

@router.post(
    "/special",
    status_code=200,
    response_model=MailResponse,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "500": {"model": exceptions.ServerError},
    })
async def send_special_email(
        event_id: str = Form(...),
        subject: str = Form(...),
        message: str = Form(...),
        file: Optional[UploadFile] = Form(None),
        user: dict = Depends(get_current_user)):
    """
    Send a special email to all registered participants of a specific event.
    """
    if not file:
        file = None

    sended = await MailController.send_special(
        event_id, subject, message, file, user
    )

    if sended == 403:
        exceptions.forbidden_403("Operation forbidden")
    if sended == 404:
        exceptions.not_fount_404("Event not found")

    return {"detail": "Email sended", "target": f"Event: {event_id}"}


###########################################
##           Send a alert Email          ##
###########################################

@router.post(
    "/alert",
    status_code=200,
    response_model=MailResponse,
    responses={
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def send_alert_email(event_id: str):
    """
    Send a email of alert when there is one day left to the event.
    """
    sended = await MailController.send_alert(event_id)

    if sended == 404:
        exceptions.not_fount_404("Event not found")

    return {"detail": "Email sended", "target": f"Event: {event_id}"}
