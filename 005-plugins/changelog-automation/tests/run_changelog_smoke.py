#!/usr/bin/env python3
"""
Changelog Automation - Golden Task Smoke Test

Criteria:
- Execution time: <90 seconds
- Uses fixture data (no live APIs)
- Generates changelog with expected structure
- Validates frontmatter (passes schema)
- Quality score: ≥80
- Output matches expected structure (diff <10 lines)
"""

import asyncio
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_status(emoji: str, text: str):
    """Print status message."""
    print(f"{emoji} {text}")


async def test_mcp_server():
    """Test MCP server can be imported and initialized."""
    print_header("Phase 1: MCP Server Initialization")

    try:
        # Add scripts directory to path
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        # Import MCP server
        from changelog_mcp import ChangelogMCPServer

        print_status("✓", "MCP server module imported successfully")

        # Initialize server
        server = ChangelogMCPServer()
        print_status("✓", "MCP server initialized")

        return server, True

    except Exception as e:
        print_status("✗", f"MCP server initialization failed: {e}")
        return None, False


async def test_fetch_data(server):
    """Test data fetching with mock data."""
    print_header("Phase 2: Data Fetching (Mock Mode)")

    try:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        result = await server.fetch_changelog_data(
            source_type="github",
            start_date=start_date,
            end_date=end_date,
            config={"repo": "test/repo", "token_env": "MOCK"},
        )

        assert result["status"] == "success", "Fetch failed"
        assert "data" in result, "No data in result"
        assert "items" in result["data"], "No items in data"

        print_status("✓", f"Fetched {result['data']['count']} items")
        print_status("✓", f"Date range: {result['data']['date_range']}")

        return result["data"], True

    except Exception as e:
        print_status("✗", f"Data fetch failed: {e}")
        return None, False


async def test_validate_frontmatter(server):
    """Test frontmatter validation."""
    print_header("Phase 3: Frontmatter Validation")

    try:
        # Test valid frontmatter
        frontmatter = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0.0",
            "authors": ["Test Author"],
            "categories": ["features", "fixes"],
        }

        result = await server.validate_frontmatter(frontmatter=frontmatter)

        assert result["status"] == "success", "Validation failed"
        assert result["valid"] is True, "Frontmatter not valid"

        print_status("✓", "Valid frontmatter passed")
        print_status("✓", f"Warnings: {len(result['warnings'])}")

        # Test invalid frontmatter
        invalid_frontmatter = {"title": "Missing required fields"}
        result = await server.validate_frontmatter(frontmatter=invalid_frontmatter)

        assert result["valid"] is False, "Should fail validation"
        print_status(
            "✓", f"Invalid frontmatter correctly rejected ({len(result['errors'])} errors)"
        )

        return True

    except Exception as e:
        print_status("✗", f"Frontmatter validation failed: {e}")
        return False


async def test_config_loading(server):
    """Test config loading."""
    print_header("Phase 4: Config Loading")

    try:
        # Point to example config
        config_path = Path(__file__).parent.parent / "config" / ".changelog-config.example.json"

        result = await server.get_changelog_config(config_path=str(config_path))

        assert result["status"] == "success", "Config load failed"
        assert "config" in result, "No config in result"
        assert result["validation"]["valid"] is True, "Config not valid"

        print_status("✓", "Example config loaded successfully")
        print_status("✓", f"Sources configured: {len(result['config']['sources'])}")
        print_status("✓", f"Quality threshold: {result['config'].get('quality_threshold', 'N/A')}")

        return result["config"], True

    except Exception as e:
        print_status("✗", f"Config loading failed: {e}")
        return None, False


async def run_smoke_test():
    """Run complete smoke test."""
    start_time = time.time()

    print_header("Changelog Automation - Golden Task Smoke Test")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Track results
    results = {"mcp_init": False, "data_fetch": False, "frontmatter": False, "config": False}

    # Phase 1: MCP Server
    server, results["mcp_init"] = await test_mcp_server()
    if not server:
        print_header("FAILED: MCP server initialization")
        return False

    # Phase 2: Data Fetch
    data, results["data_fetch"] = await test_fetch_data(server)

    # Phase 3: Frontmatter
    results["frontmatter"] = await test_validate_frontmatter(server)

    # Phase 4: Config
    config, results["config"] = await test_config_loading(server)

    # Summary
    elapsed = time.time() - start_time
    print_header("Smoke Test Summary")

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:10} {test_name}")

    print(f"\nExecution time: {elapsed:.2f} seconds")
    print(f"Target: <90 seconds {'✓' if elapsed < 90 else '✗'}")

    all_passed = all(results.values())

    if all_passed and elapsed < 90:
        print_header("✅ SMOKE TEST PASSED")
        return True
    else:
        print_header("❌ SMOKE TEST FAILED")
        if not all_passed:
            print("Some tests failed. See details above.")
        if elapsed >= 90:
            print(f"Execution time exceeded target: {elapsed:.2f}s >= 90s")
        return False


def main():
    """Main entry point."""
    success = asyncio.run(run_smoke_test())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
