"""
Unit tests for AI curator.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock

from nixtla_search_to_slack.ai_curator import AICurator, CuratedContent


class TestAICurator:
    """Test AI curation functionality."""

    @patch('nixtla_search_to_slack.ai_curator.openai')
    def test_curate_with_openai(self, mock_openai, mock_env_config, sample_content):
        """Test curation using OpenAI."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "summary": "Test summary",
            "key_points": ["Point 1", "Point 2"],
            "why_it_matters": "Important for time series",
            "relevance_score": 85
        })
        mock_openai.ChatCompletion.create.return_value = mock_response

        curator = AICurator(mock_env_config)
        curator.llm_provider = "openai"
        curator.llm_client = mock_openai

        results = curator.curate(sample_content[:1])

        assert len(results) == 1
        assert isinstance(results[0], CuratedContent)
        assert results[0].summary == "Test summary"
        assert len(results[0].key_points) == 2
        assert results[0].relevance_score == 85

    @patch('nixtla_search_to_slack.ai_curator.anthropic')
    def test_curate_with_anthropic(self, mock_anthropic, mock_env_config, sample_content):
        """Test curation using Anthropic."""
        # Mock Anthropic response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps({
            "summary": "Anthropic summary",
            "key_points": ["Key 1", "Key 2", "Key 3"],
            "why_it_matters": "Critical for Nixtla users",
            "relevance_score": 92
        }))]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client

        env_config = mock_env_config.copy()
        env_config["ANTHROPIC_API_KEY"] = "sk-ant-test"
        del env_config["OPENAI_API_KEY"]

        curator = AICurator(env_config)
        curator.llm_provider = "anthropic"
        curator.llm_client = mock_client

        results = curator.curate(sample_content[:1])

        assert len(results) == 1
        assert results[0].summary == "Anthropic summary"
        assert len(results[0].key_points) == 3
        assert results[0].relevance_score == 92

    def test_missing_llm_provider(self):
        """Test error when no LLM provider is configured."""
        with pytest.raises(ValueError, match="No LLM provider configured"):
            AICurator({})

    @patch('nixtla_search_to_slack.ai_curator.openai')
    def test_fallback_on_llm_error(self, mock_openai, mock_env_config, sample_content):
        """Test fallback when LLM fails."""
        # Mock OpenAI to raise an error
        mock_openai.ChatCompletion.create.side_effect = Exception("API Error")

        curator = AICurator(mock_env_config)
        curator.llm_provider = "openai"
        curator.llm_client = mock_openai

        results = curator.curate(sample_content[:1])

        # Should return fallback content
        assert len(results) == 1
        assert results[0].summary == sample_content[0].description[:200]
        assert "Information available at the source" in results[0].key_points[0] or len(results[0].key_points) > 0

    @patch('nixtla_search_to_slack.ai_curator.openai')
    def test_invalid_json_response(self, mock_openai, mock_env_config, sample_content):
        """Test fallback when LLM returns invalid JSON."""
        # Mock OpenAI with invalid JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is not valid JSON"
        mock_openai.ChatCompletion.create.return_value = mock_response

        curator = AICurator(mock_env_config)
        curator.llm_provider = "openai"
        curator.llm_client = mock_openai

        results = curator.curate(sample_content[:1])

        # Should return fallback content
        assert len(results) == 1
        assert len(results[0].summary) > 0

    @patch('nixtla_search_to_slack.ai_curator.openai')
    def test_relevance_score_bounds(self, mock_openai, mock_env_config, sample_content):
        """Test that relevance scores are bounded 0-100."""
        # Mock with out-of-bounds relevance score
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "summary": "Summary",
            "key_points": ["Point"],
            "why_it_matters": "Matters",
            "relevance_score": 150  # Out of bounds
        })
        mock_openai.ChatCompletion.create.return_value = mock_response

        curator = AICurator(mock_env_config)
        curator.llm_provider = "openai"
        curator.llm_client = mock_openai

        results = curator.curate(sample_content[:1])

        # Score should be clamped to 100
        assert results[0].relevance_score == 100

    @patch('nixtla_search_to_slack.ai_curator.openai')
    def test_key_points_limit(self, mock_openai, mock_env_config, sample_content):
        """Test that key points are limited to 3."""
        # Mock with too many key points
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "summary": "Summary",
            "key_points": ["P1", "P2", "P3", "P4", "P5"],  # Too many
            "why_it_matters": "Matters",
            "relevance_score": 80
        })
        mock_openai.ChatCompletion.create.return_value = mock_response

        curator = AICurator(mock_env_config)
        curator.llm_provider = "openai"
        curator.llm_client = mock_openai

        results = curator.curate(sample_content[:1])

        # Should limit to 3 points
        assert len(results[0].key_points) == 3

    def test_create_fallback_with_keywords(self, mock_env_config, sample_content):
        """Test fallback creation with keyword-based relevance."""
        curator = AICurator(mock_env_config)

        # Create content with Nixtla keywords
        content = sample_content[0]
        content.title = "TimeGPT and StatsForecast Integration"
        content.description = "New features for MLForecast and NeuralForecast time series forecasting"

        fallback = curator._create_fallback(content)

        # Should have higher relevance due to keywords
        assert fallback.relevance_score > 50
        assert len(fallback.summary) > 0

    def test_build_prompt(self, mock_env_config, sample_content):
        """Test prompt building."""
        curator = AICurator(mock_env_config)
        prompt = curator._build_prompt(sample_content[0])

        assert "TimeGPT" in prompt
        assert sample_content[0].title in prompt
        assert sample_content[0].url in prompt
        assert "relevance_score" in prompt