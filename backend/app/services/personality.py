"""
Personality engine - assigns Browser Clubs and roles based on browsing patterns.

Browser Clubs:
- rabbit_hole_researcher: Deep dives into learning/wiki content
- doomscroller: Heavy social media and news consumption
- hustle_tab_hoarder: Work/productivity focused, many tabs
- comfort_rewatcher: Entertainment focused, high revisit rate
- niche_forum_lurker: Development/gaming/niche community focus
- casual_surfer: Balanced, no strong patterns

Roles:
- archivist: High revisit rate, loyal to few sites
- explorer: High discovery rate, tries many new sites
- loyalist: Returns to same sites repeatedly
- multitasker: Many categories, switches frequently
- lurker: Low engagement signals
"""

from collections import Counter
from dataclasses import dataclass
from typing import Any

from app.models.schemas import (
    BrowserClub,
    BrowserRole,
    DomainDiscovery,
    HourlyVisits,
    Personality,
    Streaks,
    TopCategory,
)


@dataclass
class PersonalitySignals:
    """Signals extracted from browsing data for personality assignment."""

    category_mix: dict[str, float]
    night_ratio: float
    morning_ratio: float
    revisit_ratio: float
    discovery_ratio: float
    top_category: str
    unique_domains: int
    total_visits: int
    avg_daily_visits: float
    longest_streak: int


def _extract_signals(
    top_categories: list[TopCategory],
    time_of_day: list[HourlyVisits],
    domain_discovery: DomainDiscovery,
    streaks: Streaks,
    unique_domains: int,
    total_visits: int,
    active_days: int,
) -> PersonalitySignals:
    """Extract personality signals from analytics data."""
    category_mix = {
        cat.category: cat.percentage / 100.0
        for cat in top_categories
    }

    total_hourly = sum(h.visits for h in time_of_day)
    if total_hourly > 0:
        night_visits = sum(h.visits for h in time_of_day if h.hour >= 22 or h.hour < 6)
        morning_visits = sum(h.visits for h in time_of_day if 6 <= h.hour < 12)
        night_ratio = night_visits / total_hourly
        morning_ratio = morning_visits / total_hourly
    else:
        night_ratio = 0.0
        morning_ratio = 0.0

    total_domains = domain_discovery.new_domains + domain_discovery.returning_domains
    if total_domains > 0:
        discovery_ratio = domain_discovery.new_domains / total_domains
        revisit_ratio = domain_discovery.returning_domains / total_domains
    else:
        discovery_ratio = 0.5
        revisit_ratio = 0.5

    top_category = top_categories[0].category if top_categories else "other"

    avg_daily = total_visits / active_days if active_days > 0 else 0

    return PersonalitySignals(
        category_mix=category_mix,
        night_ratio=night_ratio,
        morning_ratio=morning_ratio,
        revisit_ratio=revisit_ratio,
        discovery_ratio=discovery_ratio,
        top_category=top_category,
        unique_domains=unique_domains,
        total_visits=total_visits,
        avg_daily_visits=avg_daily,
        longest_streak=streaks.longest_on_streak,
    )


def _assign_club(signals: PersonalitySignals) -> BrowserClub:
    """Assign a Browser Club based on signals."""
    cat_mix = signals.category_mix

    learning_score = cat_mix.get("learning", 0) + cat_mix.get("search", 0) * 0.5
    social_news_score = cat_mix.get("social", 0) + cat_mix.get("news", 0)
    work_score = cat_mix.get("work", 0) + cat_mix.get("development", 0) * 0.5
    entertainment_score = cat_mix.get("entertainment", 0) + cat_mix.get("gaming", 0) * 0.5
    niche_score = cat_mix.get("development", 0) + cat_mix.get("gaming", 0)

    scores: dict[BrowserClub, float] = {
        "rabbit_hole_researcher": learning_score * 2.0 + (0.3 if signals.night_ratio > 0.3 else 0),
        "doomscroller": social_news_score * 1.8 + (signals.night_ratio * 0.5),
        "hustle_tab_hoarder": work_score * 1.5 + (signals.morning_ratio * 0.5) + (0.2 if signals.avg_daily_visits > 100 else 0),
        "comfort_rewatcher": entertainment_score * 1.5 + (signals.revisit_ratio * 0.5),
        "niche_forum_lurker": niche_score * 1.5 + (0.3 if signals.unique_domains < 50 else 0),
        "casual_surfer": 0.3,
    }

    if signals.longest_streak > 30:
        scores["hustle_tab_hoarder"] += 0.2
    if signals.discovery_ratio > 0.6:
        scores["rabbit_hole_researcher"] += 0.2

    max_score = max(scores.values())
    if max_score < 0.4:
        return "casual_surfer"

    return max(scores, key=scores.get)


