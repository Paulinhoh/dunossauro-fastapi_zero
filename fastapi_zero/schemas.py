from pydantic import BaseModel, ConfigDict, EmailStr


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

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):  # reponse: read_users
    users: list[UserPublic]
