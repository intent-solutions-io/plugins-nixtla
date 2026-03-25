# Search-to-Slack Integration

## Trigger a Manual Digest

```bash
cd {baseDir}/plugins/nixtla-search-to-slack
python -m nixtla_search_to_slack --topic nixtla-core
```

## Check Configuration

```bash
cat {baseDir}/plugins/nixtla-search-to-slack/config/topics.yaml
```

## View Available Topics

```bash
python -m nixtla_search_to_slack --list-topics
```

## Run Dry Run (test without posting to Slack)

```bash
python -m nixtla_search_to_slack --topic nixtla-core --dry-run
```
