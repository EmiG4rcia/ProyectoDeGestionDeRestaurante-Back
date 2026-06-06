from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class SalesVerifyRequest(BaseModel):
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class ChangeSalesPasswordRequest(BaseModel):
    current_password: str
    new_sales_password: str


class RecoverPasswordRequest(BaseModel):
    recovery_code: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SalesTokenResponse(BaseModel):
    sales_token: str
    token_type: str = "bearer"
    expires_in_minutes: int = 15


class AdminResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True