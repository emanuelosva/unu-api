"""
Users - Controller
"""

# build-in imports
from uuid import uuid4


from auth.service import hash_password, create_access_token, authenticate_user
from .models import UserModel
from .schemas import User, UserIn, UserOnAuth, UserOut


class UserControllerModel:
    """
    User controller.
    """

    def __init__(self):
        self.model = UserModel

    async def create(self, user: UserIn) -> UserOnAuth:
        """
        Create a new user
        """
        existing_user = await self.model.find({"email": user.email})
        if existing_user:
            return False

        new_user_data = user.dict()
        hashed_password = hash_password(new_user_data["password"])
        new_user_data.update({"password": hashed_password})
        new_user_data.update({"uuid": str(uuid4())})

        new_user = User(**new_user_data)

        inserted_id = await self.model.create(new_user.dict())
        if not inserted_id:
            return False

        token = create_access_token({"email": user.email})
        return UserOnAuth(
            user=new_user.dict(),
            accessToken=token,
            tokenType="Bearer"
        )

    async def read(self, user_id: str, email: str = None) -> UserOut:
        """
        Retrieve a existing user
        """
        if email is not None:
            user = await self.model.find({"email": email})
            if not user:
                return False
            return user

        user = await self.model.find({"uuid": user_id})
        if not user:
            return False

        user["organizations"] = await self.model.find_from_foregyn_key(
            collection="organizations",
            foregyn_keys=user["organizations"],
        )
        user["myEvents"] = await self.model.find_from_foregyn_key(
            collection="events",
            foregyn_keys=user["myEvents"],
        )
        user["myCollaborations"] = await self.model.find_from_foregyn_key(
            collection="events",
            foregyn_keys=user["myCollaborations"]
        )

        return UserOut(**user)

    async def update(self, user_id: str, new_user_data: UserIn) -> int:
        """
        Update a existing user
        """
        user = await self.read(user_id)
        if not user:
            return 404

        new_data = new_user_data.dict()

        if user.email != new_data["email"]:
            used_email = await self.model.find(
                {"email": new_data["email"]},
                only_one=False
            )
            if used_email:
                return 409

        new_data.update({"password": hash_password(new_data["password"])})

        updated = await self.model.update({"uuid": user_id}, new_data)
        return updated

    async def update_to_field(
            self, user_id: str, field: str, uuid: str, action: str) -> UserOut:
        """
        Update a existing user
        """
        user = await self.read(user_id)
        if not user:
            return False

        query = {"uuid": user_id}

        if action == "add":
            await self.model.push_nested(query, field, uuid)
        if action == "remove":
            await self.model.pull_array(query, field, uuid)

        user = await self.read(user_id)
        return user

    async def delete(self, user_id: str) -> int:
        """
        Delete a existing user
        """
        user = await self.read(user_id)
        if not user:
            return 404

        deleted_count = await self.model.delete({"uuid": user_id})
        return deleted_count

    async def authenticate(self, email: str, password: str) -> UserOnAuth:
        """
        Authenticate a user and return info.
        """
        user_authenticated = await authenticate_user(email, password)
        if not user_authenticated:
            return False

        user = await self.read(user_authenticated["uuid"])
        token = create_access_token({"email": user.email})

        return UserOnAuth(
            user=user.dict(),
            accessToken=token,
            tokenType="Bearer"
        )


UserController = UserControllerModel()
