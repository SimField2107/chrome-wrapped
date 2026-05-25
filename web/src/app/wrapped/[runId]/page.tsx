import { Suspense } from "react";
import { StoryPlayer } from "@/components/story/StoryPlayer";
import { getInsights } from "@/lib/api";
import { LoadingScreen } from "@/components/LoadingScreen";
import { ErrorScreen } from "@/components/ErrorScreen";
import { EmptyScreen } from "@/components/EmptyScreen";

interface WrappedPageProps {
  params: Promise<{ runId: string }>;
}

async function WrappedContent({ runId }: { runId: string }) {
  try {
    const insights = await getInsights(runId);

    if (insights.totals.pageviews === 0) {
      return <EmptyScreen />;
    }

    return <StoryPlayer insights={insights} />;
  } catch (error) {
    console.error("Failed to fetch insights:", error);
    return <ErrorScreen runId={runId} />;
  }
}

export default async function WrappedPage({ params }: WrappedPageProps) {
  const { runId } = await params;

  return (
    <Suspense fallback={<LoadingScreen />}>
      <WrappedContent runId={runId} />
    </Suspense>
  );
}
