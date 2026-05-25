import type { HistoryItem, VisitRecord } from "@chrome-wrapped/shared";
import { getSettings, getTimeRangeMs } from "./settings";

const MAX_RESULTS = 100000;

export async function fetchHistory(): Promise<HistoryItem[]> {
  const settings = await getSettings();
  const rangeMs = getTimeRangeMs(settings.timeRange);
  const startTime = Date.now() - rangeMs;

  const items = await chrome.history.search({
    text: "",
    startTime,
    maxResults: MAX_RESULTS,
  });

  const historyItems: HistoryItem[] = [];

  for (const item of items) {
    if (!item.url) continue;

    const visits = await chrome.history.getVisits({ url: item.url });

    const visitRecords: VisitRecord[] = visits
      .filter((v) => v.visitTime && v.visitTime >= startTime)
      .map((v) => ({
        timestamp: v.visitTime!,
        transition: v.transition || "link",
      }));

    if (visitRecords.length > 0) {
      historyItems.push({
        url: item.url,
        title: item.title || "",
        visitCount: item.visitCount || visitRecords.length,
        visits: visitRecords,
      });
    }
  }

  return historyItems;
}
