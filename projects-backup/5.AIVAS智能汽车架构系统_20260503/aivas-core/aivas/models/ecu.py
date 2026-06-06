import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class ECU(Base, TimestampMixin):
    """Electronic Control Unit"""
    __tablename__ = "ecus"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="generic")  # generic / variant
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_ecu_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ecus.id"), nullable=True)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)

    parent = relationship("ECU", remote_side="ECU.id", back_populates="children")
    children: Mapped[list["ECU"]] = relationship("ECU", back_populates="parent")
    tag = relationship("Tag")
    signal_allocations: Mapped[list["SignalECUAllocation"]] = relationship("SignalECUAllocation", back_populates="ecu")
