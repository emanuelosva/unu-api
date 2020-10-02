"""
Organizations - Controller
"""

# build-in imports
from uuid import uuid4
from typing import List

# module imports
from utils.general import store_file
from .models import OrganizationModel
from .schemas import Organization, OrganizationIn, OrganizationOut


class OrganizationControllerModel:
    """
    Organization controller.
    """

    def __init__(self):
        self.model = OrganizationModel

    async def create(self, organization: OrganizationIn, user: str) -> OrganizationOut:
        """
        Create a new organization.
        """
        query = {"name": organization.name}
        existing_org = await self.model.find(query)
        if existing_org:
            return 409

        new_org_data: dict = organization.dict()
        new_org_data.update({"uuid": str(uuid4())})
        new_org_data.update({"user": user})

        logo: str = store_file(file_b64=new_org_data["logo"])
        new_org_data.update({"logo": logo})

        unu_url: str = new_org_data["name"].replace(" ", "-").lower()
        new_org_data.update({"unuUrl": unu_url})

        new_org = Organization(**new_org_data)

        inserted_id = await self.model.create(new_org.dict())
        if not inserted_id:
            return False

        return OrganizationOut(**new_org.dict())

    async def read(self, organization_id: str) -> OrganizationOut:
        """
        Retrieve a existing organization
        """
        query = {"uuid": organization_id}
        organization = await self.model.find(query)
        if not organization:
            return False
        return OrganizationOut(**organization)

    async def read_many(self, query_field: str, value: any) -> List[OrganizationOut]:
        """
        Retrieve a list of organizations
        """
        organizations = await self.model.find({f"{query_field}": value}, only_one=False)
        if not organizations:
            return []
        return organizations

    async def update(self, organization_id: str, new_org_data: OrganizationIn) -> int:
        """
        Update a existing organization
        """
        organization = await self.read(organization_id)
        if not organization:
            return 404, None

        new_data = new_org_data.dict()

        logo = store_file(file_b64=new_data["logo"])
        new_data.update({"logo": logo})

        unu_url: str = new_data["name"].replace(" ", "-").lower()
        new_data.update({"unuUrl": unu_url})

        query = {"uuid": organization_id}
        updated = await self.model.update(query, new_data)

        return updated, organization.uuid

    async def update_to_field(
        self, organization_unu_url: str, field: str, uuid: str, action: str
    ) -> OrganizationOut:
        """
        Update a existing user
        """
        query = {"unuUrl": organization_unu_url}
        if action == "add":
            updated = await self.model.add_to_set(query, field, uuid)
        if action == "remove":
            updated = await self.model.pull_array(query, field, uuid)

        return updated

    async def delete(self, organization_id: str, user: dict) -> int:
        """
        Delete a existing user
        """
        organization = await self.read(organization_id)
        if not organization:
            return 404, None

        if not organization.uuid in user["organizations"]:
            return 403, None

        deleted_count = await self.model.delete({"uuid": organization_id})
        return deleted_count, organization.user


OrganizatioController = OrganizationControllerModel()
