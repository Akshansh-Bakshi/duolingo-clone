"use client";

import type { PathSkill, PathUnit } from "@/lib/types";
import SkillNode from "./SkillNode";
import styles from "./UnitSection.module.css";

// Horizontal stagger pattern to create Duolingo's signature zig-zag trail.
const OFFSET_PATTERN = [0, 60, 0, -60];

interface Props {
  unit: PathUnit;
  startIndexOffset: number;
  nextUpSkillId: number | null;
}

export default function UnitSection({
  unit,
  startIndexOffset,
  nextUpSkillId,
}: Props) {
  const sortedSkills = [...unit.skills].sort(
    (a: PathSkill, b: PathSkill) => a.order_index - b.order_index
  );

  return (
    <section className={styles.unit}>
      <div className={styles.banner}>
        <div>
          <div className={styles.bannerTitle}>{unit.title}</div>
          <div className={styles.bannerDesc}>{unit.description}</div>
        </div>
      </div>

      <div className={styles.trail}>
        {sortedSkills.map((skill, idx) => (
          <SkillNode
            key={skill.id}
            skill={skill}
            offset={OFFSET_PATTERN[(startIndexOffset + idx) % OFFSET_PATTERN.length]}
            isNextUp={skill.id === nextUpSkillId}
          />
        ))}
      </div>
    </section>
  );
}
