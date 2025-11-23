"""
Search orchestrator for coordinating multiple search sources.
MVP implementation with web and GitHub search only.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass
from urllib.parse import urlencode

import requests

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
                api_key=self.env_config.get("SERP_API_KEY"),
                config=self.sources_config["sources"]["web"],
                provider_config=self.sources_config.get("api_providers", {}).get("serpapi", {})
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
    """Adapter for web search using SerpAPI."""

    def __init__(self, api_key: str, config: Dict[str, Any], provider_config: Dict[str, Any]):
        """
        Initialize web search adapter.

        Args:
            api_key: SerpAPI key
            config: Source-specific configuration
            provider_config: Provider API configuration
        """
        self.api_key = api_key
        self.config = config
        self.provider_config = provider_config

    def search(self, query: str, time_range: str) -> List[SearchResult]:
        """
        Search the web using SerpAPI.

        Args:
            query: Search query
            time_range: Time range for results (e.g., "7d")

        Returns:
            List of search results
        """
        results = []

        # Parse time range
        date_restrict = self._parse_time_range(time_range)

        # Combine with base queries if configured
        base_queries = self.config.get("base_queries", [])
        if base_queries:
            # Use first base query as context
            query = f"{base_queries[0]} {query}"

        # Build API request
        params = {
            "api_key": self.api_key,
            "q": query,
            "num": self.config.get("max_results", 10),
            **self.provider_config.get("default_params", {})
        }

        if date_restrict:
            params["tbs"] = f"qdr:{date_restrict}"  # Google date restrict format

        try:
            # Note: In production, use proper SerpAPI client library
            url = f"{self.provider_config.get('base_url', 'https://serpapi.com/search')}"
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Parse organic results
            for item in data.get("organic_results", [])[:self.config.get("max_results", 10)]:
                # Skip excluded domains
                if any(domain in item.get("link", "") for domain in self.config.get("exclude_domains", [])):
                    continue

                results.append(SearchResult(
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    description=item.get("snippet", ""),
                    source="web",
                    timestamp=datetime.now(),
                    metadata={
                        "position": item.get("position", 0),
                        "domain": item.get("displayed_link", ""),
                        "date": item.get("date", "")
                    }
                ))

        except Exception as e:
            logger.error(f"Web search failed: {e}")

        return results

    def _parse_time_range(self, time_range: str) -> str:
        """Convert time range to SerpAPI format."""
        if time_range.endswith("d"):
            days = int(time_range[:-1])
            if days == 1:
                return "d"
            elif days <= 7:
                return "w"
            elif days <= 30:
                return "m"
            else:
                return "y"
        return "w"  # Default to week


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