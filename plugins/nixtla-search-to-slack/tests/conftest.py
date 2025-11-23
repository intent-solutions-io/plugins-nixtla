"""
Pytest configuration and fixtures for Nixtla Search-to-Slack tests.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

import pytest
import yaml


@pytest.fixture
def mock_env_config():
    """Mock environment configuration."""
    return {
        "SLACK_BOT_TOKEN": "xoxb-test-token",
        "SERP_API_KEY": "test-serp-key",
        "GITHUB_TOKEN": "ghp_test_token",
        "OPENAI_API_KEY": "sk-test-key",
    }


@pytest.fixture
def sample_sources_config():
    """Sample sources configuration."""
    return {
        "api_providers": {
            "serpapi": {
                "base_url": "https://serpapi.com/search",
                "default_params": {"gl": "us", "hl": "en"}
            }
        },
        "sources": {
            "web": {
                "provider": "serpapi",
                "max_results": 5,
                "time_range": "7d",
                "base_queries": ["Nixtla TimeGPT"],
                "exclude_domains": ["pinterest.com"]
            },
            "github": {
                "api_base": "https://api.github.com",
                "organizations": ["Nixtla"],
                "additional_repos": ["facebook/prophet"],
                "content_types": ["issues", "releases"],
                "max_results": 10,
                "time_range": "7d"
            }
        }
    }


@pytest.fixture
def sample_topics_config():
    """Sample topics configuration."""
    return {
        "topics": {
            "test-topic": {
                "name": "Test Topic",
                "description": "Test description",
                "keywords": ["TimeGPT", "forecasting"],
                "sources": ["web", "github"],
                "filters": {"min_relevance": 50},
                "slack_channel": "#test-channel"
            }
        },
        "default_topic": "test-topic"
    }


@pytest.fixture
def sample_search_results():
    """Sample search results for testing."""
    from nixtla_search_to_slack.search_orchestrator import SearchResult

    return [
        SearchResult(
            url="https://example.com/article1",
            title="TimeGPT 2.0 Released",
            description="New version with multivariate support",
            source="web",
            timestamp=datetime.now(),
            metadata={"position": 1}
        ),
        SearchResult(
            url="https://github.com/Nixtla/TimeGPT/releases/v2.0",
            title="Release v2.0",
            description="Major update with new features",
            source="github",
            timestamp=datetime.now(),
            metadata={"type": "release"}
        ),
        SearchResult(
            url="https://example.com/article1?utm_source=twitter",  # Duplicate with tracking
            title="TimeGPT 2.0 Released",
            description="New version with multivariate support",
            source="web",
            timestamp=datetime.now(),
            metadata={"position": 2}
        )
    ]


@pytest.fixture
def sample_content():
    """Sample content for testing."""
    from nixtla_search_to_slack.content_aggregator import Content

    return [
        Content(
            url="https://example.com/article1",
            title="TimeGPT 2.0 Released",
            description="New version with multivariate support for time series forecasting",
            source="web",
            timestamp=datetime.now(),
            metadata={"position": 1}
        ),
        Content(
            url="https://github.com/Nixtla/TimeGPT/releases/v2.0",
            title="Release v2.0",
            description="Major update with new features including async support",
            source="github",
            timestamp=datetime.now(),
            metadata={"type": "release"}
        )
    ]


@pytest.fixture
def sample_curated_content(sample_content):
    """Sample curated content for testing."""
    from nixtla_search_to_slack.ai_curator import CuratedContent

    return [
        CuratedContent(
            content=sample_content[0],
            summary="TimeGPT 2.0 introduces multivariate forecasting capabilities.",
            key_points=[
                "Supports up to 100 variables",
                "15% accuracy improvement",
                "New async Python SDK"
            ],
            why_it_matters="Enables enterprise-scale forecasting previously requiring custom solutions.",
            relevance_score=95
        ),
        CuratedContent(
            content=sample_content[1],
            summary="Major release of TimeGPT with breaking changes and new features.",
            key_points=[
                "Async support added",
                "Performance improvements",
                "New API endpoints"
            ],
            why_it_matters="Critical update for production TimeGPT deployments.",
            relevance_score=90
        )
    ]


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("DRY_RUN", "true")  # Prevent actual Slack posts in tests