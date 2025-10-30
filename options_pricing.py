"""
Options pricing models for American and European options
"""
import numpy as np
from scipy.stats import norm
from datetime import datetime


class OptionsPricing:
    """Options pricing using various models"""
    
    @staticmethod
    def black_scholes(S, K, T, r, sigma, option_type='call'):
        """
        Black-Scholes formula for European options
        S: Current stock price
        K: Strike price
        T: Time to maturity (in years)
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
        """
        if T <= 0:
            if option_type == 'call':
                return max(S - K, 0)
            else:
                return max(K - S, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return price
    
    @staticmethod
    def binomial_tree_american(S, K, T, r, sigma, N, option_type='call'):
        """
        Binomial tree model for American options
        S: Current stock price
        K: Strike price
        T: Time to maturity (in years)
        r: Risk-free rate
        sigma: Volatility
        N: Number of steps
        option_type: 'call' or 'put'
        """
        if T <= 0 or N <= 0:
            if option_type == 'call':
                return max(S - K, 0)
            else:
                return max(K - S, 0)
        
        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)
        
        # Initialize asset prices at maturity
        asset_prices = np.zeros(N + 1)
        for i in range(N + 1):
            asset_prices[i] = S * (u ** (N - i)) * (d ** i)
        
        # Initialize option values at maturity
        option_values = np.zeros(N + 1)
        for i in range(N + 1):
            if option_type == 'call':
                option_values[i] = max(asset_prices[i] - K, 0)
            else:
                option_values[i] = max(K - asset_prices[i], 0)
        
        # Backward induction
        for step in range(N - 1, -1, -1):
            for i in range(step + 1):
                # Calculate stock price at this node
                stock_price = S * (u ** (step - i)) * (d ** i)
                
                # Calculate option value by discounting expected value
                option_values[i] = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])
                
                # Check for early exercise (American option)
                if option_type == 'call':
                    exercise_value = max(stock_price - K, 0)
                else:
                    exercise_value = max(K - stock_price, 0)
                
                option_values[i] = max(option_values[i], exercise_value)
        
        return option_values[0]
    
    @staticmethod
    def monte_carlo_simulation(S, T, r, sigma, num_simulations=10000):
        """
        Monte Carlo simulation for stock price at expiration
        S: Current stock price
        T: Time to maturity (in years)
        r: Risk-free rate
        sigma: Volatility
        num_simulations: Number of simulation paths
        """
        if T <= 0:
            return np.array([S] * num_simulations)
        
        # Generate random paths
        z = np.random.standard_normal(num_simulations)
        ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
        
        return ST
    
    @staticmethod
    def monte_carlo_price_paths(S, r, sigma, days, num_simulations=10000):
        """
        Monte Carlo simulation generating full price paths over time
        S: Current price
        r: Risk-free rate (annualized)
        sigma: Volatility (annualized)
        days: Number of days to simulate
        num_simulations: Number of simulation paths
        Returns: Array of shape (num_simulations, days) with price paths
        """
        dt = 1 / 252  # Daily time step (trading days)
        paths = np.zeros((num_simulations, days))
        paths[:, 0] = S
        
        for t in range(1, days):
            z = np.random.standard_normal(num_simulations)
            paths[:, t] = paths[:, t-1] * np.exp(
                (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z
            )
        
        return paths
    
    @staticmethod
    def calculate_greeks(S, K, T, r, sigma, option_type='call'):
        """Calculate option Greeks"""
        if T <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            delta = norm.cdf(d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                     r * K * np.exp(-r * T) * norm.cdf(d2))
            rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        else:
            delta = norm.cdf(d1) - 1
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + 
                     r * K * np.exp(-r * T) * norm.cdf(-d2))
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta / 365,  # Daily theta
            'vega': vega / 100,  # Vega per 1% change
            'rho': rho / 100  # Rho per 1% change
        }
    
    @staticmethod
    def days_to_expiration(expiration_date_str):
        """Calculate days to expiration"""
        try:
            exp_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
            today = datetime.now()
            days = (exp_date - today).days
            return max(days, 0)
        except:
            return 0
    
    @staticmethod
    def years_to_expiration(expiration_date_str):
        """Calculate years to expiration"""
        days = OptionsPricing.days_to_expiration(expiration_date_str)
        return days / 365.0

