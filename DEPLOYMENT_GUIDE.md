# 🌐 Web Deployment Guide

## Deploy Your AI Options Strategy Analyzer Online

This guide covers multiple deployment options to make your Streamlit app publicly accessible.

---

## 🚀 Option 1: Streamlit Cloud (Recommended - FREE!)

**Streamlit Cloud** is the easiest and FREE way to deploy Streamlit apps.

### Prerequisites
- GitHub account
- This code in a GitHub repository

### Step-by-Step Deployment

#### 1. **Prepare Your Repository**

Create a GitHub repository and push your code:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Options Strategy Analyzer"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

#### 2. **Deploy to Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account
4. Select your repository
5. Set the following:
   - **Main file path**: `app.py`
   - **Branch**: `main` (or `master`)
   - **Python version**: 3.11
6. Click **"Deploy"**

#### 3. **Wait for Deployment**
- Initial deployment takes 3-5 minutes
- You'll get a public URL like: `https://your-app-name.streamlit.app`

#### 4. **Share Your App!**
Your app is now live and accessible to anyone with the URL!

### Custom Domain (Optional)

In Streamlit Cloud settings:
1. Go to **Settings** → **General**
2. Add your custom domain
3. Update DNS settings as instructed

---

## 🔧 Option 2: Heroku Deployment

**Heroku** is another popular platform with a free tier.

