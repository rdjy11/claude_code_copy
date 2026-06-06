import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SignalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    direction: str = Field(min_length=1, max_length=20)
    feature_tag: str | None = None


class SignalUpdate(BaseModel):
    name: str | None = None
    direction: str | None = None
    feature_tag: str | None = None


class SignalResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    direction: str
    feature_tag: str | None
    ssc_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class SignalECUAllocationCreate(BaseModel):
    ecu_id: uuid.UUID
    condition: str | None = None


class SignalECUAllocationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    signal_id: uuid.UUID
    ecu_id: uuid.UUID
    condition: str | None
    created_at: datetime
    updated_at: datetime
