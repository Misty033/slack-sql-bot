# Slack SQL Bot - Deployment Guide

## Quick Summary
A minimal Slack app that converts natural language questions to SQL, executes them on PostgreSQL, and returns results. Built with LangChain + Google Gemini API.

**Tech Stack:**
- Flask (Web server)
- LangChain + Google Gemini (NL→SQL)
- PostgreSQL (Database)
- Slack Bolt (Slack integration)
- Railway.app (Deployment)

---

## 🚀 Deploy to Railway.app (5 minutes)

### Prerequisites
- GitHub account (free)
- Railway account (free, no credit card needed initially)
- Google Gemini API key (free)
- Slack app credentials

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click **"Start New Project"** → **"Deploy from GitHub"**
3. Authorize Railway to access your GitHub

### Step 2: Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/slack_sql_bot.git
git push -u origin main
```

### Step 3: Deploy from Railway
1. In Railway dashboard: **New Project** → **Deploy from GitHub**
2. Select `slack_sql_bot` repo
3. Railway auto-detects Flask and deploys
4. Wait 2-3 minutes for deployment
5. Go to **Deployments** tab → copy your **URL**
   - Format: `https://slack-sql-bot-production.up.railway.app`

### Step 4: Add Environment Variables
In Railway dashboard, go to **Variables** tab and add:
```
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
GEMINI_API_KEY=your-gemini-api-key-here
DB_HOST=your-postgres-host
DB_PORT=5432
DB_NAME=slack_bot
DB_USER=postgres
DB_PASSWORD=your-db-password
```

### Step 5: Configure Slack App
1. Go to your Slack app → **Slash Commands**
2. Edit `/ask-data` command
3. Update **Request URL** to: `https://your-railway-url/slack/events`
4. Save and reinstall app to workspace

### Step 6: Test
In any Slack channel:
```
/ask-data show revenue by region for 2025-09-01
```

**Your persistent URL is ready to share!** 🎉

---

## 📋 Database Setup (One-Time)

If using your own PostgreSQL, create the table:

```sql
CREATE DATABASE slack_bot;
\c slack_bot

CREATE TABLE IF NOT EXISTS public.sales_daily (
    date date NOT NULL,
    region text NOT NULL,
    category text NOT NULL,
    revenue numeric(12,2) NOT NULL,
    orders integer NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (date, region, category)
);

INSERT INTO public.sales_daily (date, region, category, revenue, orders) VALUES
('2025-09-01','North','Electronics',125000.50,310),
('2025-09-01','South','Grocery',54000.00,820),
('2025-09-01','West','Fashion',40500.00,190),
('2025-09-02','North','Electronics',132500.00,332),
('2025-09-02','West','Fashion',45500.00,210),
('2025-09-02','East','Grocery',62000.00,870);
```

---

## 🔑 Get API Keys

### Google Gemini API (Free)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Get API key"**
3. Create new API key
4. Copy and paste into `.env`

### Slack Bot Token & Signing Secret
1. Go to [Slack API Dashboard](https://api.slack.com/apps)
2. Select your app
3. **OAuth & Permissions** → copy **Bot User OAuth Token** (xoxb-...)
4. **Basic Information** → copy **Signing Secret**

---

## 🛠️ Troubleshooting

### Issue: "dispatch_failed" error in Slack
**Solution:** Check that `SLACK_SIGNING_SECRET` is correct in Railway variables

### Issue: "'str' object has no attribute 'content'"
**Solution:** Already fixed in code. Ensure you're running latest `app.py`

### Issue: Database connection error
**Solution:** Verify `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` in Railway variables

### Issue: SQL execution errors
**Solution:** Check that `sales_daily` table exists with correct schema

---

## 📝 Project Files

```
slack_sql_bot/
├── app.py                 # Main Flask + Slack Bolt app
├── .env                   # Environment variables (don't commit)
├── requirements.txt       # Python dependencies
└── .gitignore            # Exclude .env and venv
```

---

## 📌 Key Features

✅ Slash command `/ask-data "your question"`  
✅ NL→SQL conversion using Google Gemini  
✅ Direct PostgreSQL execution  
✅ Formatted results in Slack  
✅ Error handling with code blocks  
✅ Fetches up to 5 rows per query  

---

## 🎯 Example Queries

Try these in Slack:

```
/ask-data show revenue by region for 2025-09-01
/ask-data what is total revenue for North region
/ask-data list all categories
/ask-data show orders by category
```

---

## 📚 Architecture

1. User sends `/ask-data "question"` in Slack
2. Slack sends request to your Railway app
3. App extracts question and sends to Google Gemini LLM
4. Gemini generates valid SQL query
5. App executes SQL on PostgreSQL
6. Results formatted and sent back to Slack
7. User gets formatted reply with query and data

---

## 🆓 Free Stack

All components are **completely free**:
- ✅ Flask - Open source
- ✅ LangChain - Open source
- ✅ PostgreSQL - Open source
- ✅ Slack Bolt - Open source
- ✅ Google Gemini API - Free tier (60 requests/min)
- ✅ Railway.app - Free tier
- ✅ GitHub - Free

**Total Cost: $0/month** 🎉

---

## 💡 Next Steps

1. Deploy to Railway
2. Share the live URL with your team
3. Add more SQL tables for different datasets
4. Extend with more LLM features
5. Add query validation/guardrails if needed

**Questions?** Check the troubleshooting section above.
