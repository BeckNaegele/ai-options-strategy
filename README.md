# 📈 AI Options & Futures Strategy Analyzer

A comprehensive **Streamlit web application** for analyzing American Options and Futures with AI-powered trading recommendations.

## 🌐 Deploy as Web App

**This is already a web app!** Deploy it online in 5 minutes:

👉 **[Quick Deploy Guide](QUICK_DEPLOY.md)** - Deploy to Streamlit Cloud (FREE)  
👉 **[Complete Deployment Guide](DEPLOYMENT_GUIDE.md)** - All deployment options  
👉 **[Deploy Now!](DEPLOY_NOW.md)** - Step-by-step tutorial

**Or run locally:** `streamlit run app.py`

## 🌟 Features

### 📊 Inputs Section
- **Ticker Symbol Input**: Analyze any stock with options available
- **Expiration Date Selection**: Choose from available options expiration dates
- **Risk-Free Rate Slider**: Adjust the risk-free interest rate (0-10%)
- **Binomial Tree Steps**: Configure precision of American options pricing (10-200 steps)
- **Portfolio Parameters**: Set portfolio amount and risk percentage per trade
- **Live Market Data**: Real-time stock prices via yfinance API
- **Automated Volatility Calculation**: Historical volatility using 252 trading days

### 📊 Display Section
- **Live Options Chain**: Real-time call and put options prices, bid/ask spreads, volume, and open interest
- **Fair Value Calculations**: 
  - Black-Scholes model for European options
  - Binomial Tree model for American options
  - Side-by-side comparison of market vs fair values
- **Monte Carlo Simulation**: Customizable number of trials (1,000-100,000) to simulate price distributions at expiration
- **Machine Learning Predictions**:
  - Decision Tree Regressor with feature importance analysis
  - Support Vector Machine (SVM) with RBF kernel
  - Model performance metrics (R² scores)

### 🤖 AI Recommendation Section
- **Intelligent Strategy Generation**: Analyzes all data to recommend optimal trading strategies
- **Risk-Adjusted Returns**: Maximizes returns while considering risk
- **Portfolio Constraints**: Respects portfolio size and risk percentage limits
- **Value Analysis**: Identifies undervalued and overvalued options
- **Probability Analysis**: Calculates probability of profit based on simulations
- **Position Sizing**: Recommends number of contracts based on risk parameters
- **Confidence Ratings**: HIGH, MEDIUM, or LOW confidence recommendations
- **Liquidity Filtering**: Avoids illiquid options with low volume/open interest
- **🆕 Complete Trading Plan**: Entry and exit parameters for every recommendation
  - **Entry Parameters**: Recommended entry price, max entry price, order type, timing, breakeven
  - **Exit Parameters**: Multiple profit targets, stop loss, exit strategy
  - **Risk/Reward Analysis**: Risk/reward ratios, max loss, potential profits

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

4. **Access the application**:
   - The app will automatically open in your default browser
   - Default URL: http://localhost:8501

## 📖 Usage Guide

### Getting Started

1. **Enter a Ticker Symbol**
   - Type any valid stock ticker (e.g., AAPL, MSFT, TSLA, SPY)
   - Click "Load Data" button

2. **Select Expiration Date**
   - Choose from available options expiration dates
   - The system will load the complete options chain

3. **Configure Parameters**
   - Adjust risk-free rate (typically 4-6% for US Treasury rates)
   - Set binomial tree steps (higher = more accurate but slower)
   - Input your portfolio value
   - Set risk percentage per trade (typically 1-5%)
   - Choose number of Monte Carlo simulations

4. **Review Analysis**
   - Examine live options prices
   - Compare market prices to calculated fair values
   - Review Monte Carlo simulation results
   - Check ML model predictions
   - Read AI-generated recommendations

### Understanding the Recommendations

Each recommendation includes:
- **Action**: BUY CALL, BUY PUT, SELL CALL, SELL PUT, or HOLD
- **Confidence Level**: HIGH, MEDIUM, or LOW
- **Valuation**: Undervalued, Overvalued, or Fair
- **Probability ITM**: Chance the option finishes in-the-money
- **Risk-Adjusted Return**: Expected return relative to risk
- **Position Size**: Number of contracts to trade
- **Total Cost**: Total capital required for the position
- **🆕 Entry Parameters**:
  - Recommended entry price (optimized for bid-ask spread)
  - Max entry price (never pay more than this)
  - Order type (MARKET or LIMIT)
  - Timing recommendation (ENTER NOW, ENTER SOON, or WAIT)
  - Breakeven price at expiration
