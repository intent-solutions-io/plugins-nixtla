"""
Unit tests for search orchestrator.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import requests

from nixtla_search_to_slack.search_orchestrator import (
    SearchOrchestrator,
    SearchResult,
    WebSearchAdapter,
    GitHubSearchAdapter
)


class TestSearchOrchestrator:
    """Test search orchestration functionality."""

    def test_initialize_adapters(self, mock_env_config, sample_sources_config):
        """Test initialization of search adapters."""
        orchestrator = SearchOrchestrator(sample_sources_config, mock_env_config)

        assert "web" in orchestrator.adapters
        assert "github" in orchestrator.adapters
        assert isinstance(orchestrator.adapters["web"], WebSearchAdapter)
        assert isinstance(orchestrator.adapters["github"], GitHubSearchAdapter)

    @patch('nixtla_search_to_slack.search_orchestrator.requests.get')
    def test_search_multiple_sources(self, mock_get, mock_env_config, sample_sources_config):
        """Test searching across multiple sources."""
        # Mock web search response
        web_response = Mock()
        web_response.status_code = 200
        web_response.json.return_value = {
            "organic_results": [
                {
                    "link": "https://example.com/article",
                    "title": "Test Article",
                    "snippet": "Test description",
                    "position": 1
                }
            ]
        }

        # Mock GitHub search response
        github_response = Mock()
        github_response.status_code = 200
        github_response.json.return_value = {
            "items": [
                {
                    "html_url": "https://github.com/test/repo/issues/1",
                    "title": "Test Issue",
                    "body": "Issue body",
                    "created_at": "2024-01-01T00:00:00Z",
                    "state": "open",
                    "user": {"login": "testuser"},
                    "labels": []
                }
            ]
        }

        # Configure mock to return different responses
        mock_get.side_effect = [web_response, github_response]

        orchestrator = SearchOrchestrator(sample_sources_config, mock_env_config)

        topic = {
            "name": "Test Topic",
            "keywords": ["test", "keyword"],
            "sources": ["web", "github"]
        }

        results = orchestrator.search(topic)

        # Should have results from both sources
        assert len(results) >= 2
        sources = set(r.source for r in results)
        assert "web" in sources
        assert "github" in sources

    @patch('nixtla_search_to_slack.search_orchestrator.requests.get')
    def test_search_continues_on_source_failure(self, mock_get, mock_env_config,
                                               sample_sources_config):
        """Test that search continues even if one source fails."""
        # First call (web) fails
        mock_get.side_effect = [
            Exception("Web search failed"),
            Mock(status_code=200, json=lambda: {"items": []})
        ]

        orchestrator = SearchOrchestrator(sample_sources_config, mock_env_config)

        topic = {
            "name": "Test Topic",
            "keywords": ["test"],
            "sources": ["web", "github"]
        }

        results = orchestrator.search(topic)

        # Should still return results from GitHub
        assert isinstance(results, list)

    def test_search_unknown_source(self, mock_env_config, sample_sources_config):
        """Test handling of unknown source in topic."""
        orchestrator = SearchOrchestrator(sample_sources_config, mock_env_config)

        topic = {
            "name": "Test Topic",
            "keywords": ["test"],
            "sources": ["unknown_source"]
        }

        results = orchestrator.search(topic)

        # Should return empty list, not fail
        assert results == []


class TestWebSearchAdapter:
    """Test web search adapter functionality."""

    @patch('nixtla_search_to_slack.search_orchestrator.requests.get')
    def test_web_search_success(self, mock_get, mock_env_config, sample_sources_config):
        """Test successful web search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "organic_results": [
                {
                    "link": "https://example.com/article1",
                    "title": "Article 1",
                    "snippet": "Description 1",
                    "position": 1,
                    "displayed_link": "example.com"
                },
                {
                    "link": "https://example.com/article2",
                    "title": "Article 2",
                    "snippet": "Description 2",
                    "position": 2,
                    "displayed_link": "example.com"
                }
            ]
        }
        mock_get.return_value = mock_response

        adapter = WebSearchAdapter(
            api_key=mock_env_config["SERP_API_KEY"],
            config=sample_sources_config["sources"]["web"],
            provider_config=sample_sources_config.get("api_providers", {}).get("serpapi", {})
        )

        results = adapter.search("test query", "7d")

        assert len(results) == 2
        assert all(isinstance(r, SearchResult) for r in results)
        assert results[0].url == "https://example.com/article1"
        assert results[0].source == "web"

    @patch('nixtla_search_to_slack.search_orchestrator.requests.get')
    def test_web_search_excludes_domains(self, mock_get, mock_env_config, sample_sources_config):
        """Test that excluded domains are filtered out."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "organic_results": [
                {
                    "link": "https://example.com/article",
                    "title": "Good Article",
                    "snippet": "Good content",
                    "position": 1
                },
                {
                    "link": "https://pinterest.com/pin/123",
                    "title": "Pinterest Pin",
                    "snippet": "Should be excluded",
                    "position": 2
                }
            ]
        }
        mock_get.return_value = mock_response

        adapter = WebSearchAdapter(
            api_key=mock_env_config["SERP_API_KEY"],
            config=sample_sources_config["sources"]["web"],
            provider_config={}
        )

        results = adapter.search("test", "7d")

        # Pinterest should be excluded
        assert len(results) == 1
        assert "pinterest.com" not in results[0].url

    def test_parse_time_range(self, mock_env_config, sample_sources_config):
        """Test time range parsing."""
        adapter = WebSearchAdapter(
            api_key=mock_env_config["SERP_API_KEY"],
            config=sample_sources_config["sources"]["web"],
            provider_config={}
        )

        assert adapter._parse_time_range("1d") == "d"
        assert adapter._parse_time_range("7d") == "w"
        assert adapter._parse_time_range("30d") == "m"
        assert adapter._parse_time_range("365d") == "y"
        assert adapter._parse_time_range("invalid") == "w"  # Default


class TestGitHubSearchAdapter:
    """Test GitHub search adapter functionality."""

    @patch('nixtla_search_to_slack.search_orchestrator.requests.get')
    def test_github_search_issues(self, mock_get, mock_env_config, sample_sources_config):
        """Test GitHub issue search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "html_url": "https://github.com/Nixtla/TimeGPT/issues/1",
                    "title": "Bug: Issue with forecasting",
                    "body": "Detailed bug description",
                    "created_at": "2024-01-01T00:00:00Z",
                    "state": "open",
                    "user": {"login": "user1"},
                    "labels": [{"name": "bug"}],
                    "repository_url": "https://api.github.com/repos/Nixtla/TimeGPT"
                }
            ]
        }
        mock_get.return_value = mock_response

        adapter = GitHubSearchAdapter(
            token=mock_env_config["GITHUB_TOKEN"],
            config=sample_sources_config["sources"]["github"]
        )

        results = adapter._search_issues("bug", ["org:Nixtla"], "created:>=2024-01-01", "issues")

        assert len(results) == 1
        assert results[0].source == "github"
        assert results[0].metadata["type"] == "issues"
        assert results[0].metadata["state"] == "open"
        assert "bug" in results[0].metadata["labels"]

    @patch('nixtla_search_to_slack.search_orchestrator.requests.get')
    def test_github_search_releases(self, mock_get, mock_env_config, sample_sources_config):
        """Test GitHub release search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "html_url": "https://github.com/Nixtla/TimeGPT/releases/v2.0.0",
                "name": "TimeGPT v2.0.0",
                "tag_name": "v2.0.0",
                "body": "Major release with TimeGPT improvements",
                "published_at": "2024-01-15T00:00:00Z",
                "prerelease": False
            }
        ]
        mock_get.return_value = mock_response

        adapter = GitHubSearchAdapter(
            token=mock_env_config["GITHUB_TOKEN"],
            config=sample_sources_config["sources"]["github"]
        )

        # Note: In the real implementation, this would be called from search()
        results = adapter._search_releases("TimeGPT", [], "")

        assert len(results) > 0
        if results:  # May be empty if keyword not matched
            assert results[0].source == "github"
            assert results[0].metadata["type"] == "release"

    def test_calculate_date_filter(self, mock_env_config, sample_sources_config):
        """Test GitHub date filter calculation."""
        adapter = GitHubSearchAdapter(
            token=mock_env_config["GITHUB_TOKEN"],
            config=sample_sources_config["sources"]["github"]
        )

        # Test date filter generation
        filter_7d = adapter._calculate_date_filter("7d")
        assert "created:>=" in filter_7d

        # Test invalid format
        filter_invalid = adapter._calculate_date_filter("invalid")
        assert filter_invalid == ""