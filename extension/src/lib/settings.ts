export type TimeRange = "3_months" | "6_months" | "1_year" | "all_time";

export interface Settings {
  timeRange: TimeRange;
  apiUrl: string;
}

const DEFAULT_SETTINGS: Settings = {
  timeRange: "1_year",
  apiUrl: "http://localhost:8000",
};

export async function getSettings(): Promise<Settings> {
  const result = await chrome.storage.sync.get(DEFAULT_SETTINGS);
  return result as Settings;
}

export async function saveSettings(settings: Settings): Promise<void> {
  await chrome.storage.sync.set(settings);
}

export function getTimeRangeMs(timeRange: TimeRange): number {
  const now = Date.now();
  switch (timeRange) {
    case "3_months":
      return 90 * 24 * 60 * 60 * 1000;
    case "6_months":
      return 180 * 24 * 60 * 60 * 1000;
    case "1_year":
      return 365 * 24 * 60 * 60 * 1000;
    case "all_time":
      return now;
  }
}
