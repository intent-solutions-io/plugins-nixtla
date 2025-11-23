"""
AI curator for generating summaries and insights using LLMs.
MVP implementation with support for OpenAI and Anthropic.
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .content_aggregator import Content

logger = logging.getLogger(__name__)

# Import LLM libraries conditionally
try:
    import openai
except ImportError:
    openai = None
    logger.debug("OpenAI library not installed")

try:
    import anthropic
except ImportError:
    anthropic = None
    logger.debug("Anthropic library not installed")


@dataclass
class CuratedContent:
    """Represents AI-curated content with summary and insights."""
    content: Content
    summary: str
    key_points: List[str]
    why_it_matters: str
    relevance_score: int  # 0-100


class AICurator:
    """Curates content using AI to generate summaries and insights."""

    SYSTEM_PROMPT = """You are a specialized AI curator for time-series forecasting and Nixtla ecosystem content.
Your task is to summarize technical content for data scientists and ML engineers.
Focus on practical implications and technical insights.
Be concise but informative. Avoid marketing language."""

    def __init__(self, env_config: Dict[str, str]):
        """
        Initialize the AI curator.

        Args:
            env_config: Environment configuration with API keys
        """
        self.env_config = env_config
        self.llm_provider = self._determine_provider()
        self.llm_client = self._initialize_client()

    def _determine_provider(self) -> str:
        """Determine which LLM provider to use based on available keys."""
        if self.env_config.get("OPENAI_API_KEY") and openai:
            return "openai"
        elif self.env_config.get("ANTHROPIC_API_KEY") and anthropic:
            return "anthropic"
        else:
            raise ValueError("No LLM provider configured. Need OPENAI_API_KEY or ANTHROPIC_API_KEY")

    def _initialize_client(self):
        """Initialize the LLM client based on provider."""
        if self.llm_provider == "openai":
            if not openai:
                raise ImportError("OpenAI library not installed. Run: pip install openai")
            openai.api_key = self.env_config["OPENAI_API_KEY"]
            return openai
        elif self.llm_provider == "anthropic":
            if not anthropic:
                raise ImportError("Anthropic library not installed. Run: pip install anthropic")
            return anthropic.Anthropic(api_key=self.env_config["ANTHROPIC_API_KEY"])
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def curate(self, content_list: List[Content]) -> List[CuratedContent]:
        """
        Generate AI summaries for a list of content items.

        Args:
            content_list: List of content to curate

        Returns:
            List of curated content with summaries
        """
        curated = []

        for content in content_list:
            try:
                # Generate summary for this content
                curated_item = self._curate_single(content)
                curated.append(curated_item)
                logger.debug(f"Curated content: {content.title[:50]}...")

            except Exception as e:
                logger.error(f"Failed to curate content {content.url}: {e}")
                # Create fallback curated content
                curated.append(self._create_fallback(content))

        return curated

    def _curate_single(self, content: Content) -> CuratedContent:
        """
        Generate AI summary for a single content item.

        Args:
            content: Content to curate

        Returns:
            Curated content with AI-generated insights
        """
        # Build the prompt
        prompt = self._build_prompt(content)

        # Call LLM
        response_text = self._call_llm(prompt)

        # Parse response
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM JSON response, using fallback")
            return self._create_fallback(content)

        # Extract fields with defaults
        summary = response_data.get("summary", content.description[:200])
        key_points = response_data.get("key_points", [])
        if not isinstance(key_points, list):
            key_points = []
        key_points = key_points[:3]  # Limit to 3 points

        why_it_matters = response_data.get("why_it_matters", "Relevant to time-series forecasting practitioners.")
        relevance_score = response_data.get("relevance_score", 50)

        # Ensure relevance score is in range
        try:
            relevance_score = max(0, min(100, int(relevance_score)))
        except (ValueError, TypeError):
            relevance_score = 50

        return CuratedContent(
            content=content,
            summary=summary,
            key_points=key_points,
            why_it_matters=why_it_matters,
            relevance_score=relevance_score
        )

    def _build_prompt(self, content: Content) -> str:
        """Build the prompt for LLM curation."""
        return f"""Analyze this content and provide:
1. A 2-3 sentence summary focusing on technical aspects
2. 2-3 key technical points (as a list)
3. 1-2 sentences on why this matters specifically for Nixtla ecosystem users or time-series forecasting practitioners
4. A relevance score from 0-100 for Nixtla/time-series practitioners

Content to analyze:
Title: {content.title}
Description: {content.description[:500]}
Source: {content.source}
URL: {content.url}

Context: This is for practitioners using Nixtla tools (TimeGPT, StatsForecast, MLForecast, NeuralForecast) and working on time-series forecasting problems.

Respond ONLY with valid JSON in this exact format:
{{
  "summary": "Your 2-3 sentence summary here",
  "key_points": [
    "First key point",
    "Second key point",
    "Third key point (optional)"
  ],
  "why_it_matters": "Why this matters for Nixtla/time-series practitioners",
  "relevance_score": 75
}}"""

    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the prompt.

        Args:
            prompt: Prompt to send to LLM

        Returns:
            LLM response text
        """
        if self.llm_provider == "openai":
            return self._call_openai(prompt)
        elif self.llm_provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.llm_provider}")

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

        try:
            response = self.llm_client.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=500
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API."""
        model = os.getenv("LLM_MODEL", "claude-3-haiku-20240307")

        try:
            response = self.llm_client.messages.create(
                model=model,
                max_tokens=500,
                temperature=0.3,
                system=self.SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            raise

    def _create_fallback(self, content: Content) -> CuratedContent:
        """
        Create fallback curated content when AI fails.

        Args:
            content: Original content

        Returns:
            Curated content with basic information
        """
        # Use description as summary
        summary = content.description[:200] if content.description else content.title

        # Extract some basic points from the description
        key_points = []
        if content.description:
            sentences = content.description.split(".")[:3]
            key_points = [s.strip() for s in sentences if len(s.strip()) > 10][:2]

        # Simple heuristic for relevance based on keywords
        nixtla_keywords = ["timegpt", "statsforecast", "mlforecast", "neuralforecast", "nixtla",
                          "time series", "forecasting", "prediction", "arima", "lstm"]
        keyword_count = sum(
            1 for keyword in nixtla_keywords
            if keyword in (content.title + " " + content.description).lower()
        )
        relevance_score = min(100, 40 + (keyword_count * 10))

        return CuratedContent(
            content=content,
            summary=summary,
            key_points=key_points if key_points else ["Information available at the source"],
            why_it_matters="Potentially relevant to time-series forecasting practitioners.",
            relevance_score=relevance_score
        )