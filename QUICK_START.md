# 🚀 Quick Start Guide

## Installation (Windows)

1. **Double-click `install.bat`** to install all required packages
2. **Double-click `run.bat`** to start the application
3. Your browser will open automatically to http://localhost:8501

## Installation (Mac/Linux)

```bash
# Make the script executable
chmod +x run.sh

# Install packages
pip install -r requirements.txt

# Run the application
./run.sh
```

## First Steps

### 1. Load Stock Data
- Enter a ticker symbol in the sidebar (e.g., **AAPL**)
- Click **"Load Data"** button
- Wait for data to load (5-10 seconds)

### 2. Select Expiration Date
- Choose an expiration date from the dropdown
- The system will load all available options

### 3. Configure Settings (Optional)
- **Risk-Free Rate**: Default is 5% (adjust based on current Treasury rates)
- **Binomial Steps**: Default is 100 (higher = more accurate but slower)
- **Portfolio**: Set your portfolio amount (default $100,000)
- **Risk %**: Set risk per trade (default 2%)
- **Simulations**: Default is 10,000 Monte Carlo trials

### 4. Review Results
Scroll down to see:
- ✅ **Live Options Prices** - Current market data
- ✅ **Fair Value Analysis** - Undervalued/overvalued options
- ✅ **Monte Carlo Simulation** - Price distribution at expiration
- ✅ **ML Predictions** - Decision Tree and SVM forecasts
- ✅ **AI Recommendations** - Top trading strategies

## Example Walkthrough

### Analyzing Apple (AAPL)

1. Enter **AAPL** in the ticker box
2. Click **Load Data**
3. Select an expiration date (try 30-60 days out)
4. Keep default settings initially
5. Review the top recommendations

### Understanding a Recommendation

**Example Output:**
```
BUY CALL - CALL @ $150.00
Confidence: HIGH | Valuation: UNDERVALUED

Market Price: $5.50
Fair Value: $6.20
Value Diff: -11.29%
Probability ITM: 58.3%
Expected Payoff: $8.45
Position Size: 3 contracts
Total Cost: $1,650.00
```

**What this means:**
- The $150 call is trading **below** fair value (undervalued by 11.29%)
- There's a 58.3% chance it will be in-the-money at expiration
- The AI recommends buying **3 contracts**
- Total investment would be **$1,650** (3 × $550)
- This represents **1.65%** of a $100,000 portfolio

## Tips for Best Results

### ✅ Good Tickers to Analyze
- **Large Cap Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA
- **ETFs**: SPY, QQQ, IWM
- **High Volume Stocks**: Stocks with active options markets

### ❌ Avoid These Tickers
- Low-volume stocks with illiquid options
- Recently IPO'd companies (< 1 year)
- Stocks without listed options

### 📊 Optimal Settings

**For Quick Analysis:**
- Binomial Steps: 50
- Monte Carlo Trials: 5,000

**For Detailed Analysis:**
- Binomial Steps: 150
- Monte Carlo Trials: 50,000

**Risk Management:**
- Conservative: 1-2% risk per trade
- Moderate: 2-3% risk per trade
- Aggressive: 3-5% risk per trade

## Common Questions

### Q: How accurate are the predictions?
A: The models provide educated estimates based on historical data. No model can predict the future with certainty. Always use as one tool among many.

### Q: Should I trade based on these recommendations?
A: **NO!** This is an educational tool. Always do your own research, consider your risk tolerance, and consult a financial advisor.

### Q: What if I see "Unable to load data"?
A: Try these solutions:
1. Check your internet connection
2. Try a different ticker symbol
3. Wait a moment and try again (API may be rate-limited)

### Q: Why are some options marked as "HOLD"?
A: The AI marks options as HOLD when:
- They're fairly priced (not undervalued or overvalued)
- They have low liquidity (volume/open interest)
- The probability of profit is low
- The risk-adjusted return is unfavorable

### Q: Can I analyze multiple strategies?
A: The current version analyzes single-leg strategies (buying calls/puts). Multi-leg strategies (spreads, straddles) could be added in future versions.

## Performance Tips

- **Slow loading?** Reduce Monte Carlo trials to 5,000
- **Analysis taking too long?** Reduce binomial steps to 50
- **Want more accuracy?** Increase both parameters (will be slower)

## Safety Reminders

⚠️ **IMPORTANT:**
1. This is for **educational purposes only**
2. **Not financial advice** - do your own research
3. Options trading is **risky** - you can lose your entire investment
4. Always verify prices with your broker before trading
5. Never invest more than you can afford to lose
6. Past performance ≠ future results

## Need Help?

Check the full **README.md** for:
- Detailed feature descriptions
- Technical documentation
- Troubleshooting guide
- Advanced usage tips

---

**Ready to start?** Double-click `run.bat` (Windows) or run `./run.sh` (Mac/Linux)!

