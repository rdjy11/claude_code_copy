from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aivas.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="project", cascade="all, delete-orphan")
    requirements: Mapped[list["Requirement"]] = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")
    baselines: Mapped[list["Baseline"]] = relationship("Baseline", back_populates="project", cascade="all, delete-orphan")
