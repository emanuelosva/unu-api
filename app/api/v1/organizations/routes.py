"""
Organization - Routes.
"""

# built-in imports
from typing import List

# external imports
import requests
from fastapi import APIRouter, Body, BackgroundTasks, Depends

# module
from auth.service import get_current_user
from config import settings
from utils import exceptions, responses
from .schemas import OrganizationIn, OrganizationOut
from .controller import OrganizatioController


router = APIRouter()


###########################################
##       Create a new organization       ##
###########################################

@router.post(
    "",
    status_code=201,
    response_model=OrganizationOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "409": {"model": exceptions.Conflict},
        "500": {"model": exceptions.ServerError}
    })
async def create_a_new_organization(
        body: OrganizationIn, backgroud_task: BackgroundTasks,
        user=Depends(get_current_user)):
    """
    Create a new organization and the reference to the user owner.
    """
    user_uuid = user["uuid"]
    organization = await OrganizatioController.create(body, user_uuid)

    if organization == 409:
        exceptions.conflict_409("The name already exists")
    if not organization:
        exceptions.server_error_500("Server error")

    # Backgroud task: add the organization ref to user.organizations
    url = f"{settings.API_URL}/api/v1/users/{user_uuid}?action=add"
    body = {"field": "organizations", "uuid": organization.uuid}
    backgroud_task.add_task(requests.patch, url=url, json=body)

    return organization


###########################################
##          Retrieve a organization      ##
###########################################

@router.get(
    "/",
    status_code=200,
    response_model=List[OrganizationOut],
    responses={
        "401": {"model": exceptions.Unauthorized},
        "404": {"model": exceptions.NotFound}
    })
async def get_organizations_list(
        query_field: str, value: str,
        _=Depends(get_current_user)):
    """
    Retrieve the info of roganizations that matches the query.
    """
    organizations = await OrganizatioController.read_many(query_field, value)
    return organizations


@router.get(
    "/{organization_id}",
    status_code=200,
    response_model=OrganizationOut,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound}
    })
async def get_a_organization(
        organization_id: str, user=Depends(get_current_user)):
    """
    Retrieve the info of the existing organization.
    """
    organization = await OrganizatioController.read(organization_id)
    if not organization:
        exceptions.not_fount_404("Organization not found")

    if not organization.uuid in user["organizations"]:
        exceptions.forbidden_403("Operation Forbidden")

    return organization


###########################################
##     Update a existing Organization    ##
###########################################

@router.put(
    "/{organization_id}",
    status_code=200,
    response_model=responses.Updated,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound}
    })
async def update_a_existing_organization(
        organization_id: str, body: OrganizationIn,
        user=Depends(get_current_user)):
    """
    Update a organization info.
    """
    updated, uuid = await OrganizatioController.update(organization_id, body)

    if updated == 404:
        exceptions.not_fount_404("Organization not found")

    if not uuid in user["organizations"]:
        exceptions.forbidden_403("Operation Forbidden")

    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##      Update a Association in User     ##
###########################################

@router.patch(
    "/{organization_unu_url}",
    status_code=200,
    response_model=responses.Updated,
    responses={"404": {"model": exceptions.NotFound}})
async def update_association_in_organization(
        organization_unu_url: str, action: str,
        field: str = Body(...), uuid: str = Body(...)):
    """
    Update a nested field in organizations
    """
    updated = await OrganizatioController.update_to_field(
        organization_unu_url, field, uuid, action)
    if not updated:
        exceptions.not_fount_404("Organization not found")

    return {"detail": "Modified success", "modifiedCount": updated}


###########################################
##          Delete a Organization        ##
###########################################

@router.delete(
    "/{organizaion_id}",
    status_code=200,
    response_model=responses.Deleted,
    responses={
        "401": {"model": exceptions.Unauthorized},
        "403": {"model": exceptions.Forbidden},
        "404": {"model": exceptions.NotFound}
    })
async def delete_a_existing_organization(
        organizaion_id: str, backgroud_task: BackgroundTasks,
        user=Depends(get_current_user)):
    """
    Delete a existing organization and the associated with the user
    """
    deleted, user_id = await OrganizatioController.delete(organizaion_id, user)

    if deleted == 403:
        exceptions.forbidden_403("Operation forbidden")
    if deleted == 404:
        exceptions.not_fount_404("Organization not found")

    # Backgroud task: remove the organization ref to user.organizations
    url = f"{settings.API_URL}/api/v1/users/{user_id}?action=remove"
    body = {"field": "organizations", "uuid": organizaion_id}
    backgroud_task.add_task(requests.patch, url=url, json=body)

    return {"detail": f"Deleted count: {deleted}"}
