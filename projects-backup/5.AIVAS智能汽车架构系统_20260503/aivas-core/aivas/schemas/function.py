import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class FunctionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    parent_func_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None
    requirement_id: uuid.UUID | None = None


class FunctionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    tag_id: uuid.UUID | None = None
    requirement_id: uuid.UUID | None = None


class FunctionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    description: str | None
    parent_func_id: uuid.UUID | None
    tag_id: uuid.UUID | None
    requirement_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
