#!/usr/bin/env python3
"""
Main entry point for Nixtla Search-to-Slack plugin.
Orchestrates the search -> curate -> publish workflow.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv

from .config_loader import ConfigLoader
from .search_orchestrator import SearchOrchestrator
from .content_aggregator import ContentAggregator
from .ai_curator import AICurator
from .slack_publisher import SlackPublisher

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_environment() -> Dict[str, str]:
    """Validate required environment variables are present."""
    required = {
        "SLACK_BOT_TOKEN": "Slack bot token for posting messages",
        "SERP_API_KEY": "SerpAPI key for web searches",
        "GITHUB_TOKEN": "GitHub token for repository searches",
    }

    # At least one LLM provider required
    llm_keys = {
        "OPENAI_API_KEY": "OpenAI API key",
        "ANTHROPIC_API_KEY": "Anthropic API key",
    }

    errors = []
    config = {}

    # Check required keys
    for key, description in required.items():
        value = os.getenv(key)
        if not value:
            errors.append(f"Missing required: {key} ({description})")
        else:
            config[key] = value

    # Check for at least one LLM provider
    llm_found = False
    for key, description in llm_keys.items():
        value = os.getenv(key)
        if value:
            config[key] = value
            llm_found = True

    if not llm_found:
        errors.append("Missing LLM provider: Need either OPENAI_API_KEY or ANTHROPIC_API_KEY")

    if errors:
        logger.error("Environment validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)

    return config


def run_digest(topic_id: str = "nixtla-core") -> Dict[str, Any]:
    """
    Run a complete digest workflow for the specified topic.

    Args:
        topic_id: ID of the topic to search for

    Returns:
        Dictionary with digest results and metadata
    """
    start_time = datetime.now()
    logger.info(f"Starting digest for topic: {topic_id}")

    # Validate environment
    env_config = validate_environment()

    # Load configuration
    config_loader = ConfigLoader()
    sources_config = config_loader.load_sources()
    topics_config = config_loader.load_topics()

    # Get topic configuration
    if topic_id not in topics_config["topics"]:
        available = ", ".join(topics_config["topics"].keys())
        logger.error(f"Topic '{topic_id}' not found. Available topics: {available}")
        return {
            "success": False,
            "error": f"Topic not found. Available: {available}",
            "topic": topic_id,
            "timestamp": start_time.isoformat()
        }

    topic = topics_config["topics"][topic_id]
    logger.info(f"Loaded topic: {topic['name']}")

    try:
        # 1. Search for content
        logger.info("Phase 1: Searching for content...")
        orchestrator = SearchOrchestrator(sources_config, env_config)
        search_results = orchestrator.search(topic)
        logger.info(f"Found {len(search_results)} raw search results")

        if not search_results:
            logger.warning("No search results found")
            return {
                "success": True,
                "topic": topic_id,
                "items_found": 0,
                "items_sent": 0,
                "message": "No new content found",
                "timestamp": start_time.isoformat(),
                "duration": (datetime.now() - start_time).total_seconds()
            }

        # 2. Aggregate and deduplicate
        logger.info("Phase 2: Aggregating and deduplicating content...")
        aggregator = ContentAggregator()
        unique_content = aggregator.aggregate(search_results)
        logger.info(f"Reduced to {len(unique_content)} unique items after deduplication")

        # 3. Curate with AI
        logger.info("Phase 3: Generating AI summaries...")
        curator = AICurator(env_config)
        curated_items = curator.curate(unique_content)

        # Filter by relevance
        min_relevance = topic.get("filters", {}).get("min_relevance", 50)
        relevant_items = [
            item for item in curated_items
            if item.relevance_score >= min_relevance
        ]
        logger.info(f"Filtered to {len(relevant_items)} relevant items (min score: {min_relevance})")

        if not relevant_items:
            logger.info("No items met relevance threshold")
            return {
                "success": True,
                "topic": topic_id,
                "items_found": len(search_results),
                "items_deduplicated": len(unique_content),
                "items_curated": len(curated_items),
                "items_sent": 0,
                "message": f"No items met relevance threshold ({min_relevance})",
                "timestamp": start_time.isoformat(),
                "duration": (datetime.now() - start_time).total_seconds()
            }

        # Limit to max items
        max_items = int(os.getenv("MAX_ITEMS_PER_DIGEST", 10))
        final_items = sorted(
            relevant_items,
            key=lambda x: x.relevance_score,
            reverse=True
        )[:max_items]

        # 4. Publish to Slack
        logger.info(f"Phase 4: Publishing {len(final_items)} items to Slack...")
        publisher = SlackPublisher(env_config)

        # Get channel from topic or environment
        channel = topic.get("slack_channel", os.getenv("SLACK_CHANNEL", "#general"))

        publish_result = publisher.publish(
            items=final_items,
            channel=channel,
            topic_name=topic["name"]
        )

        # Prepare result summary
        result = {
            "success": publish_result.success,
            "topic": topic_id,
            "topic_name": topic["name"],
            "items_found": len(search_results),
            "items_deduplicated": len(unique_content),
            "items_curated": len(curated_items),
            "items_relevant": len(relevant_items),
            "items_sent": len(final_items),
            "slack_channel": channel,
            "slack_timestamp": publish_result.message_ts,
            "timestamp": start_time.isoformat(),
            "duration": (datetime.now() - start_time).total_seconds()
        }

        if not publish_result.success:
            result["error"] = publish_result.error
            logger.error(f"Failed to publish to Slack: {publish_result.error}")
        else:
            logger.info(f"Successfully published digest to {channel}")

        return result

    except Exception as e:
        logger.error(f"Digest failed with error: {str(e)}", exc_info=True)
        return {
            "success": False,
            "topic": topic_id,
            "error": str(e),
            "timestamp": start_time.isoformat(),
            "duration": (datetime.now() - start_time).total_seconds()
        }


def main():
    """Command-line interface for the digest."""
    parser = argparse.ArgumentParser(
        description="Nixtla Search-to-Slack Digest - MVP Construction Kit",
        epilog="This is an example implementation, not a production service."
    )

    parser.add_argument(
        "--topic",
        default="nixtla-core",
        help="Topic ID to search for (default: nixtla-core)"
    )

    parser.add_argument(
        "--list-topics",
        action="store_true",
        help="List available topics and exit"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run search and curation but don't post to Slack"
    )

    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Handle list-topics
    if args.list_topics:
        config_loader = ConfigLoader()
        topics = config_loader.load_topics()
        print("\nAvailable Topics:")
        print("-" * 40)
        for topic_id, topic_data in topics["topics"].items():
            print(f"  {topic_id:20} - {topic_data['name']}")
        print("\nDefault topic:", topics.get("default_topic", "nixtla-core"))
        sys.exit(0)

    # Set dry-run mode if requested
    if args.dry_run:
        os.environ["DRY_RUN"] = "true"
        logger.info("DRY RUN MODE - Will not post to Slack")

    # Run the digest
    result = run_digest(args.topic)

    # Output results
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        # Text output
        print("\n" + "=" * 50)
        print("DIGEST RESULTS")
        print("=" * 50)
        print(f"Topic: {result.get('topic_name', result['topic'])}")
        print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Items found: {result.get('items_found', 0)}")
            print(f"Items sent: {result.get('items_sent', 0)}")
            print(f"Channel: {result.get('slack_channel', 'N/A')}")
        print(f"Duration: {result.get('duration', 0):.2f} seconds")
        print("=" * 50)

    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()