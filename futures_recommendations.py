"""
Futures Trading Recommendations Module
Generates AI-powered futures trading recommendations
"""
import pandas as pd
import numpy as np
from datetime import datetime


class FuturesRecommendations:
    """Generate trading recommendations for futures contracts"""
    
    @staticmethod
    def calculate_position_size(portfolio_value, risk_percentage, margin_required):
        """Calculate number of futures contracts based on portfolio and risk"""
        if margin_required <= 0:
            return 0
        
        max_risk_amount = portfolio_value * (risk_percentage / 100)
        
        # For futures, we use margin as the capital requirement
        # Calculate how many contracts we can afford with our risk capital
        num_contracts = int(max_risk_amount / margin_required)
        
        # Ensure at least 1 contract if portfolio is sufficient
        if num_contracts == 0 and portfolio_value > margin_required:
            num_contracts = 1
        
        return num_contracts
    
    @staticmethod
    def analyze_ml_predictions_futures(current_price, ml_predictions, action):
        """
        Analyze ML predictions (SVM) for futures trading
        Returns: (ml_score, ml_insights, confidence_adjustment)
        """
        ml_score = 50  # Neutral baseline
        insights = []
        confidence_adjustment = 0
        
        if not ml_predictions or 'svm' not in ml_predictions:
            return {
                'ml_score': 50,
                'insights': ['No ML predictions available'],
                'confidence_adjustment': 0,
                'predicted_price': current_price,
                'predicted_change_pct': 0
            }
        
        svm_prediction = ml_predictions.get('svm', current_price)
        predicted_change = ((svm_prediction - current_price) / current_price) * 100
        
        # Determine if prediction supports the action
        if 'LONG' in action or 'BUY' in action:
            # Going long - want bullish prediction
            if predicted_change > 5:
                ml_score += 30
                insights.append(f"✅ SVM predicts +{predicted_change:.1f}% move - Strong bullish signal")
                confidence_adjustment += 0.15
            elif predicted_change > 2:
                ml_score += 15
                insights.append(f"✅ SVM predicts +{predicted_change:.1f}% move - Modest bullish signal")
                confidence_adjustment += 0.08
            elif predicted_change < -2:
                ml_score -= 20
                insights.append(f"⚠️ SVM predicts {predicted_change:.1f}% move - Contradicts LONG position")
                confidence_adjustment -= 0.15
            else:
                insights.append(f"ℹ️ SVM predicts {predicted_change:.1f}% move - Neutral signal")
        
        elif 'SHORT' in action or 'SELL' in action:
            # Going short - want bearish prediction
            if predicted_change < -5:
                ml_score += 30
                insights.append(f"✅ SVM predicts {predicted_change:.1f}% move - Strong bearish signal")
                confidence_adjustment += 0.15
            elif predicted_change < -2:
                ml_score += 15
                insights.append(f"✅ SVM predicts {predicted_change:.1f}% move - Modest bearish signal")
                confidence_adjustment += 0.08
            elif predicted_change > 2:
                ml_score -= 20
                insights.append(f"⚠️ SVM predicts +{predicted_change:.1f}% move - Contradicts SHORT position")
                confidence_adjustment -= 0.15
            else:
                insights.append(f"ℹ️ SVM predicts {predicted_change:.1f}% move - Neutral signal")
        
        # Magnitude of move
        abs_change = abs(predicted_change)
        if abs_change > 10:
            ml_score += 10
            insights.append(f"⚠️ Large predicted move ({abs_change:.1f}%) - High volatility expected")
        elif abs_change < 1:
            ml_score -= 10
            insights.append(f"ℹ️ Small predicted move ({abs_change:.1f}%) - Range-bound expected")
        
        # Normalize score
        ml_score = max(0, min(100, ml_score))
        
        return {
            'ml_score': ml_score,
            'insights': insights,
            'confidence_adjustment': confidence_adjustment,
            'predicted_price': svm_prediction,
            'predicted_change_pct': predicted_change
        }
    
    @staticmethod
    def analyze_monte_carlo_futures(monte_carlo_results, current_price):
        """Analyze Monte Carlo simulation results for futures"""
        if monte_carlo_results is None or len(monte_carlo_results) == 0:
            return {
                'probability_up': 0.5,
                'probability_down': 0.5,
                'expected_price': current_price,
                'upside_potential': 0,
                'downside_risk': 0,
                'volatility': 0
            }
        
        final_prices = monte_carlo_results[:, -1]
        
        # Calculate probabilities
        prob_up = np.mean(final_prices > current_price)
        prob_down = 1 - prob_up
        
        # Expected price
        expected_price = np.mean(final_prices)
        
        # Potential gains/losses
        upside_potential = np.percentile(final_prices, 75) - current_price
        downside_risk = current_price - np.percentile(final_prices, 25)
        
        # Volatility measure
        volatility = np.std(final_prices)
        
        return {
            'probability_up': prob_up,
            'probability_down': prob_down,
            'expected_price': expected_price,
            'upside_potential': upside_potential,
            'downside_risk': downside_risk,
            'volatility': volatility
        }
    
    @staticmethod
    def calculate_risk_adjusted_return(expected_return, probability, margin):
        """Calculate risk-adjusted return for futures"""
        if margin <= 0:
            return 0
        
        # Risk-adjusted return considers probability and leverage
        return (expected_return * probability) / margin
    
    @staticmethod
    def calculate_entry_parameters(action, current_price, volatility):
        """Calculate entry parameters for futures trade"""
        # Futures have simpler entry - just the futures price
        if volatility > 0:
            atr_estimate = current_price * volatility * 0.1  # Rough ATR estimate
        else:
            atr_estimate = current_price * 0.02
        
        if 'LONG' in action or 'BUY' in action:
            entry_price = current_price
            stop_loss = current_price - (2 * atr_estimate)  # 2 ATR below
            profit_target_1 = current_price + (2 * atr_estimate)  # 2:1 R/R
            profit_target_2 = current_price + (3 * atr_estimate)  # 3:1 R/R
            profit_target_3 = current_price + (4 * atr_estimate)  # 4:1 R/R
        else:  # SHORT
            entry_price = current_price
            stop_loss = current_price + (2 * atr_estimate)  # 2 ATR above
            profit_target_1 = current_price - (2 * atr_estimate)  # 2:1 R/R
            profit_target_2 = current_price - (3 * atr_estimate)  # 3:1 R/R
            profit_target_3 = current_price - (4 * atr_estimate)  # 4:1 R/R
        
        return {
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'profit_target_1': profit_target_1,
            'profit_target_2': profit_target_2,
            'profit_target_3': profit_target_3,
            'atr_estimate': atr_estimate
        }
    
    @staticmethod
    def calculate_exit_parameters(action, entry_params, multiplier, position_size):
        """Calculate exit parameters and P/L estimates"""
        entry_price = entry_params['entry_price']
        stop_loss = entry_params['stop_loss']
        pt1 = entry_params['profit_target_1']
        pt2 = entry_params['profit_target_2']
        pt3 = entry_params['profit_target_3']
        
        # Calculate P/L amounts (considering multiplier)
        if 'LONG' in action or 'BUY' in action:
            max_loss = (entry_price - stop_loss) * multiplier * position_size
            profit_1 = (pt1 - entry_price) * multiplier * position_size
            profit_2 = (pt2 - entry_price) * multiplier * position_size
            profit_3 = (pt3 - entry_price) * multiplier * position_size
        else:  # SHORT
            max_loss = (stop_loss - entry_price) * multiplier * position_size
            profit_1 = (entry_price - pt1) * multiplier * position_size
            profit_2 = (entry_price - pt2) * multiplier * position_size
            profit_3 = (entry_price - pt3) * multiplier * position_size
        
        # Risk/reward ratios
        rr1 = profit_1 / max_loss if max_loss > 0 else 0
        rr2 = profit_2 / max_loss if max_loss > 0 else 0
        rr3 = profit_3 / max_loss if max_loss > 0 else 0
        
        return {
            'max_loss': max_loss,
            'profit_1': profit_1,
            'profit_2': profit_2,
            'profit_3': profit_3,
            'risk_reward_1': rr1,
            'risk_reward_2': rr2,
            'risk_reward_3': rr3
        }
    
    @staticmethod
    def generate_futures_recommendation(
        current_price,
        futures_info,
        margin_info,
        monte_carlo_results,
        ml_predictions,
        portfolio_value,
        risk_percentage,
        volatility
    ):
        """
        Generate comprehensive futures trading recommendation
        """
        multiplier = futures_info['contract_multiplier']
        initial_margin = margin_info['initial_margin']
        
        # Position sizing
        position_size = FuturesRecommendations.calculate_position_size(
            portfolio_value, risk_percentage, initial_margin
        )
        
        # Monte Carlo analysis
        mc_analysis = FuturesRecommendations.analyze_monte_carlo_futures(
            monte_carlo_results, current_price
        )
        
        # Determine initial action based on MC probabilities
        if mc_analysis['probability_up'] > 0.55:
            action = 'LONG FUTURES'
            confidence = 'HIGH' if mc_analysis['probability_up'] > 0.65 else 'MEDIUM'
        elif mc_analysis['probability_down'] > 0.55:
            action = 'SHORT FUTURES'
            confidence = 'HIGH' if mc_analysis['probability_down'] > 0.65 else 'MEDIUM'
        else:
            action = 'HOLD'
            confidence = 'LOW'
        
        # Expected return calculation
        expected_price_change = mc_analysis['expected_price'] - current_price
        expected_return = expected_price_change * multiplier * position_size
        
        # Calculate risk-adjusted return
        prob = mc_analysis['probability_up'] if 'LONG' in action else mc_analysis['probability_down']
        risk_adjusted_return = FuturesRecommendations.calculate_risk_adjusted_return(
            expected_return, prob, initial_margin
        )
        
        # Analyze ML predictions
        ml_analysis = FuturesRecommendations.analyze_ml_predictions_futures(
            current_price, ml_predictions, action
        )
        
        # Adjust based on ML predictions
        if action != 'HOLD':
            # Factor ML score into risk-adjusted return
            ml_multiplier = ml_analysis['ml_score'] / 100
            risk_adjusted_return = risk_adjusted_return * ml_multiplier
            
            # Adjust confidence level
            if ml_analysis['confidence_adjustment'] > 0.10:
                if confidence == 'MEDIUM':
                    confidence = 'HIGH'
                elif confidence == 'LOW':
                    confidence = 'MEDIUM'
            elif ml_analysis['confidence_adjustment'] < -0.10:
                if confidence == 'HIGH':
                    confidence = 'MEDIUM'
                elif confidence == 'MEDIUM':
                    confidence = 'LOW'
        
        # Calculate entry/exit parameters
        entry_params = FuturesRecommendations.calculate_entry_parameters(
            action, current_price, volatility
        )
        
        exit_params = FuturesRecommendations.calculate_exit_parameters(
            action, entry_params, multiplier, position_size
        )
        
        # Build recommendation
        recommendation = {
            'type': 'FUTURES',
            'symbol': futures_info['symbol'],
            'action': action,
            'confidence': confidence,
            'current_price': current_price,
            'contract_multiplier': multiplier,
            'initial_margin': initial_margin,
            'position_size': position_size,
            'total_margin_required': initial_margin * position_size,
            'contract_value': current_price * multiplier * position_size,
            # Monte Carlo
            'probability_up': mc_analysis['probability_up'],
            'probability_down': mc_analysis['probability_down'],
            'expected_price': mc_analysis['expected_price'],
            'upside_potential': mc_analysis['upside_potential'],
            'downside_risk': mc_analysis['downside_risk'],
            # ML Predictions
            'ml_score': ml_analysis['ml_score'],
            'ml_insights': ' | '.join(ml_analysis['insights']),
            'svm_predicted_price': ml_analysis['predicted_price'],
            'svm_predicted_change': ml_analysis['predicted_change_pct'],
            # Entry/Exit
            'entry_price': entry_params['entry_price'],
            'stop_loss': entry_params['stop_loss'],
            'profit_target_1': entry_params['profit_target_1'],
            'profit_target_2': entry_params['profit_target_2'],
            'profit_target_3': entry_params['profit_target_3'],
            'atr_estimate': entry_params['atr_estimate'],
            # Risk/Reward
            'max_loss': exit_params['max_loss'],
            'profit_1': exit_params['profit_1'],
            'profit_2': exit_params['profit_2'],
            'profit_3': exit_params['profit_3'],
            'risk_reward_1': exit_params['risk_reward_1'],
            'risk_reward_2': exit_params['risk_reward_2'],
            'risk_reward_3': exit_params['risk_reward_3'],
            'risk_adjusted_return': risk_adjusted_return,
            'expected_return': expected_return
        }
        
        return recommendation

