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
from futures_recommendations import FuturesRecommendations

# Page configuration
st.set_page_config(
    page_title="AI Options Strategy",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for legal acceptance
if 'legal_accepted' not in st.session_state:
    st.session_state.legal_accepted = False

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
    .legal-disclaimer {
        background-color: #fff3cd;
        border: 3px solid #ff6b6b;
        border-radius: 10px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .legal-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .legal-section {
        font-size: 1.1rem;
        line-height: 1.8;
        margin: 1rem 0;
    }
    .legal-highlight {
        background-color: #ffebee;
        padding: 1rem;
        border-left: 4px solid #d32f2f;
        margin: 1rem 0;
        font-weight: bold;
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

# ============================================================================
# LEGAL DISCLAIMER - MUST BE ACCEPTED TO USE APPLICATION
# ============================================================================
if not st.session_state.legal_accepted:
    st.markdown('<div class="legal-disclaimer">', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-title">⚖️ LEGAL DISCLAIMER & TERMS OF USE</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-highlight">', unsafe_allow_html=True)
    st.markdown("""
    **🚨 IMPORTANT: YOU MUST READ AND ACCEPT THESE TERMS BEFORE USING THIS APPLICATION 🚨**
    
    By clicking "I Accept" below, you acknowledge that you have read, understood, and agree to be bound by all terms and conditions set forth in this disclaimer.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    
    # Educational Purpose Only
    st.markdown("### 1. 📚 EDUCATIONAL PURPOSES ONLY")
    st.markdown("""
    This application is provided **strictly for educational and informational purposes only**. It is designed to:
    - Demonstrate financial modeling concepts
    - Illustrate options and futures pricing theories
    - Showcase machine learning applications in finance
    - Provide learning opportunities for understanding financial markets
    
    **This is NOT a financial advisory service, investment recommendation platform, or trading tool for actual investment decisions.**
    """)
    
    # Not Financial Advice
    st.markdown("### 2. 🚫 NOT FINANCIAL ADVICE")
    st.markdown("""
    **NOTHING in this application constitutes financial, investment, tax, or legal advice.**
    
    The information, analysis, recommendations, and predictions provided:
    - Are for educational demonstration purposes only
    - Should NOT be construed as professional investment advice
    - Should NOT be relied upon for making actual trading decisions
    - Do NOT take into account your specific financial situation, goals, or risk tolerance
    
    **Always consult with a licensed financial advisor, investment professional, or tax advisor before making any investment decisions.**
    """)
    
    # No Guarantee of Accuracy
    st.markdown("### 3. ⚠️ NO GUARANTEE OF ACCURACY")
    st.markdown("""
    While we strive to provide accurate information, we make **NO WARRANTIES OR GUARANTEES** regarding:
    - The accuracy, completeness, or timeliness of data displayed
    - The correctness of pricing models, calculations, or predictions
    - The reliability of third-party data sources (including market data APIs)
    - The performance of machine learning models or AI recommendations
    
    **Data may be delayed, inaccurate, or incomplete. Models may contain errors or produce incorrect results.**
    
    All calculations are theoretical approximations based on mathematical models that may NOT reflect actual market conditions.
    """)
    
    # Risk of Loss
    st.markdown("### 4. 💸 SUBSTANTIAL RISK OF LOSS")
    st.markdown("""
    **TRADING OPTIONS, FUTURES, AND OTHER FINANCIAL INSTRUMENTS INVOLVES SUBSTANTIAL RISK OF LOSS.**
    
    You acknowledge and agree that:
    - You can lose MORE than your initial investment in futures and options trading
    - Options can expire worthless, resulting in 100% loss of premium paid
    - Futures trading involves leverage and unlimited loss potential
    - Past performance is NOT indicative of future results
    - Simulated or hypothetical performance results have inherent limitations
    
    **Only trade with capital you can afford to lose completely.**
    """)
    
    # No Liability
    st.markdown("### 5. 🛡️ LIMITATION OF LIABILITY")
    st.markdown("""
    **TO THE MAXIMUM EXTENT PERMITTED BY LAW:**
    
    The creator, developer, and operator of this application ("Provider") shall **NOT be liable** for:
    - Any trading losses, investment losses, or financial damages of any kind
    - Any decisions made based on information, analysis, or recommendations from this application
    - Any errors, omissions, interruptions, delays, or inaccuracies in data or functionality
    - Any technical failures, bugs, or malfunctions of the application
    - Any damages arising from use or inability to use this application
    
    **You use this application entirely at your own risk.**
    
    The Provider makes no representations or warranties of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.
    """)
    
    # User Responsibility
    st.markdown("### 6. 👤 USER RESPONSIBILITIES")
    st.markdown("""
    By using this application, you agree that:
    - You are solely responsible for all investment and trading decisions you make
    - You will conduct your own independent research and due diligence
    - You will seek professional advice before making any financial decisions
    - You understand the risks involved in options and futures trading
    - You will comply with all applicable laws and regulations in your jurisdiction
    - You are of legal age and have the legal capacity to use this application
    """)
    
    # Compliance and Regulations
    st.markdown("### 7. 📜 SECURITIES LAW AND REGULATORY COMPLIANCE")
    st.markdown("""
    This application is **NOT**:
    - A registered investment advisor (RIA)
    - A registered broker-dealer
    - A member of FINRA, SEC, CFTC, or any regulatory organization
    - Authorized to provide investment advice or execute trades
    
    This application does **NOT**:
    - Offer personalized investment recommendations
    - Execute trades on your behalf
    - Manage investment accounts
    - Provide fiduciary services
    
    **Users are responsible for ensuring their use complies with all applicable securities laws and regulations in their jurisdiction.**
    """)
    
    # Hypothetical Performance
    st.markdown("### 8. 📊 HYPOTHETICAL AND SIMULATED RESULTS")
    st.markdown("""
    Any performance results shown, including Monte Carlo simulations, machine learning predictions, and AI recommendations are:
    - **Hypothetical** and based on mathematical models
    - **NOT actual trading results** from real accounts
    - Subject to significant limitations and assumptions
    
    **Hypothetical results have many inherent limitations**, including:
    - They do NOT reflect actual trading, liquidity constraints, or market impact
    - They may NOT account for slippage, commissions, and fees
    - They are designed with benefit of hindsight
    - They assume perfect execution at displayed prices
    - Past hypothetical performance is NOT indicative of future results
    """)
    
    # Data Sources
    st.markdown("### 9. 🔌 THIRD-PARTY DATA SOURCES")
    st.markdown("""
    This application relies on third-party data sources (including but not limited to Yahoo Finance API). 
    
    The Provider:
    - Does NOT control or guarantee the accuracy of third-party data
    - Is NOT responsible for data delays, outages, or errors from third-party sources
    - May experience interruptions in data availability at any time
    - Does NOT warrant that data feeds will be uninterrupted or error-free
    
    **Always verify data with official sources before making any decisions.**
    """)
    
    # Changes to Terms
    st.markdown("### 10. 🔄 CHANGES TO TERMS")
    st.markdown("""
    The Provider reserves the right to modify, update, or discontinue this application or these terms at any time without notice.
    
    Continued use of the application after any changes constitutes acceptance of the modified terms.
    """)
    
    # Geographic Restrictions
    st.markdown("### 11. 🌍 GEOGRAPHIC RESTRICTIONS")
    st.markdown("""
    This application may NOT be available or suitable for use in all jurisdictions. Users are responsible for ensuring their use complies with local laws.
    
    If you are located in a jurisdiction where use of this application would be illegal or unauthorized, you must immediately cease using it.
    """)
    
    # Final Warning
    st.markdown('<div class="legal-highlight">', unsafe_allow_html=True)
    st.markdown("""
    ### ⚠️ FINAL WARNING ⚠️
    
    **IF YOU DO NOT AGREE WITH ANY OF THESE TERMS, DO NOT USE THIS APPLICATION.**
    
    **IF YOU CHOOSE TO USE THIS APPLICATION AFTER READING THESE TERMS, YOU DO SO AT YOUR OWN RISK AND ACCEPT FULL RESPONSIBILITY FOR ANY CONSEQUENCES.**
    
    **Options and futures trading is NOT suitable for everyone. You should carefully consider whether trading is appropriate for your financial situation.**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Acceptance checkbox and button
    st.markdown("---")
    st.markdown("### ✅ ACCEPTANCE REQUIRED")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        acceptance_checkbox = st.checkbox(
            "I have read, understood, and agree to all terms and conditions above. I acknowledge that this is for educational purposes only and NOT financial advice. I accept all risks and responsibilities.",
            key="acceptance_checkbox"
        )
        
        st.markdown("")  # Spacing
        
        if acceptance_checkbox:
            if st.button("✅ I ACCEPT - Enter Application", type="primary", use_container_width=True):
                st.session_state.legal_accepted = True
                st.rerun()
        else:
            st.button("✅ I ACCEPT - Enter Application", type="primary", disabled=True, use_container_width=True)
            st.info("👆 Please check the box above to confirm you have read and agree to the terms.")
        
        st.markdown("")  # Spacing
        
        if st.button("❌ I DO NOT ACCEPT - Exit", type="secondary", use_container_width=True):
            st.error("You must accept the terms to use this application. Please close this browser tab.")
            st.stop()
    
    # Stop rendering the rest of the app until accepted
    st.stop()

# ============================================================================
# END LEGAL DISCLAIMER
# ============================================================================

# Sidebar - Inputs Section
st.sidebar.markdown("## 📊 Inputs Section")

# Ticker input
ticker = st.sidebar.text_input(
    "Ticker Symbol", 
    value="AAPL", 
    help="Enter stock ticker (e.g., AAPL, MSFT) or futures symbol (e.g., ES=F, GC=F, CL=F)"
).upper()

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
            st.session_state.is_futures = data_fetcher.is_futures
            
            # Load futures or options specific data
            if data_fetcher.is_futures:
                st.session_state.futures_info = data_fetcher.get_futures_info()
                st.session_state.margin_info = data_fetcher.get_futures_margin_estimate(st.session_state.current_price)
                st.session_state.available_expirations = []
                st.sidebar.success(f"✅ Futures data loaded for {ticker}")
            else:
                st.session_state.available_expirations = data_fetcher.get_available_expirations()
                st.session_state.futures_info = None
                st.session_state.margin_info = None
                st.sidebar.success(f"✅ Stock/Options data loaded for {ticker}")
            
            st.session_state.data_loaded = True
            st.session_state.current_ticker = ticker
        except Exception as e:
            st.sidebar.error(f"Error loading data: {str(e)}")
            st.session_state.data_loaded = False

# Check if data is loaded
if st.session_state.data_loaded:
    # Display current price and volatility
    st.sidebar.markdown("### 💰 Current Market Data")
    
    # Check if futures or stock/options
    is_futures = st.session_state.get('is_futures', False)
    
    if is_futures:
        st.sidebar.info("🔮 **FUTURES CONTRACT DETECTED**")
        st.sidebar.metric("Futures Price", f"${st.session_state.current_price:.2f}")
        
        if st.session_state.futures_info:
            st.sidebar.metric("Contract Multiplier", f"{st.session_state.futures_info['contract_multiplier']}x")
            st.sidebar.metric("Contract Value", f"${st.session_state.futures_info['current_price'] * st.session_state.futures_info['contract_multiplier']:,.2f}")
        
        if st.session_state.margin_info:
            st.sidebar.metric("Est. Initial Margin", f"${st.session_state.margin_info['initial_margin']:,.2f}")
            st.sidebar.metric("Est. Maint. Margin", f"${st.session_state.margin_info['maintenance_margin']:,.2f}")
    else:
        st.sidebar.metric("Current Price", f"${st.session_state.current_price:.2f}")
    
    if st.session_state.volatility:
        st.sidebar.metric("Annual Volatility (252 days)", f"{st.session_state.volatility*100:.2f}%")
    else:
        st.sidebar.warning("Unable to calculate volatility")
    
    # Expiration date selection (only for options)
    if not is_futures:
        st.sidebar.markdown("### 📅 Expiration Date")
        if len(st.session_state.available_expirations) > 0:
            selected_expiration = st.sidebar.selectbox(
                "Select Expiration Date",
                st.session_state.available_expirations
            )
        else:
            st.sidebar.error("No expiration dates available")
            selected_expiration = None
    else:
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
                
                # Greeks Summary
                st.markdown("### 📋 Key Greeks Insights")
                
                insight_col1, insight_col2, insight_col3 = st.columns(3)
                
                # Extract calls and puts Greeks for summary
                calls_greeks_df = greeks_df[greeks_df['Type'] == 'CALL']
                puts_greeks_df = greeks_df[greeks_df['Type'] == 'PUT']
                
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
                
                # Visual Key for Diff% Columns
                with st.expander("🔑 Visual Key - Call_Diff_% & Put_Diff_% Color Coding"):
                    st.markdown("### Understanding the Percentage Difference Columns")
                    
                    key_col1, key_col2, key_col3 = st.columns(3)
                    
                    with key_col1:
                        st.markdown("""
                        #### 🟢 Green (Positive %)
                        **Market > Fair Value**
                        
                        **Meaning:** Option is trading **above** its theoretical fair value
                        
                        **Interpretation:**
                        - Potentially **overpriced**
                        - Market is paying a **premium**
                        - Consider **SELLING** if green
                        
                        **Example:**
                        ```
                        Market: $5.50
                        Fair:   $5.00
                        Diff:   +10.0% 🟢
                        
                        → Option is 10% expensive
                        → Sell opportunity
                        ```
                        """)
                    
                    with key_col2:
                        st.markdown("""
                        #### 🟡 Yellow (Near 0%)
                        **Market ≈ Fair Value**
                        
                        **Meaning:** Option is trading **at or near** its theoretical fair value
                        
                        **Interpretation:**
                        - **Fairly priced**
                        - Market is efficient
                        - No clear arbitrage
                        
                        **Example:**
                        ```
                        Market: $5.02
                        Fair:   $5.00
                        Diff:   +0.4% 🟡
                        
                        → Option is fairly priced
                        → No edge either way
                        ```
                        """)
                    
                    with key_col3:
                        st.markdown("""
                        #### 🔴 Red (Negative %)
                        **Market < Fair Value**
                        
                        **Meaning:** Option is trading **below** its theoretical fair value
                        
                        **Interpretation:**
                        - Potentially **underpriced**
                        - Market is offering a **discount**
                        - Consider **BUYING** if red
                        
                        **Example:**
                        ```
                        Market: $4.50
                        Fair:   $5.00
                        Diff:   -10.0% 🔴
                        
                        → Option is 10% cheap
                        → Buy opportunity
                        ```
                        """)
                    
                    st.markdown("---")
                    
                    st.markdown("""
                    ### 🎨 Color Gradient Scale
                    
                    The table uses a **Red-Yellow-Green gradient** (reversed) to highlight opportunities:
                    """)
                    
                    gradient_cols = st.columns([1, 3, 1])
                    
                    with gradient_cols[1]:
                        st.markdown("""
                        ```
                        🔴 Deep Red    (-15% or more)   Strong BUY signal
                        🟠 Red         (-10% to -5%)    Good BUY signal
                        🟡 Yellow      (-5% to +5%)     Fair pricing
                        🟢 Light Green (+5% to +10%)    Good SELL signal
                        🟢 Deep Green  (+15% or more)   Strong SELL signal
                        ```
                        """)
                    
                    st.markdown("---")
                    
                    st.markdown("""
                    ### 📊 How to Use This Information
                    
                    **For BUYERS (Looking to open long positions):**
                    1. Look for **red cells** (negative percentages)
                    2. Deeper red = Better deal
                    3. Target: -5% or lower for good value
                    
                    **For SELLERS (Looking to write options):**
                    1. Look for **green cells** (positive percentages)
                    2. Deeper green = Better premium
                    3. Target: +5% or higher for good premium collection
                    
                    **For ALL TRADERS:**
                    - **Yellow cells** indicate efficient pricing - no clear edge
                    - Extreme values (±15%+) may indicate:
                      - Genuine mispricing opportunity ✅
                      - Model assumptions off (volatility, etc.) ⚠️
                      - Illiquid strikes with wide spreads ⚠️
                    
                    **Important Notes:**
                    - Compare Call_Diff_% and Put_Diff_% at the same strike
                    - If both are similar color → Consistent mispricing signal
                    - If different colors → May indicate skew or model issues
                    - Always check **volume** and **open interest** for liquidity
                    """)
                    
                    st.info("""
                    💡 **Pro Tip:** The AI Recommendation system automatically incorporates these 
                    fair value differences into its analysis. Options with favorable Diff_% values 
                    (red for buys, green for sells) will rank higher in recommendations.
                    """)
                
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
                
                # Visual Key for Fair Value Chart
                with st.expander("🔑 Visual Key - Fair Value Analysis Chart"):
                    st.markdown("""
                    #### Line Types & Colors:
                    """)
                    
                    key_col1, key_col2 = st.columns(2)
                    
                    with key_col1:
                        st.markdown("""
                        **CALLS:**
                        - 🔵 **Blue Solid Line**: Market Price (what traders are paying)
                        - 🔵 **Light Blue Dashed Line**: Fair Value (theoretical price from Binomial model)
                        
                        **PUTS:**
                        - 🔴 **Red Solid Line**: Market Price (what traders are paying)
                        - 🔴 **Light Coral Dashed Line**: Fair Value (theoretical price from Binomial model)
                        """)
                    
                    with key_col2:
                        st.markdown("""
                        **How to Interpret:**
                        - **Market ABOVE Fair Value** → Option may be overpriced (potential sell)
                        - **Market BELOW Fair Value** → Option may be underpriced (potential buy)
                        - **Lines converge** → Fair pricing, efficient market
                        - **Lines diverge** → Mispricing opportunity
                        
                        **Note:** ATM (at-the-money) options typically have the most liquidity and tightest pricing.
                        """)
                    
                    st.markdown("---")
                    st.markdown("""
                    #### Table Column Meanings:
                    - **Call_Diff_%** / **Put_Diff_%**: 
                      - **Positive (Green)**: Market price is higher than fair value (potentially overvalued)
                      - **Negative (Red)**: Market price is lower than fair value (potentially undervalued)
                      - **Near 0%**: Fairly priced
                    
                    - **Black-Scholes vs Binomial**: 
                      - BS = European-style approximation
                      - Binomial = American-style (accounts for early exercise)
                      - Binomial is generally more accurate for American options
                    """)
            
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
            
            # Visual Key for Distribution Chart
            with st.expander("🔑 Visual Key - Distribution of Simulated Prices at Expiration"):
                st.markdown("#### Chart Elements:")
                
                visual_col1, visual_col2 = st.columns(2)
                
                with visual_col1:
                    st.markdown("""
                    **Visual Elements:**
                    - 📊 **Light Blue Bars**: Histogram showing frequency of simulated prices
                      - **Taller bars** = More simulations ended at this price
                      - **Peak of curve** = Most likely outcome
                    
                    - **📍 Red Dashed Vertical Line**: Current stock price (starting point)
                      - Everything to the **right** = Price increased
                      - Everything to the **left** = Price decreased
                    
                    - **📍 Green Dashed Vertical Line**: Mean (average) simulated price
                      - Expected final price at expiration
                      - Shows directional bias
                    """)
                
                with visual_col2:
                    st.markdown("""
                    **How to Interpret:**
                    - **Bell-shaped curve**: Normal market conditions
                    - **Wide spread**: High volatility, uncertain outcome
                    - **Narrow spread**: Low volatility, predictable outcome
                    - **Green line right of red**: Bullish expectation
                    - **Green line left of red**: Bearish expectation
                    
                    **Distribution Shape:**
                    - **Symmetric**: Balanced up/down probability
                    - **Right-skewed**: More upside potential
                    - **Left-skewed**: More downside risk
                    """)
                
                st.markdown("---")
                st.markdown("""
                #### Example Reading:
                
                **Scenario:** Red line at $100, Green line at $105, Peak at $103
                - **Current Price**: $100
                - **Expected Price**: $105 (5% gain expected)
                - **Most Likely**: $103 (the modal outcome)
                - **Interpretation**: Bullish bias with likely 3-5% gain
                
                **Key Metrics Explained:**
                - **10th/90th Percentile**: 80% of outcomes fall in this range
                - **Probability > Current**: Chance of any profit at expiration
                - **Mean vs Median**: If different, shows skewness (tail risk)
                """)
            
            
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
                - **SVM Model Integration**: Price predictions with RBF kernel
                - **Greeks-Enhanced Analysis**: Delta, Gamma, Theta, Vega, Rho
                - Incorporating ML predictions, fair value, and risk-adjusted returns
                - Considering liquidity, time decay, and market sentiment
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
                    
                    # ML Score & Prediction
                    ml_score_col1, ml_score_col2 = st.columns(2)
                    with ml_score_col1:
                        st.progress(row['ml_score'] / 100, text=f"SVM Model Score: {row['ml_score']:.0f}/100")
                    with ml_score_col2:
                        change_indicator = "📈" if row['svm_predicted_change'] > 0 else "📉"
                        st.metric(f"{change_indicator} SVM Prediction", 
                                 f"${row['svm_predicted_price']:.2f}", 
                                 f"{row['svm_predicted_change']:.2f}%")
                    
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
                        
                        # ML Predictions (SVM)
                        st.markdown("#### 🤖 SVM MODEL PREDICTIONS")
                        ml_col1, ml_col2, ml_col3 = st.columns(3)
                        
                        with ml_col1:
                            st.metric("ML Score", f"{row['ml_score']:.0f}/100")
                        
                        with ml_col2:
                            st.metric("Predicted Price", f"${row['svm_predicted_price']:.2f}")
                        
                        with ml_col3:
                            change_delta = "+" if row['svm_predicted_change'] > 0 else ""
                            st.metric("Predicted Change", f"{change_delta}{row['svm_predicted_change']:.2f}%")
                        
                        # Display ML insights
                        if row['ml_insights']:
                            ml_insights_list = row['ml_insights'].split(' | ')
                            for insight in ml_insights_list:
                                if '✅' in insight or 'Supports' in insight:
                                    st.success(f"✓ {insight}")
                                elif '⚠️' in insight or 'Contradicts' in insight:
                                    st.warning(f"⚠ {insight}")
                                else:
                                    st.info(f"ℹ {insight}")
                        
                        st.caption("**SVM Analysis:** Support Vector Machine with RBF kernel predicts future price movement based on historical patterns and current market conditions.")
                    
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
            
            # =================================================================
            # EXPLANATIONS SECTION
            # =================================================================
            st.markdown("### 📚 Explanations")
            
            st.markdown("""
            Understanding how the AI evaluates and scores trading opportunities:
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📐 Greeks Score (0-100)")
                st.markdown("""
                **What It Measures:** How favorable the option's Greeks are for the recommended action.
                
                **Components Analyzed:**
                - **Delta (Price Sensitivity)**
                  - For BUY: Higher delta (>0.6) = Higher score
                  - Low delta (<0.45) = Score penalty
                
                - **Gamma (Delta Change Rate)**
                  - High gamma (>0.05) = Position management complexity
                  - Moderate gamma (0.02-0.05) = Stable conditions
                
                - **Theta (Time Decay)**
                  - For BUY: High negative theta = Score penalty
                  - For SELL: High negative theta = Score boost
                  - Theta < -$0.10/day is considered "high"
                
                - **Vega (Volatility Sensitivity)**
                  - High vega + Low IV = Good for buyers (+10 bonus)
                  - High vega + High IV = Good for sellers (+10 bonus)
                
                - **Time to Expiration**
                  - < 7 days: Penalizes buyers, rewards sellers
                  - > 45 days: Rewards buyers, penalizes sellers
                
                **Score Ranges:**
                - **80-100**: Excellent Greek profile for this action
                - **60-79**: Good Greek profile
                - **40-59**: Neutral/Mixed Greek profile
                - **20-39**: Poor Greek profile
                - **0-19**: Very unfavorable Greeks
                
                **Impact on Recommendation:**
                - Greeks Score multiplies the risk-adjusted return
                - Confidence adjusts: ±0.10 can upgrade/downgrade confidence level
                - Example: Score of 70 → 70% of base risk-adjusted return
                """)
                
                with st.expander("🔍 Greeks Score Calculation Example"):
                    st.code("""
Base Score: 50 (neutral)

BUY CALL Analysis:
+ Strong Delta (0.65):        +15 points
+ High Gamma (0.06):          +10 points
- High Theta (-$0.12/day):    -15 points
+ High Vega (0.18):           +10 points
+ Low Current IV (22%):       +5 points (Vega bonus)
- Short Time (5 days):        -10 points

Final Greeks Score: 55/100
Confidence Adjustment: -0.10 (HIGH → MEDIUM)
Risk-Adj Return Multiplier: 0.55
                    """, language="text")
            
            with col2:
                st.markdown("#### 🤖 SVM Model Score (0-100)")
                st.markdown("""
                **What It Measures:** How well the machine learning prediction aligns with the recommended action.
                
                **SVM Model Details:**
                - **Algorithm**: Support Vector Machine with RBF kernel
                - **Training**: Historical price data (1 year)
                - **Features**: 20+ technical indicators (MA, RSI, momentum, volume)
                - **Prediction**: Price N days ahead (matches expiration)
                
                **Scoring Logic:**
                
                **For BUY CALL Actions:**
                - Predicted move > +5%: +30 points, +0.15 confidence
                - Predicted move > +2%: +15 points, +0.08 confidence
                - Predicted move < -2%: -20 points, -0.15 confidence
                
                **For BUY PUT Actions:**
                - Predicted move < -5%: +30 points, +0.15 confidence
                - Predicted move < -2%: +15 points, +0.08 confidence
                - Predicted move > +2%: -20 points, -0.15 confidence
                
                **For SELL Actions:**
                - Opposite logic (rewards flat/contrary predictions)
                
                **Strike Analysis:**
                - If SVM predicts price > strike (for CALL): +10 bonus
                - If SVM predicts price < strike (for PUT): +10 bonus
                
                **Score Ranges:**
                - **80-100**: Strong ML confirmation
                - **60-79**: Good ML alignment
                - **40-59**: Neutral/Mixed ML signal
                - **20-39**: ML suggests caution
                - **0-19**: ML contradicts recommendation
                
                **Impact on Recommendation:**
                - ML Score multiplies the risk-adjusted return (after Greeks)
                - Confidence adjusts: ±0.10 can upgrade/downgrade confidence
                - Example: Score of 85 → 85% of Greeks-adjusted return
                """)
                
                with st.expander("🔍 SVM Score Calculation Example"):
                    st.code("""
Base Score: 50 (neutral)

BUY CALL @ $150 Analysis:
Current Price: $148
SVM Prediction: $156 (+5.4%)

+ Bullish prediction (>5%):   +30 points
+ Price above strike:         +10 points
+ Moderate move magnitude:    +10 points

Final ML Score: 80/100
Confidence Adjustment: +0.15 (MEDIUM → HIGH)
Risk-Adj Return Multiplier: 0.80

Combined Effect:
Base Return: 0.0500
× Greeks (70): 0.0350
× ML (80):     0.0280 (final)
                    """, language="text")
            
            st.markdown("---")
            
            # Risk-Adjusted Returns Explanation
            st.markdown("#### 💰 Risk-Adjusted Return")
            
            st.markdown("""
            **What It Is:** A metric that measures the expected return of a trade relative to the capital at risk and probability of success.
            
            **Why It Matters:** High returns are meaningless if the probability of success is low or the capital required is excessive. 
            Risk-adjusted return normalizes different opportunities for fair comparison.
            """)
            
            rar_col1, rar_col2 = st.columns(2)
            
            with rar_col1:
                st.markdown("""
                **Formula:**
                ```
                Risk-Adjusted Return = 
                    (Expected Payoff × Probability ITM - Cost)
                    ────────────────────────────────────────
                              Cost × Risk Factor
                ```
                
                **Components:**
                - **Expected Payoff**: Monte Carlo simulated option value at expiration
                - **Probability ITM**: Likelihood option expires in-the-money
                - **Cost**: Option premium × 100 × contracts
                - **Risk Factor**: Greeks Score × ML Score (0-1 multipliers)
                
                **Adjustments Applied:**
                1. **Base Return** = (Expected Payoff - Cost) / Cost
                2. **× Greeks Score** = Adjusts for time decay, volatility sensitivity
                3. **× ML Score** = Adjusts for price prediction alignment
                4. **Result**: Final risk-adjusted return value
                """)
            
            with rar_col2:
                st.markdown("""
                **Interpretation:**
                - **> 0.02**: Strong return potential relative to risk
                - **0.01 - 0.02**: Good return/risk balance
                - **0 - 0.01**: Marginal return/risk profile
                - **< 0**: Negative expected return (avoid)
                
                **Example Comparison:**
                
                **Option A:**
                - Expected Return: $500
                - Cost: $1,000
                - Probability ITM: 60%
                - Greeks: 80, ML: 75
                - Risk-Adj Return: **0.0180**
                
                **Option B:**
                - Expected Return: $800
                - Cost: $2,000
                - Probability ITM: 45%
                - Greeks: 55, ML: 60
                - Risk-Adj Return: **0.0074**
                
                **Winner: Option A** (better risk-adjusted return despite lower absolute profit)
                """)
            
            with st.expander("🔍 Risk-Adjusted Return Calculation Example"):
                st.code("""
Real Trade Example:

BUY CALL @ Strike $150
Current Price: $148
Days to Expiration: 30
Option Premium: $3.50 per contract

Step 1: Monte Carlo Simulation
- Expected Option Value at Expiry: $5.80
- Probability ITM: 62%
- Expected Payoff: $5.80 × 62% = $3.60

Step 2: Base Return Calculation
- Cost: $3.50 × 100 = $350
- Expected Payoff: $3.60 × 100 = $360
- Raw Return: ($360 - $350) / $350 = 0.0286 (2.86%)

Step 3: Greeks Adjustment
- Greeks Score: 70/100 = 0.70 multiplier
- Adjusted Return: 0.0286 × 0.70 = 0.0200

Step 4: ML Adjustment
- ML Score: 85/100 = 0.85 multiplier
- Final Return: 0.0200 × 0.85 = 0.0170

Final Risk-Adjusted Return: 0.0170 (1.70%)

This means for every $1 of capital risked, you expect
$0.017 in return after accounting for all risks and
uncertainties (Greeks + ML predictions).
                """, language="text")
            
            st.markdown("---")
            
            st.markdown("#### 🎯 Combined Scoring Impact")
            
            impact_col1, impact_col2, impact_col3 = st.columns(3)
            
            with impact_col1:
                st.markdown("**📊 Risk-Adjusted Return**")
                st.code("""
Base Return
    ↓
× Greeks Score
    ↓
× ML Score
    ↓
Final Return
                """, language="text")
                st.caption("Both scores directly multiply the expected return")
            
            with impact_col2:
                st.markdown("**🎚️ Confidence Level**")
                st.code("""
Base: HIGH/MEDIUM/LOW
    ↓
+ Greeks Adjustment
    ↓
+ ML Adjustment
    ↓
Final Confidence
                """, language="text")
                st.caption("Can upgrade or downgrade by one level")
            
            with impact_col3:
                st.markdown("**💡 Best Recommendations**")
                st.markdown("""
                **Ideal Profile:**
                - Greeks: 80+
                - ML: 80+
                - Both aligned
                - High base probability
                
                **Result:**
                - High confidence
                - Top ranked
                - Clear action signal
                """)
            
            st.info("""
            💡 **Pro Tip:** Look for recommendations where BOTH Greeks and ML scores are above 70. 
            This indicates strong alignment between technical factors (Greeks) and predictive models (ML), 
            providing the highest confidence trading opportunities.
            """)
            
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
    
    elif is_futures:
        # ================================================================
        # FUTURES ANALYSIS SECTION
        # ================================================================
        st.markdown('<div class="section-header">🔮 Futures Contract Analysis</div>', unsafe_allow_html=True)
        
        futures_info = st.session_state.futures_info
        margin_info = st.session_state.margin_info
        current_price = st.session_state.current_price
        
        # Display futures contract info
        st.markdown("### 📋 Contract Information")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Symbol", futures_info['symbol'])
            st.metric("Current Price", f"${current_price:.2f}")
        
        with col2:
            st.metric("Contract Multiplier", f"{futures_info['contract_multiplier']}x")
            st.metric("Contract Value", f"${futures_info['current_price'] * futures_info['contract_multiplier']:,.2f}")
        
        with col3:
            st.metric("Initial Margin", f"${margin_info['initial_margin']:,.2f}")
            st.metric("Maintenance Margin", f"${margin_info['maintenance_margin']:,.2f}")
        
        with col4:
            st.metric("Exchange", futures_info.get('exchange', 'N/A'))
            st.metric("Currency", futures_info.get('currency', 'USD'))
        
        # ================================================================
        # MONTE CARLO SIMULATION FOR FUTURES
        # ================================================================
        st.markdown('<div class="section-header">🎲 Monte Carlo Simulation</div>', unsafe_allow_html=True)
        
        historical_data = st.session_state.historical_data
        
        if not historical_data.empty and st.session_state.volatility:
            sigma = st.session_state.volatility
            
            # Run Monte Carlo simulation (30 days forward for futures)
            with st.spinner("Running Monte Carlo simulation..."):
                mc_prices = OptionsPricing.monte_carlo_price_paths(
                    S=current_price,
                    r=risk_free_rate,
                    sigma=sigma,
                    days=30,  # 30 days forward
                    num_simulations=int(num_simulations)
                )
            
            # Plot Monte Carlo paths
            fig_mc = go.Figure()
            
            # Plot sample paths (20 random paths)
            num_paths_to_plot = min(20, num_simulations)
            for i in range(num_paths_to_plot):
                fig_mc.add_trace(go.Scatter(
                    y=mc_prices[i],
                    mode='lines',
                    line=dict(width=1, color='lightblue'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            # Plot mean path
            mean_path = mc_prices.mean(axis=0)
            fig_mc.add_trace(go.Scatter(
                y=mean_path,
                mode='lines',
                name='Mean Path',
                line=dict(width=3, color='red')
            ))
            
            # Add current price line
            fig_mc.add_hline(y=current_price, line_dash="dash", line_color="green",
                           annotation_text="Current Price")
            
            fig_mc.update_layout(
                title='Monte Carlo Price Simulation (30 Days)',
                xaxis_title='Days',
                yaxis_title='Price ($)',
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig_mc, use_container_width=True)
            
            # MC Statistics
            final_prices = mc_prices[:, -1]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Expected Price (30d)", f"${np.mean(final_prices):.2f}")
                st.metric("Probability Up", f"{np.mean(final_prices > current_price)*100:.1f}%")
            
            with col2:
                st.metric("Median Price", f"${np.median(final_prices):.2f}")
                st.metric("Probability Down", f"{np.mean(final_prices < current_price)*100:.1f}%")
            
            with col3:
                st.metric("95th Percentile", f"${np.percentile(final_prices, 95):.2f}")
                st.metric("Upside Potential", f"${np.percentile(final_prices, 75) - current_price:.2f}")
            
            with col4:
                st.metric("5th Percentile", f"${np.percentile(final_prices, 5):.2f}")
                st.metric("Downside Risk", f"${current_price - np.percentile(final_prices, 25):.2f}")
            
            # Chart Legend/Key
            with st.expander("📊 Chart Legend - Monte Carlo Price Paths"):
                st.markdown(f"""
                **Price Path Simulation Chart:**
                - **Light Blue Lines**: 20 random sample price paths out of {num_simulations:,} simulations
                - **Red Bold Line**: Mean (average) path across all simulations
                - **Green Dashed Line**: Current futures price (starting point)
                
                **How to Read:**
                - Each line shows one possible price trajectory over 30 days
                - Wider spread = Higher volatility/uncertainty
                - Mean path = Expected price movement
                - Convergence/divergence = Stability/instability expectations
                
                **Key Metrics:**
                - **Expected Price**: Average final price across all simulations
                - **Probability Up/Down**: Likelihood of price movement direction
                - **Percentiles**: Range of probable outcomes (95th = only 5% chance of exceeding)
                - **Upside/Downside**: Expected gains/losses from current price
                """)
            
            # ================================================================
            # ML PREDICTIONS FOR FUTURES
            # ================================================================
            st.markdown('<div class="section-header">🤖 Machine Learning Predictions</div>', unsafe_allow_html=True)
            
            with st.spinner("Training predictive models..."):
                # Target 30 days ahead for futures
                target_days = 30
                
                # Decision Tree
                dt_model, dt_stats, dt_error = PredictiveModels.train_decision_tree(
                    historical_data, target_days
                )
                
                # SVM
                svm_model, svm_scaler, svm_stats, svm_error = PredictiveModels.train_svm_rbf(
                    historical_data, target_days
                )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🌲 Decision Tree")
                if dt_model and dt_stats:
                    df_features = PredictiveModels.prepare_features(historical_data)
                    if not df_features.empty:
                        feature_cols = [col for col in df_features.columns if col != 'Close']
                        X_latest = df_features[feature_cols].iloc[-1:].values
                        dt_prediction = dt_model.predict(X_latest)[0]
                        dt_change = ((dt_prediction - current_price) / current_price) * 100
                        
                        st.metric("Predicted Price", f"${dt_prediction:.2f}", f"{dt_change:+.2f}%")
                        st.metric("Train R²", f"{dt_stats['train_score']:.4f}")
                        st.metric("Test R²", f"{dt_stats['test_score']:.4f}")
                    else:
                        dt_prediction = current_price
                        st.warning("Unable to make prediction")
                else:
                    dt_prediction = current_price
                    st.error(f"Training failed: {dt_error}")
            
            with col2:
                st.markdown("#### 🎯 SVM (RBF)")
                if svm_model and svm_stats:
                    df_features = PredictiveModels.prepare_features(historical_data)
                    if not df_features.empty:
                        feature_cols = [col for col in df_features.columns if col != 'Close']
                        X_latest = df_features[feature_cols].iloc[-1:].values
                        X_latest_scaled = svm_scaler.transform(X_latest)
                        svm_prediction = svm_model.predict(X_latest_scaled)[0]
                        svm_change = ((svm_prediction - current_price) / current_price) * 100
                        
                        st.metric("Predicted Price", f"${svm_prediction:.2f}", f"{svm_change:+.2f}%")
                        st.metric("Train R²", f"{svm_stats['train_score']:.4f}")
                        st.metric("Test R²", f"{svm_stats['test_score']:.4f}")
                    else:
                        svm_prediction = current_price
                        st.warning("Unable to make prediction")
                else:
                    svm_prediction = current_price
                    st.error(f"Training failed: {svm_error}")
            
            with col3:
                st.markdown("#### 📊 Consensus")
                avg_pred = (dt_prediction + svm_prediction) / 2
                avg_change = ((avg_pred - current_price) / current_price) * 100
                
                st.metric("Average Price", f"${avg_pred:.2f}", f"{avg_change:+.2f}%")
                if avg_change > 0:
                    st.success("🐂 **Bullish**")
                else:
                    st.error("🐻 **Bearish**")
                st.caption(f"Models predict {abs(avg_change):.2f}% move")
            
            # Build ML predictions dict
            ml_predictions = {}
            if dt_model and dt_stats:
                ml_predictions['decision_tree'] = dt_prediction
            if svm_model and svm_stats:
                ml_predictions['svm'] = svm_prediction
            
            # ================================================================
            # FUTURES AI RECOMMENDATIONS
            # ================================================================
            st.markdown('<div class="section-header">🎯 AI Futures Trading Recommendation</div>', unsafe_allow_html=True)
            
            # Generate futures recommendation
            with st.spinner("Generating AI recommendation..."):
                recommendation = FuturesRecommendations.generate_futures_recommendation(
                    current_price=current_price,
                    futures_info=futures_info,
                    margin_info=margin_info,
                    monte_carlo_results=mc_prices,
                    ml_predictions=ml_predictions,
                    portfolio_value=portfolio_value,
                    risk_percentage=risk_percentage,
                    volatility=sigma
                )
            
            # Display recommendation
            st.markdown("### 🏆 Trading Recommendation")
            
            st.info(f"""
            **AI Analysis Summary:**
            - Portfolio Value: ${portfolio_value:,.2f}
            - Risk per Trade: {risk_percentage}% (${portfolio_value * risk_percentage / 100:,.2f})
            - Based on {num_simulations:,} Monte Carlo simulations
            - **SVM Model Integration**: Price predictions with RBF kernel
            - Contract multiplier: {futures_info['contract_multiplier']}x
            """)
            
            # Recommendation card
            confidence_class = f"recommendation-{recommendation['confidence'].lower()}"
            
            st.markdown(f"""
            <div class="{confidence_class}">
            <h3>{recommendation['action']} - {recommendation['confidence']} CONFIDENCE</h3>
            <p><strong>Symbol:</strong> {recommendation['symbol']}</p>
            <p><strong>Current Price:</strong> ${recommendation['current_price']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics display
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Probability Up", f"{recommendation['probability_up']*100:.1f}%")
                st.metric("Expected Price", f"${recommendation['expected_price']:.2f}")
            
            with col2:
                st.metric("Probability Down", f"{recommendation['probability_down']*100:.1f}%")
                st.metric("Risk-Adj Return", f"{recommendation['risk_adjusted_return']:.4f}")
            
            with col3:
                st.metric("Position Size", f"{recommendation['position_size']} contracts")
                st.metric("Total Margin", f"${recommendation['total_margin_required']:,.2f}")
            
            with col4:
                st.metric("Contract Value", f"${recommendation['contract_value']:,.2f}")
                st.metric("Expected Return", f"${recommendation['expected_return']:,.2f}")
            
            # SVM Model Score and Prediction
            ml_score_col1, ml_score_col2 = st.columns(2)
            with ml_score_col1:
                st.progress(recommendation['ml_score'] / 100, text=f"SVM Model Score: {recommendation['ml_score']:.0f}/100")
            with ml_score_col2:
                change_indicator = "📈" if recommendation['svm_predicted_change'] > 0 else "📉"
                st.metric(f"{change_indicator} SVM Prediction", 
                         f"${recommendation['svm_predicted_price']:.2f}", 
                         f"{recommendation['svm_predicted_change']:.2f}%")
            
            # Trading Plan Details
            with st.expander("📋 Trading Plan & Execution Details"):
                # Entry Parameters
                st.markdown("#### 🎯 ENTRY PARAMETERS")
                entry_col1, entry_col2, entry_col3 = st.columns(3)
                
                with entry_col1:
                    st.metric("Entry Price", f"${recommendation['entry_price']:.2f}")
                    st.metric("Contract Multiplier", f"{recommendation['contract_multiplier']}x")
                
                with entry_col2:
                    st.metric("Position Size", f"{recommendation['position_size']} contracts")
                    st.metric("Total Margin Required", f"${recommendation['total_margin_required']:,.2f}")
                
                with entry_col3:
                    st.metric("Contract Value", f"${recommendation['contract_value']:,.2f}")
                    st.metric("ATR Estimate", f"${recommendation['atr_estimate']:.2f}")
                
                st.markdown("---")
                
                # Exit Parameters
                st.markdown("#### 🎯 EXIT PARAMETERS")
                exit_col1, exit_col2, exit_col3 = st.columns(3)
                
                with exit_col1:
                    st.metric("Profit Target 1 (2:1)", f"${recommendation['profit_target_1']:.2f}")
                    st.metric("Potential Profit", f"${recommendation['profit_1']:,.2f}")
                
                with exit_col2:
                    st.metric("Profit Target 2 (3:1)", f"${recommendation['profit_target_2']:.2f}")
                    st.metric("Potential Profit", f"${recommendation['profit_2']:,.2f}")
                
                with exit_col3:
                    st.metric("Stop Loss", f"${recommendation['stop_loss']:.2f}")
                    st.metric("Max Loss", f"${recommendation['max_loss']:,.2f}")
                
                st.markdown("---")
                
                # Risk/Reward Analysis
                st.markdown("#### ⚖️ RISK/REWARD ANALYSIS")
                rr_col1, rr_col2, rr_col3 = st.columns(3)
                
                with rr_col1:
                    st.metric("Risk/Reward Ratio 1", f"{recommendation['risk_reward_1']:.2f}:1")
                
                with rr_col2:
                    st.metric("Risk/Reward Ratio 2", f"{recommendation['risk_reward_2']:.2f}:1")
                
                with rr_col3:
                    st.metric("% of Portfolio at Risk", f"{(recommendation['max_loss']/portfolio_value)*100:.2f}%")
                
                st.markdown("---")
                
                # ML Insights
                st.markdown("#### 🤖 SVM MODEL INSIGHTS")
                ml_col1, ml_col2, ml_col3 = st.columns(3)
                
                with ml_col1:
                    st.metric("ML Score", f"{recommendation['ml_score']:.0f}/100")
                
                with ml_col2:
                    st.metric("Predicted Price", f"${recommendation['svm_predicted_price']:.2f}")
                
                with ml_col3:
                    change_delta = "+" if recommendation['svm_predicted_change'] > 0 else ""
                    st.metric("Predicted Change", f"{change_delta}{recommendation['svm_predicted_change']:.2f}%")
                
                # Display ML insights
                if recommendation['ml_insights']:
                    ml_insights_list = recommendation['ml_insights'].split(' | ')
                    for insight in ml_insights_list:
                        if '✅' in insight or 'Supports' in insight or 'Strong' in insight:
                            st.success(f"✓ {insight}")
                        elif '⚠️' in insight or 'Contradicts' in insight:
                            st.warning(f"⚠ {insight}")
                        else:
                            st.info(f"ℹ {insight}")
                
                st.caption("**SVM Analysis:** Support Vector Machine with RBF kernel predicts future price movement based on historical patterns and current market conditions.")
            
            # Risk Warning
            st.warning("""
            ⚠️ **FUTURES TRADING RISK WARNING:**
            - Futures contracts are leveraged instruments with substantial risk
            - Margin requirements can change based on volatility
            - Losses can exceed initial margin deposited
            - These are AI-generated recommendations for educational purposes
            - Always use proper risk management and stop losses
            """)
        
        else:
            st.error("Insufficient historical data for analysis.")
    
    else:
        st.warning("⚠️ Please select an expiration date from the sidebar.")

else:
    st.info("👈 Please enter a ticker symbol and click 'Load Data' to begin analysis.")
    
    # Quick start guide
    st.markdown("""
    ## 📚 Quick Start Guide
    
    ### How to Use This Application:
    
    1. **Enter Ticker Symbol** - Input any stock ticker (e.g., AAPL, MSFT) or futures symbol (e.g., ES=F, GC=F, CL=F)
    2. **Load Data** - Click the "Load Data" button to fetch market data
    3. **Select Expiration** - Choose an options expiration date (for stocks) or skip (for futures)
    4. **Adjust Parameters** - Fine-tune risk parameters and portfolio settings
    5. **Review Analysis** - Examine the comprehensive analysis including:
       - Live options/futures prices
       - Fair value calculations (options)
       - Monte Carlo simulations
       - ML price predictions
       - AI-powered trading recommendations
    
    ### Features:
    
    - **📊 Live Data:** Real-time stock, options, and futures prices
    - **🔮 Futures Support:** Full support for futures contracts with margin analysis
    - **💎 Fair Value:** Black-Scholes and Binomial Tree pricing (options)
    - **🎲 Monte Carlo:** Thousands of simulated price paths
    - **🤖 Machine Learning:** Decision Tree and SVM predictions
    - **🎯 AI Recommendations:** Smart trading strategies based on all data
    - **⚠️ Risk Management:** Position sizing and portfolio constraints
    
    ### Risk Disclaimer:
    
    ⚠️ **This application is for educational and informational purposes only.**
    It does NOT constitute financial advice. Trading options involves substantial
    risk and is NOT suitable for all investors. Past performance does NOT guarantee
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

