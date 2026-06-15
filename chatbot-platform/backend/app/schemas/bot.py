import uuid

from pydantic import BaseModel, ConfigDict


class BotCreate(BaseModel):
    name: str
    description: str | None = None


class BotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    is_active: bool
    organization_id: uuid.UUID
