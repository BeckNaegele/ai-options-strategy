# 📊 Trading Parameters Guide

## New AI-Enhanced Buy & Sell Parameters

The AI recommendation system now includes comprehensive **entry and exit parameters** for every trade recommendation, giving you a complete trading plan.

---

## 🎯 Entry Parameters (BUY Signals)

### 1. **Recommended Entry Price**
The AI calculates the optimal entry price based on:
- Current bid-ask spread
- Fair value calculations
- Liquidity conditions

**For BUY orders:**
- If bid-ask spread < 5%: Use the ASK price (can use MARKET order)
- If bid-ask spread ≥ 5%: Place LIMIT order 30% above BID
- Never pay more than fair value + 5%

**For SELL orders:**
- If bid-ask spread < 5%: Use the BID price (can use MARKET order)
- If bid-ask spread ≥ 5%: Place LIMIT order 70% above BID
- Never sell below fair value - 5%

### 2. **Max Entry Price**
The maximum price you should pay for the option to maintain positive expected value.

### 3. **Order Type**
- **MARKET**: For liquid options with tight spreads (<5%)
- **LIMIT**: For wider spreads to avoid overpaying

### 4. **Timing Recommendation**
Based on probability analysis:
- **ENTER NOW**: Probability ITM > 60% (high confidence setup)
- **ENTER SOON**: Probability ITM > 50% (good setup)
- **WAIT FOR BETTER SETUP**: Probability ITM < 50% (wait for confirmation)

### 5. **Breakeven Price**
The stock price at expiration where you break even:
- **CALL**: Strike + Entry Premium
- **PUT**: Strike - Entry Premium

### 6. **Bid-Ask Spread %**
Shows liquidity quality:
- < 5%: Excellent liquidity
- 5-10%: Good liquidity
- 10-20%: Moderate liquidity
- > 20%: Poor liquidity (avoid)

---

## 🎯 Exit Parameters (SELL/Close Signals)

### 1. **Profit Target 1 (Conservative)**
**For BUYING options:**
- Target: 50% profit (1.5x entry price)
- Recommended for securing partial gains
- Good for volatile markets

**For SELLING options:**
- Target: Buy back at 50% of sold price
- 50% profit already captured
- Lower risk of assignment

### 2. **Profit Target 2 (Aggressive)**
**For BUYING options:**
- Target: 100% profit (2x entry price)
- Swing for bigger gains
- Hold for favorable moves

**For SELLING options:**
- Target: Buy back at 25% of sold price
- 75% profit captured
- Near maximum profit

### 3. **Profit Target 3 (Maximum)**
**For BUYING options:**
- Based on 75th percentile Monte Carlo outcome
- Capped at 3x entry price
- "Moon shot" scenario

**For SELLING options:**
- Target: $0.05 (nearly worthless)
- Option expires worthless
- Maximum profit achieved

### 4. **Stop Loss Price**
Automatic exit to limit losses:

**For BUYING options:**
- High probability (>60%): Stop at 50% loss
- Medium probability (50-60%): Stop at 60% loss
- Lower probability (<50%): Stop at 70% loss

**For SELLING options:**
- Stop if option doubles in price (200%)
- Prevents unlimited loss risk
- Protects against assignment

### 5. **Stop Loss %**
Percentage loss from entry price to trigger stop.

### 6. **Exit Strategy**
Complete rule-based exit plan:

**For BUYING options (High Probability):**
```
HOLD TO EXPIRATION if ITM, else exit at 50% loss
```

**For BUYING options (Lower Probability):**
```
EXIT at 50% profit or 50% loss, or 5 days before expiration
```

**For SELLING options:**
```
BUY TO CLOSE at 50-80% profit, or if price doubles (stop loss)
```

---

## ⚖️ Risk/Reward Analysis

### 1. **Risk/Reward Ratio 1**
Expected reward divided by max loss for Profit Target 1.
- **> 2.0**: Excellent risk/reward
- **1.5 - 2.0**: Good risk/reward
- **1.0 - 1.5**: Acceptable risk/reward
- **< 1.0**: Poor risk/reward (avoid)

