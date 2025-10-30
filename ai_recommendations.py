"""
AI-powered recommendations for options trading strategies
"""
import numpy as np
import pandas as pd
from options_pricing import OptionsPricing


class AIRecommendations:
    """Generate intelligent trading recommendations"""
    
    @staticmethod
    def analyze_option_value(fair_value, market_price, option_type='call'):
        """
        Analyze if an option is undervalued or overvalued
        Returns: 'undervalued', 'overvalued', or 'fair'
        """
        if market_price is None or fair_value is None or market_price <= 0:
            return 'unknown', 0
        
        diff_pct = ((market_price - fair_value) / fair_value) * 100
        
        # Threshold for considering under/over valued
        threshold = 10  # 10% difference
        
        if diff_pct < -threshold:
            return 'undervalued', diff_pct
        elif diff_pct > threshold:
            return 'overvalued', diff_pct
        else:
            return 'fair', diff_pct
    
    @staticmethod
    def calculate_risk_adjusted_return(expected_return, probability, risk):
        """Calculate risk-adjusted return using Sharpe-like ratio"""
        if risk <= 0:
            return 0
        return (expected_return * probability) / risk
    
    @staticmethod
    def analyze_monte_carlo_results(simulated_prices, current_price, strike_price, option_type='call'):
        """
        Analyze Monte Carlo simulation results
        Returns probability of profit and expected payoff
        """
        if option_type == 'call':
            payoffs = np.maximum(simulated_prices - strike_price, 0)
            prob_itm = np.mean(simulated_prices > strike_price)
        else:
            payoffs = np.maximum(strike_price - simulated_prices, 0)
            prob_itm = np.mean(simulated_prices < strike_price)
        
        expected_payoff = np.mean(payoffs)
        payoff_std = np.std(payoffs)
        
        # Percentiles
        percentiles = {
            '10th': np.percentile(simulated_prices, 10),
            '25th': np.percentile(simulated_prices, 25),
            '50th': np.percentile(simulated_prices, 50),
            '75th': np.percentile(simulated_prices, 75),
            '90th': np.percentile(simulated_prices, 90)
        }
        
        return {
            'probability_itm': prob_itm,
            'expected_payoff': expected_payoff,
            'payoff_std': payoff_std,
            'percentiles': percentiles
        }
    
    @staticmethod
    def calculate_position_size(portfolio_value, risk_percentage, option_price, max_loss_per_contract=100):
        """
        Calculate optimal position size based on risk management
        """
        if option_price <= 0:
            return 0
        
        # Amount willing to risk
        risk_amount = portfolio_value * (risk_percentage / 100)
        
        # For buying options, max loss is premium paid
        max_loss = option_price * 100  # Per contract
        
        # Number of contracts
        num_contracts = int(risk_amount / max_loss)
        
        # Ensure at least 1 contract if there's enough capital
        if num_contracts == 0 and portfolio_value > option_price * 100:
            num_contracts = 1
        
        return num_contracts
    
    @staticmethod
    def calculate_buy_parameters(action, option_type, strike, current_price, bid, ask, 
                                 market_price, fair_value, probability_itm, mc_analysis):
        """
        Calculate detailed buy parameters for entry
        """
        # Entry price recommendations
        bid_ask_spread = ask - bid
        spread_pct = (bid_ask_spread / market_price * 100) if market_price > 0 else 0
        
        # Recommended entry price (between bid and fair value for buys)
        if 'BUY' in action:
            # Try to get better than ask price
            if spread_pct < 5:  # Tight spread
                entry_price = ask  # Can use market order
                order_type = 'MARKET'
            else:  # Wide spread
                # Place limit order between bid and ask, closer to bid
                entry_price = bid + (bid_ask_spread * 0.3)
                order_type = 'LIMIT'
            
            # But don't pay more than fair value + 5%
            max_entry_price = fair_value * 1.05
            entry_price = min(entry_price, max_entry_price)
            
        else:  # SELL
            if spread_pct < 5:
                entry_price = bid  # Can use market order
                order_type = 'MARKET'
            else:
                # Place limit order closer to ask when selling
                entry_price = bid + (bid_ask_spread * 0.7)
                order_type = 'LIMIT'
            
            # Don't sell below fair value - 5%
            min_entry_price = fair_value * 0.95
            entry_price = max(entry_price, min_entry_price)
        
        # Timing recommendation
        if probability_itm > 0.60:
            timing = 'ENTER NOW'
        elif probability_itm > 0.50:
            timing = 'ENTER SOON'
        else:
            timing = 'WAIT FOR BETTER SETUP'
        
        # Calculate break-even
        if option_type == 'CALL':
            breakeven = strike + entry_price
        else:  # PUT
            breakeven = strike - entry_price
        
        return {
            'entry_price': entry_price,
            'max_entry_price': max_entry_price if 'BUY' in action else entry_price * 1.10,
            'order_type': order_type,
            'timing': timing,
            'breakeven': breakeven,
            'spread_pct': spread_pct
        }
    
    @staticmethod
    def calculate_sell_parameters(action, option_type, strike, entry_price, expected_payoff,
                                  probability_itm, mc_analysis, position_size):
        """
        Calculate detailed sell/exit parameters
        """
        # Profit targets based on probability and expected payoff
        percentiles = mc_analysis.get('percentiles', {})
        
        if 'BUY' in action:
            # For buying options
            # Conservative target: 50% profit
            profit_target_1 = entry_price * 1.50
            # Aggressive target: 100% profit
            profit_target_2 = entry_price * 2.00
            # Moon shot: Based on 75th percentile outcome
            if option_type == 'CALL':
                best_case_payoff = max(percentiles.get('75th', strike) - strike, 0)
            else:
                best_case_payoff = max(strike - percentiles.get('25th', strike), 0)
            
            profit_target_3 = min(best_case_payoff, entry_price * 3.00)
            
            # Stop loss: typically 30-50% of premium for options
            if probability_itm > 0.60:
                stop_loss = entry_price * 0.50  # 50% loss max for high probability
            elif probability_itm > 0.50:
                stop_loss = entry_price * 0.40  # 60% loss max
            else:
                stop_loss = entry_price * 0.30  # 70% loss max (more speculative)
            
            # Time-based exit
            if probability_itm > 0.55:
                exit_strategy = 'HOLD TO EXPIRATION if ITM, else exit at 50% loss'
            else:
                exit_strategy = 'EXIT at 50% profit or 50% loss, or 5 days before expiration'
            
        else:  # SELL options
            # For selling options - we want them to expire worthless
            # Take profit if option loses 50-80% of value
            profit_target_1 = entry_price * 0.50  # Buy back at 50% of sold price
            profit_target_2 = entry_price * 0.25  # Buy back at 75% profit
            profit_target_3 = 0.05  # Nearly worthless
            
            # Stop loss: if option increases 100-150% (threat of assignment)
            stop_loss = entry_price * 2.00
            
            exit_strategy = 'BUY TO CLOSE at 50-80% profit, or if price doubles (stop loss)'
        
        # Risk/Reward ratios
        total_cost = entry_price * 100 * position_size
        
        profit_1_amount = (profit_target_1 - entry_price) * 100 * position_size
        profit_2_amount = (profit_target_2 - entry_price) * 100 * position_size
        
        if 'BUY' in action:
            max_loss = total_cost * (1 - stop_loss / entry_price)
            risk_reward_1 = profit_1_amount / max_loss if max_loss > 0 else 0
            risk_reward_2 = profit_2_amount / max_loss if max_loss > 0 else 0
        else:
            max_loss = (stop_loss - entry_price) * 100 * position_size
            risk_reward_1 = abs(profit_1_amount / max_loss) if max_loss > 0 else 0
            risk_reward_2 = abs(profit_2_amount / max_loss) if max_loss > 0 else 0
        
        return {
            'profit_target_1': profit_target_1,
            'profit_target_2': profit_target_2,
            'profit_target_3': profit_target_3,
            'stop_loss': stop_loss,
            'stop_loss_pct': ((stop_loss - entry_price) / entry_price * 100),
            'exit_strategy': exit_strategy,
            'risk_reward_ratio_1': risk_reward_1,
            'risk_reward_ratio_2': risk_reward_2,
            'max_loss_amount': max_loss,
            'profit_1_amount': profit_1_amount,
            'profit_2_amount': profit_2_amount
        }
    
    @staticmethod
    def generate_strategy_recommendation(
        current_price,
        strike_prices,
        options_data,
        fair_values,
        monte_carlo_results,
        ml_predictions,
        portfolio_value,
        risk_percentage,
        expiration_date,
        risk_free_rate,
        volatility
    ):
        """
        Generate comprehensive trading strategy recommendation
        """
        recommendations = []
        
        T = OptionsPricing.years_to_expiration(expiration_date)
        
        # Analyze calls
        for strike in strike_prices:
            call_data = options_data['calls'][options_data['calls']['strike'] == strike]
            
            if call_data.empty:
                continue
            
            market_call_price = call_data['lastPrice'].values[0]
            call_bid = call_data['bid'].values[0]
            call_ask = call_data['ask'].values[0]
            call_volume = call_data['volume'].values[0]
            call_oi = call_data['openInterest'].values[0]
            
            # Get fair value
            fair_call = fair_values.get(f'call_{strike}', market_call_price)
            
            # Analyze value
            valuation, diff_pct = AIRecommendations.analyze_option_value(
                fair_call, market_call_price, 'call'
            )
            
            # Monte Carlo analysis
            mc_analysis = AIRecommendations.analyze_monte_carlo_results(
                monte_carlo_results, current_price, strike, 'call'
            )
            
            # Position sizing
            position_size = AIRecommendations.calculate_position_size(
                portfolio_value, risk_percentage, market_call_price
            )
            
            # Calculate expected return
            expected_payoff = mc_analysis['expected_payoff']
            cost = market_call_price * 100
            expected_return = (expected_payoff * 100 - cost) if cost > 0 else 0
            risk_adjusted_return = AIRecommendations.calculate_risk_adjusted_return(
                expected_return,
                mc_analysis['probability_itm'],
                cost
            )
            
            # Create recommendation
            if valuation == 'undervalued' and mc_analysis['probability_itm'] > 0.45:
                action = 'BUY CALL'
                confidence = 'HIGH' if mc_analysis['probability_itm'] > 0.55 else 'MEDIUM'
            elif valuation == 'overvalued' and mc_analysis['probability_itm'] < 0.40:
                action = 'SELL CALL'
                confidence = 'MEDIUM'
            else:
                action = 'HOLD'
                confidence = 'LOW'
            
            # Add liquidity check
            if call_volume < 10 or call_oi < 50:
                confidence = 'LOW'
                action = 'HOLD'  # Avoid illiquid options
            
            # Calculate buy/sell parameters
            buy_params = AIRecommendations.calculate_buy_parameters(
                action, 'CALL', strike, current_price, call_bid, call_ask,
                market_call_price, fair_call, mc_analysis['probability_itm'], mc_analysis
            )
            
            sell_params = AIRecommendations.calculate_sell_parameters(
                action, 'CALL', strike, buy_params['entry_price'], expected_payoff,
                mc_analysis['probability_itm'], mc_analysis, position_size
            )
            
            recommendations.append({
                'type': 'CALL',
                'strike': strike,
                'action': action,
                'confidence': confidence,
                'valuation': valuation,
                'fair_value': fair_call,
                'market_price': market_call_price,
                'bid': call_bid,
                'ask': call_ask,
                'value_diff_pct': diff_pct,
                'probability_itm': mc_analysis['probability_itm'],
                'expected_payoff': expected_payoff,
                'risk_adjusted_return': risk_adjusted_return,
                'position_size': position_size,
                'total_cost': market_call_price * 100 * position_size,
                'volume': call_volume,
                'open_interest': call_oi,
                # Buy parameters
                'entry_price': buy_params['entry_price'],
                'max_entry_price': buy_params['max_entry_price'],
                'order_type': buy_params['order_type'],
                'timing': buy_params['timing'],
                'breakeven': buy_params['breakeven'],
                'spread_pct': buy_params['spread_pct'],
                # Sell parameters
                'profit_target_1': sell_params['profit_target_1'],
                'profit_target_2': sell_params['profit_target_2'],
                'profit_target_3': sell_params['profit_target_3'],
                'stop_loss': sell_params['stop_loss'],
                'stop_loss_pct': sell_params['stop_loss_pct'],
                'exit_strategy': sell_params['exit_strategy'],
                'risk_reward_ratio_1': sell_params['risk_reward_ratio_1'],
                'risk_reward_ratio_2': sell_params['risk_reward_ratio_2'],
                'max_loss_amount': sell_params['max_loss_amount'],
                'profit_1_amount': sell_params['profit_1_amount'],
                'profit_2_amount': sell_params['profit_2_amount']
            })
        
        # Analyze puts
        for strike in strike_prices:
            put_data = options_data['puts'][options_data['puts']['strike'] == strike]
            
            if put_data.empty:
                continue
            
            market_put_price = put_data['lastPrice'].values[0]
            put_bid = put_data['bid'].values[0]
            put_ask = put_data['ask'].values[0]
            put_volume = put_data['volume'].values[0]
            put_oi = put_data['openInterest'].values[0]
            
            # Get fair value
            fair_put = fair_values.get(f'put_{strike}', market_put_price)
            
            # Analyze value
            valuation, diff_pct = AIRecommendations.analyze_option_value(
                fair_put, market_put_price, 'put'
            )
            
            # Monte Carlo analysis
            mc_analysis = AIRecommendations.analyze_monte_carlo_results(
                monte_carlo_results, current_price, strike, 'put'
            )
            
            # Position sizing
            position_size = AIRecommendations.calculate_position_size(
                portfolio_value, risk_percentage, market_put_price
            )
            
            # Calculate expected return
            expected_payoff = mc_analysis['expected_payoff']
            cost = market_put_price * 100
            expected_return = (expected_payoff * 100 - cost) if cost > 0 else 0
            risk_adjusted_return = AIRecommendations.calculate_risk_adjusted_return(
                expected_return,
                mc_analysis['probability_itm'],
                cost
            )
            
            # Create recommendation
            if valuation == 'undervalued' and mc_analysis['probability_itm'] > 0.45:
                action = 'BUY PUT'
                confidence = 'HIGH' if mc_analysis['probability_itm'] > 0.55 else 'MEDIUM'
            elif valuation == 'overvalued' and mc_analysis['probability_itm'] < 0.40:
                action = 'SELL PUT'
                confidence = 'MEDIUM'
            else:
                action = 'HOLD'
                confidence = 'LOW'
            
            # Add liquidity check
            if put_volume < 10 or put_oi < 50:
                confidence = 'LOW'
                action = 'HOLD'
            
            # Calculate buy/sell parameters
            buy_params = AIRecommendations.calculate_buy_parameters(
                action, 'PUT', strike, current_price, put_bid, put_ask,
                market_put_price, fair_put, mc_analysis['probability_itm'], mc_analysis
            )
            
            sell_params = AIRecommendations.calculate_sell_parameters(
                action, 'PUT', strike, buy_params['entry_price'], expected_payoff,
                mc_analysis['probability_itm'], mc_analysis, position_size
            )
            
            recommendations.append({
                'type': 'PUT',
                'strike': strike,
                'action': action,
                'confidence': confidence,
                'valuation': valuation,
                'fair_value': fair_put,
                'market_price': market_put_price,
                'bid': put_bid,
                'ask': put_ask,
                'value_diff_pct': diff_pct,
                'probability_itm': mc_analysis['probability_itm'],
                'expected_payoff': expected_payoff,
                'risk_adjusted_return': risk_adjusted_return,
                'position_size': position_size,
                'total_cost': market_put_price * 100 * position_size,
                'volume': put_volume,
                'open_interest': put_oi,
                # Buy parameters
                'entry_price': buy_params['entry_price'],
                'max_entry_price': buy_params['max_entry_price'],
                'order_type': buy_params['order_type'],
                'timing': buy_params['timing'],
                'breakeven': buy_params['breakeven'],
                'spread_pct': buy_params['spread_pct'],
                # Sell parameters
                'profit_target_1': sell_params['profit_target_1'],
                'profit_target_2': sell_params['profit_target_2'],
                'profit_target_3': sell_params['profit_target_3'],
                'stop_loss': sell_params['stop_loss'],
                'stop_loss_pct': sell_params['stop_loss_pct'],
                'exit_strategy': sell_params['exit_strategy'],
                'risk_reward_ratio_1': sell_params['risk_reward_ratio_1'],
                'risk_reward_ratio_2': sell_params['risk_reward_ratio_2'],
                'max_loss_amount': sell_params['max_loss_amount'],
                'profit_1_amount': sell_params['profit_1_amount'],
                'profit_2_amount': sell_params['profit_2_amount']
            })
        
        # Sort by risk-adjusted return
        recommendations_df = pd.DataFrame(recommendations)
        if not recommendations_df.empty:
            recommendations_df = recommendations_df.sort_values('risk_adjusted_return', ascending=False)
        
        return recommendations_df
    
    @staticmethod
    def get_top_recommendations(recommendations_df, top_n=5):
        """Get top N recommendations with HIGH or MEDIUM confidence"""
        if recommendations_df.empty:
            return pd.DataFrame()
        
        # Filter for actionable recommendations
        actionable = recommendations_df[
            (recommendations_df['action'] != 'HOLD') & 
            (recommendations_df['confidence'].isin(['HIGH', 'MEDIUM']))
        ]
        
        return actionable.head(top_n)

