"""
Web search provider - Uses Claude Code's built-in WebSearch.

This plugin runs inside Claude Code, which has WebSearch built-in.
No external API keys needed for web search.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class WebSearchResult:
    """Represents a single web search result."""

    url: str
    title: str
    description: str
    timestamp: datetime
    metadata: Dict[str, Any]


class ClaudeCodeWebSearchProvider:
    """
    Stub provider for Claude Code's built-in WebSearch.

    When running inside Claude Code, web searches are performed by Claude
    using its native WebSearch tool. This class exists for compatibility
    with the existing architecture.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        logger.info("Using Claude Code WebSearch (no API key needed)")

    def is_configured(self) -> bool:
        """Always configured - Claude Code handles search."""
        return True

    def search(
        self, query: str, max_results: int = 10, time_range: str = "7d"
    ) -> List[WebSearchResult]:
        """
        Return empty list - Claude Code performs searches directly.

        When using this plugin:
        1. Ask Claude to search for the topic
        2. Claude uses WebSearch tool
        3. Pass results to aggregator/curator
        4. Post to Slack
        """
        logger.info(f"Web search for '{query}' - handled by Claude Code WebSearch")
        logger.info("Tip: Ask Claude to search, then use results with this plugin")
        return []


def create_web_search_provider(
    env_config: Dict[str, str] = None, provider_config: Dict[str, Any] = None
) -> ClaudeCodeWebSearchProvider:
    """
    Factory function - returns Claude Code WebSearch provider.

    No API keys needed. Claude Code has built-in WebSearch.
    """
    return ClaudeCodeWebSearchProvider(config=provider_config or {})
