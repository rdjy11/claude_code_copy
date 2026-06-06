import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class Baseline(Base, TimestampMixin):
    __tablename__ = "baselines"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")  # draft/locked/released
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="baselines")
    tag = relationship("Tag")
    items: Mapped[list["BaselineItem"]] = relationship("BaselineItem", back_populates="baseline", cascade="all, delete-orphan")


class BaselineItem(Base, TimestampMixin):
    __tablename__ = "baseline_items"

    baseline_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("baselines.id"), nullable=False)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)  # requirement/function/sc/ssc/ecu/signal
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    baseline = relationship("Baseline", back_populates="items")
