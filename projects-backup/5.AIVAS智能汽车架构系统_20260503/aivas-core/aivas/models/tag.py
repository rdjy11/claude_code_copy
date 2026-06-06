import uuid

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1=L1, 2=L2, 3=L3
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    parent_tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)

    project = relationship("Project", back_populates="tags")
    parent = relationship("Tag", remote_side="Tag.id", back_populates="children")
    children: Mapped[list["Tag"]] = relationship("Tag", back_populates="parent", cascade="all, delete-orphan")
