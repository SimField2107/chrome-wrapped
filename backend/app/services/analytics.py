"""
Analytics service - computes all insights from browsing history.
"""

from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any

import tldextract

from app.models.schemas import (
    DayOfWeekVisits,
    DomainDiscovery,
    HeatmapDay,
    HourlyVisits,
    Insights,
    InsightsMeta,
    InsightsTotals,
    MonthlyRanking,
    Personality,
    SessionInfo,
    StandoutDay,
    Streaks,
    TopCategory,
    TopSite,
)
from app.services.categorizer import categorize_url
from app.services.personality import compute_personality


def _extract_domain(url: str) -> str:
    """Extract registrable domain from URL."""
    extracted = tldextract.extract(url)
    if extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}".lower()
    return extracted.domain.lower()


def _timestamp_to_datetime(ts: float | int) -> datetime:
    """Convert millisecond timestamp to datetime."""
    return datetime.fromtimestamp(ts / 1000, tz=UTC)


def _compute_totals(
    history: list[dict[str, Any]],
    all_visits: list[tuple[datetime, str, str]],
) -> InsightsTotals:
    """Compute total pageviews, unique domains, and active days."""
    domains = set()
    active_dates = set()

    for url, title, visit_count, visits in _iter_history(history):
        domain = _extract_domain(url)
        domains.add(domain)
        for ts, _ in visits:
            dt = _timestamp_to_datetime(ts)
            active_dates.add(dt.date())

    return InsightsTotals(
        pageviews=len(all_visits),
        unique_domains=len(domains),
        active_days=len(active_dates),
    )


def _iter_history(history: list[dict[str, Any]]):
    """Iterator over history items, yielding (url, title, visit_count, visits)."""
    for item in history:
        url = item.get("url", "")
        title = item.get("title", "")
        visit_count = item.get("visit_count", item.get("visitCount", 0))
        visits = [
            (v.get("timestamp", 0), v.get("transition", "link"))
            for v in item.get("visits", [])
        ]
        yield url, title, visit_count, visits


def _get_all_visits(history: list[dict[str, Any]]) -> list[tuple[datetime, str, str]]:
    """Get all visits as (datetime, domain, url) tuples."""
    visits = []
    for url, title, _, item_visits in _iter_history(history):
        domain = _extract_domain(url)
        for ts, _ in item_visits:
            dt = _timestamp_to_datetime(ts)
            visits.append((dt, domain, url))
    return sorted(visits, key=lambda x: x[0])


def _compute_top_sites(
    history: list[dict[str, Any]],
    limit: int = 10,
) -> list[TopSite]:
    """Compute top visited sites."""
    domain_visits: Counter[str] = Counter()
    domain_titles: dict[str, str] = {}

    for url, title, _, visits in _iter_history(history):
        domain = _extract_domain(url)
        domain_visits[domain] += len(visits)
        if domain not in domain_titles or len(title) > len(domain_titles[domain]):
            domain_titles[domain] = title

    top_sites = []
    for domain, visits in domain_visits.most_common(limit):
        top_sites.append(
            TopSite(
                domain=domain,
                title=domain_titles.get(domain, domain),
                visits=visits,
                favicon=f"https://www.google.com/s2/favicons?domain={domain}&sz=64",
            )
        )
    return top_sites


def _compute_top_categories(
    history: list[dict[str, Any]],
    limit: int = 10,
) -> list[TopCategory]:
    """Compute top categories by visit count."""
    category_visits: Counter[str] = Counter()
    total_visits = 0

    for url, title, _, visits in _iter_history(history):
        result = categorize_url(url, title)
        visit_count = len(visits)
        category_visits[result.category] += visit_count
        total_visits += visit_count

    top_categories = []
    for category, visits in category_visits.most_common(limit):
        pct = (visits / total_visits * 100) if total_visits > 0 else 0
        top_categories.append(
            TopCategory(
                category=category,
                visits=visits,
                percentage=round(pct, 1),
            )
        )
    return top_categories


def _compute_time_of_day(
    all_visits: list[tuple[datetime, str, str]],
) -> list[HourlyVisits]:
    """Compute visits by hour of day."""
    hour_counts = Counter(dt.hour for dt, _, _ in all_visits)
    return [HourlyVisits(hour=h, visits=hour_counts.get(h, 0)) for h in range(24)]


def _compute_day_of_week(
    all_visits: list[tuple[datetime, str, str]],
) -> list[DayOfWeekVisits]:
    """Compute visits by day of week (0=Monday, 6=Sunday)."""
    dow_counts = Counter(dt.weekday() for dt, _, _ in all_visits)
    return [
        DayOfWeekVisits(day_of_week=d, visits=dow_counts.get(d, 0)) for d in range(7)
    ]


