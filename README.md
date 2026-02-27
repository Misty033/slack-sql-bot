# Slack NL→SQL Bot

A minimal Slack integration that allows users to query a PostgreSQL database using natural language. It uses LangChain and llm to translate user questions into SQL, executes them, and returns formatted results directly in Slack.

<p align="center">
  <figure>
    <img src="workflow.png" alt="Workflow of the pipeline" width:"300">
    <figcaption>Figure 1: Workflow of the pipeline </figcaption>
  </figure>
</p>

## Try!!
The Slack NL→SQL bot is deployed on Railway and can be tested in any Slack workspace.

### Step 1: Install the app
- Click this link to install the bot in your Slack workspace:  
[Install Slack NL→SQL Bot](https://app.slack.com/app-settings/T0AHA2G02RG/A0AHDMGK7FW/oauth)

### Step 2: Use the slash command
- In Slack, type:
  **/ask-data show revenue by region for 2025-09-01**
- The bot will respond using the Railway deployment and database.
> Note: Only workspaces where the app is installed can use the slash command.


### Optionally [for workspace members]:
You can test the Slack NL→SQL bot using the deployed Railway URL:
[Slack NL→SQL Bot](https://slack-sql-bot-production.up.railway.app/slack/events)
> Note: You need access to the Slack workspace where the bot is installed.

### Demo   
[Demo Video](Demo/demo_video.mp4)

In Slack, type:
`/ask-data show revenue by region for 2025-09-01`
**Bot response:**
| Region | Revenue |
| :--- | :--- |
| North | 125000.50 |
| South | 54000.00 |
| West | 40500.00 |

<p align="center">
  <figure>
    <img src="Demo/demo_img1.png" alt="Bot response of /ask-data show revenue by region for 2025-09-01" width="700">
    <figcaption>Figure 1: Bot response screenshot</figcaption>
  </figure>
</p>

### Features
- Slack slash command /ask-data "<question>"
- Natural Language → SQL conversion using LangChain
- Direct SQL execution on Postgres
- Compact and formatted replies in Slack
- Minimal error handling (SQL errors returned in code blocks)

### Tech Stack
- Python 
- Flask – web server for Slack events
- LangChain – NLP to SQL conversion
- PostgreSQL – database, hosted on Docker for local dev or Railway in production
- Slack API – slash commands and responses
- Docker – containerized Postgres for local development
- Railway.app – production DB hosting

### Tools & Notes:
| Step      | Tool             | Role                             |
| --------- | ---------------- | -------------------------------- |
| NL→SQL    | LangChain        | Generate SQL from user query     |
| Webserver | Flask            | Receives Slack commands          |
| DB        | Postgres         | Stores data and executes queries |
| Slack     | Slack API        | Slash command & bot response     |
| Dev DB    | Docker Postgres  | Isolated local testing           |
| Prod DB   | Railway Postgres | Cloud database for production    |


### Database Setup:
```bash
CREATE DATABASE analytics;
\c analytics

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

### Docker Setup:
Set docker-compose.yml
* Start container: docker compose up -d
* Connect: psql -h localhost -U postgres -d slack_bot

### Installation
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/your-username/slack-nl-sql-bot.git](https://github.com/your-username/slack-nl-sql-bot.git)
   cd slack-nl-sql-bot
2. **Set up environment:**
   ```bash
   python -m venv bot_venv
   .\bot_venv\Scripts\activate (#windows)
   source bot_venv/bin/activate (#linux/mac)
   
   pip install -r requirements.txt
   ```
3. **Configure:**
   Create a .env file with your credentials:
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-token
   SLACK_SIGNING_SECRET=your-signing-secre
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=slack_bot
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```
4. **Run:**
   ```bash
   docker compose up -d
   python app.py

### Error Handling:
- If LangChain generates invalid SQL, the database will raise an error.
- The Flask app catches these exceptions and displays them inside a Markdown   code block in Slack to help the user debug their query.
- Bot does not attempt validation, keeping it minimal.

### Future Enhancements:
- Add a button to export CSV for the last query.
- Add a small chart image for a date range query.
- Add caching to speed up repeated questions.
- In a follow-up phase, add safeguards and validation.

### MIT License
Copyright (c) 2026 Misty Roy
