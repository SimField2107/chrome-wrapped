/**
 * A single visit to a URL, as extracted from chrome.history
 */
export interface VisitRecord {
  timestamp: number;
  transition: string;
}

/**
 * A history item with all its visits, sent from extension to backend
 */
export interface HistoryItem {
  url: string;
  title: string;
  visitCount: number;
  visits: VisitRecord[];
}

/**
 * Request body for creating a new Wrapped run
 */
export interface CreateRunRequest {
  history: HistoryItem[];
  timezone: string;
  rangeStart: string;
  rangeEnd: string;
}

/**
 * Response from creating a new Wrapped run
 */
export interface CreateRunResponse {
  runId: string;
}

/**
 * Metadata about the Wrapped run
 */
export interface InsightsMeta {
  runId: string;
  generatedAt: string;
  rangeStart: string;
  rangeEnd: string;
  timezone: string;
}

/**
 * Total counts for the wrapped period
 */
export interface InsightsTotals {
  pageviews: number;
  uniqueDomains: number;
  activeDays: number;
}

/**
 * A top site entry
 */
export interface TopSite {
  domain: string;
  title: string;
  visits: number;
  favicon: string;
}

/**
 * A category with visit stats
 */
export interface TopCategory {
  category: string;
  visits: number;
  percentage: number;
}

/**
 * Hourly visit distribution
 */
export interface HourlyVisits {
  hour: number;
  visits: number;
}

/**
 * Day of week visit distribution
 */
export interface DayOfWeekVisits {
  dayOfWeek: number;
  visits: number;
}

/**
 * Heatmap data point
 */
export interface HeatmapDay {
  date: string;
  visits: number;
}

/**
 * Monthly top sites ranking
 */
export interface MonthlyRanking {
  month: string;
  ranking: string[];
}

/**
 * A standout day with optional narrative
 */
export interface StandoutDay {
  date: string;
  visits: number;
  topDomain: string;
  narrative?: string;
}

/**
 * Streak information
 */
export interface Streaks {
  longestOnStreak: number;
  longestOffStreak: number;
}

/**
 * Browser Club assignment
 */
export type BrowserClub =
  | "rabbit_hole_researcher"
  | "doomscroller"
  | "hustle_tab_hoarder"
  | "comfort_rewatcher"
  | "niche_forum_lurker"
  | "casual_surfer";

/**
 * Role within a Browser Club
 */
export type BrowserRole = "archivist" | "explorer" | "loyalist" | "multitasker" | "lurker";

/**
 * Personality assignment
 */
export interface Personality {
  club: BrowserClub;
  role: BrowserRole;
  blurb: string;
}

/**
 * Session information
 */
export interface SessionInfo {
  longestSessionMinutes: number;
  longestSessionDomain: string;
  longestSessionDate: string;
}

/**
 * New vs returning domains stats
 */
export interface DomainDiscovery {
  newDomains: number;
  returningDomains: number;
  topNewDomain: string;
  topRideOrDie: string;
}

/**
 * Time personality badge
 */
export type TimeBadge = "night_owl" | "early_bird" | "all_day_surfer";

/**
 * Category evolution over months
 */
export interface CategoryEvolution {
  month: string;
  categories: Record<string, number>;
}

/**
 * Full insights payload returned by the backend
 */
export interface Insights {
  meta: InsightsMeta;
  totals: InsightsTotals;
  topSites: TopSite[];
  topCategories: TopCategory[];
  timeOfDay: HourlyVisits[];
  dayOfWeek: DayOfWeekVisits[];
  heatmap: HeatmapDay[];
  monthlyTopSites: MonthlyRanking[];
  standoutDays: StandoutDay[];
  streaks: Streaks;
  personality: Personality;
  session: SessionInfo;
  domainDiscovery: DomainDiscovery;
  peakHour: number;
  timeBadge: TimeBadge;
  guiltyPleasureCategory: string;
  mostChronicallyOnlineDay: StandoutDay;
}

/**
 * Categories for website classification
 */
export type WebsiteCategory =
  | "social"
  | "work"
  | "entertainment"
  | "news"
  | "shopping"
  | "learning"
  | "development"
  | "communication"
  | "finance"
  | "health"
  | "travel"
  | "food"
  | "gaming"
  | "adult"
  | "other";

/**
 * API error response
 */
export interface ApiError {
  detail: string;
}