def _compute_heatmap(
    all_visits: list[tuple[datetime, str, str]],
) -> list[HeatmapDay]:
    """Compute daily visit counts for heatmap."""
    date_counts: Counter[str] = Counter()
    for dt, _, _ in all_visits:
        date_str = dt.strftime("%Y-%m-%d")
        date_counts[date_str] += 1

    return [
        HeatmapDay(date=date, visits=visits)
        for date, visits in sorted(date_counts.items())
    ]


def _compute_monthly_top_sites(
    all_visits: list[tuple[datetime, str, str]],
    top_n: int = 5,
) -> list[MonthlyRanking]:
    """Compute top sites per month."""
    monthly_visits: dict[str, Counter[str]] = defaultdict(Counter)

    for dt, domain, _ in all_visits:
        month = dt.strftime("%Y-%m")
        monthly_visits[month][domain] += 1

    rankings = []
    for month in sorted(monthly_visits.keys()):
        top_domains = [d for d, _ in monthly_visits[month].most_common(top_n)]
        rankings.append(MonthlyRanking(month=month, ranking=top_domains))

    return rankings


def _compute_standout_days(
    all_visits: list[tuple[datetime, str, str]],
    limit: int = 5,
) -> list[StandoutDay]:
    """Find the most active days."""
    daily_stats: dict[str, dict] = defaultdict(
        lambda: {"visits": 0, "domains": Counter()}
    )

    for dt, domain, _ in all_visits:
        date_str = dt.strftime("%Y-%m-%d")
        daily_stats[date_str]["visits"] += 1
        daily_stats[date_str]["domains"][domain] += 1

    sorted_days = sorted(
        daily_stats.items(), key=lambda x: x[1]["visits"], reverse=True
    )

    standout_days = []
    for date, stats in sorted_days[:limit]:
        top_domain = stats["domains"].most_common(1)
        standout_days.append(
            StandoutDay(
                date=date,
                visits=stats["visits"],
                top_domain=top_domain[0][0] if top_domain else "",
            )
        )

    return standout_days


def _compute_streaks(all_visits: list[tuple[datetime, str, str]]) -> Streaks:
    """Compute longest online and offline streaks."""
    if not all_visits:
        return Streaks(longest_on_streak=0, longest_off_streak=0)

    active_dates = sorted(set(dt.date() for dt, _, _ in all_visits))
    if not active_dates:
        return Streaks(longest_on_streak=0, longest_off_streak=0)

    longest_on = 1
    current_on = 1
    longest_off = 0

    for i in range(1, len(active_dates)):
        diff = (active_dates[i] - active_dates[i - 1]).days
        if diff == 1:
            current_on += 1
            longest_on = max(longest_on, current_on)
        else:
            current_on = 1
            gap = diff - 1
            longest_off = max(longest_off, gap)

    return Streaks(longest_on_streak=longest_on, longest_off_streak=longest_off)


def _compute_session_info(
    all_visits: list[tuple[datetime, str, str]],
) -> SessionInfo:
    """Compute longest browsing session."""
    if not all_visits:
        return SessionInfo(
            longest_session_minutes=0,
            longest_session_domain="",
            longest_session_date="",
        )

    session_gap = timedelta(minutes=30)
    sessions: list[tuple[datetime, datetime, Counter]] = []
    current_start = all_visits[0][0]
    current_end = all_visits[0][0]
    current_domains: Counter[str] = Counter()

    for dt, domain, _ in all_visits:
        if dt - current_end > session_gap:
            sessions.append((current_start, current_end, current_domains))
            current_start = dt
            current_domains = Counter()
        current_end = dt
        current_domains[domain] += 1

    sessions.append((current_start, current_end, current_domains))

    longest_session = max(sessions, key=lambda s: (s[1] - s[0]).total_seconds())
    duration = (longest_session[1] - longest_session[0]).total_seconds() / 60
    top_domain = longest_session[2].most_common(1)

    return SessionInfo(
        longest_session_minutes=int(duration),
        longest_session_domain=top_domain[0][0] if top_domain else "",
        longest_session_date=longest_session[0].strftime("%Y-%m-%d"),
    )


