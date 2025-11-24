"""
Web search providers with support for multiple APIs.
Users can choose from FREE and PAID options.
"""

import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)


@dataclass
class WebSearchResult:
    """Represents a single web search result."""
    url: str
    title: str
    description: str
    timestamp: datetime
    metadata: Dict[str, Any]


class BaseWebSearchProvider(ABC):
    """Base class for all web search providers."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the search provider.

        Args:
            config: Provider-specific configuration
        """
        self.config = config

    @abstractmethod
    def search(self, query: str, max_results: int = 10, time_range: str = "7d") -> List[WebSearchResult]:
        """
        Execute a web search.

        Args:
            query: Search query
            max_results: Maximum number of results to return
            time_range: Time range for results (e.g., "7d", "30d")

        Returns:
            List of search results
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if this provider is properly configured."""
        pass

    def _parse_time_range_days(self, time_range: str) -> int:
        """Convert time range string to number of days."""
        if time_range.endswith("d"):
            return int(time_range[:-1])
        elif time_range.endswith("w"):
            return int(time_range[:-1]) * 7
        elif time_range.endswith("m"):
            return int(time_range[:-1]) * 30
        elif time_range.endswith("y"):
            return int(time_range[:-1]) * 365
        return 7  # Default to 7 days


class BraveSearchProvider(BaseWebSearchProvider):
    """Brave Search API provider (FREE - 2,000 queries/month)."""

    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, max_results: int = 10, time_range: str = "7d") -> List[WebSearchResult]:
        """Search using Brave Search API."""
        if not self.is_configured():
            raise ValueError("Brave Search API key not configured")

        results = []
        days = self._parse_time_range_days(time_range)

        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key
            }

            params = {
                "q": query,
                "count": max_results,
                "freshness": f"pd{days}" if days <= 30 else "pm",  # past day/month
            }

            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("web", {}).get("results", [])[:max_results]:
                # Skip excluded domains
                if any(domain in item.get("url", "") for domain in self.config.get("exclude_domains", [])):
                    continue

                results.append(WebSearchResult(
                    url=item.get("url", ""),
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    timestamp=datetime.now(),
                    metadata={
                        "provider": "brave",
                        "age": item.get("age", ""),
                        "language": item.get("language", ""),
                    }
                ))

            logger.info(f"Brave Search returned {len(results)} results")

        except Exception as e:
            logger.error(f"Brave Search failed: {e}")

        return results


class GoogleCustomSearchProvider(BaseWebSearchProvider):
    """Google Custom Search API provider (FREE - 100 queries/day)."""

    def __init__(self, api_key: str, search_engine_id: str, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def is_configured(self) -> bool:
        return bool(self.api_key and self.search_engine_id)

    def search(self, query: str, max_results: int = 10, time_range: str = "7d") -> List[WebSearchResult]:
        """Search using Google Custom Search API."""
        if not self.is_configured():
            raise ValueError("Google Custom Search API key or Search Engine ID not configured")

        results = []
        days = self._parse_time_range_days(time_range)

        try:
            # Google CSE supports dateRestrict parameter
            date_restrict = f"d{days}" if days <= 30 else "m1"

            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": query,
                "num": min(max_results, 10),  # Google CSE max is 10 per request
                "dateRestrict": date_restrict,
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", [])[:max_results]:
                # Skip excluded domains
                if any(domain in item.get("link", "") for domain in self.config.get("exclude_domains", [])):
                    continue

                results.append(WebSearchResult(
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    description=item.get("snippet", ""),
                    timestamp=datetime.now(),
                    metadata={
                        "provider": "google",
                        "displayLink": item.get("displayLink", ""),
                    }
                ))

            logger.info(f"Google Custom Search returned {len(results)} results")

        except Exception as e:
            logger.error(f"Google Custom Search failed: {e}")

        return results


class BingSearchProvider(BaseWebSearchProvider):
    """Bing Web Search API provider (FREE - 1,000 queries/month)."""

    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = api_key
        self.base_url = "https://api.bing.microsoft.com/v7.0/search"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, max_results: int = 10, time_range: str = "7d") -> List[WebSearchResult]:
        """Search using Bing Web Search API."""
        if not self.is_configured():
            raise ValueError("Bing Search API key not configured")

        results = []
        days = self._parse_time_range_days(time_range)

        try:
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key
            }

            # Bing uses freshness parameter
            freshness = "Day" if days == 1 else "Week" if days <= 7 else "Month"

            params = {
                "q": query,
                "count": max_results,
                "freshness": freshness,
                "responseFilter": "Webpages",
            }

            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("webPages", {}).get("value", [])[:max_results]:
                # Skip excluded domains
                if any(domain in item.get("url", "") for domain in self.config.get("exclude_domains", [])):
                    continue

                results.append(WebSearchResult(
                    url=item.get("url", ""),
                    title=item.get("name", ""),
                    description=item.get("snippet", ""),
                    timestamp=datetime.now(),
                    metadata={
                        "provider": "bing",
                        "displayUrl": item.get("displayUrl", ""),
                        "dateLastCrawled": item.get("dateLastCrawled", ""),
                    }
                ))

            logger.info(f"Bing Search returned {len(results)} results")

        except Exception as e:
            logger.error(f"Bing Search failed: {e}")

        return results


