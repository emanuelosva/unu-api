"""
Organization - Routes.
"""

# built-in imports
from typing import List

# external imports
import requests
from fastapi import APIRouter, Body, BackgroundTasks, Depends

# module
from auth.service import get_current_user, check_permission
from config import settings
from utils import exceptions, responses
from .schemas import EventsIn, EventOut, Event, EventUpdate
from .controller import EventController


router = APIRouter()


###########################################
##           Create a new Event          ##
###########################################


@router.post(
    "",
    status_code=201,
    response_model=EventOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "500": {"model": exceptions.ServerError},
    },
)
async def create_a_new_event(
    body: EventsIn, backgroud_task: BackgroundTasks, user=Depends(get_current_user)
):
    """
    Create a new event and the reference
    to the user owner and organization.
    """
    user_uuid = user["uuid"]
    event = await EventController.create(body, user_uuid)

    if not event:
        exceptions.server_error_500("Server error")

    # Backgroud tasks:

    # Add the event ref to user.events
    url = f"{settings.API_URL}/api/v1/users/{user_uuid}?action=add"
    json = {"field": "myEvents", "uuid": event.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    # Add the event ref organization.events
    org_url = body.organizationUrl
    url = f"{settings.API_URL}/api/v1/organizations/{org_url}?action=add"
    json = {"field": "events", "uuid": event.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    # Create a new participants directory
    url = f"{settings.API_URL}/api/v1/participants?event_id={event.uuid}"
    backgroud_task.add_task(requests.post, url=url)

    return event


###########################################
##             Retrieve Events           ##
###########################################


@router.get(
    "/published",
    status_code=200,
    response_model=List[Event],
    responses={"500": {"model": exceptions.ServerError}},
)
async def get_events_list():
    """
    Retrieve all the published events.
    """
    events = await EventController.get_published()
    return events


@router.get(
    "/from-url",
    status_code=200,
    response_model=Event,
    responses={
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def get_events_from_url(organization_url: str, url: str):
    """
    Retrieve a event that mathces the url.
    """
    event = await EventController.get_from_url(organization_url, url)
    if not event:
        exceptions.not_fount_404("Event not found")
    return event


@router.get(
    "/{event_id}",
    status_code=200,
    response_model=EventOut,
    responses={
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def get_a_event(event_id: str, user=Depends(get_current_user)):
    """
    Retrieve the info a specific event.
    """
    event = await EventController.read(event_id)
    if not event:
        exceptions.not_fount_404("Event not found")

    if not event.uuid in user["myEvents"]:
        if not event.uuid in user["myCollaborations"]:
            exceptions.forbidden_403("Operation Forbidden")

    return event


###########################################
##        Update a existing Event        ##
###########################################


@router.put(
    "/{event_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def update_a_existing_event(
    event_id: str, body: EventUpdate, user=Depends(get_current_user)
):
    """
    Update a event info.
    """
    updated, uuid = await EventController.update(event_id, body)

    if updated == 404:
        exceptions.not_fount_404("Event not found")

    if not uuid in user["myEvents"]:
        if not uuid in user["myCollaborations"]:
            exceptions.forbidden_403("Operation Forbidden")

    return {"detail": "Modified success", "modifiedCount": updated}


@router.put(
    "/{event_id}/change_status",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def change_publication_status(
    event_id: str, actual_status: bool, user=Depends(get_current_user)
):
    """
    Change the publication status of one event only if the user owner call
    the endpoint.
    """
    event = await EventController.read(event_id)
    if not event:
        exceptions.not_fount_404("Event not found")

    check_permission(user, event.user)

    updated = await EventController.change_status(event_id, actual_status)
    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##      Update a Association in Event    ##
###########################################


@router.patch(
    "/{event_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={"404": {"model": exceptions.NotFound}},
)
async def update_association_in_event(
    event_id: str, action: str, field: str = Body(...), uuid: str = Body(...)
):
    """
    Add or remove a association in one event.
    """
    updated = await EventController.update_to_field(event_id, field, uuid, action)
    if not updated:
        exceptions.not_fount_404("Event not found")

    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##             Delete a Event            ##
###########################################

###
# Should delete all registries associated with event
###
@router.delete(
    "/{event_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError},
    },
)
async def delete_a_existing_event(
    event_id: str, backgroud_task: BackgroundTasks, user=Depends(get_current_user)
):
    """
    Delete a existing event and its associations with user and organization.
    """
    deleted, event = await EventController.delete(event_id, user)

    if deleted == 403:
        exceptions.forbidden_403("Operation Forbidden")
    if deleted == 404:
        exceptions.not_fount_404("Event not found")

    # Backgroud task: remove the event ref

    # from user.myEvents,
    url = f"{settings.API_URL}/api/v1/users/{event.user}?action=remove"
    json = {"field": "myEvents", "uuid": event.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    # from user.myCollaborations
    json = {"field": "myCollaborations", "uuid": event.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    # from organization.events
    org_url = event.organizationUrl
    url = f"{settings.API_URL}/api/v1/organizations/{org_url}?action=remove"
    json = {"field": "events", "uuid": event_id}
    backgroud_task.add_task(requests.patch, url=url, json=json)

    return {"detail": f"Deleted count: {deleted}"}
