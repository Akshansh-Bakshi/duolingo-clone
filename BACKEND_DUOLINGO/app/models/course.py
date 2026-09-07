from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Course(Base):
    """A language course, e.g. English -> Spanish. Contains many Units."""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_language: Mapped[str] = mapped_column(String(50), nullable=False)
    target_language: Mapped[str] = mapped_column(String(50), nullable=False)

    units: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Unit.order_index",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Course id={self.id} name={self.name!r}>"