class DuckDuckGoProvider(BaseWebSearchProvider):
    """DuckDuckGo search provider (100% FREE - No API key needed)."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = "https://api.duckduckgo.com/"

    def is_configured(self) -> bool:
        return True  # Always available, no API key needed

    def search(self, query: str, max_results: int = 10, time_range: str = "7d") -> List[WebSearchResult]:
        """
        Search using DuckDuckGo Instant Answer API.

        Note: DDG's free API is limited to instant answers, not full web search.
        For full web search, would need to use unofficial scraping (not recommended).
        This implementation uses the official API with its limitations.
        """
        results = []

        try:
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1,
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # DuckDuckGo Instant Answer API returns different structure
            # Abstract is the main result
            if data.get("Abstract"):
                results.append(WebSearchResult(
                    url=data.get("AbstractURL", ""),
                    title=data.get("Heading", query),
                    description=data.get("Abstract", ""),
                    timestamp=datetime.now(),
                    metadata={
                        "provider": "duckduckgo",
                        "type": "abstract",
                    }
                ))

            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results - 1]:
                if isinstance(topic, dict) and topic.get("FirstURL"):
                    results.append(WebSearchResult(
                        url=topic.get("FirstURL", ""),
                        title=topic.get("Text", "")[:100],  # Use first part as title
                        description=topic.get("Text", ""),
                        timestamp=datetime.now(),
                        metadata={
                            "provider": "duckduckgo",
                            "type": "related",
                        }
                    ))

            logger.info(f"DuckDuckGo returned {len(results)} results")

        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")

        return results


class SerpAPIProvider(BaseWebSearchProvider):
    """SerpAPI provider (PAID - $50/month minimum)."""

    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, max_results: int = 10, time_range: str = "7d") -> List[WebSearchResult]:
        """Search using SerpAPI (original implementation)."""
        if not self.is_configured():
            raise ValueError("SerpAPI key not configured")

        results = []

        try:
            # Parse time range for Google's tbs parameter
            days = self._parse_time_range_days(time_range)
            if days == 1:
                date_restrict = "d"
            elif days <= 7:
                date_restrict = "w"
            elif days <= 30:
                date_restrict = "m"
            else:
                date_restrict = "y"

            params = {
                "api_key": self.api_key,
                "q": query,
                "num": max_results,
            }

            if date_restrict:
                params["tbs"] = f"qdr:{date_restrict}"

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for item in data.get("organic_results", [])[:max_results]:
                # Skip excluded domains
                if any(domain in item.get("link", "") for domain in self.config.get("exclude_domains", [])):
                    continue

                results.append(WebSearchResult(
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    description=item.get("snippet", ""),
                    timestamp=datetime.now(),
                    metadata={
                        "provider": "serpapi",
                        "position": item.get("position", 0),
                        "domain": item.get("displayed_link", ""),
                    }
                ))

            logger.info(f"SerpAPI returned {len(results)} results")

        except Exception as e:
            logger.error(f"SerpAPI search failed: {e}")

        return results


def create_web_search_provider(env_config: Dict[str, str], provider_config: Dict[str, Any]) -> BaseWebSearchProvider:
    """
    Factory function to create the appropriate web search provider.

    Priority order (first configured provider wins):
    1. Brave Search (FREE - 2,000/month)
    2. Google Custom Search (FREE - 100/day)
    3. Bing Search (FREE - 1,000/month)
    4. DuckDuckGo (FREE - unlimited, limited features)
    5. SerpAPI (PAID - $50/month)

    Args:
        env_config: Environment variables
        provider_config: Provider configuration

    Returns:
        Configured search provider

    Raises:
        ValueError: If no provider is configured
    """
    # Check for Brave Search (FREE - RECOMMENDED)
    if env_config.get("BRAVE_API_KEY"):
        logger.info("Using Brave Search (FREE - 2,000 queries/month)")
        return BraveSearchProvider(
            api_key=env_config["BRAVE_API_KEY"],
            config=provider_config
        )

    # Check for Google Custom Search (FREE)
    if env_config.get("GOOGLE_API_KEY") and env_config.get("GOOGLE_SEARCH_ENGINE_ID"):
        logger.info("Using Google Custom Search (FREE - 100 queries/day)")
        return GoogleCustomSearchProvider(
            api_key=env_config["GOOGLE_API_KEY"],
            search_engine_id=env_config["GOOGLE_SEARCH_ENGINE_ID"],
            config=provider_config
        )

    # Check for Bing Search (FREE)
    if env_config.get("BING_API_KEY"):
        logger.info("Using Bing Search (FREE - 1,000 queries/month)")
        return BingSearchProvider(
            api_key=env_config["BING_API_KEY"],
            config=provider_config
        )

    # DuckDuckGo (Always available, no key needed - but limited)
    # Note: Only use as fallback due to limitations
    use_duckduckgo = env_config.get("USE_DUCKDUCKGO", "false").lower() == "true"
    if use_duckduckgo:
        logger.info("Using DuckDuckGo (FREE - unlimited, but limited features)")
        logger.warning("DuckDuckGo Instant Answer API has limited search capabilities")
        return DuckDuckGoProvider(config=provider_config)

    # Check for SerpAPI (PAID)
    if env_config.get("SERP_API_KEY"):
        logger.info("Using SerpAPI (PAID - $50/month)")
        return SerpAPIProvider(
            api_key=env_config["SERP_API_KEY"],
            config=provider_config
        )

    # No provider configured
    raise ValueError(
        "No web search provider configured. Set one of:\n"
        "  BRAVE_API_KEY (free - 2,000/month - recommended)\n"
        "  GOOGLE_API_KEY + GOOGLE_SEARCH_ENGINE_ID (free - 100/day)\n"
        "  BING_API_KEY (free - 1,000/month)\n"
        "  USE_DUCKDUCKGO=true (free - unlimited, limited features)\n"
        "  SERP_API_KEY (paid - $50/month)"
    )
