---
name: nixtla-research-assistant
description: "Research and summarize Nixtla ecosystem updates and time-series forecasting content from the web and GitHub. Use when gathering release notes, recent changes, or best-practice references. Trigger with \"Nixtla updates\", \"what's new with TimeGPT\", or \"find time-series papers\"."
allowed-tools: WebFetch,WebSearch,Bash(python:*),Read,Write,Glob
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatible-with: claude-code
tags: [nixtla, research, time-series, timegpt, web-search]
argument-hint: "<topic or query>"
---

# Nixtla Research Assistant

## Overview

Find relevant sources (releases, PRs, blog posts, papers), then produce short, actionable summaries with links and a clear "why it matters" section.

Expertise covers:
- **TimeGPT**: Nixtla's foundation model for time-series
- **StatsForecast**: Statistical forecasting methods
- **MLForecast**: Machine learning forecasting
- **NeuralForecast**: Neural network forecasting
- **Time-series best practices**: Research, papers, techniques

## Prerequisites

- A topic, repo, or question to research (and optional time window, e.g. "last 30 days").
- Optional: Slack configuration if posting results via the plugin workflow.

## Instructions

1. Search official repos and recent release notes first, then broaden to the web. See [search strategy](references/search-strategy.md) for the full search order and summary format.
2. Extract changes, breaking notes, and practical impact; avoid speculation.
3. Output a digest with sources and suggested action items.
4. For Slack integration, use the [slack integration guide](references/slack-integration.md).

## Output

- A markdown digest with sources, key points, and recommended next steps.
- Format: technical but accessible, concise (2-3 sentence summaries), actionable, and citing primary sources.
- Use markdown headers for organization, clickable links, code blocks for technical content, and tables for comparisons.

## Error Handling

- If WebSearch/WebFetch returns sparse results, broaden query terms and report the search strategy used.
- If a source is inaccessible, note it and provide an alternative source when possible.

## Examples

- "What's new with TimeGPT in the last 30 days?"
- "Summarize recent StatsForecast releases and breaking changes."

For full worked examples, see [examples reference](references/examples.md).

## Resources

- Search strategy and provider details: [search-strategy](references/search-strategy.md)
- Slack integration commands: [slack-integration](references/slack-integration.md)
- Worked examples: [examples](references/examples.md)
- Nixtla Documentation: https://docs.nixtla.io/
- TimeGPT API Docs: https://docs.nixtla.io/docs/getting-started-timegpt
- StatsForecast: https://nixtla.github.io/statsforecast/
- MLForecast: https://nixtla.github.io/mlforecast/
- NeuralForecast: https://nixtla.github.io/neuralforecast/
- GitHub Organization: https://github.com/Nixtla
