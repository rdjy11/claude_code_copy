import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class SC(Base, TimestampMixin):
    """System Component - 系统组件"""
    __tablename__ = "scs"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)
    function_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("functions.id"), nullable=True)

    sscs: Mapped[list["SSC"]] = relationship("SSC", back_populates="sc", cascade="all, delete-orphan")
    tag = relationship("Tag")
    function = relationship("Function", back_populates="scs")


class SSC(Base, TimestampMixin):
    """Sub-System Component - 子系统组件"""
    __tablename__ = "sscs"

    sc_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scs.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)

    sc = relationship("SC", back_populates="sscs")
    tag = relationship("Tag")
    versions: Mapped[list["SSCVersion"]] = relationship("SSCVersion", back_populates="ssc", cascade="all, delete-orphan")
    signals: Mapped[list["Signal"]] = relationship("Signal", back_populates="ssc")


class SSCVersion(Base, TimestampMixin):
    """SSC branch version - SSC 分支版本"""
    __tablename__ = "ssc_versions"

    ssc_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sscs.id"), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    branch_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parent_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ssc_versions.id"), nullable=True)
    tag_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=True)
    conflict_source: Mapped[str | None] = mapped_column(String(255), nullable=True)

    ssc = relationship("SSC", back_populates="versions")
    parent_version = relationship("SSCVersion", remote_side="SSCVersion.id")
    tag = relationship("Tag")
