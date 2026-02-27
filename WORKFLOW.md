# Bot Architecture & Workflow

This document explains the technical flow of the Slack NL→SQL bot, from the initial Slack command to the final database result.

### High-Level Process Flow

| Step | Component | Action |
| :--- | :--- | :--- |
| 1 | **Slack** | User triggers `/ask-data` with a natural language query. |
| 2 | **Flask** | Receives the POST payload from Slack and validates the signature. |
| 3 | **LangChain** | Parses the input, applies the schema context, and generates a `SELECT` statement. |
| 4 | **Postgres** | Executes the generated SQL query securely. |
| 5 | **Response** | Flask formats the output rows into a Slack-friendly table and sends it back. |

### Technical Stack
* **NLP:** LangChain (LLM-based SQL generation)
* **Web Server:** Flask (Slack events endpoint)
* **Database:** PostgreSQL (Containerized via Docker)
* **Integration:** Slack API (Slash commands & Webhooks)

### Database Schema
The bot expects a `sales_daily` table for its primary analytics functions:

```sql
CREATE TABLE IF NOT EXISTS public.sales_daily (
    date date NOT NULL,
    region text NOT NULL,
    category text NOT NULL,
    revenue numeric(12,2) NOT NULL,
    orders integer NOT NULL,
    PRIMARY KEY (date, region, category)
);
