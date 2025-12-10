"""
AI curator - Uses Claude Code's built-in capabilities.

This plugin runs inside Claude Code, which IS Claude.
No external AI API keys needed - Claude curates content directly.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from .content_aggregator import Content

logger = logging.getLogger(__name__)


@dataclass
class CuratedContent:
    """Represents curated content ready for Slack."""

    content: Content
    summary: str
    key_points: List[str]
    why_it_matters: str
    relevance_score: int  # 0-100


class AICurator:
    """
    Stub curator for Claude Code plugin.

    When running inside Claude Code, AI curation is performed by Claude
    directly during the conversation. This class provides pass-through
    functionality with keyword-based relevance scoring.

    Workflow:
    1. User asks Claude to search for Nixtla content
    2. Claude uses built-in WebSearch tool
    3. Claude curates/summarizes results (built-in capability)
    4. This plugin posts curated content to Slack

    No external API keys needed - Claude Code IS the AI.
    """

    # Keywords for relevance scoring
    NIXTLA_KEYWORDS = [
        "timegpt",
        "statsforecast",
        "mlforecast",
        "neuralforecast",
        "nixtla",
        "time series",
        "time-series",
        "forecasting",
        "prediction",
        "arima",
        "lstm",
        "prophet",
        "autoets",
        "autotheta",
        "seasonal",
    ]

    def __init__(self, env_config: Dict[str, str] = None):
        """
        Initialize the curator.

        Args:
            env_config: Environment configuration (not used - no API keys needed)
        """
        self.env_config = env_config or {}
        logger.info("AI Curator initialized (using Claude Code built-in capabilities)")

    def curate(self, content_list: List[Content]) -> List[CuratedContent]:
        """
        Prepare content for Slack posting.

        Claude Code performs actual curation during the conversation.
        This method provides basic relevance scoring and formatting.

        Args:
            content_list: List of content to process

        Returns:
            List of curated content ready for Slack
        """
        curated = []

        for content in content_list:
            curated_item = self._process_content(content)
            curated.append(curated_item)
            logger.debug(f"Processed: {content.title[:50]}...")

        return curated

    def _process_content(self, content: Content) -> CuratedContent:
        """
        Process a single content item.

        Uses keyword-based relevance scoring. Actual AI summarization
        happens in Claude Code's conversation context.

        Args:
            content: Content to process

        Returns:
            Curated content with relevance score
        """
        # Use description as summary (Claude will have already summarized in conversation)
        summary = content.description[:300] if content.description else content.title

        # Extract key points from description
        key_points = self._extract_key_points(content.description)

        # Calculate relevance based on Nixtla-related keywords
        relevance_score = self._calculate_relevance(content)

        # Generic "why it matters" - Claude provides real insights in conversation
        why_it_matters = self._generate_why_it_matters(content, relevance_score)

        return CuratedContent(
            content=content,
            summary=summary,
            key_points=key_points,
            why_it_matters=why_it_matters,
            relevance_score=relevance_score,
        )

    def _extract_key_points(self, description: str) -> List[str]:
        """Extract key points from description."""
        if not description:
            return ["See source for details"]

        # Split into sentences and take first 3 meaningful ones
        sentences = description.replace("\n", ". ").split(".")
        key_points = []

        for sentence in sentences:
            cleaned = sentence.strip()
            if len(cleaned) > 20 and len(key_points) < 3:
                key_points.append(cleaned)

        return key_points if key_points else ["See source for details"]

    def _calculate_relevance(self, content: Content) -> int:
        """
        Calculate relevance score based on Nixtla-related keywords.

        Args:
            content: Content to score

        Returns:
            Relevance score 0-100
        """
        text = f"{content.title} {content.description}".lower()

        # Count keyword matches
        keyword_matches = sum(1 for kw in self.NIXTLA_KEYWORDS if kw in text)

        # Base score 30, +10 per keyword match, max 100
        score = min(100, 30 + (keyword_matches * 10))

        # Boost for direct Nixtla mentions
        if "nixtla" in text:
            score = min(100, score + 20)
        if "timegpt" in text:
            score = min(100, score + 15)

        return score

    def _generate_why_it_matters(self, content: Content, relevance_score: int) -> str:
        """Generate contextual relevance statement."""
        if relevance_score >= 80:
            return "Directly relevant to Nixtla ecosystem and time-series forecasting."
        elif relevance_score >= 60:
            return "Relevant to time-series forecasting practitioners."
        elif relevance_score >= 40:
            return "May be of interest to data scientists and ML engineers."
        else:
            return "General interest for the forecasting community."
