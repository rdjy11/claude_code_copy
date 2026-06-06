import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class Requirement(Base, TimestampMixin):
    __tablename__ = "requirements"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # market/functional/system/regulation/safety/security
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)
    version: Mapped[int] = mapped_column(default=1)
    parent_req_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("requirements.id"), nullable=True)

    project = relationship("Project", back_populates="requirements")
    tag = relationship("Tag")
    parent = relationship("Requirement", remote_side="Requirement.id", back_populates="children")
    children: Mapped[list["Requirement"]] = relationship("Requirement", back_populates="parent")
    functions: Mapped[list["Function"]] = relationship("Function", back_populates="requirement")
