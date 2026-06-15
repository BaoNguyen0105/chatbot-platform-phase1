import uuid

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import UserRole


class OrganizationCreate(BaseModel):
    name: str
    slug: str


class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    # Either join an existing org by id, or create a new one
    organization_name: str
    organization_slug: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    full_name: str | None
    role: UserRole
    organization_id: uuid.UUID
    is_active: bool


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str
