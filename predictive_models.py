"""
Machine learning predictive models for price forecasting
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class PredictiveModels:
    """ML models for predicting future stock prices"""
    
    @staticmethod
    def prepare_features(historical_data, forecast_days=30):
        """
        Prepare features from historical data
        Creates technical indicators and lagged features
        """
        df = historical_data.copy()
        
        # Basic features
        df['Returns'] = df['Close'].pct_change()
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Moving averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        
        # Volatility
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        
        # Volume features
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA']
        
        # Price momentum
        df['Momentum'] = df['Close'] - df['Close'].shift(10)
        
        # RSI-like indicator
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Lagged prices
        for i in [1, 2, 3, 5, 10]:
            df[f'Close_Lag_{i}'] = df['Close'].shift(i)
        
        # Drop NaN values
        df = df.dropna()
        
        return df
    
    @staticmethod
    def train_decision_tree(historical_data, target_days=30):
        """
        Train Decision Tree model to predict future price
        """
        try:
            df = PredictiveModels.prepare_features(historical_data, target_days)
            
            if len(df) < 50:
                return None, None, "Insufficient data for training"
            
            # Create target: price N days in the future
            df['Target'] = df['Close'].shift(-target_days)
            df = df.dropna()
            
            # Feature columns
            feature_cols = [col for col in df.columns if col not in ['Target', 'Close']]
            
            X = df[feature_cols]
            y = df['Target']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            # Train model
            model = DecisionTreeRegressor(max_depth=10, min_samples_split=10, random_state=42)
            model.fit(X_train, y_train)
            
            # Score
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return model, {
                'train_score': train_score,
                'test_score': test_score,
                'feature_importance': feature_importance
            }, None
            
        except Exception as e:
            return None, None, str(e)
    
    @staticmethod
    def train_svm_rbf(historical_data, target_days=30):
        """
        Train SVM with RBF kernel to predict future price
        """
        try:
            df = PredictiveModels.prepare_features(historical_data, target_days)
            
            if len(df) < 50:
                return None, None, None, "Insufficient data for training"
            
            # Create target
            df['Target'] = df['Close'].shift(-target_days)
            df = df.dropna()
            
            # Feature columns
            feature_cols = [col for col in df.columns if col not in ['Target', 'Close']]
            
            X = df[feature_cols]
            y = df['Target']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            # Scale features (important for SVM)
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
            model.fit(X_train_scaled, y_train)
            
            # Score
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            return model, scaler, {
                'train_score': train_score,
                'test_score': test_score
            }, None
            
        except Exception as e:
            return None, None, None, str(e)
    
    @staticmethod
    def predict_price(model, scaler, current_data, feature_cols):
        """
        Make price prediction using trained model
        """
        try:
            # Prepare features
            df = PredictiveModels.prepare_features(current_data)
            
            if df.empty:
                return None
            
            # Get latest data point
            X = df[feature_cols].iloc[-1:].values
            
            # Scale if scaler provided (for SVM)
            if scaler is not None:
                X = scaler.transform(X)
            
            # Predict
            prediction = model.predict(X)[0]
            
            return prediction
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    @staticmethod
    def calculate_prediction_confidence(historical_data, model, scaler=None):
        """
        Calculate confidence metrics for predictions
        """
        try:
            df = PredictiveModels.prepare_features(historical_data)
            
            if len(df) < 20:
                return None
            
            # Use recent data for validation
            feature_cols = [col for col in df.columns if col not in ['Close']]
            X_recent = df[feature_cols].iloc[-20:].values
            y_actual = df['Close'].iloc[-20:].values
            
            if scaler is not None:
                X_recent = scaler.transform(X_recent)
            
            predictions = model.predict(X_recent)
            
            # Calculate metrics
            errors = np.abs(predictions - y_actual)
            mean_error = np.mean(errors)
            std_error = np.std(errors)
            mean_pct_error = np.mean(errors / y_actual) * 100
            
            return {
                'mean_absolute_error': mean_error,
                'std_error': std_error,
                'mean_percentage_error': mean_pct_error
            }
            
        except Exception as e:
            print(f"Confidence calculation error: {e}")
            return None