def _assign_role(signals: PersonalitySignals) -> BrowserRole:
    """Assign a role within the club based on behavior patterns."""
    scores: dict[BrowserRole, float] = {
        "archivist": signals.revisit_ratio * 1.5 + (0.3 if signals.unique_domains < 30 else 0),
        "explorer": signals.discovery_ratio * 1.5 + (0.2 if signals.unique_domains > 100 else 0),
        "loyalist": signals.revisit_ratio * 1.2 + (signals.longest_streak / 100),
        "multitasker": len(signals.category_mix) / 10 + (0.3 if signals.avg_daily_visits > 80 else 0),
        "lurker": 0.3 - (signals.avg_daily_visits / 500),
    }

    if signals.avg_daily_visits < 20:
        scores["lurker"] += 0.4

    return max(scores, key=scores.get)


def _generate_blurb(club: BrowserClub, role: BrowserRole, signals: PersonalitySignals) -> str:
    """Generate a personality blurb based on club and role."""
    club_descriptions = {
        "rabbit_hole_researcher": "You're a knowledge seeker who loves to dive deep. Wikipedia tabs multiply when you're around, and 3 AM finds you learning about obscure topics.",
        "doomscroller": "You've got your finger on the pulse. News, social media, trending topics - if it's happening, you're probably reading about it.",
        "hustle_tab_hoarder": "Your browser is your command center. Work tabs, productivity tools, documentation - you're always building something.",
        "comfort_rewatcher": "You know what you like. Whether it's your favorite videos or go-to entertainment, you've built a cozy corner of the internet.",
        "niche_forum_lurker": "You've found your community. Whether it's dev forums, gaming discussions, or niche subreddits, you're deep in the scene.",
        "casual_surfer": "You're a balanced browser. A little bit of everything, no obsessions - just enjoying the internet as it comes.",
    }

    role_additions = {
        "archivist": "You keep coming back to your trusted sources.",
        "explorer": "You're always discovering something new.",
        "loyalist": "Once you find a good site, you stick with it.",
        "multitasker": "You juggle multiple interests with ease.",
        "lurker": "You observe more than you participate.",
    }

    base = club_descriptions.get(club, "")
    addition = role_additions.get(role, "")

    return f"{base} {addition}".strip()


def compute_personality(
    top_categories: list[TopCategory],
    time_of_day: list[HourlyVisits],
    domain_discovery: DomainDiscovery,
    streaks: Streaks,
    unique_domains: int,
    total_visits: int,
    active_days: int,
) -> Personality:
    """
    Compute Browser Club and role assignment.

    Returns a Personality with club, role, and personalized blurb.
    """
    if not top_categories or total_visits == 0:
        return Personality(
            club="casual_surfer",
            role="explorer",
            blurb="Start browsing to discover your personality!",
        )

    signals = _extract_signals(
        top_categories=top_categories,
        time_of_day=time_of_day,
        domain_discovery=domain_discovery,
        streaks=streaks,
        unique_domains=unique_domains,
        total_visits=total_visits,
        active_days=active_days,
    )

    club = _assign_club(signals)
    role = _assign_role(signals)
    blurb = _generate_blurb(club, role, signals)

    return Personality(club=club, role=role, blurb=blurb)
