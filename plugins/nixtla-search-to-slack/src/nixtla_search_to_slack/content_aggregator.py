"""
Content aggregator for deduplication and metadata enrichment.
MVP implementation with simple URL and title-based deduplication.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from difflib import SequenceMatcher

from .search_orchestrator import SearchResult

logger = logging.getLogger(__name__)


@dataclass
class Content:
    """Represents a deduplicated content item."""
    url: str
    title: str
    description: str
    source: str
    timestamp: Any  # datetime
    duplicate_of: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContentAggregator:
    """Aggregates and deduplicates content from multiple sources."""

    def __init__(self):
        """Initialize the content aggregator."""
        self.seen_urls = set()
        self.seen_titles = {}
        self.content_map = {}

    def aggregate(self, search_results: List[SearchResult]) -> List[Content]:
        """
        Aggregate and deduplicate search results.

        Args:
            search_results: List of raw search results

        Returns:
            List of unique content items
        """
        unique_content = []
        duplicate_count = 0

        # Sort by timestamp to keep the most recent version
        sorted_results = sorted(search_results, key=lambda x: x.timestamp, reverse=True)

        for result in sorted_results:
            # Normalize URL for comparison
            normalized_url = self._normalize_url(result.url)

            # Check for URL duplicate
            if normalized_url in self.seen_urls:
                duplicate_count += 1
                logger.debug(f"Duplicate URL found: {result.url}")
                continue

            # Check for title similarity
            normalized_title = self._normalize_title(result.title)
            is_duplicate, similar_to = self._is_duplicate_title(normalized_title, result.url)

            if is_duplicate:
                duplicate_count += 1
                logger.debug(f"Duplicate title found: {result.title} (similar to {similar_to})")
                continue

            # Create content object
            content = Content(
                url=result.url,
                title=result.title,
                description=result.description,
                source=result.source,
                timestamp=result.timestamp,
                metadata=result.metadata
            )

            # Track for deduplication
            self.seen_urls.add(normalized_url)
            self.seen_titles[normalized_title] = result.url
            self.content_map[result.url] = content

            unique_content.append(content)

        logger.info(f"Deduplicated {duplicate_count} items from {len(search_results)} total results")
        return unique_content

    def _normalize_url(self, url: str) -> str:
        """
        Normalize a URL for deduplication.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL string
        """
        try:
            # Parse URL
            parsed = urlparse(url.lower())

            # Remove tracking parameters
            if parsed.query:
                params = parse_qs(parsed.query)
                # Remove common tracking parameters
                tracking_params = {
                    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                    'ref', 'referer', 'source', 'fbclid', 'gclid', 'msclkid',
                    's', 'sr_share', 'attribution_id', 'amp'
                }
                clean_params = {
                    k: v for k, v in params.items()
                    if k.lower() not in tracking_params
                }
                clean_query = urlencode(clean_params, doseq=True)
            else:
                clean_query = ""

            # Remove trailing slashes from path
            clean_path = parsed.path.rstrip("/") or "/"

            # Remove fragment (hash)
            # Rebuild URL without fragment and with clean params
            normalized = urlunparse((
                parsed.scheme,
                parsed.netloc,
                clean_path,
                "",  # params
                clean_query,
                ""   # fragment
            ))

            return normalized

        except Exception as e:
            logger.warning(f"Failed to normalize URL {url}: {e}")
            return url.lower()

    def _normalize_title(self, title: str) -> str:
        """
        Normalize a title for comparison.

        Args:
            title: Title to normalize

        Returns:
            Normalized title string
        """
        # Convert to lowercase
        normalized = title.lower()

        # Remove special characters and extra whitespace
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)

        # Strip whitespace
        normalized = normalized.strip()

        return normalized

    def _is_duplicate_title(self, normalized_title: str, url: str) -> tuple[bool, Optional[str]]:
        """
        Check if a title is a duplicate of an already seen title.

        Args:
            normalized_title: Normalized title to check
            url: URL of the content (for domain comparison)

        Returns:
            Tuple of (is_duplicate, similar_to_url)
        """
        # Extract domain for comparison
        try:
            domain = urlparse(url).netloc
        except:
            domain = ""

        # Check against all seen titles
        for seen_title, seen_url in self.seen_titles.items():
            # Calculate similarity
            similarity = SequenceMatcher(None, normalized_title, seen_title).ratio()

            # High similarity threshold (0.9) for MVP
            if similarity > 0.9:
                # Additional check: same domain makes duplicate more likely
                try:
                    seen_domain = urlparse(seen_url).netloc
                    if domain == seen_domain:
                        # Same domain and very similar title = duplicate
                        return True, seen_url
                    elif similarity > 0.95:
                        # Different domain but extremely similar = likely duplicate
                        return True, seen_url
                except:
                    pass

        return False, None

    def get_statistics(self) -> Dict[str, int]:
        """
        Get aggregation statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            "unique_urls": len(self.seen_urls),
            "unique_titles": len(self.seen_titles),
            "total_content": len(self.content_map)
        }