### 2. **Risk/Reward Ratio 2**
Expected reward divided by max loss for Profit Target 2.
- Higher potential but requires bigger move
- Should be significantly higher than Ratio 1

### 3. **Max Loss Amount**
The maximum dollar amount you can lose on this trade:
- For buying: Premium paid × 100 × contracts
- For selling: Calculated based on stop loss

### 4. **Profit Amounts**
Dollar amounts at each profit target:
- **Profit 1 Amount**: Gain if Target 1 hit
- **Profit 2 Amount**: Gain if Target 2 hit

### 5. **% of Portfolio at Risk**
Percentage of total portfolio at risk in this trade.
- **< 2%**: Conservative
- **2-3%**: Moderate
- **3-5%**: Aggressive
- **> 5%**: Very aggressive (not recommended)

---

## 📋 Complete Trading Plan Example

### Example: BUY CALL Recommendation

```
Stock: AAPL @ $175.00
Strike: $180 CALL
Expiration: 30 days

ENTRY PARAMETERS:
✓ Recommended Entry: $4.80
✓ Max Entry Price: $5.25
✓ Order Type: LIMIT
✓ Timing: ENTER SOON
✓ Breakeven: $184.80
✓ Bid-Ask Spread: 2.5%

EXIT PARAMETERS:
✓ Profit Target 1: $7.20 (50% profit)
   - Potential Profit: $240 per contract
✓ Profit Target 2: $9.60 (100% profit)
   - Potential Profit: $480 per contract
✓ Stop Loss: $2.40
   - Max Loss: $240 per contract

RISK/REWARD:
✓ Risk/Reward Ratio 1: 1.0:1
✓ Risk/Reward Ratio 2: 2.0:1
✓ Position Size: 2 contracts
✓ Total Risk: $480 (2.4% of $20,000 portfolio)

EXIT STRATEGY:
"EXIT at 50% profit or 50% loss, or 5 days before expiration"
```

---

## 🎓 How to Use These Parameters

### Step 1: Review Entry Parameters
1. Check if timing is favorable (ENTER NOW/SOON)
2. Verify entry price vs. current ask
3. Note the order type (MARKET or LIMIT)
4. Understand breakeven point

### Step 2: Set Your Orders
**Entering the Trade:**
- Place LIMIT order at recommended entry price
- Set expiration to DAY or GTC
- Monitor for fill

