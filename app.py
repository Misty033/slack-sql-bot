import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import psycopg2
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Slack app with token and signing secret
slack_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)
handler = SlackRequestHandler(slack_app)

# Flask app
flask_app = Flask(__name__)

# DB connection
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        dbname=os.getenv("DB_NAME", "slack_bot"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )

# LangChain + Gemini prompt
PROMPT = """
You are a PostgreSQL expert.

Table: sales_daily
Columns: date, region, category, revenue, orders, created_at

Return only ONE valid SQL SELECT query. Do not add markdown formatting or explanations.

Question: {question}
SQL:
"""

llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-2.5-flash",
    temperature=0.2,
    max_retries=4
)

def question_to_sql(question):
    prompt = PromptTemplate(
        input_variables=["question"],
        template=PROMPT
    )
    chain = prompt | llm
    response = chain.invoke({"question": question})
    return response.content.strip()

def execute_query(sql):
    """Execute SQL and return rows"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchmany(5)
    cur.close()
    conn.close()
    return rows

def format_results(sql, rows):
    """Format query results for display"""
    result = f"```\nSQL:\n{sql}\n\nResult:\n"
    if rows:
        for row in rows:
            result += str(row) + "\n"
    else:
        result += "(No results)\n"
    result += "```"
    return result

# Slack slash command handler
@slack_app.command("/ask-data")
def handle_ask(ack, respond, command):
    ack()
    question = command["text"]
    try:
        sql = question_to_sql(question)
        rows = execute_query(sql)
        result = format_results(sql, rows)
        respond(result)
    except Exception as e:
        respond(f"```Error:\n{str(e)}```")

# Slack events endpoint - Slack Bolt handles all request types
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Local test route (for development/testing without Slack)
@flask_app.route("/ask-data", methods=["POST"])
def ask_data():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        sql = question_to_sql(question)
        rows = execute_query(sql)
        result = f"SQL:\n{sql}\n\nResult:\n"
        for row in rows:
            result += str(row) + "\n"
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    flask_app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )