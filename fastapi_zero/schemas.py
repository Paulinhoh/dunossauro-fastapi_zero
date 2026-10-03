from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):  # model
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):  # dto
    id: int
    username: str
    email: EmailStr


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):  # reponse: read_users
    users: list[UserPublic]
