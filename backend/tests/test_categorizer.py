import pytest

from app.services.categorizer import (
    CategoryResult,
    categorize_batch,
    categorize_url,
    get_category_display_name,
)


class TestCategorizeUrl:
    def test_known_domain_exact_match(self):
        result = categorize_url("https://github.com/user/repo")
        assert result.category == "development"
        assert result.confidence == 1.0
        assert result.source == "domain_map"

    def test_known_domain_with_subdomain(self):
        result = categorize_url("https://www.gmail.com/inbox")
        assert result.category == "communication"
        assert result.confidence == 1.0
        assert result.source == "domain_map"

    def test_google_is_search(self):
        result = categorize_url("https://www.google.com/search?q=test")
        assert result.category == "search"
        assert result.source == "domain_map"

    def test_youtube_entertainment(self):
        result = categorize_url("https://www.youtube.com/watch?v=abc123")
        assert result.category == "entertainment"
        assert result.source == "domain_map"

    def test_social_media(self):
        result = categorize_url("https://twitter.com/user/status/123")
        assert result.category == "social"

        result = categorize_url("https://www.reddit.com/r/programming")
        assert result.category == "social"

    def test_shopping_sites(self):
        result = categorize_url("https://www.amazon.com/dp/B00ABC123")
        assert result.category == "shopping"

        result = categorize_url("https://www.ebay.com/itm/12345")
        assert result.category == "shopping"

    def test_news_sites(self):
        result = categorize_url("https://www.nytimes.com/article")
        assert result.category == "news"

        result = categorize_url("https://www.bbc.com/news/world")
        assert result.category == "news"

    def test_keyword_fallback_shopping(self):
        result = categorize_url(
            "https://unknown-store.com/product/123",
            title="Buy Amazing Product - Add to Cart"
        )
        assert result.category == "shopping"
        assert result.source == "keywords"

    def test_keyword_fallback_development(self):
        result = categorize_url(
            "https://docs.random-lib.io/api/v2",
            title="API Reference - random-lib SDK Documentation"
        )
        assert result.category == "development"
        assert result.source == "keywords"

    def test_keyword_fallback_news(self):
        result = categorize_url(
            "https://localnews.example.com/story",
            title="Breaking: Major News Story Headline"
        )
        assert result.category == "news"
        assert result.source == "keywords"

    def test_unknown_domain_no_keywords(self):
        result = categorize_url(
            "https://completely-unknown-site.xyz/page",
            title="Random Page"
        )
        assert result.category == "other"
        assert result.confidence == 0.0
        assert result.source == "fallback"

    def test_finance_detection(self):
        result = categorize_url("https://www.chase.com/checking")
        assert result.category == "finance"

    def test_gaming_detection(self):
        result = categorize_url("https://store.steampowered.com/app/123")
        assert result.category == "gaming"

    def test_health_detection(self):
        result = categorize_url("https://www.webmd.com/condition")
        assert result.category == "health"


class TestCategorizeBatch:
    def test_batch_categorization(self):
        items = [
            ("https://github.com/user/repo", "User Repo - GitHub"),
            ("https://www.youtube.com/watch?v=abc", "Cool Video - YouTube"),
            ("https://unknown.xyz/page", "Random Page"),
        ]
        results = categorize_batch(items)

        assert len(results) == 3
        assert results[0].category == "development"
        assert results[1].category == "entertainment"
        assert results[2].category == "other"


class TestGetCategoryDisplayName:
    def test_known_categories(self):
        assert get_category_display_name("social") == "Social Media"
        assert get_category_display_name("development") == "Development & Tech"
        assert get_category_display_name("entertainment") == "Entertainment"
        assert get_category_display_name("finance") == "Finance & Banking"

    def test_other_category(self):
        assert get_category_display_name("other") == "Other"
