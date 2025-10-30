"""
Data fetcher module for retrieving stock, options, and futures data
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataFetcher:
    """Fetches live market data for stocks, options, and futures"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.is_futures = self._check_if_futures(ticker)
        
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
    
    def _check_if_futures(self, ticker: str) -> bool:
        """Check if ticker is a futures contract"""
        # Common futures patterns
        futures_indicators = ['=F', '/']
        return any(indicator in ticker.upper() for indicator in futures_indicators)
    
    def get_futures_info(self):
        """Get futures contract information"""
        if not self.is_futures:
            return None
        
        try:
            info = self.stock.info
            current_price = self.get_current_price()
            
            # Calculate contract multiplier based on common futures
            multiplier = self._get_contract_multiplier(self.ticker)
            
            return {
                'symbol': self.ticker,
                'current_price': current_price,
                'contract_multiplier': multiplier,
                'currency': info.get('currency', 'USD'),
                'name': info.get('shortName', self.ticker),
                'exchange': info.get('exchange', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching futures info: {e}")
            # Return basic info even if API fails
            return {
                'symbol': self.ticker,
                'current_price': self.get_current_price(),
                'contract_multiplier': self._get_contract_multiplier(self.ticker),
                'currency': 'USD',
                'name': self.ticker,
                'exchange': 'N/A'
            }
    
    def _get_contract_multiplier(self, ticker: str) -> int:
        """Get contract multiplier for common futures contracts"""
        ticker_upper = ticker.upper()
        
        # Common futures multipliers
        multipliers = {
            'ES': 50,      # E-mini S&P 500
            'NQ': 20,      # E-mini Nasdaq-100
            'YM': 5,       # E-mini Dow
            'RTY': 50,     # E-mini Russell 2000
            'CL': 1000,    # Crude Oil
            'GC': 100,     # Gold
            'SI': 5000,    # Silver
            'NG': 10000,   # Natural Gas
            'ZB': 1000,    # 30-Year T-Bond
            'ZN': 1000,    # 10-Year T-Note
            'ZC': 50,      # Corn
            'ZS': 50,      # Soybeans
            'ZW': 50,      # Wheat
            '6E': 125000,  # Euro FX
            '6J': 12500000,# Japanese Yen
            '6B': 62500,   # British Pound
        }
        
        # Check for known multipliers
        for symbol, multiplier in multipliers.items():
            if ticker_upper.startswith(symbol):
                return multiplier
        
        # Default multiplier for unknown contracts
        return 1
    
    def get_futures_margin_estimate(self, current_price: float) -> dict:
        """Estimate initial and maintenance margin for futures contract"""
        # These are rough estimates - actual margins vary by broker and contract
        multiplier = self._get_contract_multiplier(self.ticker)
        contract_value = current_price * multiplier
        
        # Typical margin is 5-15% of contract value
        initial_margin = contract_value * 0.10  # 10% estimate
        maintenance_margin = contract_value * 0.075  # 7.5% estimate
        
        return {
            'initial_margin': initial_margin,
            'maintenance_margin': maintenance_margin,
            'contract_value': contract_value,
            'multiplier': multiplier
        }

