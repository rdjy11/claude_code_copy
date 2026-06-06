import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class Function(Base, TimestampMixin):
    __tablename__ = "functions"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_func_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("functions.id"), nullable=True)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)
    requirement_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("requirements.id"), nullable=True)

    parent = relationship("Function", remote_side="Function.id", back_populates="children")
    children: Mapped[list["Function"]] = relationship("Function", back_populates="parent")
    tag = relationship("Tag")
    requirement = relationship("Requirement", back_populates="functions")
    scs: Mapped[list["SC"]] = relationship("SC", back_populates="function")
