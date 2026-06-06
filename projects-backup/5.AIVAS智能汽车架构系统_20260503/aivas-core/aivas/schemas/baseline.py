import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class BaselineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    tag_id: uuid.UUID | None = None


class BaselineUpdate(BaseModel):
    name: str | None = None
    status: str | None = None


class BaselineResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    tag_id: uuid.UUID | None
    status: str
    locked_at: datetime | None
    created_at: datetime
    updated_at: datetime


class BaselineItemCreate(BaseModel):
    item_type: str = Field(min_length=1, max_length=50)
    item_id: uuid.UUID
    version: str | None = None


class BaselineItemResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    baseline_id: uuid.UUID
    item_type: str
    item_id: uuid.UUID
    version: str | None
    created_at: datetime
    updated_at: datetime
