"""
Unit tests for Slack publisher.
"""

import os
import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from nixtla_search_to_slack.slack_publisher import SlackPublisher, PublishResult


class TestSlackPublisher:
    """Test Slack publishing functionality."""

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_publish_success(self, mock_webclient, mock_env_config, sample_curated_content):
        """Test successful publishing to Slack."""
        # Mock Slack client
        mock_client = Mock()
        mock_client.chat_postMessage.return_value = {
            "ok": True,
            "ts": "1234567890.123456"
        }
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        result = publisher.publish(
            items=sample_curated_content,
            channel="#test-channel",
            topic_name="Test Topic"
        )

        assert result.success is True
        assert result.channel == "#test-channel"
        assert result.message_ts is not None

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_publish_dry_run(self, mock_webclient, mock_env_config, sample_curated_content,
                            monkeypatch):
        """Test dry run mode doesn't post to Slack."""
        monkeypatch.setenv("DRY_RUN", "true")

        # Mock should not be called in dry run
        mock_client = Mock()
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        result = publisher.publish(
            items=sample_curated_content,
            channel="#test-channel",
            topic_name="Test Topic"
        )

        assert result.success is True
        assert result.message_ts == "dry-run-message-ts"
        # Slack client should not be called
        mock_client.chat_postMessage.assert_not_called()

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    @patch('nixtla_search_to_slack.slack_publisher.SlackApiError')
    def test_publish_slack_error(self, mock_error, mock_webclient, mock_env_config,
                                 sample_curated_content):
        """Test handling of Slack API errors."""
        # Mock Slack error
        mock_client = Mock()
        error = Mock()
        error.response = {"error": "channel_not_found"}
        mock_client.chat_postMessage.side_effect = error
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        result = publisher.publish(
            items=sample_curated_content,
            channel="#nonexistent",
            topic_name="Test Topic"
        )

        assert result.success is False
        assert result.error is not None

    def test_missing_slack_token(self):
        """Test error when Slack token is missing."""
        with pytest.raises(ValueError, match="SLACK_BOT_TOKEN not configured"):
            SlackPublisher({})

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_build_message_blocks(self, mock_webclient, mock_env_config, sample_curated_content):
        """Test Slack Block Kit message building."""
        mock_client = Mock()
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        blocks = publisher._build_message_blocks(
            sample_curated_content,
            "Test Topic",
            datetime.now()
        )

        # Check header block
        assert blocks[0]["type"] == "header"
        assert "Test Topic" in blocks[0]["text"]["text"]

        # Check context block with metadata
        assert blocks[1]["type"] == "context"
        assert "Items: 2" in blocks[1]["elements"][0]["text"]

        # Check divider
        assert blocks[2]["type"] == "divider"

        # Check that items are included
        item_blocks = [b for b in blocks if b.get("type") == "section"]
        assert len(item_blocks) > 0

        # Check for buttons
        action_blocks = [b for b in blocks if b.get("type") == "actions"]
        assert len(action_blocks) == len(sample_curated_content)

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_build_item_blocks(self, mock_webclient, mock_env_config, sample_curated_content):
        """Test building blocks for individual items."""
        mock_client = Mock()
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        blocks = publisher._build_item_blocks(sample_curated_content[0], 1)

        # Should have multiple blocks per item
        assert len(blocks) >= 4  # Title, summary, key points, why it matters, button

        # Check title block
        title_block = blocks[0]
        assert title_block["type"] == "section"
        assert "*1. TimeGPT 2.0 Released*" in title_block["text"]["text"]
        assert "Relevance: 95%" in title_block["text"]["text"]

        # Check for key points
        points_blocks = [b for b in blocks if "*Key Points:*" in b.get("text", {}).get("text", "")]
        assert len(points_blocks) == 1

        # Check for action button
        action_blocks = [b for b in blocks if b["type"] == "actions"]
        assert len(action_blocks) == 1
        assert action_blocks[0]["elements"][0]["text"]["text"] == "View Source →"

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_truncate_text(self, mock_webclient, mock_env_config):
        """Test text truncation."""
        mock_client = Mock()
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)

        # Test short text (no truncation)
        short = "Short text"
        assert publisher._truncate(short, 20) == short

        # Test long text (should truncate)
        long = "This is a very long text that should be truncated"
        truncated = publisher._truncate(long, 20)
        assert len(truncated) == 20
        assert truncated.endswith("...")

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_test_connection_success(self, mock_webclient, mock_env_config):
        """Test successful Slack connection test."""
        mock_client = Mock()
        mock_client.auth_test.return_value = {
            "ok": True,
            "bot_id": "B12345"
        }
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        assert publisher.test_connection() is True

    @patch('nixtla_search_to_slack.slack_publisher.WebClient')
    def test_test_connection_failure(self, mock_webclient, mock_env_config):
        """Test failed Slack connection test."""
        mock_client = Mock()
        mock_client.auth_test.side_effect = Exception("Invalid token")
        mock_webclient.return_value = mock_client

        publisher = SlackPublisher(mock_env_config)
        assert publisher.test_connection() is False