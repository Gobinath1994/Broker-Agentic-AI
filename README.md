# 📊 Broker Task Automation Agent

An intelligent assistant for mortgage brokers to automate daily operational tasks such as:
- Following up with clients
- Sending reminder emails
- Scheduling appointments via Google Calendar
- Updating CRM notes

## 🔧 Features

- ✅ Auto-generates top 3 daily tasks using LLM planning
- 📧 Sends email reminders to clients for missing documents
- 🗓️ Creates Google Calendar events for client appointments
- 📝 Updates client notes in the CRM
- 📥 Document uploads and progress insights via a Streamlit dashboard
- 📤 Sends daily summary digest to selected clients

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/broker-task-agent.git
cd broker-task-agent
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Google APIs

- Set up a project at https://console.developers.google.com/
- Enable Gmail API and Google Calendar API
- Download `credentials.json` and place it in the `tools/` folder

### 4. Set Up MySQL

Create a database named `broker_ai` and run the schema:

```sql
CREATE DATABASE broker_ai;

-- Add your tables: clients, documents, appointments, completed_tasks, etc.
```

Update DB credentials inside `utils/db.py`.

### 5. Run the App

```bash
streamlit run ui/dashboard.py
```

## 📁 Folder Structure

```
├── agents/               # Email, calendar, CRM automation logic
├── models/               # LLM call wrapper (offline/local server)
├── tools/                # Gmail, calendar, CRM utilities
├── utils/                # DB connection, logger, helpers
├── ui/                   # Streamlit dashboard
├── uploads/              # Uploaded client documents
├── logs/                 # Execution logs
└── main.py               # Orchestrator script
```

## 📬 Daily Digest Example

Sends a daily summary like:

```
Here’s a summary of today’s broker activity:

- [Email] Followed up with client X
- [Calendar] Scheduled call for Y
- [CRM] Updated notes for Z
```

## 🧠 Powered by

- OpenAI-compatible local LLM (via HTTP call)
- Google APIs (Gmail, Calendar)
- MySQL
- Streamlit
# Broker-Agentic-AI
