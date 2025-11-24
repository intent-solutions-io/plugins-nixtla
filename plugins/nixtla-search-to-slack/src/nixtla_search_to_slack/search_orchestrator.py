"""
Search orchestrator for coordinating multiple search sources.
Supports multiple web search providers (FREE and PAID options).
"""

import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass
from urllib.parse import urlencode

import requests

from .web_search_providers import create_web_search_provider, WebSearchResult

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Represents a single search result."""
    url: str
    title: str
    description: str
    source: str  # 'web' or 'github'
    timestamp: datetime
    metadata: Dict[str, Any]


class SearchOrchestrator:
    """Orchestrates searches across multiple sources."""

    def __init__(self, sources_config: Dict[str, Any], env_config: Dict[str, str]):
        """
        Initialize the search orchestrator.

        Args:
            sources_config: Configuration for search sources
            env_config: Environment variables configuration
        """
        self.sources_config = sources_config
        self.env_config = env_config
        self.adapters = self._initialize_adapters()

    def _initialize_adapters(self) -> Dict[str, Any]:
        """Initialize search adapters based on configuration."""
        adapters = {}

        # Initialize web search adapter if configured
        if "web" in self.sources_config["sources"]:
            adapters["web"] = WebSearchAdapter(
                env_config=self.env_config,
                config=self.sources_config["sources"]["web"]
            )

        # Initialize GitHub search adapter if configured
        if "github" in self.sources_config["sources"]:
            adapters["github"] = GitHubSearchAdapter(
                token=self.env_config.get("GITHUB_TOKEN"),
                config=self.sources_config["sources"]["github"]
            )

        logger.info(f"Initialized {len(adapters)} search adapters")
        return adapters

    def search(self, topic: Dict[str, Any]) -> List[SearchResult]:
        """
        Execute searches for a given topic across all configured sources.

        Args:
            topic: Topic configuration with keywords and sources

        Returns:
            List of search results from all sources
        """
        results = []
        query = " OR ".join(topic["keywords"][:5])  # Limit keywords for query length

        for source_name in topic.get("sources", []):
            if source_name not in self.adapters:
                logger.warning(f"Source '{source_name}' not configured, skipping")
                continue

            try:
                logger.info(f"Searching {source_name} for topic: {topic['name']}")
                adapter = self.adapters[source_name]
                source_results = adapter.search(
                    query=query,
                    time_range=self.sources_config["sources"][source_name].get("time_range", "7d")
                )
                results.extend(source_results)
                logger.info(f"Found {len(source_results)} results from {source_name}")

            except Exception as e:
                logger.error(f"Search failed for source {source_name}: {e}")
                # Continue with other sources even if one fails

        return results


class WebSearchAdapter:
    """
    Adapter for web search using multiple providers.

    Supports FREE and PAID options:
    - Brave Search (FREE - 2,000/month)
    - Google Custom Search (FREE - 100/day)
    - Bing Search (FREE - 1,000/month)
    - DuckDuckGo (FREE - unlimited, limited features)
    - SerpAPI (PAID - $50/month)
    """

    def __init__(self, env_config: Dict[str, str], config: Dict[str, Any]):
        """
        Initialize web search adapter with provider auto-detection.

        Args:
            env_config: Environment variables (contains API keys)
            config: Source-specific configuration
        """
        self.config = config
        self.env_config = env_config

        # Create the appropriate provider based on available API keys
        self.provider = create_web_search_provider(env_config, config)
        logger.info(f"Web search initialized with provider: {self.provider.__class__.__name__}")

    def search(self, query: str, time_range: str) -> List[SearchResult]:
        """
        Search the web using the configured provider.

        Args:
            query: Search query
            time_range: Time range for results (e.g., "7d")

        Returns:
            List of search results
        """
        results = []

        # Combine with base queries if configured
        base_queries = self.config.get("base_queries", [])
        if base_queries:
            query = f"{base_queries[0]} {query}"

        try:
            # Call the provider's search method
            web_results = self.provider.search(
                query=query,
                max_results=self.config.get("max_results", 10),
                time_range=time_range
            )

            # Convert WebSearchResult to SearchResult format
            for web_result in web_results:
                results.append(SearchResult(
                    url=web_result.url,
                    title=web_result.title,
                    description=web_result.description,
                    source="web",
                    timestamp=web_result.timestamp,
                    metadata=web_result.metadata
                ))

        except Exception as e:
            logger.error(f"Web search failed: {e}")

        return results


class GitHubSearchAdapter:
    """Adapter for GitHub search using GitHub API."""

    def __init__(self, token: str, config: Dict[str, Any]):
        """
        Initialize GitHub search adapter.

        Args:
            token: GitHub API token
            config: Source-specific configuration
        """
        self.token = token
        self.config = config
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def search(self, query: str, time_range: str) -> List[SearchResult]:
        """
        Search GitHub repositories and issues.

        Args:
            query: Search query
            time_range: Time range for results

        Returns:
            List of search results
        """
        results = []

        # Calculate date filter
        date_filter = self._calculate_date_filter(time_range)

        # Build organization/repo filters
        org_filters = []
        for org in self.config.get("organizations", []):
            org_filters.append(f"org:{org}")

        for repo in self.config.get("additional_repos", []):
            org_filters.append(f"repo:{repo}")

        # Search different content types
        content_types = self.config.get("content_types", ["issues", "pull_requests", "releases"])

        for content_type in content_types:
            try:
                if content_type in ["issues", "pull_requests"]:
                    results.extend(self._search_issues(query, org_filters, date_filter, content_type))
                elif content_type == "releases":
                    results.extend(self._search_releases(query, org_filters, date_filter))
                # Note: GitHub API doesn't have direct discussion search in MVP

            except Exception as e:
                logger.error(f"GitHub {content_type} search failed: {e}")

        return results[:self.config.get("max_results", 20)]

    def _search_issues(self, query: str, org_filters: List[str], date_filter: str,
                      content_type: str) -> List[SearchResult]:
        """Search GitHub issues and pull requests."""
        results = []

        # Build search query
        type_filter = "is:issue" if content_type == "issues" else "is:pr"
        org_query = " OR ".join(f"({f})" for f in org_filters) if org_filters else ""
        full_query = f"{query} {type_filter} {date_filter} {org_query}".strip()

        url = f"{self.config.get('api_base', 'https://api.github.com')}/search/issues"
        params = {
            "q": full_query,
            "sort": "created",
            "order": "desc",
            "per_page": min(self.config.get("max_results", 20), 30)
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                results.append(SearchResult(
                    url=item.get("html_url", ""),
                    title=item.get("title", ""),
                    description=item.get("body", "")[:300] if item.get("body") else "",
                    source="github",
                    timestamp=datetime.fromisoformat(item.get("created_at", "").replace("Z", "+00:00")),
                    metadata={
                        "type": content_type,
                        "state": item.get("state", ""),
                        "repository": item.get("repository_url", "").split("/")[-1] if item.get("repository_url") else "",
                        "author": item.get("user", {}).get("login", ""),
                        "labels": [label["name"] for label in item.get("labels", [])]
                    }
                ))

        except Exception as e:
            logger.error(f"GitHub issues search error: {e}")

        return results

    def _search_releases(self, query: str, org_filters: List[str], date_filter: str) -> List[SearchResult]:
        """Search GitHub releases (simplified for MVP)."""
        results = []

        # For MVP, we'll check releases for specific repos
        for repo in self.config.get("additional_repos", []):
            try:
                url = f"{self.config.get('api_base', 'https://api.github.com')}/repos/{repo}/releases"
                params = {"per_page": 10}

                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                for release in data:
                    # Simple keyword matching in release name/body
                    if any(keyword.lower() in (release.get("name", "") + release.get("body", "")).lower()
                          for keyword in query.split()):
                        results.append(SearchResult(
                            url=release.get("html_url", ""),
                            title=f"{repo}: {release.get('name', release.get('tag_name', ''))}",
                            description=release.get("body", "")[:300] if release.get("body") else "",
                            source="github",
                            timestamp=datetime.fromisoformat(release.get("published_at", "").replace("Z", "+00:00")),
                            metadata={
                                "type": "release",
                                "tag": release.get("tag_name", ""),
                                "repository": repo,
                                "prerelease": release.get("prerelease", False)
                            }
                        ))

            except Exception as e:
                logger.debug(f"Could not fetch releases for {repo}: {e}")

        return results

    def _calculate_date_filter(self, time_range: str) -> str:
        """Calculate GitHub date filter from time range."""
        if time_range.endswith("d"):
            days = int(time_range[:-1])
            date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            return f"created:>={date}"
        return ""