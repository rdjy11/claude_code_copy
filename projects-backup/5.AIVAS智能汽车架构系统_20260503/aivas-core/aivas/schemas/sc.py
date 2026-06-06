import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SCCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: str | None = None
    description: str | None = None
    tag_id: uuid.UUID | None = None
    function_id: uuid.UUID | None = None


class SCUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    description: str | None = None
    tag_id: uuid.UUID | None = None
    function_id: uuid.UUID | None = None


class SCResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    type: str | None
    description: str | None
    tag_id: uuid.UUID | None
    function_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class SSCCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    tag_id: uuid.UUID | None = None


class SSCUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    tag_id: uuid.UUID | None = None


class SSCResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    sc_id: uuid.UUID
    name: str
    description: str | None
    tag_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class SSCVersionCreate(BaseModel):
    version: str = Field(min_length=1, max_length=50)
    branch_name: str | None = None
    parent_version_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None
    conflict_source: str | None = None


class SSCVersionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    ssc_id: uuid.UUID
    version: str
    branch_name: str | None
    parent_version_id: uuid.UUID | None
    tag_id: uuid.UUID | None
    conflict_source: str | None
    created_at: datetime
    updated_at: datetime
