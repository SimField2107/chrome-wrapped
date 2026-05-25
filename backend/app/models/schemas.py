from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class VisitRecord(BaseModel):
    timestamp: float
    transition: str

    @field_validator("timestamp", mode="before")
    @classmethod
    def coerce_timestamp(cls, v):
        return float(v) if v is not None else 0.0


class HistoryItem(BaseModel):
    url: str
    title: str = ""
    visit_count: int = Field(default=0, alias="visitCount")
    visits: list[VisitRecord]

    model_config = {"populate_by_name": True}

    @field_validator("title", mode="before")
    @classmethod
    def coerce_title(cls, v):
        return v if v is not None else ""


class CreateRunRequest(BaseModel):
    history: list[HistoryItem]
    timezone: str
    range_start: str = Field(alias="rangeStart")
    range_end: str = Field(alias="rangeEnd")

    model_config = {"populate_by_name": True}


class CreateRunResponse(BaseModel):
    run_id: str = Field(alias="runId")

    model_config = {"populate_by_name": True, "by_alias": True}


class InsightsMeta(BaseModel):
    run_id: str = Field(alias="runId")
    generated_at: str = Field(alias="generatedAt")
    range_start: str = Field(alias="rangeStart")
    range_end: str = Field(alias="rangeEnd")
    timezone: str

    model_config = {"populate_by_name": True, "by_alias": True}


class InsightsTotals(BaseModel):
    pageviews: int
    unique_domains: int = Field(alias="uniqueDomains")
    active_days: int = Field(alias="activeDays")

    model_config = {"populate_by_name": True, "by_alias": True}


class TopSite(BaseModel):
    domain: str
    title: str
    visits: int
    favicon: str


class TopCategory(BaseModel):
    category: str
    visits: int
    percentage: float


class HourlyVisits(BaseModel):
    hour: int
    visits: int


class DayOfWeekVisits(BaseModel):
    day_of_week: int = Field(alias="dayOfWeek")
    visits: int

    model_config = {"populate_by_name": True, "by_alias": True}


class HeatmapDay(BaseModel):
    date: str
    visits: int


class MonthlyRanking(BaseModel):
    month: str
    ranking: list[str]


class StandoutDay(BaseModel):
    date: str
    visits: int
    top_domain: str = Field(alias="topDomain")
    narrative: str | None = None

    model_config = {"populate_by_name": True, "by_alias": True}


class Streaks(BaseModel):
    longest_on_streak: int = Field(alias="longestOnStreak")
    longest_off_streak: int = Field(alias="longestOffStreak")

    model_config = {"populate_by_name": True, "by_alias": True}


BrowserClub = Literal[
    "rabbit_hole_researcher",
    "doomscroller",
    "hustle_tab_hoarder",
    "comfort_rewatcher",
    "niche_forum_lurker",
    "casual_surfer",
]

BrowserRole = Literal["archivist", "explorer", "loyalist", "multitasker", "lurker"]


class Personality(BaseModel):
    club: BrowserClub
    role: BrowserRole
    blurb: str


class SessionInfo(BaseModel):
    longest_session_minutes: int = Field(alias="longestSessionMinutes")
    longest_session_domain: str = Field(alias="longestSessionDomain")
    longest_session_date: str = Field(alias="longestSessionDate")

    model_config = {"populate_by_name": True, "by_alias": True}


class DomainDiscovery(BaseModel):
    new_domains: int = Field(alias="newDomains")
    returning_domains: int = Field(alias="returningDomains")
    top_new_domain: str = Field(alias="topNewDomain")
    top_ride_or_die: str = Field(alias="topRideOrDie")

    model_config = {"populate_by_name": True, "by_alias": True}


TimeBadge = Literal["night_owl", "early_bird", "all_day_surfer"]


class CategoryEvolution(BaseModel):
    month: str
    categories: dict[str, int]


class Insights(BaseModel):
    meta: InsightsMeta
    totals: InsightsTotals
    top_sites: list[TopSite] = Field(alias="topSites")
    top_categories: list[TopCategory] = Field(alias="topCategories")
    time_of_day: list[HourlyVisits] = Field(alias="timeOfDay")
    day_of_week: list[DayOfWeekVisits] = Field(alias="dayOfWeek")
    heatmap: list[HeatmapDay]
    monthly_top_sites: list[MonthlyRanking] = Field(alias="monthlyTopSites")
    standout_days: list[StandoutDay] = Field(alias="standoutDays")
    streaks: Streaks
    personality: Personality
    session: SessionInfo
    domain_discovery: DomainDiscovery = Field(alias="domainDiscovery")
    peak_hour: int = Field(alias="peakHour")
    time_badge: TimeBadge = Field(alias="timeBadge")
    guilty_pleasure_category: str = Field(alias="guiltyPleasureCategory")
    most_chronically_online_day: StandoutDay = Field(alias="mostChronicallyOnlineDay")

    model_config = {"populate_by_name": True, "by_alias": True}


WebsiteCategory = Literal[
    "social",
    "work",
    "entertainment",
    "news",
    "shopping",
    "learning",
    "development",
    "communication",
    "finance",
    "health",
    "travel",
    "food",
    "gaming",
    "adult",
    "other",
]
