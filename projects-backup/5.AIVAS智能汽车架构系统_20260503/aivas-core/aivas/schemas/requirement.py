import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RequirementCreate(BaseModel):
    type: str = Field(min_length=1, max_length=50)
    content: str
    tag_id: uuid.UUID | None = None
    parent_req_id: uuid.UUID | None = None


class RequirementUpdate(BaseModel):
    type: str | None = None
    content: str | None = None
    tag_id: uuid.UUID | None = None


class RequirementResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    type: str
    content: str
    tag_id: uuid.UUID | None
    version: int
    parent_req_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
