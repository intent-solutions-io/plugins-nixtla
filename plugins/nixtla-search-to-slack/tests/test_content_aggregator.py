"""
Unit tests for content aggregator.
"""

import pytest
from datetime import datetime

from nixtla_search_to_slack.content_aggregator import ContentAggregator, Content
from nixtla_search_to_slack.search_orchestrator import SearchResult


class TestContentAggregator:
    """Test content aggregation and deduplication."""

    def test_deduplicate_exact_url(self, sample_search_results):
        """Test deduplication of exact URL matches."""
        aggregator = ContentAggregator()

        # Add duplicate with same URL
        duplicate = SearchResult(
            url=sample_search_results[0].url,
            title="Different Title",
            description="Different description",
            source="web",
            timestamp=datetime.now(),
            metadata={}
        )
        results = sample_search_results + [duplicate]

        content = aggregator.aggregate(results)

        # Should deduplicate the exact URL match
        assert len(content) == 2  # Original 3 minus 1 duplicate with tracking params
        unique_urls = [c.url for c in content]
        assert len(set(unique_urls)) == len(unique_urls)

    def test_deduplicate_url_with_tracking_params(self):
        """Test deduplication of URLs with tracking parameters."""
        aggregator = ContentAggregator()

        results = [
            SearchResult(
                url="https://example.com/article?id=123",
                title="Article",
                description="Description",
                source="web",
                timestamp=datetime.now(),
                metadata={}
            ),
            SearchResult(
                url="https://example.com/article?id=123&utm_source=twitter&utm_campaign=social",
                title="Article",
                description="Description",
                source="web",
                timestamp=datetime.now(),
                metadata={}
            )
        ]

        content = aggregator.aggregate(results)

        # Should deduplicate URL with tracking params
        assert len(content) == 1
        assert "utm_source" not in content[0].url

    def test_deduplicate_similar_titles(self):
        """Test deduplication of very similar titles from same domain."""
        aggregator = ContentAggregator()

        results = [
            SearchResult(
                url="https://example.com/article1",
                title="TimeGPT 2.0 Released with New Features",
                description="Description 1",
                source="web",
                timestamp=datetime.now(),
                metadata={}
            ),
            SearchResult(
                url="https://example.com/article2",
                title="TimeGPT 2.0 Released With New Features!",  # Very similar
                description="Description 2",
                source="web",
                timestamp=datetime.now(),
                metadata={}
            )
        ]

        content = aggregator.aggregate(results)

        # Should deduplicate very similar titles from same domain
        assert len(content) == 1

    def test_keep_similar_titles_different_domains(self):
        """Test keeping similar titles from different domains."""
        aggregator = ContentAggregator()

        results = [
            SearchResult(
                url="https://example1.com/article",
                title="TimeGPT 2.0 Released",
                description="Description 1",
                source="web",
                timestamp=datetime.now(),
                metadata={}
            ),
            SearchResult(
                url="https://example2.com/news",
                title="TimeGPT 2.0 Released",  # Same title, different domain
                description="Description 2",
                source="web",
                timestamp=datetime.now(),
                metadata={}
            )
        ]

        content = aggregator.aggregate(results)

        # Should keep both since they're from different domains
        assert len(content) == 2

    def test_normalize_url(self):
        """Test URL normalization."""
        aggregator = ContentAggregator()

        # Test with tracking parameters
        url = "https://Example.COM/Article?utm_source=twitter&id=123&utm_campaign=test#section"
        normalized = aggregator._normalize_url(url)

        assert "example.com" in normalized  # Lowercase
        assert "utm_source" not in normalized  # Tracking param removed
        assert "id=123" in normalized  # Real param kept
        assert "#section" not in normalized  # Fragment removed

    def test_normalize_title(self):
        """Test title normalization."""
        aggregator = ContentAggregator()

        title = "  TimeGPT 2.0 Released!!! - Latest News  "
        normalized = aggregator._normalize_title(title)

        assert normalized == "timegpt 2 0 released latest news"
        assert "!" not in normalized
        assert "  " not in normalized

    def test_preserve_metadata(self, sample_search_results):
        """Test that metadata is preserved during aggregation."""
        aggregator = ContentAggregator()

        # Use just the unique results
        results = sample_search_results[:2]
        content = aggregator.aggregate(results)

        assert len(content) == 2
        for c in content:
            assert c.metadata is not None
            assert len(c.metadata) > 0

    def test_sort_by_timestamp(self):
        """Test that results are sorted by timestamp."""
        aggregator = ContentAggregator()

        now = datetime.now()
        from datetime import timedelta

        results = [
            SearchResult(
                url="https://example.com/old",
                title="Old Article",
                description="Old",
                source="web",
                timestamp=now - timedelta(days=7),
                metadata={}
            ),
            SearchResult(
                url="https://example.com/new",
                title="New Article",
                description="New",
                source="web",
                timestamp=now,
                metadata={}
            ),
            SearchResult(
                url="https://example.com/middle",
                title="Middle Article",
                description="Middle",
                source="web",
                timestamp=now - timedelta(days=3),
                metadata={}
            )
        ]

        content = aggregator.aggregate(results)

        # Should be sorted by timestamp, newest first
        assert len(content) == 3
        assert content[0].title == "New Article"
        assert content[1].title == "Middle Article"
        assert content[2].title == "Old Article"

    def test_get_statistics(self, sample_search_results):
        """Test statistics gathering."""
        aggregator = ContentAggregator()
        aggregator.aggregate(sample_search_results)

        stats = aggregator.get_statistics()

        assert "unique_urls" in stats
        assert "unique_titles" in stats
        assert "total_content" in stats
        assert stats["unique_urls"] > 0