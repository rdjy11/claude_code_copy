import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    level: int = Field(ge=1, le=3)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    parent_tag_id: uuid.UUID | None = None


class TagUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    parent_tag_id: uuid.UUID | None = None


class TagResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    level: int
    name: str
    description: str | None
    parent_tag_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class TagTree(TagResponse):
    children: list["TagTree"] = []
