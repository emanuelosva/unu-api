"""
Authentication logic.
"""

# build-in imports
from typing import Optional
from datetime import datetime, timedelta

# external imports
from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611
from jose import JWTError, jwt
from passlib.context import CryptContext

# module imports
from db.crud import CRUD
from config import settings


###########################################
##             Auth Settings             ##
###########################################

SECRET = settings.SECRET_JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


###########################################
##            Security Instances         ##
###########################################

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = APIKeyHeader(name="Authorization")


###########################################
##          Users CRUD Instance          ##
###########################################
USER_COLLECTION_NAME = "users"
users_crud = CRUD(USER_COLLECTION_NAME)


###########################################
##              Token Schemas            ##
###########################################

class Token(BaseModel):
    """
    Token base schema
    """
    accessToken: str = Field(description="The encoded jwt")
    tokenType: str = Field(description="The token type: 'Bearer'")


class TokenData(BaseModel):
    """
    Token request schema
    """
    email: Optional[str] = None


###########################################
##          Helper Auth Functions        ##
###########################################

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the enter password with the hashed password stored in db.

    Params:
    ------
    plain_password: str - The plain password from the request form.
    hashed_password: str -The hashed password stored in db.

    Return:
    ------
    Boolean: True if correct password, False if not.
    """

    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """
    Generate a hash of the current password.

    Params:
    ------
    plain_password: str - The plain password from the request form.

    Return:
    ------
    hashed_password: str - The password hashed.
    """

    return pwd_context.hash(plain_password)


async def authenticate_user(email: str, password: str) -> dict:
    """
    Auhenticate the user recived in the request.

    Params:
    ------
    email: str - The user email
    password: str - The password email

    Return:
    ------
    user: UserOut - The user class. If not authenticated, returns False.
    """

    user = await users_crud.find({"email": email})
    if not user:
        return False
    if not verify_password(password, user.get("password")):
        return False
    return user


def create_access_token(
        data: dict, expires_delta: timedelta = None) -> bytes:
    """
    Return a encoded jwt.

    Params:
    ------
    data: dict
        The data to encoded in jwt paayload.
    expires_delta: timedelta (optional)
        The time in minutes to expire token.

    Return:
    ------
    encode_jwt: bytes - The encoded json web token.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


###########################################
##        Authentication Middleware      ##
###########################################

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verify the user in token and return the user if token is valid.

    Params:
    ------
    taken: str - The jwt in the header request.

    Return:
    user: UserOut - The user data.
    """
    try:
        if token.startswith("Bearer"):
            token = token.split(" ")[1]

        payload: dict = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception from credentials_exception

    token_data = TokenData(email=email)
    user = await users_crud.find({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user


def check_permission(entitie: dict, uuid: str) -> None:
    """
    Check permission.
    """
    if entitie["uuid"] != uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation forbidden"
        )


def check_authorization_on_event(user: dict, event_id) -> bool:
    """
    Check if the user have persmission of edit a event entities
    """
    if not event_id in user["myEvents"]:
        if not event_id in user["myCollaborations"]:
            return False
    return True
