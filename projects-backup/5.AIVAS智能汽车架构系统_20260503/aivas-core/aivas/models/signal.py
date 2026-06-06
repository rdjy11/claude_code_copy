import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from aivas.models.base import Base, TimestampMixin


class Signal(Base, TimestampMixin):
    __tablename__ = "signals"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[str] = mapped_column(String(20), nullable=False)  # input / output / bidirectional
    feature_tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ssc_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sscs.id"), nullable=False)

    ssc = relationship("SSC", back_populates="signals")
    ecu_allocations: Mapped[list["SignalECUAllocation"]] = relationship("SignalECUAllocation", back_populates="signal")


class SignalECUAllocation(Base, TimestampMixin):
    __tablename__ = "signal_ecu_allocations"

    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("signals.id"), nullable=False)
    ecu_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ecus.id"), nullable=False)
    condition: Mapped[str | None] = mapped_column(String(500), nullable=True)

    signal = relationship("Signal", back_populates="ecu_allocations")
    ecu = relationship("ECU", back_populates="signal_allocations")