### Prerequisites
- Heroku account ([signup here](https://signup.heroku.com/))
- Heroku CLI installed

### Files Required

Create these additional files:

**1. `Procfile`** (in root directory):
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**2. `setup.sh`** (in root directory):
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# Open your app
heroku open
```

Your app will be at: `https://your-app-name.herokuapp.com`

---

## ☁️ Option 3: Railway Deployment

**Railway** offers a modern deployment experience with generous free tier.

### Steps

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Choose **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Streamlit
6. Click **"Deploy"**

Railway will automatically:
- Detect `requirements.txt`
- Install dependencies
- Deploy your app

Your app will be at: `https://your-app-name.up.railway.app`

---

## 🐳 Option 4: Docker Deployment

Deploy anywhere that supports Docker containers.

### Create Dockerfile

**`Dockerfile`**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build Docker image
docker build -t ai-options-strategy .

# Run container
docker run -p 8501:8501 ai-options-strategy
```

### Deploy to Cloud Platforms

**Google Cloud Run:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-options-strategy
gcloud run deploy --image gcr.io/PROJECT_ID/ai-options-strategy --platform managed
```

**AWS ECS, Azure Container Instances:** Similar process with their respective CLIs.

---

## 🌟 Option 5: Hugging Face Spaces

**Hugging Face Spaces** is free for public apps and ML-friendly.

### Steps

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose **Streamlit** as the SDK
4. Upload your files or connect GitHub
5. Space automatically deploys

Your app will be at: `https://huggingface.co/spaces/USERNAME/SPACE_NAME`

---

## 📊 Performance Optimization for Web Deployment

### 1. **Add Caching**

Already implemented in `app.py`, but you can add more:

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_options_data(ticker, expiration):
    # Your data fetching logic
    pass

@st.cache_resource
def load_ml_model():
    # Load expensive models once
    pass
```

### 2. **Reduce Default Simulations**

For faster initial load, modify defaults in `app.py`:

```python
num_simulations = st.sidebar.number_input(
    "Monte Carlo Trials",
    min_value=1000,
    max_value=100000,
    value=5000,  # Changed from 10000 for faster web performance
    step=1000
)
```

### 3. **Add Loading Progress**

Shows users the app is working:

```python
with st.spinner("Loading data..."):
    progress_bar = st.progress(0)
    # Update progress as operations complete
    progress_bar.progress(50)
```

### 4. **Memory Management**

For cloud deployments with memory limits:

```python
# Limit data retention
if 'historical_data' in st.session_state:
    if len(st.session_state.historical_data) > 1000:
        st.session_state.historical_data = st.session_state.historical_data.tail(1000)
```

---

## 🔒 Security Considerations

### 1. **Environment Variables**

Never hardcode sensitive data. Use Streamlit secrets:

**In `.streamlit/secrets.toml`** (local):
```toml
[api_keys]
my_api_key = "secret_key_here"
```

**In code**:
```python
import streamlit as st
api_key = st.secrets["api_keys"]["my_api_key"]
```

**In Streamlit Cloud**:
- Add secrets in the app settings dashboard

### 2. **Rate Limiting**

Protect your app from abuse:

```python
import time
from functools import wraps

def rate_limit(seconds=60):
    def decorator(func):
        last_called = {}
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            user_id = st.session_state.get('user_id', 'anonymous')
            if user_id in last_called:
                if now - last_called[user_id] < seconds:
                    st.warning(f"Please wait {seconds} seconds between requests")
                    return None
            last_called[user_id] = now
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(seconds=60)
def fetch_data(ticker):
    # Your data fetching logic
    pass
```

### 3. **Input Validation**

Already implemented, but ensure all user inputs are validated:

```python
ticker = st.text_input("Ticker").upper()
if ticker and not ticker.isalnum():
    st.error("Invalid ticker symbol")
    st.stop()
```

---

## 📈 Monitoring and Analytics

### 1. **Google Analytics** (Optional)

Add to your app for usage tracking:

```python
# In app.py, add to the head section
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

### 2. **Error Tracking**

Add Sentry for error monitoring:

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")
```

---

## 🎨 Custom Branding

### 1. **Custom Domain**

Most platforms support custom domains:
- **Streamlit Cloud**: Settings → General → Custom domain
- **Heroku**: `heroku domains:add www.yourdomain.com`
- **Railway**: Settings → Domains

### 2. **Favicon**

Add in `.streamlit/config.toml`:

```toml
[browser]
favicon = "📈"
```

Or use a custom image:

```python
st.set_page_config(
    page_icon="path/to/favicon.png"
)
```

### 3. **Custom Styling**

Already have custom CSS in `app.py`, but you can add more:

```python
st.markdown("""
<style>
    /* Your custom styles */
    .stApp {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)
```

---

## 💰 Cost Considerations

### Free Tiers:

| Platform | Free Tier | Limitations |
|----------|-----------|-------------|
| **Streamlit Cloud** | ✅ Unlimited public apps | 1GB RAM, shared CPU |
| **Heroku** | ✅ 550 hours/month | Sleeps after 30min inactivity |
| **Railway** | ✅ $5 credit/month | Good for small apps |
| **Hugging Face** | ✅ Unlimited | Public only, 16GB storage |
| **Google Cloud Run** | ✅ 2M requests/month | Pay per use after |

### Recommended for This App:
**Streamlit Cloud** - Best for Streamlit apps, no sleep time, easy deployment.

---

## 🐛 Troubleshooting Deployment Issues

### Issue 1: "ModuleNotFoundError"
**Solution**: Ensure `requirements.txt` is complete and properly formatted.

### Issue 2: App Crashes on Startup
**Solution**: Check logs:
```bash
# Streamlit Cloud: View logs in dashboard
# Heroku: heroku logs --tail
# Railway: View logs in dashboard
```

### Issue 3: Memory Errors
**Solution**: Reduce default Monte Carlo simulations, add caching, or upgrade plan.

### Issue 4: Slow Performance
**Solution**: 
- Add `@st.cache_data` decorators
- Reduce default parameters
- Use faster algorithms
- Consider CDN for static assets

### Issue 5: yfinance API Errors
**Solution**: 
- Add retry logic
- Implement fallback data sources
- Show user-friendly error messages

---

## 📱 Mobile Optimization

Streamlit is responsive, but you can enhance mobile experience:

```python
# Detect mobile
import streamlit.components.v1 as components

components.html("""
<script>
if (window.innerWidth < 768) {
    // Mobile-specific adjustments
    document.body.style.fontSize = '14px';
}
</script>
""")

# Adjust columns for mobile
if st.session_state.get('is_mobile', False):
    col1 = st.container()
    col2 = st.container()
else:
    col1, col2 = st.columns(2)
```

---

## 🔗 Sharing Your Deployed App

### Create a Landing Page

Add to README or create separate page:

```markdown
# 🌐 Live Demo

Try the live app: [AI Options Strategy Analyzer](https://your-app.streamlit.app)

## Features
- Real-time market data
- AI-powered recommendations
- Complete trading plans
- Risk management tools

## How to Use
1. Enter ticker symbol
2. Select expiration date
3. Review AI recommendations
4. Get complete entry/exit parameters
```

### Social Media Share Card

Add meta tags (for sharing on social media):

```python
st.markdown("""
<meta property="og:title" content="AI Options Strategy Analyzer">
<meta property="og:description" content="Get AI-powered options trading recommendations with complete trading plans">
<meta property="og:image" content="https://your-app.streamlit.app/preview.png">
<meta property="og:url" content="https://your-app.streamlit.app">
<meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)
```

---

## 🎓 Post-Deployment Checklist

After deploying, verify:

- [ ] App loads without errors
- [ ] Data fetching works correctly
- [ ] All features function properly
- [ ] Mobile view looks good
- [ ] Error messages are user-friendly
- [ ] Performance is acceptable
- [ ] Links and documentation are accessible
- [ ] Analytics/monitoring is set up
- [ ] Backup/version control is in place
- [ ] Support contact info is visible

---

## 🚀 Quick Start Deployment (Streamlit Cloud)

**5-Minute Deployment:**

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy AI Options Strategy"
git remote add origin YOUR_GITHUB_URL
git push -u origin main

# 2. Go to share.streamlit.io
# 3. Click "New app"
# 4. Select your repo and app.py
# 5. Click "Deploy"
# 6. Wait 3-5 minutes
# 7. Share your public URL!
```

**That's it! Your app is now live! 🎉**

---

## 📞 Support

If you encounter issues:
1. Check [Streamlit Community Forum](https://discuss.streamlit.io)
2. Review [Streamlit Documentation](https://docs.streamlit.io)
3. Check platform-specific docs (Heroku, Railway, etc.)

---

## 🎉 Congratulations!

Your AI Options Strategy Analyzer is now accessible worldwide! 🌍

**Share your URL with:**
- Friends and colleagues
- Trading communities
- Social media
- Your portfolio/resume

**Remember**: This is an educational tool. Always include appropriate disclaimers about financial advice.

---

*Happy Deploying! 🚀📈*

