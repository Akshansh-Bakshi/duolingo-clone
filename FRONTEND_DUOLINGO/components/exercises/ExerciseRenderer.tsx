"use client";

import type { ExerciseComponentProps } from "./types";
import MultipleChoice from "./MultipleChoice";
import Translate from "./Translate";
import WordBank from "./WordBank";
import MatchPairs from "./MatchPairs";
import FillBlank from "./FillBlank";
import TypeAnswer from "./TypeAnswer";

/**
 * Selects the correct exercise UI component based on `exercise.type`.
 * All six types documented in FRONTEND_API_CONTRACT.md / FINAL_HANDOFF.md
 * are covered. Render with `key={exercise.id}` from the caller so each
 * exercise mounts fresh (important for WordBank/MatchPairs' local state).
 */
export default function ExerciseRenderer(props: ExerciseComponentProps) {
  switch (props.exercise.type) {
    case "multiple_choice":
      return <MultipleChoice {...props} />;
    case "translate":
      return <Translate {...props} />;
    case "word_bank":
      return <WordBank {...props} />;
    case "match":
      return <MatchPairs {...props} />;
    case "fill_blank":
      return <FillBlank {...props} />;
    case "type_answer":
      return <TypeAnswer {...props} />;
    default:
      return (
        <p style={{ color: "var(--color-red)" }}>
          Unsupported exercise type: {props.exercise.type}
        </p>
      );
  }
}
