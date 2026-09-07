from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Unit(Base):
    """A thematic grouping of Skills within a Course (e.g. 'Basics')."""

    __tablename__ = "units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    course: Mapped["Course"] = relationship("Course", back_populates="units")
    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        back_populates="unit",
        cascade="all, delete-orphan",
        order_by="Skill.order_index",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Unit id={self.id} title={self.title!r}>"
