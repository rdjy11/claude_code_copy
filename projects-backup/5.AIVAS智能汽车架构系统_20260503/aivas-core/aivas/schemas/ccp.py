import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CCPCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    value_type: str = Field(min_length=1, max_length=50)
    ssc_id: uuid.UUID


class CCPUpdate(BaseModel):
    name: str | None = None
    value_type: str | None = None


class CCPResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    value_type: str
    ssc_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
