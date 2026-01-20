# 🚀 Deployment Guide - Contract Management System

This guide will help you deploy your Contract Management System for **FREE** on Render.

## 📋 Prerequisites

1. A GitHub account (free)
2. A Google Gemini API key (free)
3. A Render account (free)

---

## 🔑 Step 1: Get Your Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (you'll need this later)

---

## 📦 Step 2: Push Your Code to GitHub

### Option A: Using GitHub Desktop (Easiest)
1. Download [GitHub Desktop](https://desktop.github.com/)
2. Click **File → Add Local Repository**
3. Select your `ManageContract` folder
4. Click **"Create a repository"** if prompted
5. Click **"Publish repository"**
6. Make it **Public** (required for free Render deployment)

### Option B: Using Command Line
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Contract Management System"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 3: Deploy on Render

### Create Your Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account (easiest option)

### Deploy Your App
1. **Click "New +"** → **"Web Service"**

2. **Connect Your Repository**
   - Find your `ManageContract` repository
   - Click **"Connect"**

3. **Configure Your Service**
   - **Name**: `contract-management-system` (or any name you like)
   - **Region**: Choose the closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

4. **Set Environment Variables**
   Click **"Advanced"** → **"Add Environment Variable"**
   
   Add these variables:
   - **Key**: `GEMINI_API_KEY`  
     **Value**: Your Google Gemini API key from Step 1
   
   - **Key**: `PYTHON_VERSION`  
     **Value**: `3.11.0`
   
   - **Key**: `DATABASE_URL`  
     **Value**: `sqlite+aiosqlite:///./contracts.db`

5. **Choose Free Plan**
   - Select **"Free"** plan (750 hours/month free)

6. **Click "Create Web Service"**

### Wait for Deployment
- Render will build and deploy your app (takes 5-10 minutes)
- You'll see build logs in real-time
- When done, you'll get a URL like: `https://contract-management-system.onrender.com`

---

## ⚠️ Important Notes

### About Free Tier Limitations

1. **Sleep After Inactivity**
   - Free apps sleep after 15 minutes of no activity
   - First request after sleep takes 30-60 seconds to wake up
   - Solution: Use [UptimeRobot](https://uptimerobot.com/) to ping your app every 14 minutes

2. **Database Resets**
   - SQLite database resets when app restarts
   - For persistent data, upgrade to PostgreSQL (still free on Render)
   - [Guide to add PostgreSQL](https://render.com/docs/databases)

3. **Build Time**
   - Some dependencies (chromadb) take time to build
   - Be patient during first deployment

---

## 🎉 Step 4: Test Your Deployment

1. Visit your Render URL
2. You should see your Contract Management System
3. Try uploading a contract
4. Ask questions using the AI assistant

---

## 🐛 Troubleshooting

### Build Fails
- Check if all files are committed to GitHub
- Verify `requirements.txt` is present
- Check Render build logs for specific errors

### App Crashes on Start
- Verify `GEMINI_API_KEY` is set correctly in environment variables
- Check application logs in Render dashboard

### ChromaDB Issues
- If chromadb fails to install, it might be due to Python version
- Try Python 3.11.0 (already set in runtime.txt)

---

## 🔄 Alternative Free Deployment Options

### Railway (Alternative #1)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Add environment variables
6. Deploy! ($5 free credit/month)

### Fly.io (Alternative #2)
1. Install Fly CLI: `npm install -g flyctl`
2. Run: `fly launch`
3. Follow prompts
4. Add environment variables: `fly secrets set GEMINI_API_KEY=your_key`
5. Deploy: `fly deploy`

---

## 📧 Sharing with Your Friend

Once deployed, simply share your Render URL:
```
https://your-app-name.onrender.com
```

Your friend can:
- Access it from any browser
- Upload contracts
- Get AI-powered insights
- View early warnings and alerts

---

## 🎓 Pro Tips

1. **Custom Domain** (Optional)
   - Buy a domain from Namecheap/GoDaddy ($1-10/year)
   - Add custom domain in Render dashboard
   - Free SSL included!

2. **Keep It Awake**
   - Use [UptimeRobot](https://uptimerobot.com/) (free)
   - Ping your app every 14 minutes
   - Prevents sleep on free tier

3. **Monitor Usage**
   - Check Render dashboard for usage stats
   - Free tier: 750 hours/month = 31.25 days
   - More than enough for personal use!

---

## ✅ Checklist

- [ ] Got Google Gemini API key
- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Created Render account
- [ ] Deployed web service
- [ ] Added environment variables
- [ ] Tested the deployed app
- [ ] Shared URL with friend

---

## 🆘 Need Help?

If you encounter issues:
1. Check Render logs for errors
2. Verify all environment variables are set
3. Make sure GitHub repository is public
4. Confirm Google Gemini API key is valid

---

## 🎊 Congratulations!

You've successfully deployed your Contract Management System for FREE! 
Your friend can now access it from anywhere in the world.

**Estimated Time**: 15-20 minutes  
**Cost**: $0 (FREE)  
**Difficulty**: Easy ⭐⭐☆☆☆
