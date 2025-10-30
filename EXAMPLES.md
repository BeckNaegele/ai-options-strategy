# 📚 Usage Examples

## Example 1: Conservative Strategy on Blue-Chip Stock

### Scenario
Analyzing Apple (AAPL) for a conservative investor with a $100,000 portfolio.

### Settings
- **Ticker**: AAPL
- **Expiration**: 30-45 days out
- **Risk-Free Rate**: 5.0%
- **Binomial Steps**: 100
- **Portfolio**: $100,000
- **Risk per Trade**: 1.5%
- **Monte Carlo Trials**: 10,000

### Expected Output
The AI will look for:
- High-probability (>55%) trades
- Well-priced options (undervalued by >10%)
- High liquidity (volume >100, OI >500)
- Position sizes around $1,500 per trade

### Interpretation
Look for recommendations with:
- ✅ HIGH confidence
- ✅ Probability ITM > 55%
- ✅ Risk-adjusted return > 0.01

---

## Example 2: Aggressive Strategy on High Volatility Stock

### Scenario
Trading Tesla (TSLA) with higher risk tolerance.

### Settings
- **Ticker**: TSLA
- **Expiration**: 14-30 days out
- **Risk-Free Rate**: 5.0%
- **Binomial Steps**: 150
- **Portfolio**: $50,000
- **Risk per Trade**: 5.0%
- **Monte Carlo Trials**: 20,000

### Expected Output
The AI will identify:
- More options opportunities
- Higher premium options
- Greater expected payoffs
- Position sizes around $2,500 per trade

### Interpretation
Focus on:
- Risk-adjusted returns
- Maximum loss scenarios
- Probability distributions from Monte Carlo

---

## Example 3: SPY Index Options Analysis

### Scenario
Trading SPY (S&P 500 ETF) for market-neutral strategy.

### Settings
- **Ticker**: SPY
- **Expiration**: 30-60 days out
- **Risk-Free Rate**: 5.0%
- **Binomial Steps**: 100
- **Portfolio**: $250,000
- **Risk per Trade**: 2.0%
- **Monte Carlo Trials**: 50,000

### Expected Output
High-quality data due to:
- Extreme liquidity in SPY options
- Tight bid-ask spreads
- Accurate pricing models
- Multiple opportunities across strikes

### Strategy Ideas
- Look for undervalued options near ATM
- Check both calls and puts
- Consider probability distributions
- Compare ML predictions

---

## Example 4: Earnings Play Analysis

### Scenario
Analyzing a stock before earnings announcement.

### Settings
- **Ticker**: (Any stock with upcoming earnings)
- **Expiration**: Week of earnings + 1-2 weeks
- **Risk-Free Rate**: 5.0%
- **Binomial Steps**: 150
- **Portfolio**: $100,000
- **Risk per Trade**: 3.0%
- **Monte Carlo Trials**: 25,000

### What to Look For

**High IV Environment**:
- Options will be more expensive
- Fair values may show overvaluation
- Higher expected payoffs
- Greater uncertainty in Monte Carlo

**Recommendation Strategy**:
- Be cautious with HIGH confidence ratings
- Check historical volatility vs implied volatility
- Consider waiting for IV crush post-earnings
- Look at the probability distributions

---

## Parameter Guide

### Risk-Free Rate
**When to adjust:**
- Use current 10-year Treasury rate
- Typically 3-6% in normal markets
- Higher rates → lower option values

### Binomial Steps
**Recommended values:**
- **Quick analysis**: 50 steps (5 seconds)
- **Standard**: 100 steps (10 seconds)
- **Precise**: 150-200 steps (20-30 seconds)

**Trade-off**: Accuracy vs. Speed

### Portfolio Amount
**Examples:**
- **Small**: $10,000-$25,000
- **Medium**: $50,000-$100,000
- **Large**: $250,000-$500,000+

**Effect**: Determines position sizes

### Risk Per Trade
**Guidelines:**
- **Conservative**: 1-2%
- **Moderate**: 2-3%
- **Aggressive**: 3-5%
- **Very Aggressive**: 5-10% (not recommended)

**Rule**: Never exceed 10% per single trade

### Monte Carlo Trials
**Recommended values:**
- **Fast**: 5,000 trials (2 seconds)
- **Standard**: 10,000 trials (4 seconds)
- **Detailed**: 25,000 trials (10 seconds)
- **Research**: 50,000-100,000 trials (30-60 seconds)

**Effect**: More trials = smoother distributions, better probability estimates

---

## Reading Recommendations

### High Confidence Buy Call Example

```
BUY CALL - CALL @ $155.00
Confidence: HIGH | Valuation: UNDERVALUED

Market Price: $4.50
Fair Value: $5.20
Value Diff: -13.46%
Probability ITM: 62.5%
Expected Payoff: $7.80
Risk-Adj Return: 0.0245
Position Size: 4 contracts
Total Cost: $1,800
```

