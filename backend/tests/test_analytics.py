import pytest
from datetime import datetime, UTC

from app.services.analytics import (
    compute_insights,
    _compute_totals,
    _compute_top_sites,
    _compute_top_categories,
    _compute_time_of_day,
    _compute_day_of_week,
    _compute_streaks,
    _compute_peak_hour,
    _compute_time_badge,
    _get_all_visits,
)


@pytest.fixture
def sample_history():
    base_ts = int(datetime(2024, 6, 15, 14, 30, tzinfo=UTC).timestamp() * 1000)
    hour = 3600 * 1000
    day = 24 * hour

    return [
        {
            "url": "https://github.com/user/repo",
            "title": "user/repo - GitHub",
            "visitCount": 50,
            "visits": [
                {"timestamp": base_ts, "transition": "link"},
                {"timestamp": base_ts + hour, "transition": "link"},
                {"timestamp": base_ts + 2 * hour, "transition": "typed"},
                {"timestamp": base_ts + day, "transition": "link"},
                {"timestamp": base_ts + day + hour, "transition": "link"},
            ],
        },
        {
            "url": "https://www.youtube.com/watch?v=abc123",
            "title": "Cool Video - YouTube",
            "visitCount": 30,
            "visits": [
                {"timestamp": base_ts + 3 * hour, "transition": "link"},
                {"timestamp": base_ts + day + 3 * hour, "transition": "link"},
                {"timestamp": base_ts + 2 * day, "transition": "link"},
            ],
        },
        {
            "url": "https://twitter.com/user/status/123",
            "title": "User on Twitter",
            "visitCount": 20,
            "visits": [
                {"timestamp": base_ts + 4 * hour, "transition": "link"},
                {"timestamp": base_ts + day + 4 * hour, "transition": "link"},
            ],
        },
        {
            "url": "https://www.amazon.com/dp/B00ABC123",
            "title": "Amazing Product - Amazon",
            "visitCount": 10,
            "visits": [
                {"timestamp": base_ts + 5 * hour, "transition": "link"},
            ],
        },
    ]


class TestComputeTotals:
    def test_counts_visits_correctly(self, sample_history):
        all_visits = _get_all_visits(sample_history)
        totals = _compute_totals(sample_history, all_visits)

        assert totals.pageviews == 11
        assert totals.unique_domains == 4
        assert totals.active_days == 3


class TestComputeTopSites:
    def test_returns_sites_sorted_by_visits(self, sample_history):
        top_sites = _compute_top_sites(sample_history)

        assert len(top_sites) == 4
        assert top_sites[0].domain == "github.com"
        assert top_sites[0].visits == 5
        assert top_sites[1].domain == "youtube.com"
        assert top_sites[1].visits == 3

    def test_includes_favicon_urls(self, sample_history):
        top_sites = _compute_top_sites(sample_history)

        for site in top_sites:
            assert site.favicon.startswith("https://www.google.com/s2/favicons")
            assert site.domain in site.favicon


class TestComputeTopCategories:
    def test_categorizes_visits(self, sample_history):
        categories = _compute_top_categories(sample_history)

        assert len(categories) > 0
        category_names = [c.category for c in categories]
        assert "development" in category_names
        assert "entertainment" in category_names

    def test_percentages_sum_to_100(self, sample_history):
        categories = _compute_top_categories(sample_history)
        total_pct = sum(c.percentage for c in categories)
        assert 99 <= total_pct <= 101


class TestComputeTimeOfDay:
    def test_returns_24_hours(self, sample_history):
        all_visits = _get_all_visits(sample_history)
        time_of_day = _compute_time_of_day(all_visits)

        assert len(time_of_day) == 24
        hours = [h.hour for h in time_of_day]
        assert hours == list(range(24))


class TestComputeDayOfWeek:
    def test_returns_7_days(self, sample_history):
        all_visits = _get_all_visits(sample_history)
        day_of_week = _compute_day_of_week(all_visits)

        assert len(day_of_week) == 7


class TestComputeStreaks:
    def test_calculates_consecutive_days(self, sample_history):
        all_visits = _get_all_visits(sample_history)
        streaks = _compute_streaks(all_visits)

        assert streaks.longest_on_streak >= 1

    def test_empty_history(self):
        streaks = _compute_streaks([])
        assert streaks.longest_on_streak == 0
        assert streaks.longest_off_streak == 0


class TestComputePeakHour:
    def test_finds_busiest_hour(self, sample_history):
        all_visits = _get_all_visits(sample_history)
        time_of_day = _compute_time_of_day(all_visits)
        peak = _compute_peak_hour(time_of_day)

        assert 0 <= peak <= 23


class TestComputeTimeBadge:
    def test_night_owl_detection(self):
        night_heavy = [
            {"hour": h, "visits": 100 if h >= 22 or h < 6 else 10}
            for h in range(24)
        ]
        from app.models.schemas import HourlyVisits
        night_hours = [HourlyVisits(hour=h["hour"], visits=h["visits"]) for h in night_heavy]
        badge = _compute_time_badge(night_hours)
        assert badge == "night_owl"

    def test_early_bird_detection(self):
        morning_heavy = [
            {"hour": h, "visits": 100 if 6 <= h < 12 else 5}
            for h in range(24)
        ]
        from app.models.schemas import HourlyVisits
        morning_hours = [HourlyVisits(hour=h["hour"], visits=h["visits"]) for h in morning_heavy]
        badge = _compute_time_badge(morning_hours)
        assert badge == "early_bird"


class TestComputeInsights:
    def test_returns_complete_insights(self, sample_history):
        insights = compute_insights(
            history=sample_history,
            run_id="test-run-123",
            timezone="America/New_York",
            range_start="2024-01-01T00:00:00Z",
            range_end="2024-12-31T23:59:59Z",
        )

        assert insights.meta.run_id == "test-run-123"
        assert insights.totals.pageviews > 0
        assert len(insights.top_sites) > 0
        assert len(insights.top_categories) > 0
        assert len(insights.time_of_day) == 24
        assert len(insights.day_of_week) == 7
        assert insights.personality is not None

    def test_empty_history(self):
        insights = compute_insights(
            history=[],
            run_id="empty-run",
            timezone="UTC",
            range_start="2024-01-01T00:00:00Z",
            range_end="2024-12-31T23:59:59Z",
        )

        assert insights.totals.pageviews == 0
        assert insights.totals.unique_domains == 0
        assert len(insights.top_sites) == 0
