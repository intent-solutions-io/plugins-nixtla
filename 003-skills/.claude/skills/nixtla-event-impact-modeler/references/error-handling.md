## Error Handling

| Error | Solution |
|-------|----------|
| Event dates outside price range | Adjust event dates or expand price data range |
| Missing event descriptions | Ensure `event` column exists in events CSV |
| TimeGPT API request failed | Verify `NIXTLA_TIMEGPT_API_KEY` and internet connection |
| CausalImpact failed to converge | Increase `--niter` parameter or adjust event windows |
| Insufficient pre-intervention data | Expand price history before first event |
