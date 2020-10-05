"""
Authentication logic.
"""

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security.api_key import APIKeyCookie
from jose import JWTError, jwt
from passlib.context import CryptContext

from db.crud import CRUD
from api.v1.users.schemas import User, UsersModel
from utils import exceptions
from config import settings


#################
# Auth Settings #
#################

SECRET = settings.SECRET_JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30  # One month


######################
# Security Instances #
######################

pwd_context = CryptContext(schemes=["bcrypt"])
auth_scheme = APIKeyCookie(name=settings.COOKIE_SESSION_NAME)


#######################
# Users CRUD Instance #
#######################

users_db = CRUD(UsersModel, User)


##########################
#  Helper Auth Functions #
##########################


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the enter password with the hashed password stored in db.

    Params:
    ------
    - plain_password: str - The plain password from the request form.
    - hashed_password: str -The hashed password stored in db.

    Return:
    ------
    - Boolean: True if correct password, False if not.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """
    Generate a hash of the current password.

    Params:
    ------
    - plain_password: str - The plain password from the request form.

    Return:
    ------
    - hashed_password: str - The password hashed.
    """
    return pwd_context.hash(plain_password)


def create_access_token(email: str, for_recovery_password: bool = False) -> str:
    """
    Return a encoded jwt.

    Params:
    ------
    - data: dict - The data to encoded in jwt paayload.
    - for_recovery_password: bool - Indicate if the token has a short time duration.

    Return:
    ------
    - encode_jwt: bytes - The encoded json web token.
    """
    to_encode = {"email": email}
    expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def get_from_token(token: str) -> str:
    """
    Verify the token and return the email in payload if is valid.

    Params:
    ------
    - token: str - The encoded JWT

    Return:
    ------
    - email: str - The user email
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = payload["email"]
    except (JWTError, KeyError):
        raise exceptions.unauthorized_401()
    return email


#############################
# Authentication Middleware #
#############################


async def get_auth_user(token: str = Depends(auth_scheme)) -> any:
    """
    Extract the token from cookie and validate if is valid.

    Params:
    ------
    - taken: str - The jwt in the cookie request.

    Return:
    - user: UserOut - The user data.
    """
    email = get_from_token(token)
    user = await users_db.read_one({"email": email}, return_db_model=True)
    if not user:
        raise exceptions.unauthorized_401()
    return user
