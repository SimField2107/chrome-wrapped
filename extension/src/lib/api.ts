import type { CreateRunRequest, CreateRunResponse, Insights } from "@chrome-wrapped/shared";
import { getSettings } from "./settings";

export async function createRun(request: CreateRunRequest): Promise<CreateRunResponse> {
  const settings = await getSettings();
  
  let response: Response;
  try {
    response = await fetch(`${settings.apiUrl}/runs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch (fetchError) {
    throw new Error(`Network error: Could not connect to ${settings.apiUrl}. Is the backend running?`);
  }

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({ detail: "Server error" }));
    let errorMessage = `HTTP ${response.status}`;
    if (typeof errorBody.detail === "string") {
      errorMessage = errorBody.detail;
    } else if (Array.isArray(errorBody.detail)) {
      errorMessage = errorBody.detail.map((e: any) => e.msg || JSON.stringify(e)).join("; ");
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

export async function getInsights(runId: string): Promise<Insights> {
  const settings = await getSettings();
  const response = await fetch(`${settings.apiUrl}/runs/${runId}/insights`);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}
