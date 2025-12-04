# Nixtla Usage Optimizer - Best Practices

## 1. Run Audit Quarterly

Rerun this skill every 3 months to catch:
- New TimeGPT usage patterns
- Opportunities from product updates
- Changing cost dynamics

---

## 2. Track Routing Decisions

Log every routing decision:
```python
logging.info(f"Routing decision: {model_chosen} (reason: {reason})")
```

Review logs to validate routing logic is working as intended.

---

## 3. A/B Test Routing Changes

Before fully committing to routing changes:
- Run both old and new approach in parallel
- Compare accuracy and costs
- Verify assumptions hold in practice

---

## 4. Combine with Usage Metrics

If you have access to Nixtla dashboard or usage logs:
- Include actual API call counts
- Show real cost data
- Calculate precise ROI instead of estimates