**Analysis:**
- ✅ **Undervalued** by 13.46% → Good value
- ✅ **High probability** (62.5%) of profit
- ✅ **Good risk-adjusted return** (0.0245)
- ✅ **Reasonable cost** ($1,800 = 1.8% of $100k portfolio)

**Action**: Strong buy candidate

### Medium Confidence Buy Put Example

```
BUY PUT - PUT @ $145.00
Confidence: MEDIUM | Valuation: UNDERVALUED

Market Price: $3.20
Fair Value: $3.85
Value Diff: -16.88%
Probability ITM: 48.2%
Expected Payoff: $5.10
Risk-Adj Return: 0.0152
Position Size: 6 contracts
Total Cost: $1,920
```

**Analysis:**
- ✅ **Undervalued** by 16.88% → Good value
- ⚠️ **Moderate probability** (48.2%) → Less certain
- ✅ **Decent risk-adjusted return** (0.0152)
- ✅ **Acceptable cost** ($1,920)

**Action**: Consider, but with caution

### Low Confidence / Hold Example

```
HOLD - CALL @ $160.00
Confidence: LOW | Valuation: FAIR

Market Price: $2.10
Fair Value: $2.15
Value Diff: -2.33%
Probability ITM: 38.5%
Expected Payoff: $2.80
Risk-Adj Return: 0.0045
Position Size: 9 contracts
Total Cost: $1,890
```

**Analysis:**
- ⚠️ **Fairly priced** → No value edge
- ❌ **Low probability** (38.5%) of profit
- ❌ **Poor risk-adjusted return** (0.0045)

**Action**: Skip this trade

---

## Advanced Usage Tips

### 1. Compare Multiple Expirations
Run the analysis on 2-3 different expiration dates to see:
- How time decay affects pricing
- Which expiration offers best value
- Probability changes over time

### 2. Watch for Divergence
Pay attention when:
- Decision Tree and SVM predict very different prices
- Monte Carlo shows bimodal distribution
- Fair values differ significantly from market

### 3. Liquidity Matters
Always check:
- **Volume** > 50 (preferably >100)
- **Open Interest** > 100 (preferably >500)
- **Bid-Ask Spread** < 10% of option price

### 4. Use Greeks (Future Feature)
Current app shows:
- Delta: Sensitivity to price changes
- Gamma: Rate of delta change
- Theta: Time decay
- Vega: Volatility sensitivity

### 5. Risk Management Rules
**Never:**
- ❌ Risk more than 2-3% on any single trade
- ❌ Use entire portfolio at once
- ❌ Ignore the probability metrics
- ❌ Trade illiquid options

**Always:**
- ✅ Verify prices with your broker
- ✅ Set stop losses
- ✅ Take profits at targets
- ✅ Review positions daily

---

## Troubleshooting Scenarios

### "No HIGH confidence recommendations"

**Possible reasons:**
1. All options are fairly priced
2. High volatility environment (options expensive)
3. Low probability setups
4. Illiquid options filtered out

**Solutions:**
- Try different expiration date
- Adjust risk parameters
- Check different ticker
- Review MEDIUM confidence trades

### "ML models show very different predictions"

**What it means:**
- High uncertainty in future price
- Models capturing different patterns
- Potential for large price move

**What to do:**
- Look at Monte Carlo distribution width
- Check recent news/events
- Be more conservative with position sizing

### "Fair values very different from market"

**Possible causes:**
1. Volatility parameter incorrect
2. Upcoming catalyst (earnings, FDA decision)
3. Market pricing in information not in historical data
4. Illiquid options (wide spreads)

**Investigation:**
- Check implied volatility vs historical
- Look for upcoming events
- Verify option is actively traded
- Compare to similar strikes

---

## Best Practices Checklist

Before making any trade based on recommendations:

- [ ] Verify current market price with broker
- [ ] Check option liquidity (volume, OI, spread)
- [ ] Understand maximum loss
- [ ] Set profit target
- [ ] Plan exit strategy
- [ ] Confirm position size fits risk tolerance
- [ ] Review probability of profit
- [ ] Check for upcoming events (earnings, etc.)
- [ ] Ensure sufficient buying power
- [ ] Record trade thesis for future review

---

## Educational Exercise

Try this learning exercise:

1. **Pick a familiar stock** (e.g., AAPL)
2. **Run analysis** with standard parameters
3. **Note top 3 recommendations**
4. **Wait 1 week** without trading
5. **Re-run analysis** with new data
6. **Compare**: Were the predictions accurate?
7. **Learn**: What changed? Why?

This "paper trading" approach helps you:
- Understand the tool
- See how markets move
- Build intuition
- Avoid costly mistakes

---

**Remember**: This tool is a starting point for research, not a complete trading system. Always combine with your own analysis, risk management, and due diligence.

Happy learning! 📚🎓

