"""
Participants - Routes.
"""

# external imports
from fastapi import APIRouter, Depends

# module
from auth.service import get_current_user
from utils import exceptions, responses
from .schemas import PariticipantsDir, PariticipantsDirOut, RegisterResponse
from .controller import ParticipantsController


router = APIRouter()


###########################################
##    Create a Participants directory    ##
###########################################

@router.post(
    "",
    status_code=201,
    response_model=PariticipantsDir,
    responses={
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError},
    })
async def create_a_new_pariticpants_directory(event_id: str):
    """
    Create a new participants directory.
    """
    participants_dir = await ParticipantsController.create(event_id)

    if participants_dir == 409:
        exceptions.conflict_409("There is a directory for this event")
    if not event_id:
        exceptions.server_error_500("Server Error")

    return participants_dir


###########################################
##         Register a participant        ##
###########################################

@router.post(
    "/register",
    status_code=201,
    response_model=RegisterResponse,
    responses={
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def register_a_participant(event_id: str, email: str):
    """
    Register a new participant to one event. Add the email to
    the respective participnats directory.
    """
    registered = await ParticipantsController.register(event_id, email)

    if registered == 404:
        exceptions.not_fount_404("Event not found")
    if registered is None:
        exceptions.server_error_500("Server Error")
    if registered == 0:
        return {"detail": "Email already registered", "event": event_id}

    return {"detail": "Registered successful", "event": event_id}


###########################################
##      Get  Participants Directory      ##
###########################################

@router.get(
    "",
    status_code=200,
    response_model=PariticipantsDirOut,
    responses={
        "404": {"model": exceptions.NotFound},
        "403": {"model": exceptions.Forbidden},
        "500": {"model": exceptions.ServerError},
    })
async def get_participants_dir(
        event_id: str,
        user: dict = Depends(get_current_user)):
    """
    Return the participants directory of a specific event
    """
    participants_dir = await ParticipantsController.read(event_id, user)

    if participants_dir == 403:
        exceptions.forbidden_403("Resource forbidden")
    if participants_dir == 404:
        exceptions.not_fount_404("Directory for event not found")

    return participants_dir


###########################################
##    Delete a Participants Directory    ##
###########################################

@router.delete(
    "",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def delete_a_participants_directory(event_id: str):
    """
    Delete a participants directory when event is deleted.
    """
    deleted = await ParticipantsController.delete(event_id)

    if deleted == 404:
        return exceptions.not_fount_404("Directory for passed event not found")

    return {"detail": f"deleted count: {deleted}"}
