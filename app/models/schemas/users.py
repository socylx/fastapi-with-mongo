from pydantic import EmailStr

from app.core import security
from app.models.common import IDModelMixin
from app.models.domain.rwmodel import DateTimeRWModel, BaseRWModel


class User(BaseRWModel):
    username: str
    email: str


class UserInLogin(BaseRWModel):
    email: EmailStr
    password: str


class UserInCreate(DateTimeRWModel, UserInLogin):
    username: str
    salt: str = ""

    def change_password(self) -> None:
        self.salt = security.generate_salt()
        self.password = security.get_password_hash(self.salt + self.password)


class UserInDB(IDModelMixin, DateTimeRWModel, User):
    salt: str = ""
    password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.password)


class UserWithToken(DateTimeRWModel, User):
    token: str


class UserInResponse(BaseRWModel):
    user: UserWithToken
