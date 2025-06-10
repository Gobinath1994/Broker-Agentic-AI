"""
dashboard.py

Streamlit-based UI for the Broker Task Automation Agent.
Features:
- Manual agent execution.
- Filtering and displaying of daily tasks.
- Uploading documents.
- Viewing task history and metrics.
- Sending a daily digest email to selected clients.
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to sys.path to allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import core functionalities
from main import run_agent
from utils.db import fetch_task_log, log_task_completion, fetch_client_emails
from tools.gmail_tool import send_daily_digest

# Set Streamlit app page configuration
st.set_page_config(page_title="Broker Task Automation Agent", layout="wide")

# App title
st.title("📊 Broker Task Automation Agent")

# Initialize session state to store tasks (avoids rerunning agent unnecessarily)
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Button to manually trigger the agent and update session state with tasks
if st.button("🔁 Run Agent Now"):
    st.session_state.tasks = run_agent()
    st.success("Agent ran successfully!")

# Task filter UI section
st.subheader("📋 Today's Tasks")
filter_type = st.selectbox("Filter by task type", options=["All", "email", "calendar", "crm"])

# Display filtered tasks
for task in st.session_state.tasks:
    # Apply filter if selected
    if filter_type != "All" and task["type"] != filter_type:
        continue

    # Layout for task: checkbox and description
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        completed = st.checkbox("✔️", key=task["content"])
        if completed:
            # Log completed task to DB
            log_task_completion(task["type"], task["content"])
    with col2:
        st.markdown(f"**{task['type'].capitalize()}**: {task['content']}")

# Upload document section
st.subheader("📎 Upload Documents")
uploaded_file = st.file_uploader(
    "Attach client documents (PDF, docx, etc.)", type=["pdf", "docx"]
)
if uploaded_file:
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    # Save uploaded file
    with open(f"uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded!")

# Dashboard metrics section
st.subheader("📊 Dashboard Insights")
task_logs = fetch_task_log()

# Display number of tasks completed and pending uploads
col1, col2 = st.columns(2)
col1.metric("Tasks Completed", len(task_logs))
col2.metric("Pending Uploads", len(os.listdir("uploads")) if os.path.exists("uploads") else 0)

# Display task history log
st.subheader("📝 Task History")
for log in task_logs:
    st.markdown(
        f"✔️ **{log['type'].capitalize()}**: {log['content']} on {log.get('completed_at', 'Unknown')}"
    )

# Digest email sending section
st.subheader("📧 Send Daily Digest")

# Dropdown to select a client email
clients = fetch_client_emails()
selected_client = st.selectbox("Select client to notify", options=clients)

# Button to send daily digest email
if st.button("Send Digest Email"):
    tasks_for_digest = fetch_task_log()  # Use completed tasks for digest
    success = send_daily_digest(selected_client, tasks_for_digest)
    if success:
        st.success(f"Digest email sent to {selected_client}")
    else:
        st.error("Failed to send digest.")