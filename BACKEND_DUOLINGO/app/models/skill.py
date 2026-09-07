from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Skill(Base):
    """
    A skill within a Unit (e.g. 'Greetings'), made up of several Lessons.

    `required_skill_id` is a self-referential FK used purely to drive
    lock/unlock progression: a skill is LOCKED until its required skill is
    completed. A null value means the skill has no prerequisite (it is
    unlocked from the start, e.g. the first skill in the course).
    """

    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    required_skill_id: Mapped[int | None] = mapped_column(
        ForeignKey("skills.id"), nullable=True
    )

    unit: Mapped["Unit"] = relationship("Unit", back_populates="skills")
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="skill",
        cascade="all, delete-orphan",
        order_by="Lesson.order_index",
    )

    # Self-referential relationship: the skill that must be completed
    # before this one unlocks.
    required_skill: Mapped["Skill | None"] = relationship(
        "Skill", remote_side=[id], foreign_keys=[required_skill_id]
    )

    progress_entries: Mapped[list["UserSkillProgress"]] = relationship(
        "UserSkillProgress", back_populates="skill", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Skill id={self.id} title={self.title!r}>"
