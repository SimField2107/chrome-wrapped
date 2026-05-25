"""
Website categorization service.
Uses domain mapping + URL/title keyword heuristics.
"""

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

import tldextract
import yaml

from app.models.schemas import WebsiteCategory

CategorySource = Literal["domain_map", "keywords", "fallback"]


@dataclass
class CategoryResult:
    category: WebsiteCategory
    confidence: float
    source: CategorySource


@lru_cache(maxsize=1)
def _load_domain_categories() -> dict[str, WebsiteCategory]:
    """Load and invert the domain categories map."""
    data_path = Path(__file__).parent.parent / "data" / "domain_categories.json"
    with open(data_path) as f:
        category_to_domains: dict[str, list[str]] = json.load(f)

    domain_to_category: dict[str, WebsiteCategory] = {}
    for category, domains in category_to_domains.items():
        for domain in domains:
            domain_to_category[domain.lower()] = category  # type: ignore

    return domain_to_category


@lru_cache(maxsize=1)
def _load_keyword_rules() -> list[dict]:
    """Load keyword rules from YAML."""
    data_path = Path(__file__).parent.parent / "data" / "keyword_rules.yaml"
    with open(data_path) as f:
        data = yaml.safe_load(f)
    return data.get("rules", [])


def _extract_domain(url: str) -> str:
    """Extract the registrable domain from a URL."""
    extracted = tldextract.extract(url)
    if extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}".lower()
    return extracted.domain.lower()


def categorize_url(url: str, title: str = "") -> CategoryResult:
    """
    Categorize a URL based on domain mapping and keyword heuristics.

    Args:
        url: The full URL to categorize
        title: Optional page title for keyword matching

    Returns:
        CategoryResult with category, confidence, and source
    """
    domain = _extract_domain(url)
    domain_categories = _load_domain_categories()

    if domain in domain_categories:
        return CategoryResult(
            category=domain_categories[domain],
            confidence=1.0,
            source="domain_map",
        )

    for parent_domain in [
        ".".join(domain.split(".")[-2:]),
        ".".join(domain.split(".")[-3:]) if len(domain.split(".")) > 2 else None,
    ]:
        if parent_domain and parent_domain in domain_categories:
            return CategoryResult(
                category=domain_categories[parent_domain],
                confidence=0.95,
                source="domain_map",
            )

    combined_text = f"{url} {title}".lower()
    keyword_rules = _load_keyword_rules()

    best_match: CategoryResult | None = None
    best_confidence = 0.0

    for rule in keyword_rules:
        pattern = rule["pattern"]
        category = rule["category"]
        confidence = rule.get("confidence", 0.5)

        if re.search(pattern, combined_text, re.IGNORECASE):
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = CategoryResult(
                    category=category,
                    confidence=confidence,
                    source="keywords",
                )

    if best_match:
        return best_match

    return CategoryResult(
        category="other",
        confidence=0.0,
        source="fallback",
    )


def categorize_batch(
    items: list[tuple[str, str]],
) -> list[CategoryResult]:
    """
    Categorize multiple URLs efficiently.

    Args:
        items: List of (url, title) tuples

    Returns:
        List of CategoryResults in same order
    """
    return [categorize_url(url, title) for url, title in items]


def get_category_display_name(category: WebsiteCategory) -> str:
    """Get a human-readable name for a category."""
    display_names = {
        "social": "Social Media",
        "work": "Work & Productivity",
        "entertainment": "Entertainment",
        "news": "News & Media",
        "shopping": "Shopping",
        "learning": "Learning & Education",
        "development": "Development & Tech",
        "communication": "Communication",
        "finance": "Finance & Banking",
        "health": "Health & Fitness",
        "travel": "Travel",
        "food": "Food & Dining",
        "gaming": "Gaming",
        "adult": "Adult",
        "search": "Search",
        "other": "Other",
    }
    return display_names.get(category, category.title())
