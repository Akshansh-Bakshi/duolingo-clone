import LessonPlayer from "@/components/lesson/LessonPlayer";
import { ErrorState } from "@/components/common/StateViews";

export default function LessonPage({
  params,
}: {
  params: { lessonId: string };
}) {
  const lessonId = Number(params.lessonId);

  if (!Number.isFinite(lessonId) || lessonId <= 0) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center" }}>
        <ErrorState
          title="Invalid lesson"
          message={`"${params.lessonId}" isn't a valid lesson id.`}
        />
      </div>
    );
  }

  return <LessonPlayer lessonId={lessonId} />;
}
