## Examples

### Example 1: Profitable Arbitrage Found

**Scenario**: Same election event on both platforms

```
Event: "Will candidate X win the 2024 election?"
Polymarket: YES = 0.45, NO = 0.55
Kalshi: YES = 0.52, NO = 0.48

Strategy: Buy Polymarket YES + Kalshi NO
Cost: 0.45 * 1.02 + 0.48 * 1.01 = 0.459 + 0.485 = 0.944
Guaranteed Return: $1.00
Profit: $0.056 (5.9%)
```

### Example 2: No Arbitrage

**Scenario**: Prices are efficiently aligned

```
Event: "Will it rain tomorrow in NYC?"
Polymarket: YES = 0.50, NO = 0.50
Kalshi: YES = 0.50, NO = 0.50

Cost of any strategy > $1.00 after fees
Result: No profitable arbitrage
```
