"""
Organization - Routes.
"""

# built-in imports
from typing import List

# external imports
import requests
from fastapi import APIRouter, BackgroundTasks, Depends

# module
from auth.service import get_current_user, check_authorization_on_event
from config import settings
from utils import exceptions, responses
from .schemas import AssociatedIn, AssociatedOut
from .controller import AssociatedController


router = APIRouter()


###########################################
##        Create a new Associated        ##
###########################################


@router.post(
    "",
    status_code=201,
    response_model=AssociatedOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "500": {"model": exceptions.ServerError},
    },
)
async def create_a_new_associated(
    body: AssociatedIn, backgroud_task: BackgroundTasks, user=Depends(get_current_user)
):
    """
    Create a new associated and reference it to one event.
    """
    if not check_authorization_on_event(user, body.event):
        exceptions.forbidden_403("Operation forbidden")

    associated = await AssociatedController.create(body)

    if not associated:
        exceptions.server_error_500("Server error")

    # Backgroud task: add the associated ref to event.associateds
    event_uuid = body.event
    url = f"{settings.API_URL}/api/v1/events/{event_uuid}?action=add"
    json = {"field": "associateds", "uuid": associated.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    return associated


###########################################
##          Retrieve Associateds         ##
###########################################


@router.get(
    "",
    status_code=200,
    response_model=List[AssociatedOut],
    responses={"500": {"model": exceptions.ServerError}},
)
async def get_all_associated_in_event(event_id: str):
    """
    Return all associateds in one event
    """
    associateds = await AssociatedController.read(associated_id="", event_id=event_id)
    return associateds


@router.get(
    "/{associated_id}",
    status_code=200,
    response_model=AssociatedOut,
    responses={
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def get_associated(associated_id: str, _=Depends(get_current_user)):
    """
    Retrieve a existing associated.
    """
    associated = await AssociatedController.read(associated_id)
    if not associated:
        exceptions.not_fount_404("Associated not Found")
    return associated


###########################################
##        Update a existing Event        ##
###########################################


@router.put(
    "/{associated_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError},
    },
)
async def update_a_associated(
    associated_id: str, body: AssociatedIn, user=Depends(get_current_user)
):
    """
    Update a existing associated.
    """
    updated = await AssociatedController.update(associated_id, body, user)

    if updated == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if updated == 404:
        exceptions.not_fount_404("Associated not found")

    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##             Delete a Event            ##
###########################################


@router.delete(
    "/{associated_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def delete_a_existing_associated(
    associated_id: str, backgroud_task: BackgroundTasks, user=Depends(get_current_user)
):
    """
    Delete a existing event and its associations with user and organization.
    """

    deleted, associated = await AssociatedController.delete(associated_id, user)
    if deleted == 403:
        exceptions.forbidden_403("Operation Forbiden")
    if deleted == 404:
        exceptions.not_fount_404("Event not found")

    # Backgroud task: remove the associated from event

    url = f"{settings.API_URL}/api/v1/events/{associated.event}?action=remove"
    json = {"field": "associateds", "uuid": associated.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    return {"detail": f"Deleted count: {deleted}"}
