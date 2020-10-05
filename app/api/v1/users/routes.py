"""
Users - Routes.
"""

from fastapi import APIRouter, Response, Body, Depends, BackgroundTasks

from config import settings
from db import CRUD, IntegrityError
from mails import send_welcome_email, send_recovery_password_email
from utils import responses, exceptions
from auth import (
    get_auth_user,
    create_access_token,
    verify_password,
    get_from_token,
    hash_password,
)

from .schemas import User, UserIn, UserLogin
from .models import UsersModel


router = APIRouter()
users_crud = CRUD(UsersModel, User)


##########
# SIGNUP #
##########
@router.post(
    "/signup",
    status_code=201,
    responses={
        "201": {"model": User},
        "409": {"model": responses.Conflict},
        "500": {"model": responses.ServerError},
    },
)
async def register_a_new_user(
    user_info: UserIn, response: Response, background_task: BackgroundTasks
) -> User:
    """
    Register a new user and set the session cookie.
    """
    try:
        user = await users_crud.create(user_info.dict())
    except IntegrityError:
        exceptions.conflict_409("Email already exists")

    response.set_cookie(
        key=settings.COOKIE_SESSION_NAME,
        value=create_access_token(user.email),
        max_age=settings.COOKIE_SESSION_AGE,
        # If debug mode, not secure.
        secure=not settings.DEBUG_MODE,
        httponly=not settings.DEBUG_MODE,
    )

    background_task.add_task(send_welcome_email, username=user.name, email=user.email)
    return user


#########
# LOGIN #
#########
@router.post(
    "/login",
    status_code=200,
    responses={
        "200": {"model": User},
        "401": {"model": responses.Unauthorized},
        "500": {"model": responses.ServerError},
    },
)
async def login_and_set_cookie_session(
    creadentials: UserLogin, response: Response
) -> User:
    """
    Verify the user credentials and set the cookie session.
    """
    user = users_crud.read_one({"email": creadentials.email})

    if not user or not verify_password(creadentials.password, user.password):
        exceptions.unauthorized_401("Invalid credentials")

    response.set_cookie(
        key=settings.COOKIE_SESSION_NAME,
        value=create_access_token(user.email),
        max_age=settings.COOKIE_SESSION_AGE,
        # If debug mode, not secure.
        secure=not settings.DEBUG_MODE,
        httponly=not settings.DEBUG_MODE,
    )
    return user


#####################
# RECOVERY PASSWORD #
#####################
@router.post(
    "/recovery-password/{email}",
    status_code=200,
    responses={
        "200": {"model": responses.EmailMsg},
        "404": {"model": responses.NotFound},
        "500": {"model": responses.ServerError},
    },
)
async def send_recovery_password_email(email: str) -> responses.EmailMsg:
    """
    Check if the email is valid and then
    send a email for create a new password.
    """
    user = await users_crud.read_one({"email": email})
    if not user:
        exceptions.not_fount_404("Email not found")

    token = create_access_token(email, for_recovery_password=True)
    send_welcome_email(email=email, token=token)
    return responses.EmailMsg()


##################
# RESET PASSWORD #
##################
@router.post(
    "/reset-password",
    status_code=200,
    responses={
        "200": {"model": responses.Msg},
        "400": {"model": responses.BadRequest},
        "401": {"model": responses.Unauthorized},
        "500": {"model": responses.ServerError},
    },
)
async def reset_password(
    token: str = Body(...), new_password: str = Body(...)
) -> responses.Msg:
    """
    Verify the token and reset password if all correct.
    """
    email = get_from_token(token)
    user = await users_crud.read_one({"email": email})

    if not user:
        exceptions.bad_request_400("Invalid token")

    hashed_password = hash_password(new_password)
    await users_crud.update(user.id, {"password": hashed_password})
    return responses.Msg()


################
# CURRENT USER #
################
@router.get(
    "/current",
    status_code=200,
    responses={
        "200": {"model": User},
        "401": {"model": responses.Unauthorized},
        "500": {"model": responses.ServerError},
    },
)
async def get_current_user(user: User = Depends(get_auth_user)) -> User:
    """
    Retrieve the info of the logen current user.
    """
    return user


###############
# UPDATE USER #
###############
@router.put(
    "/{user_id}",
    status_code=200,
    responses={
        "200": {"model": User},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "500": {"model": responses.ServerError},
    },
)
async def update_a_existing_user(
    user_id: str, user_info: UserIn, current_user=Depends(get_auth_user)
) -> User:
    """
    Update a existing user if the session is valid.
    """
    if current_user.id != user_id:
        exceptions.forbidden_403("Forbidden")

    user = await users_crud.update(user_id, user_info.dict())
    return user


###############
# DELETE USER #
###############
@router.delete(
    "/{user_id}",
    status_code=200,
    responses={
        "200": {"model": User},
        "401": {"model": responses.Unauthorized},
        "403": {"model": responses.Forbidden},
        "500": {"model": responses.ServerError},
    },
)
async def delete_a_existing_user(user_id: str, user=Depends(get_current_user)) -> User:
    """
    Delete a existing user
    """
    if current_user.id != user_id:
        exceptions.forbidden_403("Forbidden")

    user = await users_crud.delete(user_id)
    return user