def _compute_domain_discovery(
    all_visits: list[tuple[datetime, str, str]],
) -> DomainDiscovery:
    """Compute new vs returning domains and find standouts."""
    if not all_visits:
        return DomainDiscovery(
            new_domains=0,
            returning_domains=0,
            top_new_domain="",
            top_ride_or_die="",
        )

    domain_first_visit: dict[str, datetime] = {}
    domain_visit_counts: Counter[str] = Counter()

    for dt, domain, _ in all_visits:
        if domain not in domain_first_visit:
            domain_first_visit[domain] = dt
        domain_visit_counts[domain] += 1

    mid_point = all_visits[len(all_visits) // 2][0]

    new_domains = [d for d, dt in domain_first_visit.items() if dt >= mid_point]
    returning_domains = [d for d, dt in domain_first_visit.items() if dt < mid_point]

    new_domain_visits = {d: domain_visit_counts[d] for d in new_domains}
    returning_domain_visits = {d: domain_visit_counts[d] for d in returning_domains}

    top_new = max(new_domain_visits, key=new_domain_visits.get) if new_domain_visits else ""
    top_returning = max(returning_domain_visits, key=returning_domain_visits.get) if returning_domain_visits else ""

    return DomainDiscovery(
        new_domains=len(new_domains),
        returning_domains=len(returning_domains),
        top_new_domain=top_new,
        top_ride_or_die=top_returning,
    )


def _compute_peak_hour(time_of_day: list[HourlyVisits]) -> int:
    """Find the hour with most visits."""
    if not time_of_day:
        return 12
    return max(time_of_day, key=lambda h: h.visits).hour


def _compute_time_badge(time_of_day: list[HourlyVisits]) -> str:
    """Determine if user is night owl, early bird, or all-day surfer."""
    night_visits = sum(h.visits for h in time_of_day if h.hour >= 22 or h.hour < 6)
    morning_visits = sum(h.visits for h in time_of_day if 6 <= h.hour < 12)
    total_visits = sum(h.visits for h in time_of_day)

    if total_visits == 0:
        return "all_day_surfer"

    night_ratio = night_visits / total_visits
    morning_ratio = morning_visits / total_visits

    if night_ratio > 0.3:
        return "night_owl"
    elif morning_ratio > 0.35:
        return "early_bird"
    return "all_day_surfer"


def _compute_guilty_pleasure_category(
    history: list[dict[str, Any]],
    all_visits: list[tuple[datetime, str, str]],
) -> str:
    """Find the category with highest growth in second half of period."""
    if not all_visits:
        return "other"

    mid_point = all_visits[len(all_visits) // 2][0]

    first_half: Counter[str] = Counter()
    second_half: Counter[str] = Counter()

    for url, title, _, visits in _iter_history(history):
        result = categorize_url(url, title)
        for ts, _ in visits:
            dt = _timestamp_to_datetime(ts)
            if dt < mid_point:
                first_half[result.category] += 1
            else:
                second_half[result.category] += 1

    growth: dict[str, float] = {}
    for cat in set(first_half.keys()) | set(second_half.keys()):
        first = first_half.get(cat, 0)
        second = second_half.get(cat, 0)
        if first > 0:
            growth[cat] = (second - first) / first
        elif second > 0:
            growth[cat] = float("inf")
        else:
            growth[cat] = 0

    if not growth:
        return "other"

    valid_growth = {k: v for k, v in growth.items() if v != float("inf") and v > 0}
    if valid_growth:
        return max(valid_growth, key=valid_growth.get)

    return max(second_half, key=second_half.get) if second_half else "other"


def compute_insights(
    history: list[dict[str, Any]],
    run_id: str,
    timezone: str,
    range_start: str,
    range_end: str,
) -> Insights:
    """Compute all insights from browsing history."""
    all_visits = _get_all_visits(history)

    totals = _compute_totals(history, all_visits)
    top_sites = _compute_top_sites(history)
    top_categories = _compute_top_categories(history)
    time_of_day = _compute_time_of_day(all_visits)
    day_of_week = _compute_day_of_week(all_visits)
    heatmap = _compute_heatmap(all_visits)
    monthly_top_sites = _compute_monthly_top_sites(all_visits)
    standout_days = _compute_standout_days(all_visits)
    streaks = _compute_streaks(all_visits)
    session = _compute_session_info(all_visits)
    domain_discovery = _compute_domain_discovery(all_visits)
    peak_hour = _compute_peak_hour(time_of_day)
    time_badge = _compute_time_badge(time_of_day)
    guilty_pleasure = _compute_guilty_pleasure_category(history, all_visits)

    most_online = standout_days[0] if standout_days else StandoutDay(
        date="", visits=0, top_domain=""
    )

    personality = compute_personality(
        top_categories=top_categories,
        time_of_day=time_of_day,
        domain_discovery=domain_discovery,
        streaks=streaks,
        unique_domains=totals.unique_domains,
        total_visits=totals.pageviews,
        active_days=totals.active_days,
    )

    return Insights(
        meta=InsightsMeta(
            run_id=run_id,
            generated_at=datetime.now(UTC).isoformat(),
            range_start=range_start,
            range_end=range_end,
            timezone=timezone,
        ),
        totals=totals,
        top_sites=top_sites,
        top_categories=top_categories,
        time_of_day=time_of_day,
        day_of_week=day_of_week,
        heatmap=heatmap,
        monthly_top_sites=monthly_top_sites,
        standout_days=standout_days,
        streaks=streaks,
        personality=personality,
        session=session,
        domain_discovery=domain_discovery,
        peak_hour=peak_hour,
        time_badge=time_badge,
        guilty_pleasure_category=guilty_pleasure,
        most_chronically_online_day=most_online,
    )
