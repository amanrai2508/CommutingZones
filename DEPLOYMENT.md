# 🚀 Deployment Guide

This guide will help you deploy the European Commuting Zones Explorer to GitHub and make it accessible to users worldwide.

## 📋 Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account
- [ ] Streamlit Cloud account (free)
- [ ] All project files ready

## 🎯 Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy your app for free.

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository:**
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit changes
   git commit -m "Initial commit: European Commuting Zones Explorer"
   
   # Create repository on GitHub (via web interface)
   # Then link your local repo
   git remote add origin https://github.com/yourusername/european-commuting-zones.git
   git branch -M main
   git push -u origin main
   ```

2. **Ensure these files are in your repository:**
   ```
   ├── app.py                          # Main Streamlit app
   ├── requirements.txt                # Python dependencies
   ├── README.md                       # Project documentation
   ├── .streamlit/
   │   └── config.toml                # Streamlit configuration
   └── .gitignore                     # Git ignore file
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Configure your app:**
   - **Repository**: Select your `european-commuting-zones` repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (optional)

5. **Click "Deploy"**

6. **Wait for deployment** (usually 2-5 minutes)

### Step 3: Configure R Dependencies

Since Streamlit Cloud doesn't support R by default, we need to handle this:

1. **Add a `packages.txt` file:**
   ```bash
   echo "r-base" > packages.txt
   ```

2. **Update your app to handle R dependency gracefully:**
   ```python
   # In app.py, add error handling for R
   try:
       # R processing code
   except Exception as e:
       st.error("R processing not available in cloud deployment. Using sample data.")
       # Fallback to sample data
   ```

3. **Redeploy** your app

### Step 4: Share Your App

Once deployed, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

Share this URL with users!

## 🎯 Option 2: GitHub Pages + Streamlit

For a more professional setup:

### Step 1: Create GitHub Pages

1. **Go to your repository settings**
2. **Scroll to "Pages" section**
3. **Select "Deploy from a branch"**
4. **Choose `main` branch and `/docs` folder**
5. **Save**

### Step 2: Create Landing Page

Create a `docs/index.html` file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>European Commuting Zones Explorer</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .button { background: #1f77b4; color: white; padding: 15px 30px; 
                 text-decoration: none; border-radius: 5px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗺️ European Commuting Zones Explorer</h1>
        <p>Explore commuting zones across Europe with interactive geographic maps.</p>
        <a href="https://your-app-name.streamlit.app" class="button">
            🚀 Launch App
        </a>
    </div>
</body>
</html>
```

## 🎯 Option 3: Docker Deployment

For advanced users who want containerized deployment:

### Step 1: Create Dockerfile

```dockerfile
# Use Python base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install R packages
RUN R -e "install.packages(c('remotes', 'dplyr', 'jsonlite', 'sf'), repos='https://cran.rstudio.com/')"
RUN R -e "remotes::install_github('facebookincubator/CommutingZones')"

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Deploy to Cloud Platforms

**Heroku:**
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

**Google Cloud Run:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/commuting-zones
gcloud run deploy --image gcr.io/your-project/commuting-zones --platform managed
```

## 🔧 Configuration Options

### Environment Variables

Create a `.env` file for local development:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Custom Domain

For Streamlit Cloud:
1. Go to your app settings
2. Add custom domain
3. Configure DNS records

## 📊 Monitoring and Analytics

### Streamlit Cloud Analytics

Streamlit Cloud provides:
- **Page views**
- **User sessions**
- **Performance metrics**
- **Error logs**

### Custom Analytics

Add Google Analytics to your app:

```python
# In app.py
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

## 🚨 Troubleshooting

### Common Issues

**1. R Dependencies Not Available**
- Use sample data fallback
- Pre-process data and include JSON files
- Use alternative Python libraries

**2. Memory Issues**
- Optimize data loading with caching
- Reduce data size for cloud deployment
- Use lazy loading for large datasets

**3. Performance Issues**
- Enable caching with `@st.cache_data`
- Optimize map rendering
- Use pagination for large tables

### Debug Mode

For local debugging:

```bash
# Run with debug info
streamlit run app.py --logger.level=debug

# Check logs
tail -f ~/.streamlit/logs/streamlit.log
```

## 📈 Scaling Considerations

### For High Traffic

1. **Upgrade to Streamlit Cloud Pro**
2. **Use CDN for static assets**
3. **Implement caching strategies**
4. **Optimize database queries**

### Performance Tips

- Cache expensive computations
- Use lazy loading for maps
- Optimize image sizes
- Minimize API calls

## 🔒 Security Considerations

1. **Environment Variables**: Never commit secrets
2. **Input Validation**: Validate user inputs
3. **Rate Limiting**: Implement if needed
4. **HTTPS**: Always use secure connections

## 📞 Support

If you encounter deployment issues:

1. **Check Streamlit Cloud logs**
2. **Review GitHub Actions** (if using)
3. **Test locally first**
4. **Consult Streamlit documentation**

## 🎉 Success!

Once deployed, your app will be accessible to users worldwide. Share the URL and start exploring European commuting zones!

---

**Need help?** Create an issue in the repository or contact the maintainers. 