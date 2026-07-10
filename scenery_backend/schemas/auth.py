from pydantic import BaseModel, Field


class RegisterForm(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    phone: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6, max_length=30)
    confirm_password: str = Field(..., min_length=6, max_length=30)


class LoginForm(BaseModel):
    account: str = Field(..., min_length=2, max_length=30)
    password: str = Field(..., min_length=1, max_length=30)
