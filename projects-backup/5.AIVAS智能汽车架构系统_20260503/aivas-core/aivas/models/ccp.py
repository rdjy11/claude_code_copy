import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class CCP(Base, TimestampMixin):
    """Calibration / Configuration Parameter"""
    __tablename__ = "ccps"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value_type: Mapped[str] = mapped_column(String(50), nullable=False)  # scalar / curve / map
    ssc_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sscs.id"), nullable=False)

    ssc = relationship("SSC")
