from pydantic import BaseModel


class UserStatusForm(BaseModel):
    status: str


class UserRoleForm(BaseModel):
    role: str
