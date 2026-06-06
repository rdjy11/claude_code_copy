import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ECUCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: str = "generic"
    description: str | None = None
    parent_ecu_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None


class ECUUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    description: str | None = None
    tag_id: uuid.UUID | None = None


class ECUResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    type: str
    description: str | None
    parent_ecu_id: uuid.UUID | None
    tag_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
