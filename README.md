# Slack NL→SQL Bot

A minimal Slack integration that allows users to query a PostgreSQL database using natural language. It uses LangChain and llm to translate user questions into SQL, executes them, and returns formatted results directly in Slack.

### Demo   

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

[Demo Video](Demo/demo_video.mp4)

### Features
* **Natural Language:** Query your database without writing SQL.
* **Simple Setup:** Uses a single slash command (`/ask-data`).
* **Fast:** Direct execution on Postgres with instant replies.

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
   SLACK_SIGNING_SECRET=your-signing-secret
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
