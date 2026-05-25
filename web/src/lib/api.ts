import type { Insights } from "@chrome-wrapped/shared";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getInsights(runId: string): Promise<Insights> {
  const response = await fetch(`${API_BASE}/runs/${runId}/insights`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch insights: ${response.status}`);
  }

  return response.json();
}