- **🆕 Exit Parameters**:
  - Profit Target 1 (50% gain - conservative)
  - Profit Target 2 (100% gain - aggressive)
  - Profit Target 3 (maximum upside scenario)
  - Stop loss price and percentage
  - Complete exit strategy rules
- **🆕 Risk/Reward Analysis**:
  - Risk/Reward Ratio for each profit target
  - Maximum loss amount in dollars
  - Potential profit amounts at each target
  - Percentage of portfolio at risk

## 📊 Technical Details

### Options Pricing Models

**Black-Scholes Model**:
- Used for European-style options
- Analytical solution
- Fast computation

**Binomial Tree Model**:
- Used for American-style options
- Accounts for early exercise premium
- Configurable number of steps for accuracy

### Monte Carlo Simulation
- Generates thousands of price paths using geometric Brownian motion
- Provides probability distributions for price at expiration
- Calculates expected payoffs for different strike prices

### Machine Learning Models

**Decision Tree Regressor**:
- Features: Moving averages, volatility, momentum, RSI, lagged prices
- Max depth: 10, Min samples split: 10
- Provides feature importance rankings

**SVM with RBF Kernel**:
- Non-linear kernel for complex price patterns
- Feature scaling using StandardScaler
- Optimized hyperparameters (C=100, gamma='scale')

### AI Recommendation Logic

The AI analyzes:
1. **Fair Value Deviation**: Identifies mispriced options
2. **Probability Analysis**: Uses Monte Carlo results
3. **ML Predictions**: Incorporates both DT and SVM forecasts
4. **Risk Management**: Applies portfolio constraints
5. **Liquidity**: Filters for adequate volume and open interest
6. **Expected Returns**: Calculates risk-adjusted metrics

## ⚠️ Important Disclaimers

### Risk Warning
- Options trading involves substantial risk and is not suitable for all investors
- You can lose your entire investment
- Past performance does not guarantee future results
- This tool is for educational purposes only

### Not Financial Advice
- This application does not constitute financial, investment, or trading advice
- Always do your own research and due diligence
- Consult with a qualified financial advisor before making investment decisions
- The creators are not responsible for any financial losses

### Data Accuracy
- Market data is sourced from yfinance (Yahoo Finance API)
- Data may be delayed or inaccurate
- Always verify prices with your broker before trading
- Model predictions are estimates and may be incorrect

## 🛠️ Troubleshooting

### Common Issues

**"Unable to load data"**:
- Check internet connection
- Verify ticker symbol is valid
- Try a different ticker
- Yahoo Finance API may be temporarily unavailable

**"No expiration dates available"**:
- Stock may not have listed options
- Try a more liquid stock (e.g., AAPL, SPY)

**"Insufficient data for training"**:
- Stock needs at least 6-12 months of historical data
- Try a different ticker with longer history

**"Model training failed"**:
- May occur with very new stocks
- Increase the time period for historical data
- Try a more established company

### Performance Tips

- Use fewer Monte Carlo simulations for faster results (1,000-5,000)
- Reduce binomial tree steps for quicker calculations (50-100)
- Analyze fewer strikes by selecting a narrower price range
- Close unused browser tabs to free up memory

## 📦 Dependencies

- **streamlit**: Web application framework
- **yfinance**: Yahoo Finance API for market data
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **scipy**: Scientific computing and statistics
- **scikit-learn**: Machine learning models
- **matplotlib**: Data visualization
- **seaborn**: Statistical data visualization
- **plotly**: Interactive charts and graphs
- **requests**: HTTP library

## 🔄 Future Enhancements

Potential features for future versions:
- Real-time data streaming
- Multi-leg strategy builder (spreads, straddles, etc.)
- Backtesting capabilities
- Integration with broker APIs for live trading
- Portfolio optimization across multiple positions
- Greeks calculator and visualization
- Earnings and dividend adjustments
- Implied volatility surface analysis
- Options flow data integration

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your own use.

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Verify all dependencies are installed correctly

## 🙏 Acknowledgments

- Market data provided by Yahoo Finance
- Built with Streamlit, scikit-learn, and other open-source libraries
- Options pricing theory based on Black-Scholes and Cox-Ross-Rubinstein models

---

**Remember**: This is an educational tool. Always practice proper risk management and never invest more than you can afford to lose.

Happy Trading! 📈🎯

