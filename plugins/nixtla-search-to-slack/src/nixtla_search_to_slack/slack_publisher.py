"""
Slack publisher for formatting and posting digests to Slack channels.
Uses Slack Block Kit for rich formatting.
"""

import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .ai_curator import CuratedContent

logger = logging.getLogger(__name__)

# Import Slack SDK conditionally
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    WebClient = None
    SlackApiError = None
    logger.warning("Slack SDK not installed. Run: pip install slack-sdk")


@dataclass
class PublishResult:
    """Result of publishing to Slack."""
    success: bool
    channel: str
    timestamp: str
    message_ts: Optional[str] = None
    error: Optional[str] = None


class SlackPublisher:
    """Publishes curated content digests to Slack."""

    def __init__(self, env_config: Dict[str, str]):
        """
        Initialize the Slack publisher.

        Args:
            env_config: Environment configuration with Slack token
        """
        self.env_config = env_config
        self.client = self._initialize_client()

    def _initialize_client(self) -> Optional[WebClient]:
        """Initialize Slack client."""
        if not WebClient:
            raise ImportError("Slack SDK not installed. Run: pip install slack-sdk")

        token = self.env_config.get("SLACK_BOT_TOKEN")
        if not token:
            raise ValueError("SLACK_BOT_TOKEN not configured")

        return WebClient(token=token)

    def publish(self, items: List[CuratedContent], channel: str,
               topic_name: str = "Digest") -> PublishResult:
        """
        Publish a digest to Slack.

        Args:
            items: List of curated content items
            channel: Slack channel to post to
            topic_name: Name of the topic for the digest

        Returns:
            Result of the publish operation
        """
        timestamp = datetime.now()

        # Check for dry run mode
        if os.getenv("DRY_RUN", "false").lower() == "true":
            logger.info(f"DRY RUN: Would post {len(items)} items to {channel}")
            return PublishResult(
                success=True,
                channel=channel,
                timestamp=timestamp.isoformat(),
                message_ts="dry-run-message-ts"
            )

        try:
            # Build the message blocks
            blocks = self._build_message_blocks(items, topic_name, timestamp)

            # Post to Slack
            response = self.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f"📊 {topic_name} - {len(items)} new items"  # Fallback text
            )

            logger.info(f"Successfully posted digest to {channel}")

            return PublishResult(
                success=True,
                channel=channel,
                timestamp=timestamp.isoformat(),
                message_ts=response.get("ts")
            )

        except SlackApiError as e:
            error_msg = f"Slack API error: {e.response.get('error', 'Unknown error')}"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                channel=channel,
                timestamp=timestamp.isoformat(),
                error=error_msg
            )

        except Exception as e:
            error_msg = f"Failed to publish to Slack: {str(e)}"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                channel=channel,
                timestamp=timestamp.isoformat(),
                error=error_msg
            )

    def _build_message_blocks(self, items: List[CuratedContent],
                             topic_name: str, timestamp: datetime) -> List[Dict[str, Any]]:
        """
        Build Slack Block Kit message blocks.

        Args:
            items: Curated content items
            topic_name: Name of the topic
            timestamp: Timestamp of the digest

        Returns:
            List of Slack blocks
        """
        blocks = []

        # Header block
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📊 {topic_name}",
                "emoji": True
            }
        })

        # Context block with metadata
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Generated: {timestamp.strftime('%b %d, %Y at %I:%M %p %Z')} | Items: {len(items)}"
                }
            ]
        })

        # Divider
        blocks.append({"type": "divider"})

        # Add each content item
        for idx, item in enumerate(items, 1):
            blocks.extend(self._build_item_blocks(item, idx))

            # Add divider between items (but not after the last one)
            if idx < len(items):
                blocks.append({"type": "divider"})

        # Footer context
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "_This digest is generated by an example plugin and is not endorsed by Nixtla._"
                }
            ]
        })

        return blocks

    def _build_item_blocks(self, item: CuratedContent, index: int) -> List[Dict[str, Any]]:
        """
        Build blocks for a single content item.

        Args:
            item: Curated content item
            index: Item index (for numbering)

        Returns:
            List of blocks for this item
        """
        blocks = []

        # Title and metadata section
        title_text = f"*{index}. {self._truncate(item.content.title, 100)}*\n"
        title_text += f"Source: {item.content.source.title()} • "
        title_text += f"Relevance: {item.relevance_score}%"

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title_text
            }
        })

        # Summary section (as a quote)
        if item.summary:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"> {self._truncate(item.summary, 300)}"
                }
            })

        # Key points section
        if item.key_points:
            points_text = "*Key Points:*\n"
            for point in item.key_points[:3]:  # Limit to 3 points
                points_text += f"• {self._truncate(point, 150)}\n"

            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": points_text.rstrip()
                }
            })

        # Why it matters section
        if item.why_it_matters:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Why this matters:* {self._truncate(item.why_it_matters, 200)}"
                }
            })

        # Action button
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Source →",
                        "emoji": True
                    },
                    "url": item.content.url,
                    "action_id": f"view_source_{index}"
                }
            ]
        })

        return blocks

    def _truncate(self, text: str, max_length: int) -> str:
        """
        Truncate text to a maximum length with ellipsis.

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

    def test_connection(self) -> bool:
        """
        Test the Slack connection.

        Returns:
            True if connection is successful
        """
        try:
            response = self.client.auth_test()
            logger.info(f"Slack connection successful. Bot: {response.get('bot_id')}")
            return True
        except Exception as e:
            logger.error(f"Slack connection test failed: {e}")
            return False