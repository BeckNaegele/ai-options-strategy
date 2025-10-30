"""
Data fetcher module for retrieving stock and options data
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataFetcher:
    """Fetches live market data for stocks and options"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        
    def get_current_price(self):
        """Get current stock price"""
        try:
            data = self.stock.history(period='1d')
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None
    
    def get_historical_data(self, period='1y'):
        """Get historical price data"""
        try:
            data = self.stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def calculate_historical_volatility(self, days=252):
        """Calculate annualized historical volatility"""
        try:
            hist_data = self.get_historical_data(period='1y')
            if hist_data.empty or len(hist_data) < 2:
                return None
            
            # Calculate log returns
            log_returns = np.log(hist_data['Close'] / hist_data['Close'].shift(1))
            
            # Calculate annualized volatility
            volatility = log_returns.std() * np.sqrt(days)
            return volatility
        except Exception as e:
            print(f"Error calculating volatility: {e}")
            return None
    
    def get_options_chain(self, expiration_date):
        """Get options chain for a specific expiration date"""
        try:
            # Get options data
            opts = self.stock.option_chain(expiration_date)
            return {
                'calls': opts.calls,
                'puts': opts.puts
            }
        except Exception as e:
            print(f"Error fetching options chain: {e}")
            return None
    
    def get_available_expirations(self):
        """Get all available expiration dates"""
        try:
            return self.stock.options
        except Exception as e:
            print(f"Error fetching expiration dates: {e}")
            return []
    
    def get_risk_free_rate_estimate(self):
        """Estimate risk-free rate using Treasury data"""
        try:
            # Use 10-year Treasury as proxy
            tnx = yf.Ticker("^TNX")
            data = tnx.history(period='5d')
            if not data.empty:
                return data['Close'].iloc[-1] / 100  # Convert from percentage
            return 0.05  # Default fallback
        except:
            return 0.05  # Default fallback