**Protecting the Trade:**
- Set stop loss order immediately after entry
- Use GTC (Good 'Til Canceled) order
- Consider trailing stop as trade moves in your favor

**Taking Profits:**
- Set LIMIT order at Profit Target 1
- Close 50% of position at Target 1
- Move stop to breakeven for remaining position
- Close remaining at Target 2 or use trailing stop

### Step 3: Follow Exit Strategy
Adhere to the AI-recommended exit strategy:
- Don't get greedy beyond targets
- Always honor stop losses
- Exit before expiration if appropriate

---

## 🚨 Important Risk Management Rules

### Always:
✅ **Enter at or below recommended entry price**  
✅ **Set stop loss immediately after entry**  
✅ **Take profits at targets (at least partial)**  
✅ **Exit before expiration if uncertain**  
✅ **Never risk more than planned**  
✅ **Keep position sizes within limits**  

### Never:
❌ **Chase the trade above max entry price**  
❌ **Ignore stop losses**  
❌ **Let winners turn into losers**  
❌ **Hold illiquid options to expiration**  
❌ **Average down on losing positions**  
❌ **Risk more than portfolio allows**  

---

## 📊 Interpreting the AI Signals

### High Confidence Recommendations
- Entry timing: Usually "ENTER NOW" or "ENTER SOON"
- Risk/Reward: Typically > 1.5:1
- Stop Loss: Tighter (50% loss max)
- Strategy: Can hold longer with discipline

### Medium Confidence Recommendations
- Entry timing: "ENTER SOON" or "WAIT"
- Risk/Reward: 1.0-1.5:1
- Stop Loss: Moderate (50-60% loss)
- Strategy: Take profits earlier, faster exits

### Position Sizing by Confidence
**High Confidence:**
- Can use recommended position size
- Risk up to 2-3% of portfolio

**Medium Confidence:**
- Consider 50% of recommended size
- Risk 1-2% of portfolio

**Low Confidence:**
- Skip the trade or paper trade only
- Don't risk real capital

---

## 🔄 Adjusting Parameters for Your Style

### Conservative Traders
- Use tighter stop losses (30-40%)
- Take profits at Target 1 (50% gain)
- Exit 5-7 days before expiration
- Reduce position sizes by 50%

### Moderate Traders
- Use recommended stop losses
- Take 50% profit at Target 1, hold rest for Target 2
- Follow exit strategy as stated
- Use recommended position sizes

### Aggressive Traders
- Wider stop losses (60-70%)
- Hold for Target 2 or Target 3
- Hold closer to expiration
- Can increase position size if experienced (not recommended for beginners)

---

## 💡 Pro Tips

1. **Use Profit Target 1 to Remove Risk**
   - Close 50% of position at Target 1
   - Move stop to breakeven on remaining
   - "Play with house money" for Target 2

2. **Trailing Stops**
   - After Target 1 hit, use trailing stops
   - Trail by 20-30% of gains
   - Locks in profits while allowing upside

3. **Time Decay Awareness**
   - Exit 5-7 days before expiration if not ITM
   - Theta accelerates in final week
   - Don't fight time decay

4. **Scale In/Out**
   - Enter 50% position at recommended entry
   - Add 50% if trade moves favorably
   - Exit in stages at multiple targets

5. **Paper Trade First**
   - Test these parameters without real money
   - Build confidence in the system
   - Understand how parameters work

---

## 📈 Tracking Your Trades

### Record for Each Trade:
- [ ] Entry date and price
- [ ] Position size (contracts)
- [ ] Target prices set
- [ ] Stop loss set
- [ ] Actual exit price
- [ ] Profit/loss amount
- [ ] Win/loss (did you hit target or stop?)
- [ ] Notes on what worked/didn't work

### Monthly Review:
- Calculate win rate
- Calculate average win vs. average loss
- Review risk/reward achieved vs. planned
- Identify patterns in successful trades
- Adjust strategy based on results

---

## ⚠️ Final Disclaimer

These parameters are **AI-generated recommendations** based on:
- Historical data and patterns
- Probability calculations
- Fair value analysis
- Risk management principles

**However:**
- Markets are unpredictable
- Past performance ≠ future results
- No system is 100% accurate
- Always do your own due diligence
- Only risk capital you can afford to lose
- Consult a financial advisor

---

## 🎯 Quick Reference Card

**Print this for your trading desk:**

```
═══════════════════════════════════════════════════
           AI TRADING PARAMETERS CHECKLIST
═══════════════════════════════════════════════════

BEFORE ENTRY:
□ Check timing recommendation
□ Verify entry price is favorable
□ Confirm position size fits portfolio
□ Understand breakeven price
□ Check liquidity (volume, OI, spread)

ENTERING TRADE:
□ Place LIMIT order at entry price
□ Set stop loss immediately
□ Record trade in journal
□ Set calendar reminder for expiration

MANAGING TRADE:
□ Check daily if ITM/OTM
□ Adjust stop to breakeven after 20% gain
□ Take 50% profit at Target 1
□ Trail stop on remaining position
□ Exit before expiration if OTM

EXIT SIGNALS:
□ Profit Target 1 hit → Close 50%
□ Profit Target 2 hit → Close remaining
□ Stop loss hit → Close immediately
□ 5 days to expiration → Close if OTM
□ Exit strategy triggered → Follow plan

POST-TRADE:
□ Record actual exit price
□ Calculate profit/loss
□ Note what worked/didn't work
□ Review for monthly summary
═══════════════════════════════════════════════════
```

---

**Happy Trading! Remember: Discipline and risk management are more important than any single trade.** 📊🎯

