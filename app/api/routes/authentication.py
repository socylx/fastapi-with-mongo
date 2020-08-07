from fastapi import APIRouter, Depends, HTTPException, Body
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.create import get_create
from app.api.dependencies.database import get_repository
from app.core import jwt
from app.core.config import SECRET_KEY
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInCreate, UserInResponse, UserWithToken, UserInLogin, User, UserInDB
from app.resources import strings
from app.services.users import check_username_is_taken, check_email_is_taken

router = APIRouter()


@router.post("", status_code=HTTP_201_CREATED, name="auth:register")
async def register(
        user_create: UserInCreate = Depends(get_create(UserInCreate, alias="user")),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserInResponse:
    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN
        )

    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN
        )

    user = await users_repo.create(CREATE_MODEL=UserInCreate, RETURN_MODEL=UserInDB)(user_create)

    token = jwt.create_access_token_for_user(user, str(SECRET_KEY))

    return UserInResponse(user=UserWithToken(token=token, **user.dict()))


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
        user_login: UserInLogin = Body(..., embed=True, alias="user"),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT
    )

    try:
        user = await users_repo.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = jwt.create_access_token_for_user(user, str(SECRET_KEY))

    return UserInResponse(user=UserWithToken(token=token, **user.dict()))


@router.get("", response_model=UserInResponse, name="users:get-current-user")
async def retrieve_current_user(
        user: User = Depends(get_current_user_authorizer())
) -> UserInResponse:
    token = jwt.create_access_token_for_user(user, str(SECRET_KEY))

    return UserInResponse(user=UserWithToken(token=token, **user.dict()))
