"""
Organization - Routes.
"""

from typing import List

from fastapi import APIRouter, Depends

from auth.service import get_auth_user
from db import CRUD, IntegrityError
from utils import responses, exceptions
from .schemas import Organization, OrganizationIn
from .models import OrganizationsModel


########################
# ORGANIZATIONS ROUTER #
########################
router = APIRouter()


#######################################
# DATA ACCESS FOR ORGANIZATIONS TABLE #
#######################################
organizations_crud = CRUD(OrganizationsModel, Organization)


#########################
# CREATE A ORGANIZATION #
#########################
@router.post(
    "",
    status_code=201,
    responses={
        "201": {"model": Organization},
        "401": {"model": responses.Unauthorized},
        "409": {"model": responses.Conflict},
        "500": {"model": responses.ServerError},
    },
)
async def create_a_new_organization(
    organization_info: OrganizationIn,
    user=Depends(get_auth_user),
) -> Organization:
    """
    Create a new organization and the reference to the user owner.
    """
    try:
        organization_data = organization_info.dict()
        unu_url = organization_data["name"].replace(" ", "-").lower()
        organization_data.update({"unu_url": unu_url})
        organization_data.update({"owner": user})
        organization = await organizations_crud.create(organization_data)
    except IntegrityError:
        exceptions.conflict_409("The name already exists")

    return organization


##############################
# RETRIEVE ALL ORGANIZATIONS #
##############################
@router.get(
    "",
    status_code=200,
    responses={
        "200": {"model": Organization},
        "401": {"model": responses.Unauthorized},
        "500": {"model": responses.ServerError},
    },
)
async def get_organizations_list(user=Depends(get_auth_user)) -> List[Organization]:
    """
    Retrieve all organizations of the current users.
    """
    organizations = await organizations_crud.read({"owner": user.id})
    return organizations


###########################
# RETRIEVE A ORGANIZATION #
###########################
@router.get(
    "/{organization_id}",
    status_code=200,
    responses={
        "200": {"model": Organization},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "500": {"model": responses.ServerError},
    },
)
async def get_organization(
    organization_id: str, user=Depends(get_auth_user)
) -> Organization:
    """
    Retrieve the organization with specific ID.
    """
    organization = await organizations_crud.read_one({"id": organization_id})
    if not organization:
        exceptions.not_fount_404("Organization not found")
    if organization.owner.id != user.id:
        exceptions.forbidden_403("Forbidden")
    return organization


#######################
# UPDATE ORGANIZATION #
#######################
@router.put(
    "/{organization_id}",
    status_code=200,
    responses={
        "200": {"model": Organization},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "404": {"model": responses.NotFound},
    },
)
async def update_a_existing_organization(
    organization_id: str,
    organization_info: OrganizationIn,
    user=Depends(get_auth_user),
) -> Organization:
    """
    Update a organization info.
    """
    organization: Organization = await organizations_crud.read_one(
        {"id": organization_id}
    )
    if organization.owner.id != user.id:
        exceptions.forbidden_403("Forbidden")

    organization = await organizations_crud.update(
        organization_id, organization_info.dict()
    )
    return organization


#######################
# DELETE ORGANIZATION #
#######################
@router.delete(
    "/{organization_id}",
    status_code=200,
    responses={
        "200": {"model": Organization},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "404": {"model": responses.NotFound},
    },
)
async def delete_a_existing_organization(
    organization_id: str, user=Depends(get_auth_user)
):
    """
    Delete a existing organization and return the info of it.
    """
    organization: Organization = await organizations_crud.read_one(
        {"id": organization_id}
    )
    if organization.owner.id != user.id:
        exceptions.forbidden_403("Forbidden")
    organization = await organizations_crud.delete(organization_id)
    return organization
