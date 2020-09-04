"""
Organization - Routes.
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
from .schemas import DayIn, DayOut, ConferenceIn, ConferenceOut
from .controller import AgendaController


router = APIRouter()


###########################################
##        Create a Agenda Entities       ##
###########################################

@router.post(
    "/days",
    status_code=201,
    response_model=DayOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError},
    })
async def create_a_new_day(
        body: DayIn,
        backgroud_task: BackgroundTasks,
        user=Depends(get_current_user)):
    """
    Create a new day in agenda and reference it to one event.
    """
    day = await AgendaController.create_day(body, user)

    if day == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if day == 409:
        exceptions.conflict_409("The date is already taken")
    if not day:
        exceptions.server_error_500("Server error")

    # Backgroud task: add the day ref to event.agenda
    event_uuid = body.event
    url = f"{settings.API_URL}/api/v1/events/{event_uuid}?action=add"
    json = {"field": "agenda", "uuid": day.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    return day


@router.post(
    "/conferences",
    status_code=201,
    response_model=ConferenceOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def create_a_conference_to_day(
        day_id: str, body: ConferenceIn,
        user=Depends(get_current_user)):
    """
    Add a new conference to one day.
    """
    conference = await AgendaController.create_conference(day_id, body, user)

    if conference == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if conference == 404:
        exceptions.not_fount_404("Day not found")
    if not conference:
        exceptions.server_error_500("Server Error")

    return conference


###########################################
##        Retrieve Agenda Entities       ##
###########################################

@router.get(
    "/days",
    status_code=200,
    response_model=List[DayOut],
    responses={
        "500": {"model": exceptions.ServerError},
    })
async def get_all_days(event_id: str):
    """
    Return all day of one event.
    """
    days = await AgendaController.read_all_days(event_id)
    return days


@router.get(
    "/days/{day_id}",
    status_code=200,
    response_model=DayOut,
    responses={
        "404": {"mode": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def get_a_day(day_id: str, _=Depends(get_current_user)):
    """
    Return a day info.
    """
    day = await AgendaController.read_day(day_id)

    if not day:
        exceptions.not_fount_404("Day not found")

    return day


@router.get(
    "/conferences/{conference_id}",
    status_code=200,
    response_model=ConferenceOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError}
    })
async def get_one_conference(conference_id: str, _=Depends(get_current_user)):
    """
    Retrieve a existing conference.
    """
    conference = await AgendaController.get_conference(conference_id)
    if not conference:
        exceptions.not_fount_404("conference not Found")
    return conference


###########################################
##         Update Agenda Entities        ##
###########################################

@router.put(
    "/days/{day_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "409": {"model": exceptions.Conflict},
        "412": {"mode": exceptions.FailPrecondition},
        "500": {"model": exceptions.ServerError},
    })
async def update_a_existing_day(
        day_id: str, body: DayIn,
        user=Depends(get_current_user)):
    """
    Update a existing day.
    """
    updated = await AgendaController.update_day(day_id, body, user)

    if updated == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if updated == 404:
        exceptions.not_fount_404("Day not found")
    if updated == 409:
        exceptions.conflict_409("The date is already ocuped")
    if updated == 412:
        exceptions.fail_precondition_412(
            "This day doesn't belongs to the passed event"
        )

    return {"detail": "Modified success", "modifiedCount": updated}


@router.put(
    "/conferences/{conference_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def update_a_conference(
        conference_id, body: ConferenceIn,
        user=Depends(get_current_user)):
    """
    Update a existing conference.
    """
    updated = await AgendaController.update_conference(
        conference_id, body, user
    )

    if updated == 403:
        exceptions.forbidden_403("Operation forbidden")
    if updated == 404:
        exceptions.not_fount_404("Conference not found")

    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##         Delete Agenda entities        ##
###########################################

@router.delete(
    "/conferences/{conference_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"mode": exceptions.ServerError},
    })
async def delete_a_conference(
        conference_id: str, user: dict = Depends(get_current_user)):
    """
    Delete a conference from a day.
    """
    deleted = await AgendaController.delete_conferene(
        conference_id,
        user,
    )

    if deleted == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if deleted == 404:
        exceptions.not_fount_404("Conference not found")

    return {"detail": f"Deleted count: {deleted}"}


@router.delete(
    "/days/{day_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    })
async def delete_a_existing_day(
        day_id: str, backgroud_task: BackgroundTasks,
        user: dict = Depends(get_current_user)):
    """
    Delete a existing day and remove the association from event.
    """
    deleted, day = await AgendaController.delete_day(day_id, user)

    if deleted == 403:
        exceptions.forbidden_403("Operation Forbiden")
    if deleted == 404:
        exceptions.not_fount_404("Event not found")

    # Backgroud task: remove the day from event
    url = f"{settings.API_URL}/api/v1/events/{day.event}?action=remove"
    json = {"field": "agenda", "uuid": day.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    return {"detail": f"Deleted count: {deleted}"}
