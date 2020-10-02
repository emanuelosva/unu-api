"""
Speaker - Routes.
"""

# built-in imports
from typing import List

# external imports
import requests
from fastapi import APIRouter, BackgroundTasks, Depends

# module
from auth.service import get_current_user
from config import settings
from utils import exceptions, responses
from .schemas import SpeakerIn, SpeakerOut
from .controller import SpeakerController


router = APIRouter()


###########################################
##         Create a new Speaker          ##
###########################################


@router.post(
    "",
    status_code=201,
    response_model=SpeakerOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError},
    },
)
async def create_a_new_speaker(
    body: SpeakerIn, backgroud_task: BackgroundTasks, user=Depends(get_current_user)
):
    """
    Create a new speaker and the reference to the event.
    """
    speaker = await SpeakerController.create(body, user)

    if speaker == 403:
        exceptions.forbidden_403("Operation forbidden")
    if speaker == 409:
        exceptions.conflict_409("The name already exists")
    if not speaker:
        exceptions.server_error_500("Server error")

    # Backgroud task: add the speaker ref to event.speakers
    url = f"{settings.API_URL}/api/v1/events/{body.event}?action=add"
    body = {"field": "speakers", "uuid": speaker.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=body)

    return speaker


###########################################
##            Retrieve a speaker         ##
###########################################


@router.get(
    "",
    status_code=200,
    response_model=List[SpeakerOut],
    responses={"500": {"model": exceptions.ServerError}},
)
async def get_speakers_list(event_id: str):
    """
    Retrieve all speakers that belongs to the event.
    """
    speakers = await SpeakerController.read_many(event_id)
    return speakers


@router.get(
    "/{speaker_id}",
    status_code=200,
    response_model=SpeakerOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def get_a_speaker(speaker_id: str, _=Depends(get_current_user)):
    """
    Retrieve the info of a existing speaker.
    """
    speaker = await SpeakerController.read(speaker_id)
    if not speaker:
        exceptions.not_fount_404("speaker not found")

    return speaker


# ###########################################
# ##       Update a existing Speaker       ##
# ###########################################


@router.put(
    "/{speaker_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def update_a_existing_speaker(
    speaker_id: str, body: SpeakerIn, user=Depends(get_current_user)
):
    """
    Update a speaker info.
    """
    updated = await SpeakerController.update(speaker_id, body, user)

    if updated == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if updated == 404:
        exceptions.not_fount_404("speaker not found")

    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##            Delete a Speaker           ##
###########################################


@router.delete(
    "/{speaker_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.NotFound},
    },
)
async def delete_a_existing_speaker(
    speaker_id: str, backgroud_task: BackgroundTasks, user=Depends(get_current_user)
):
    """
    Delete a existing Speaker and the associated with the user
    """
    deleted, event_id = await SpeakerController.delete(speaker_id, user)

    if deleted == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if deleted == 404:
        exceptions.not_fount_404("Speaker not found")

    # Backgroud task: remove the Speaker ref to user.Speakers
    url = f"{settings.API_URL}/api/v1/events/{event_id}?action=remove"
    body = {"field": "speakers", "uuid": speaker_id}
    backgroud_task.add_task(requests.patch, url=url, json=body)

    return {"detail": f"Deleted count: {deleted}"}
