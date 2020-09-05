"""
Users - Routes.
"""

# external imports
import requests
from fastapi import APIRouter, Body, Depends, BackgroundTasks

# module imports
from config import settings
from auth.service import get_current_user, check_permission
from utils import exceptions, responses
from mails.service import send_welcome_email
from .schemas import UserIn, UserOut, UserOnAuth, UserLogin, UserCollaborator
from .controller import UserController


router = APIRouter()


###########################################
##          Register a new user          ##
###########################################

@router.post(
    "/signup",
    status_code=201,
    response_model=UserOnAuth,
    responses={
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError}
    })
async def register_a_new_user(body: UserIn, background_task: BackgroundTasks):
    """
    Register a new user and return the access token.
    """
    register_response = await UserController.create(user=body)
    if not register_response:
        exceptions.conflict_409("The email already exists")

    background_task.add_task(
        send_welcome_email,
        username=body.name,
        email=body.email
    )

    return register_response


@router.post(
    "/add_collaborator",
    status_code=201,
    response_model=responses.Created,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError},
    })
async def add_user_as_collaborator(
        body: UserCollaborator, background_task: BackgroundTasks,
        event_id: str, existing: bool = False,
        user=Depends(get_current_user)):
    """
    Add a new user as collaboration.
    """
    if not event_id in user["myEvents"]:
        exceptions.forbidden_403("Operation forbidden")

    # Add as collaborator a existing user

    if existing:
        user = await UserController.read(email=body.email, user_id="")
        if not user:
            exceptions.not_fount_404("User not found")

        # Add the collaborator to the event
        user_uuid = user["uuid"]
        url = f"{settings.API_URL}/api/v1/events/{event_id}?action=add"
        json = {"field": "collaborators", "uuid": user_uuid}
        background_task.add_task(requests.patch, url=url, json=json)

        # Add the event to the user in his collaboration
        url = f"{settings.API_URL}/api/v1/users/{user_uuid}?action=add"
        json = {"field": "myCollaborations", "uuid": event_id}
        background_task.add_task(requests.patch, url=url, json=json)

        return {"detail": "User added as collaborator", "uuid": user_uuid}

    # Register a new user and add as collaborator

    register_response = await UserController.create(user=body)
    if not register_response:
        exceptions.conflict_409("The email already exists")

    # Add the collaborator to the event
    user_uuid = register_response.user.uuid
    url = f"{settings.API_URL}/api/v1/events/{event_id}?action=add"
    json = {"field": "collaborators", "uuid": user_uuid}
    background_task.add_task(requests.patch, url=url, json=json)

    # Add the event to the user in his collaboration
    url = f"{settings.API_URL}/api/v1/users/{user_uuid}?action=add"
    json = {"field": "myCollaborations", "uuid": event_id}
    background_task.add_task(requests.patch, url=url, json=json)

    # Send welcome email to the new user
    background_task.add_task(
        send_welcome_email,
        username=body.name,
        email=body.email
    )

    return {"detail": "Created and added entitie", "uuid": user_uuid}


###########################################
##              Login a User             ##
###########################################

@ router.post(
    "/login",
    status_code=200,
    response_model=UserOnAuth,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "500": {"model": exceptions.ServerError}
    })
async def login_for_acces_token(body: UserLogin):
    """
    Login a user
    """
    user_authenticated = await UserController.authenticate(
        body.email, body.password)
    if not user_authenticated:
        exceptions.unauthorized_401("Invalid credentials")

    return user_authenticated


###########################################
##          Retrieve a loged User        ##
###########################################

@ router.get(
    "",
    status_code=200,
    response_model=UserOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError}
    })
async def get_a_logged_user(user: dict = Depends(get_current_user)):
    """
    Retrieve the info of the logen current user.
    """
    user: UserOut = await UserController.read(user["uuid"])
    if not user:
        exceptions.not_fount_404("User not found")
    return user


###########################################
##          Update a existing User       ##
###########################################

@router.put(
    "/{user_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError}
    })
async def update_a_existing_user(
        user_id: str, body: UserIn, user=Depends(get_current_user)):
    """
    Update a existing user
    """
    check_permission(user, user_id)

    updated_count = await UserController.update(user_id, body)
    if updated_count == 404:
        exceptions.not_fount_404("User not found")
    if updated_count == 409:
        exceptions.conflict_409("The email already exists")
    return {"detail": "Modified success", "modifiedCount": updated_count}


###########################################
##      Update a Association in User     ##
###########################################

@router.patch(
    "/{user_id}",
    status_code=200,
    response_model=UserOut,
    responses={"404": {"model": exceptions.NotFound}})
async def update_association_in_user(
        user_id: str, action: str,
        field: str = Body(...), uuid: str = Body(...)):
    """
    Update a associated field in user
    """
    user_updated = await UserController.update_to_field(
        user_id, field, uuid, action)

    if not user_updated:
        exceptions.not_fount_404("User not found")
    return user_updated


###########################################
##          Delete a existing User       ##
###########################################

@ router.delete(
    "/{user_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound},
        "500": {"model": exceptions.ServerError}
    })
async def delete_a_existing_user(user_id: str, user=Depends(get_current_user)):
    """
    Delete a existing user
    """
    check_permission(user, user_id)

    deleted = await UserController.delete(user_id)
    if deleted == 404:
        exceptions.not_fount_404("User not found")
    return {"detail": f"Deleted count: {deleted}"}
