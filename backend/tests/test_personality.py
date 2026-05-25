import pytest

from app.models.schemas import (
    DomainDiscovery,
    HourlyVisits,
    Streaks,
    TopCategory,
)
from app.services.personality import (
    PersonalitySignals,
    _assign_club,
    _assign_role,
    _extract_signals,
    _generate_blurb,
    compute_personality,
)


@pytest.fixture
def learning_heavy_categories():
    return [
        TopCategory(category="learning", visits=500, percentage=50.0),
        TopCategory(category="search", visits=200, percentage=20.0),
        TopCategory(category="other", visits=300, percentage=30.0),
    ]


@pytest.fixture
def social_heavy_categories():
    return [
        TopCategory(category="social", visits=400, percentage=40.0),
        TopCategory(category="news", visits=300, percentage=30.0),
        TopCategory(category="entertainment", visits=300, percentage=30.0),
    ]


@pytest.fixture
def work_heavy_categories():
    return [
        TopCategory(category="work", visits=400, percentage=40.0),
        TopCategory(category="development", visits=300, percentage=30.0),
        TopCategory(category="communication", visits=300, percentage=30.0),
    ]


@pytest.fixture
def entertainment_heavy_categories():
    return [
        TopCategory(category="entertainment", visits=600, percentage=60.0),
        TopCategory(category="gaming", visits=200, percentage=20.0),
        TopCategory(category="social", visits=200, percentage=20.0),
    ]


@pytest.fixture
def balanced_time_of_day():
    return [HourlyVisits(hour=h, visits=100) for h in range(24)]


@pytest.fixture
def night_owl_time_of_day():
    return [
        HourlyVisits(hour=h, visits=200 if h >= 22 or h < 6 else 20)
        for h in range(24)
    ]


@pytest.fixture
def default_domain_discovery():
    return DomainDiscovery(
        new_domains=50,
        returning_domains=50,
        top_new_domain="new-site.com",
        top_ride_or_die="favorite.com",
    )


@pytest.fixture
def default_streaks():
    return Streaks(longest_on_streak=30, longest_off_streak=5)


class TestExtractSignals:
    def test_extracts_category_mix(self, learning_heavy_categories, balanced_time_of_day, default_domain_discovery, default_streaks):
        signals = _extract_signals(
            top_categories=learning_heavy_categories,
            time_of_day=balanced_time_of_day,
            domain_discovery=default_domain_discovery,
            streaks=default_streaks,
            unique_domains=100,
            total_visits=1000,
            active_days=30,
        )

        assert signals.category_mix["learning"] == 0.5
        assert signals.top_category == "learning"


class TestAssignClub:
    def test_rabbit_hole_researcher(self, learning_heavy_categories, night_owl_time_of_day, default_domain_discovery, default_streaks):
        signals = _extract_signals(
            top_categories=learning_heavy_categories,
            time_of_day=night_owl_time_of_day,
            domain_discovery=default_domain_discovery,
            streaks=default_streaks,
            unique_domains=100,
            total_visits=1000,
            active_days=30,
        )
        club = _assign_club(signals)
        assert club == "rabbit_hole_researcher"

    def test_doomscroller(self, social_heavy_categories, night_owl_time_of_day, default_domain_discovery, default_streaks):
        signals = _extract_signals(
            top_categories=social_heavy_categories,
            time_of_day=night_owl_time_of_day,
            domain_discovery=default_domain_discovery,
            streaks=default_streaks,
            unique_domains=100,
            total_visits=1000,
            active_days=30,
        )
        club = _assign_club(signals)
        assert club == "doomscroller"

    def test_comfort_rewatcher(self, entertainment_heavy_categories, balanced_time_of_day, default_streaks):
        high_revisit = DomainDiscovery(
            new_domains=10,
            returning_domains=90,
            top_new_domain="new.com",
            top_ride_or_die="youtube.com",
        )
        signals = _extract_signals(
            top_categories=entertainment_heavy_categories,
            time_of_day=balanced_time_of_day,
            domain_discovery=high_revisit,
            streaks=default_streaks,
            unique_domains=50,
            total_visits=1000,
            active_days=30,
        )
        club = _assign_club(signals)
        assert club == "comfort_rewatcher"


class TestAssignRole:
    def test_explorer_high_discovery(self, learning_heavy_categories, balanced_time_of_day, default_streaks):
        high_discovery = DomainDiscovery(
            new_domains=90,
            returning_domains=10,
            top_new_domain="new.com",
            top_ride_or_die="old.com",
        )
        signals = _extract_signals(
            top_categories=learning_heavy_categories,
            time_of_day=balanced_time_of_day,
            domain_discovery=high_discovery,
            streaks=default_streaks,
            unique_domains=200,
            total_visits=1000,
            active_days=30,
        )
        role = _assign_role(signals)
        assert role == "explorer"

    def test_archivist_high_revisit(self, learning_heavy_categories, balanced_time_of_day, default_streaks):
        high_revisit = DomainDiscovery(
            new_domains=5,
            returning_domains=95,
            top_new_domain="new.com",
            top_ride_or_die="favorite.com",
        )
        signals = _extract_signals(
            top_categories=learning_heavy_categories,
            time_of_day=balanced_time_of_day,
            domain_discovery=high_revisit,
            streaks=default_streaks,
            unique_domains=20,
            total_visits=1000,
            active_days=30,
        )
        role = _assign_role(signals)
        assert role in ["archivist", "loyalist"]


class TestGenerateBlurb:
    def test_generates_non_empty_blurb(self):
        blurb = _generate_blurb(
            club="rabbit_hole_researcher",
            role="explorer",
            signals=PersonalitySignals(
                category_mix={"learning": 0.5},
                night_ratio=0.3,
                morning_ratio=0.2,
                revisit_ratio=0.5,
                discovery_ratio=0.5,
                top_category="learning",
                unique_domains=100,
                total_visits=1000,
                avg_daily_visits=33,
                longest_streak=30,
            ),
        )
        assert len(blurb) > 0
        assert "knowledge" in blurb.lower() or "deep" in blurb.lower()


class TestComputePersonality:
    def test_returns_valid_personality(self, learning_heavy_categories, balanced_time_of_day, default_domain_discovery, default_streaks):
        personality = compute_personality(
            top_categories=learning_heavy_categories,
            time_of_day=balanced_time_of_day,
            domain_discovery=default_domain_discovery,
            streaks=default_streaks,
            unique_domains=100,
            total_visits=1000,
            active_days=30,
        )

        assert personality.club in [
            "rabbit_hole_researcher",
            "doomscroller",
            "hustle_tab_hoarder",
            "comfort_rewatcher",
            "niche_forum_lurker",
            "casual_surfer",
        ]
        assert personality.role in [
            "archivist",
            "explorer",
            "loyalist",
            "multitasker",
            "lurker",
        ]
        assert len(personality.blurb) > 0

    def test_empty_data_returns_casual_surfer(self):
        personality = compute_personality(
            top_categories=[],
            time_of_day=[],
            domain_discovery=DomainDiscovery(
                new_domains=0,
                returning_domains=0,
                top_new_domain="",
                top_ride_or_die="",
            ),
            streaks=Streaks(longest_on_streak=0, longest_off_streak=0),
            unique_domains=0,
            total_visits=0,
            active_days=0,
        )

        assert personality.club == "casual_surfer"
        assert personality.role == "explorer"
