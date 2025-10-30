"""
American Options & Futures Trading Application
Streamlit-based application for options analysis and AI-powered recommendations
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Import custom modules
from data_fetcher import DataFetcher
from options_pricing import OptionsPricing
from predictive_models import PredictiveModels
from ai_recommendations import AIRecommendations

# Page configuration
st.set_page_config(
    page_title="AI Options Strategy",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2ca02c;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-high {
        background-color: #d4edda;
        padding: 1rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .recommendation-medium {
        background-color: #fff3cd;
        padding: 1rem;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .recommendation-low {
        background-color: #f8d7da;
        padding: 1rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📈 AI Options & Futures Strategy Analyzer</div>', unsafe_allow_html=True)

# Sidebar - Inputs Section
st.sidebar.markdown("## 📊 Inputs Section")

# Ticker input
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL", help="Enter stock ticker symbol (e.g., AAPL, MSFT, TSLA)").upper()

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = None

# Load data button
if st.sidebar.button("Load Data") or st.session_state.current_ticker != ticker:
    with st.spinner(f"Loading data for {ticker}..."):
        try:
            data_fetcher = DataFetcher(ticker)
            st.session_state.data_fetcher = data_fetcher
            st.session_state.current_price = data_fetcher.get_current_price()
            st.session_state.historical_data = data_fetcher.get_historical_data()
            st.session_state.volatility = data_fetcher.calculate_historical_volatility()
            st.session_state.available_expirations = data_fetcher.get_available_expirations()
            st.session_state.data_loaded = True
            st.session_state.current_ticker = ticker
            st.sidebar.success(f"✅ Data loaded for {ticker}")
        except Exception as e:
            st.sidebar.error(f"Error loading data: {str(e)}")
            st.session_state.data_loaded = False

# Check if data is loaded
if st.session_state.data_loaded:
    # Display current price and volatility
    st.sidebar.markdown("### 💰 Current Market Data")
    st.sidebar.metric("Current Price", f"${st.session_state.current_price:.2f}")
    
    if st.session_state.volatility:
        st.sidebar.metric("Annual Volatility (252 days)", f"{st.session_state.volatility*100:.2f}%")
    else:
        st.sidebar.warning("Unable to calculate volatility")
    
    # Expiration date selection
    st.sidebar.markdown("### 📅 Expiration Date")
    if len(st.session_state.available_expirations) > 0:
        selected_expiration = st.sidebar.selectbox(
            "Select Expiration Date",
            st.session_state.available_expirations
        )
    else:
        st.sidebar.error("No expiration dates available")
        selected_expiration = None
    
    # Risk parameters
    st.sidebar.markdown("### ⚙️ Risk Parameters")
    
    risk_free_rate = st.sidebar.slider(
        "Risk-Free Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.1,
        help="Annual risk-free interest rate"
    ) / 100
    
    num_steps = st.sidebar.slider(
        "Binomial Tree Steps",
        min_value=10,
        max_value=200,
        value=100,
        step=10,
        help="Number of steps in binomial tree model"
    )
    
    # Portfolio parameters
    st.sidebar.markdown("### 💼 Portfolio Parameters")
    
    portfolio_value = st.sidebar.number_input(
        "Portfolio Amount ($)",
        min_value=1000.0,
        max_value=10000000.0,
        value=100000.0,
        step=1000.0,
        help="Total portfolio value"
    )
    
    risk_percentage = st.sidebar.slider(
        "Risk Per Trade (%)",
        min_value=0.5,
        max_value=20.0,
        value=2.0,
        step=0.5,
        help="Percentage of portfolio to risk per trade"
    )
    
    # Monte Carlo simulation parameters
    st.sidebar.markdown("### 🎲 Simulation Parameters")
    
    num_simulations = st.sidebar.number_input(
        "Monte Carlo Trials",
        min_value=1000,
        max_value=100000,
        value=10000,
        step=1000,
        help="Number of Monte Carlo simulation paths"
    )
    
    # Main content area
    if selected_expiration:
        
        # Load options data
        with st.spinner("Loading options chain..."):
            options_data = st.session_state.data_fetcher.get_options_chain(selected_expiration)
        
        if options_data:
            calls_df = options_data['calls']
            puts_df = options_data['puts']
            
            # Calculate time to expiration
            T = OptionsPricing.years_to_expiration(selected_expiration)
            days_to_exp = OptionsPricing.days_to_expiration(selected_expiration)
            
            st.info(f"📅 Days to Expiration: {days_to_exp} | ⏰ Years: {T:.4f}")
            
            # =================================================================
            # GREEKS SECTION
            # =================================================================
            st.markdown('<div class="section-header">📐 Option Greeks Analysis</div>', unsafe_allow_html=True)
            
            st.markdown("""
            **The Greeks** measure the sensitivity of options prices to various factors:
            - **Delta (Δ)**: Rate of change in option price relative to stock price change
            - **Gamma (Γ)**: Rate of change in Delta relative to stock price change  
            - **Theta (Θ)**: Rate of time decay (daily)
            - **Vega (ν)**: Sensitivity to volatility changes (per 1% change)
            - **Rho (ρ)**: Sensitivity to interest rate changes (per 1% change)
            """)
            
            # Calculate Greeks for ATM and nearby strikes
            current_price = st.session_state.current_price
            if st.session_state.volatility:
                sigma = st.session_state.volatility
            else:
                sigma = 0.3  # Default 30%
            
            # Select strikes within 10% of current price (ATM region)
            strike_range = current_price * 0.10
            atm_strikes = calls_df[
                (calls_df['strike'] >= current_price - strike_range) &
                (calls_df['strike'] <= current_price + strike_range)
            ]['strike'].values
            
            if len(atm_strikes) > 0:
                # Limit to 5 strikes for cleaner display
                if len(atm_strikes) > 5:
                    # Get closest 5 strikes to ATM
                    distances = np.abs(atm_strikes - current_price)
                    closest_indices = np.argsort(distances)[:5]
                    atm_strikes = atm_strikes[closest_indices]
                    atm_strikes = np.sort(atm_strikes)
                
                greeks_data = []
                
                for strike in atm_strikes:
                    # Calculate Greeks for calls
                    call_greeks = OptionsPricing.calculate_greeks(
                        current_price, strike, T, risk_free_rate, sigma, 'call'
                    )
                    
                    # Calculate Greeks for puts
                    put_greeks = OptionsPricing.calculate_greeks(
                        current_price, strike, T, risk_free_rate, sigma, 'put'
                    )
                    
                    # Get market prices
                    call_price = calls_df[calls_df['strike'] == strike]['lastPrice'].values[0] if len(calls_df[calls_df['strike'] == strike]) > 0 else 0
                    put_price = puts_df[puts_df['strike'] == strike]['lastPrice'].values[0] if len(puts_df[puts_df['strike'] == strike]) > 0 else 0
                    
                    greeks_data.append({
                        'Strike': strike,
                        'Type': 'CALL',
                        'Price': call_price,
                        'Delta': call_greeks['delta'],
                        'Gamma': call_greeks['gamma'],
                        'Theta': call_greeks['theta'],
                        'Vega': call_greeks['vega'],
                        'Rho': call_greeks['rho']
                    })
                    
                    greeks_data.append({
                        'Strike': strike,
                        'Type': 'PUT',
                        'Price': put_price,
                        'Delta': put_greeks['delta'],
                        'Gamma': put_greeks['gamma'],
                        'Theta': put_greeks['theta'],
                        'Vega': put_greeks['vega'],
                        'Rho': put_greeks['rho']
                    })
                
                greeks_df = pd.DataFrame(greeks_data)
                
                # Display Greeks table
                st.markdown("### 📊 Greeks by Strike Price")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📞 Call Options Greeks")
                    calls_greeks = greeks_df[greeks_df['Type'] == 'CALL'][['Strike', 'Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho']]
                    st.dataframe(
                        calls_greeks.style.format({
                            'Strike': '${:.2f}',
                            'Price': '${:.2f}',
                            'Delta': '{:.4f}',
                            'Gamma': '{:.4f}',
                            'Theta': '{:.4f}',
                            'Vega': '{:.4f}',
                            'Rho': '{:.4f}'
                        }).background_gradient(subset=['Delta'], cmap='RdYlGn', vmin=-1, vmax=1),
                        use_container_width=True
                    )
                
                with col2:
                    st.markdown("#### 📉 Put Options Greeks")
                    puts_greeks = greeks_df[greeks_df['Type'] == 'PUT'][['Strike', 'Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho']]
                    st.dataframe(
                        puts_greeks.style.format({
                            'Strike': '${:.2f}',
                            'Price': '${:.2f}',
                            'Delta': '{:.4f}',
                            'Gamma': '{:.4f}',
                            'Theta': '{:.4f}',
                            'Vega': '{:.4f}',
                            'Rho': '{:.4f}'
                        }).background_gradient(subset=['Delta'], cmap='RdYlGn_r', vmin=-1, vmax=1),
                        use_container_width=True
                    )
                
                # Greeks Visualization
                st.markdown("### 📈 Greeks Visualization")
                
                tab1, tab2, tab3 = st.tabs(["Delta & Gamma", "Theta & Vega", "Rho"])
                
                with tab1:
                    fig1 = go.Figure()
                    
                    # Delta for calls
                    calls_greeks_df = greeks_df[greeks_df['Type'] == 'CALL']
                    fig1.add_trace(go.Scatter(
                        x=calls_greeks_df['Strike'],
                        y=calls_greeks_df['Delta'],
                        name='Call Delta',
                        mode='lines+markers',
                        line=dict(color='green', width=2),
                        marker=dict(size=8)
                    ))
                    
                    # Delta for puts
                    puts_greeks_df = greeks_df[greeks_df['Type'] == 'PUT']
                    fig1.add_trace(go.Scatter(
                        x=puts_greeks_df['Strike'],
                        y=puts_greeks_df['Delta'],
                        name='Put Delta',
                        mode='lines+markers',
                        line=dict(color='red', width=2),
                        marker=dict(size=8)
                    ))
                    
                    # Gamma for both (overlaid)
                    fig1.add_trace(go.Scatter(
                        x=calls_greeks_df['Strike'],
                        y=calls_greeks_df['Gamma'],
                        name='Gamma',
                        mode='lines+markers',
                        line=dict(color='blue', width=2, dash='dash'),
                        marker=dict(size=6),
                        yaxis='y2'
                    ))
                    
                    # Add current price line
                    fig1.add_vline(x=current_price, line_dash="dash", line_color="gray",
                                  annotation_text=f"Current: ${current_price:.2f}")
                    
                    fig1.update_layout(
                        title='Delta and Gamma by Strike',
                        xaxis_title='Strike Price',
                        yaxis_title='Delta',
                        yaxis2=dict(title='Gamma', overlaying='y', side='right'),
                        hovermode='x unified',
                        height=400
                    )
                    
                    st.plotly_chart(fig1, use_container_width=True)
                
                with tab2:
                    fig2 = go.Figure()
                    
                    # Theta
                    fig2.add_trace(go.Scatter(
                        x=calls_greeks_df['Strike'],
                        y=calls_greeks_df['Theta'],
                        name='Call Theta',
                        mode='lines+markers',
                        line=dict(color='purple', width=2)
                    ))
                    
                    fig2.add_trace(go.Scatter(
                        x=puts_greeks_df['Strike'],
                        y=puts_greeks_df['Theta'],
                        name='Put Theta',
                        mode='lines+markers',
                        line=dict(color='orange', width=2)
                    ))
                    
                    # Vega (same for calls and puts)
                    fig2.add_trace(go.Scatter(
                        x=calls_greeks_df['Strike'],
                        y=calls_greeks_df['Vega'],
                        name='Vega',
                        mode='lines+markers',
                        line=dict(color='cyan', width=2, dash='dash'),
                        yaxis='y2'
                    ))
                    
                    fig2.add_vline(x=current_price, line_dash="dash", line_color="gray",
                                  annotation_text=f"Current: ${current_price:.2f}")
                    
                    fig2.update_layout(
                        title='Theta and Vega by Strike',
                        xaxis_title='Strike Price',
                        yaxis_title='Theta (Daily Decay)',
                        yaxis2=dict(title='Vega', overlaying='y', side='right'),
                        hovermode='x unified',
                        height=400
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                
                with tab3:
                    fig3 = go.Figure()
                    
                    fig3.add_trace(go.Scatter(
                        x=calls_greeks_df['Strike'],
                        y=calls_greeks_df['Rho'],
                        name='Call Rho',
                        mode='lines+markers',
                        line=dict(color='teal', width=2)
                    ))
                    
                    fig3.add_trace(go.Scatter(
                        x=puts_greeks_df['Strike'],
                        y=puts_greeks_df['Rho'],
                        name='Put Rho',
                        mode='lines+markers',
                        line=dict(color='brown', width=2)
                    ))
                    
                    fig3.add_vline(x=current_price, line_dash="dash", line_color="gray",
                                  annotation_text=f"Current: ${current_price:.2f}")
                    
                    fig3.update_layout(
                        title='Rho by Strike (Interest Rate Sensitivity)',
                        xaxis_title='Strike Price',
                        yaxis_title='Rho',
                        hovermode='x unified',
                        height=400
                    )
                    
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Greeks Summary
                st.markdown("### 📋 Key Greeks Insights")
                
                insight_col1, insight_col2, insight_col3 = st.columns(3)
                
                # Find ATM option (closest to current price)
                atm_call = calls_greeks_df.iloc[(calls_greeks_df['Strike'] - current_price).abs().argsort()[:1]]
                atm_put = puts_greeks_df.iloc[(puts_greeks_df['Strike'] - current_price).abs().argsort()[:1]]
                
                with insight_col1:
                    st.metric("ATM Call Delta", f"{atm_call['Delta'].values[0]:.3f}")
                    st.caption("~0.5 means 50% chance of expiring ITM")
                    st.metric("ATM Put Delta", f"{atm_put['Delta'].values[0]:.3f}")
                    st.caption("Negative for puts")
                
                with insight_col2:
                    st.metric("ATM Gamma", f"{atm_call['Gamma'].values[0]:.4f}")
                    st.caption("Higher = Delta changes faster")
                    st.metric("ATM Theta (Daily)", f"${atm_call['Theta'].values[0]:.2f}")
                    st.caption("Daily time decay")
                
                with insight_col3:
                    st.metric("ATM Vega", f"{atm_call['Vega'].values[0]:.2f}")
                    st.caption("Gain per 1% volatility increase")
                    st.metric("ATM Rho", f"{atm_call['Rho'].values[0]:.2f}")
                    st.caption("Gain per 1% rate increase")
            
            else:
                st.warning("No ATM options found for Greeks calculation.")
            
            # =================================================================
            # DISPLAY SECTION
            # =================================================================
            st.markdown('<div class="section-header">📊 Display Section</div>', unsafe_allow_html=True)
            
            # Options Chain Display
            st.markdown("### 🔗 Live Options Chain")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📞 Call Options")
                calls_display = calls_df[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']].copy()
                calls_display.columns = ['Strike', 'Last', 'Bid', 'Ask', 'Volume', 'OI', 'IV']
                st.dataframe(calls_display, use_container_width=True, height=400)
            
            with col2:
                st.markdown("#### 📉 Put Options")
                puts_display = puts_df[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']].copy()
                puts_display.columns = ['Strike', 'Last', 'Bid', 'Ask', 'Volume', 'OI', 'IV']
                st.dataframe(puts_display, use_container_width=True, height=400)
            
            # Fair Value Calculations
            st.markdown("### 💎 Fair Value Analysis")
            
            with st.spinner("Calculating fair values..."):
                # Select strikes around current price
                current_price = st.session_state.current_price
                strike_range = current_price * 0.2  # +/- 20% of current price
                
                relevant_strikes = calls_df[
                    (calls_df['strike'] >= current_price - strike_range) &
                    (calls_df['strike'] <= current_price + strike_range)
                ]['strike'].values
                
                if st.session_state.volatility:
                    sigma = st.session_state.volatility
                else:
                    sigma = 0.3  # Default 30% if calculation failed
                
                fair_values = {}
                fair_value_comparison = []
                
                for strike in relevant_strikes:
                    # Calculate fair values using both methods
                    bs_call = OptionsPricing.black_scholes(
                        current_price, strike, T, risk_free_rate, sigma, 'call'
                    )
                    bs_put = OptionsPricing.black_scholes(
                        current_price, strike, T, risk_free_rate, sigma, 'put'
                    )
                    
                    binomial_call = OptionsPricing.binomial_tree_american(
                        current_price, strike, T, risk_free_rate, sigma, num_steps, 'call'
                    )
                    binomial_put = OptionsPricing.binomial_tree_american(
                        current_price, strike, T, risk_free_rate, sigma, num_steps, 'put'
                    )
                    
                    # Store fair values (using binomial for American options)
                    fair_values[f'call_{strike}'] = binomial_call
                    fair_values[f'put_{strike}'] = binomial_put
                    
                    # Get market prices
                    call_market = calls_df[calls_df['strike'] == strike]['lastPrice'].values
                    put_market = puts_df[puts_df['strike'] == strike]['lastPrice'].values
                    
                    if len(call_market) > 0 and len(put_market) > 0:
                        call_market_price = call_market[0]
                        put_market_price = put_market[0]
                        
                        fair_value_comparison.append({
                            'Strike': strike,
                            'Call_Market': call_market_price,
                            'Call_Fair_BS': bs_call,
                            'Call_Fair_Binomial': binomial_call,
                            'Call_Diff_%': ((call_market_price - binomial_call) / binomial_call * 100) if binomial_call > 0 else 0,
                            'Put_Market': put_market_price,
                            'Put_Fair_BS': bs_put,
                            'Put_Fair_Binomial': binomial_put,
                            'Put_Diff_%': ((put_market_price - binomial_put) / binomial_put * 100) if binomial_put > 0 else 0
                        })
            
            fair_value_df = pd.DataFrame(fair_value_comparison)
            
            if not fair_value_df.empty:
                st.dataframe(fair_value_df.style.format({
                    'Strike': '${:.2f}',
                    'Call_Market': '${:.2f}',
                    'Call_Fair_BS': '${:.2f}',
                    'Call_Fair_Binomial': '${:.2f}',
                    'Call_Diff_%': '{:.2f}%',
                    'Put_Market': '${:.2f}',
                    'Put_Fair_BS': '${:.2f}',
                    'Put_Fair_Binomial': '${:.2f}',
                    'Put_Diff_%': '{:.2f}%'
                }).background_gradient(subset=['Call_Diff_%', 'Put_Diff_%'], cmap='RdYlGn_r'),
                    use_container_width=True)
                
                # Visualization of fair value vs market
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=fair_value_df['Strike'],
                    y=fair_value_df['Call_Market'],
                    name='Call Market Price',
                    mode='lines+markers',
                    line=dict(color='blue')
                ))
                fig.add_trace(go.Scatter(
                    x=fair_value_df['Strike'],
                    y=fair_value_df['Call_Fair_Binomial'],
                    name='Call Fair Value',
                    mode='lines+markers',
                    line=dict(color='lightblue', dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=fair_value_df['Strike'],
                    y=fair_value_df['Put_Market'],
                    name='Put Market Price',
                    mode='lines+markers',
                    line=dict(color='red')
                ))
                fig.add_trace(go.Scatter(
                    x=fair_value_df['Strike'],
                    y=fair_value_df['Put_Fair_Binomial'],
                    name='Put Fair Value',
                    mode='lines+markers',
                    line=dict(color='lightcoral', dash='dash')
                ))
                
                fig.update_layout(
                    title='Market Price vs Fair Value',
                    xaxis_title='Strike Price',
                    yaxis_title='Option Price',
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Monte Carlo Simulation
            st.markdown("### 🎲 Monte Carlo Price Simulation")
            
            with st.spinner(f"Running {num_simulations:,} Monte Carlo simulations..."):
                mc_prices = OptionsPricing.monte_carlo_simulation(
                    current_price, T, risk_free_rate, sigma, int(num_simulations)
                )
                
                # Store in session state
                st.session_state.mc_prices = mc_prices
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Mean Simulated Price", f"${np.mean(mc_prices):.2f}")
                st.metric("Median Simulated Price", f"${np.median(mc_prices):.2f}")
            
            with col2:
                st.metric("Std Deviation", f"${np.std(mc_prices):.2f}")
                st.metric("10th Percentile", f"${np.percentile(mc_prices, 10):.2f}")
            
            with col3:
                st.metric("90th Percentile", f"${np.percentile(mc_prices, 90):.2f}")
                st.metric("Probability > Current", f"{np.mean(mc_prices > current_price)*100:.1f}%")
            
            # Distribution plot
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=mc_prices,
                nbinsx=50,
                name='Simulated Prices',
                marker_color='lightblue'
            ))
            fig_hist.add_vline(x=current_price, line_dash="dash", line_color="red",
                              annotation_text=f"Current: ${current_price:.2f}")
            fig_hist.add_vline(x=np.mean(mc_prices), line_dash="dash", line_color="green",
                              annotation_text=f"Mean: ${np.mean(mc_prices):.2f}")
            
            fig_hist.update_layout(
                title=f'Distribution of Simulated Prices at Expiration ({num_simulations:,} trials)',
                xaxis_title='Stock Price',
                yaxis_title='Frequency',
                height=400
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Machine Learning Predictions
            st.markdown("### 🤖 Machine Learning Price Predictions")
            
            with st.spinner("Training predictive models..."):
                # Calculate target days
                target_days = days_to_exp
                
                # Decision Tree
                dt_model, dt_stats, dt_error = PredictiveModels.train_decision_tree(
                    st.session_state.historical_data, target_days
                )
                
                # SVM
                svm_model, svm_scaler, svm_stats, svm_error = PredictiveModels.train_svm_rbf(
                    st.session_state.historical_data, target_days
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🌲 Decision Tree Model")
                if dt_model and dt_stats:
                    # Make prediction
                    df_features = PredictiveModels.prepare_features(st.session_state.historical_data)
                    if not df_features.empty:
                        feature_cols = [col for col in df_features.columns if col != 'Close']
                        X_latest = df_features[feature_cols].iloc[-1:].values
                        dt_prediction = dt_model.predict(X_latest)[0]
                        
                        st.metric("Predicted Price", f"${dt_prediction:.2f}")
                        st.metric("vs Current", f"{((dt_prediction/current_price - 1) * 100):.2f}%")
                        st.metric("Train R²", f"{dt_stats['train_score']:.4f}")
                        st.metric("Test R²", f"{dt_stats['test_score']:.4f}")
                        
                        # Feature importance
                        with st.expander("Feature Importance"):
                            top_features = dt_stats['feature_importance'].head(10)
                            fig_feat = px.bar(
                                top_features,
                                x='importance',
                                y='feature',
                                orientation='h',
                                title='Top 10 Features'
                            )
                            st.plotly_chart(fig_feat, use_container_width=True)
                    else:
                        st.warning("Unable to make prediction")
                else:
                    st.error(f"Model training failed: {dt_error}")
            
            with col2:
                st.markdown("#### 🎯 SVM (RBF Kernel) Model")
                if svm_model and svm_stats:
                    # Make prediction
                    df_features = PredictiveModels.prepare_features(st.session_state.historical_data)
                    if not df_features.empty:
                        feature_cols = [col for col in df_features.columns if col != 'Close']
                        X_latest = df_features[feature_cols].iloc[-1:].values
                        X_latest_scaled = svm_scaler.transform(X_latest)
                        svm_prediction = svm_model.predict(X_latest_scaled)[0]
                        
                        st.metric("Predicted Price", f"${svm_prediction:.2f}")
                        st.metric("vs Current", f"{((svm_prediction/current_price - 1) * 100):.2f}%")
                        st.metric("Train R²", f"{svm_stats['train_score']:.4f}")
                        st.metric("Test R²", f"{svm_stats['test_score']:.4f}")
                    else:
                        st.warning("Unable to make prediction")
                else:
                    st.error(f"Model training failed: {svm_error}")
            
            # =================================================================
            # AI RECOMMENDATION SECTION
            # =================================================================
            st.markdown('<div class="section-header">🤖 AI Recommendation Section</div>', unsafe_allow_html=True)
            
            with st.spinner("Generating AI-powered trading recommendations..."):
                # ML predictions dict
                ml_predictions = {}
                if dt_model and dt_stats:
                    ml_predictions['decision_tree'] = dt_prediction
                if svm_model and svm_stats:
                    ml_predictions['svm'] = svm_prediction
                
                # Generate recommendations
                recommendations_df = AIRecommendations.generate_strategy_recommendation(
                    current_price=current_price,
                    strike_prices=relevant_strikes,
                    options_data={'calls': calls_df, 'puts': puts_df},
                    fair_values=fair_values,
                    monte_carlo_results=mc_prices,
                    ml_predictions=ml_predictions,
                    portfolio_value=portfolio_value,
                    risk_percentage=risk_percentage,
                    expiration_date=selected_expiration,
                    risk_free_rate=risk_free_rate,
                    volatility=sigma
                )
                
                # Get top recommendations
                top_recs = AIRecommendations.get_top_recommendations(recommendations_df, top_n=5)
            
            if not top_recs.empty:
                st.markdown("### 🏆 Top Trading Recommendations")
                
                st.info(f"""
                **AI Analysis Summary:**
                - Portfolio Value: ${portfolio_value:,.2f}
                - Risk per Trade: {risk_percentage}% (${portfolio_value * risk_percentage / 100:,.2f})
                - Based on {num_simulations:,} Monte Carlo simulations
                - Incorporating ML predictions and fair value analysis
                - **Greeks-Enhanced Analysis**: Delta, Gamma, Theta, Vega, Rho
                - Considering liquidity, time decay, and risk-adjusted returns
                """)
                
                for idx, row in top_recs.iterrows():
                    confidence_class = f"recommendation-{row['confidence'].lower()}"
                    
                    st.markdown(f"""
                    <div class="{confidence_class}">
                        <h4>{row['action']} - {row['type']} @ ${row['strike']:.2f}</h4>
                        <p><strong>Confidence:</strong> {row['confidence']} | <strong>Valuation:</strong> {row['valuation'].upper()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Market Price", f"${row['market_price']:.2f}")
                        st.metric("Fair Value", f"${row['fair_value']:.2f}")
                    
                    with col2:
                        st.metric("Value Diff", f"{row['value_diff_pct']:.2f}%")
                        st.metric("Probability ITM", f"{row['probability_itm']*100:.1f}%")
                    
                    with col3:
                        st.metric("Expected Payoff", f"${row['expected_payoff']:.2f}")
                        st.metric("Risk-Adj Return", f"{row['risk_adjusted_return']:.4f}")
                    
                    with col4:
                        st.metric("Position Size", f"{row['position_size']} contracts")
                        st.metric("Total Cost", f"${row['total_cost']:.2f}")
                    
                    # Greeks Summary (compact display)
                    greeks_col1, greeks_col2, greeks_col3, greeks_col4 = st.columns(4)
                    with greeks_col1:
                        st.metric("Delta", f"{row['delta']:.3f}", help="Price sensitivity")
                    with greeks_col2:
                        st.metric("Gamma", f"{row['gamma']:.4f}", help="Delta change rate")
                    with greeks_col3:
                        st.metric("Theta", f"${row['theta']:.2f}", help="Daily time decay")
                    with greeks_col4:
                        st.metric("Vega", f"{row['vega']:.2f}", help="Volatility sensitivity")
                    
                    # Greeks Score
                    st.progress(row['greeks_score'] / 100, text=f"Greeks Score: {row['greeks_score']:.0f}/100")
                    
                    with st.expander("📋 Trading Plan & Execution Details"):
                        # Entry Parameters
                        st.markdown("#### 🎯 ENTRY PARAMETERS")
                        entry_col1, entry_col2, entry_col3 = st.columns(3)
                        
                        with entry_col1:
                            st.metric("Recommended Entry", f"${row['entry_price']:.2f}")
                            st.metric("Max Entry Price", f"${row['max_entry_price']:.2f}")
                        
                        with entry_col2:
                            st.metric("Order Type", row['order_type'])
                            st.metric("Timing", row['timing'])
                        
                        with entry_col3:
                            st.metric("Breakeven Price", f"${row['breakeven']:.2f}")
                            st.metric("Bid-Ask Spread", f"{row['spread_pct']:.2f}%")
                        
                        st.write(f"**Bid:** ${row['bid']:.2f} | **Ask:** ${row['ask']:.2f}")
                        st.write(f"**Volume:** {row['volume']:,.0f} | **Open Interest:** {row['open_interest']:,.0f}")
                        
                        st.markdown("---")
                        
                        # Exit Parameters
                        st.markdown("#### 🎯 EXIT PARAMETERS (Sell/Close)")
                        exit_col1, exit_col2, exit_col3 = st.columns(3)
                        
                        with exit_col1:
                            st.metric("Profit Target 1 (50%)", f"${row['profit_target_1']:.2f}")
                            st.metric("Potential Profit", f"${row['profit_1_amount']:.2f}")
                        
                        with exit_col2:
                            st.metric("Profit Target 2 (100%)", f"${row['profit_target_2']:.2f}")
                            st.metric("Potential Profit", f"${row['profit_2_amount']:.2f}")
                        
                        with exit_col3:
                            st.metric("Stop Loss Price", f"${row['stop_loss']:.2f}")
                            st.metric("Max Loss", f"${row['max_loss_amount']:.2f}")
                        
                        st.markdown("---")
                        
                        # Risk/Reward Analysis
                        st.markdown("#### ⚖️ RISK/REWARD ANALYSIS")
                        rr_col1, rr_col2, rr_col3 = st.columns(3)
                        
                        with rr_col1:
                            st.metric("Risk/Reward Ratio 1", f"{row['risk_reward_ratio_1']:.2f}:1")
                        
                        with rr_col2:
                            st.metric("Risk/Reward Ratio 2", f"{row['risk_reward_ratio_2']:.2f}:1")
                        
                        with rr_col3:
                            st.metric("% of Portfolio at Risk", f"{(row['max_loss_amount']/portfolio_value)*100:.2f}%")
                        
                        st.info(f"**Exit Strategy:** {row['exit_strategy']}")
                        
                        st.markdown("---")
                        
                        # Greeks Insights
                        st.markdown("#### 📐 GREEKS INSIGHTS")
                        st.write(f"**Greeks Score:** {row['greeks_score']:.0f}/100")
                        
                        # Display insights as bullet points
                        if row['greeks_insights']:
                            insights_list = row['greeks_insights'].split(' | ')
                            for insight in insights_list:
                                if '✅' in insight or 'Good' in insight or 'Strong' in insight:
                                    st.success(f"✓ {insight}")
                                elif '⚠️' in insight or 'High risk' in insight or 'Low' in insight:
                                    st.warning(f"⚠ {insight}")
                                else:
                                    st.info(f"ℹ {insight}")
                        
                        st.caption("**Greeks Analysis:** The AI has analyzed Delta, Gamma, Theta, Vega, and Rho to assess this trade's sensitivity to price, time, and volatility changes.")
                    
                    st.markdown("---")
                
                # Full recommendations table
                with st.expander("📋 View All Recommendations"):
                    display_recs = recommendations_df[[
                        'type', 'strike', 'action', 'confidence', 'market_price', 'fair_value',
                        'probability_itm', 'risk_adjusted_return', 'position_size', 'total_cost'
                    ]].copy()
                    
                    display_recs.columns = [
                        'Type', 'Strike', 'Action', 'Confidence', 'Market', 'Fair Value',
                        'P(ITM)', 'Risk-Adj Return', 'Contracts', 'Total Cost'
                    ]
                    
                    st.dataframe(
                        display_recs.style.format({
                            'Strike': '${:.2f}',
                            'Market': '${:.2f}',
                            'Fair Value': '${:.2f}',
                            'P(ITM)': '{:.2%}',
                            'Risk-Adj Return': '{:.4f}',
                            'Total Cost': '${:.2f}'
                        }).background_gradient(subset=['Risk-Adj Return'], cmap='RdYlGn'),
                        use_container_width=True,
                        height=400
                    )
            else:
                st.warning("No high-confidence recommendations available for the current parameters.")
                
                # Show all recommendations anyway
                if not recommendations_df.empty:
                    st.markdown("### 📊 All Analyzed Options")
                    display_all = recommendations_df[[
                        'type', 'strike', 'action', 'confidence', 'market_price', 'fair_value',
                        'probability_itm', 'risk_adjusted_return'
                    ]].copy()
                    
                    display_all.columns = [
                        'Type', 'Strike', 'Action', 'Confidence', 'Market', 'Fair Value',
                        'P(ITM)', 'Risk-Adj Return'
                    ]
                    
                    st.dataframe(display_all, use_container_width=True)
            
            # Risk Analysis Summary
            st.markdown("### ⚠️ Risk Analysis Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Market Volatility", f"{sigma*100:.2f}%")
                st.metric("Days to Expiration", f"{days_to_exp}")
            
            with col2:
                prob_up = np.mean(mc_prices > current_price) * 100
                prob_down = 100 - prob_up
                st.metric("Probability Price Up", f"{prob_up:.1f}%")
                st.metric("Probability Price Down", f"{prob_down:.1f}%")
            
            with col3:
                if not top_recs.empty:
                    total_risk = top_recs['total_cost'].sum()
                    st.metric("Total Recommended Capital", f"${total_risk:.2f}")
                    st.metric("% of Portfolio", f"{(total_risk/portfolio_value)*100:.2f}%")
                else:
                    st.metric("Total Recommended Capital", "$0.00")
                    st.metric("% of Portfolio", "0.00%")
            
        else:
            st.error("Unable to load options data for selected expiration date.")
    
    else:
        st.warning("⚠️ Please select an expiration date from the sidebar.")

else:
    st.info("👈 Please enter a ticker symbol and click 'Load Data' to begin analysis.")
    
    # Quick start guide
    st.markdown("""
    ## 📚 Quick Start Guide
    
    ### How to Use This Application:
    
    1. **Enter Ticker Symbol** - Input any stock ticker (e.g., AAPL, MSFT, TSLA)
    2. **Load Data** - Click the "Load Data" button to fetch market data
    3. **Select Expiration** - Choose an options expiration date
    4. **Adjust Parameters** - Fine-tune risk parameters and portfolio settings
    5. **Review Analysis** - Examine the comprehensive analysis including:
       - Live options prices
       - Fair value calculations
       - Monte Carlo simulations
       - ML price predictions
       - AI-powered trading recommendations
    
    ### Features:
    
    - **📊 Live Data:** Real-time stock and options prices
    - **💎 Fair Value:** Black-Scholes and Binomial Tree pricing
    - **🎲 Monte Carlo:** Thousands of simulated price paths
    - **🤖 Machine Learning:** Decision Tree and SVM predictions
    - **🎯 AI Recommendations:** Smart trading strategies based on all data
    - **⚠️ Risk Management:** Position sizing and portfolio constraints
    
    ### Risk Disclaimer:
    
    ⚠️ **This application is for educational and informational purposes only.**
    It does not constitute financial advice. Trading options involves substantial
    risk and is not suitable for all investors. Past performance does not guarantee
    future results. Always do your own research and consult with a financial advisor.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>American Options & Futures Strategy Analyzer | Built with Streamlit</p>
    <p>⚠️ For educational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)

