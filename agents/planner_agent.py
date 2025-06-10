# Import the local LLM runner for generating task plans
from models.offline_model_runner import run_llm

# Import database functions for getting necessary data
from utils.db import (
    fetch_clients_for_followup,
    fetch_missing_documents,
    fetch_upcoming_appointments
)

def generate_daily_plan():
    """
    Gathers client data and generates a plan using an LLM (Language Model).

    Steps:
    1. Fetch follow-up clients, missing documents, and upcoming appointments from the database.
    2. Format that data into structured text for the LLM.
    3. Pass the prompt to the language model to get 3 actionable tasks.
    4. Return the parsed list of tasks.

    Returns:
        list of dict: Each dict represents a task with 'type' and 'content' keys.
    """

    # Step 1: Fetch follow-up clients, missing documents, and appointments
    followups = fetch_clients_for_followup()
    documents = fetch_missing_documents()
    appointments = fetch_upcoming_appointments()

    # Step 2: Format follow-up data as a readable list
    followup_text = "\n".join(
        f"{c['name']} ({c['status']}) - Last contacted: {c['last_contacted']}"
        for c in followups
    )

    # Format missing documents as a list of client names and document types
    docs_text = "\n".join(
        f"{d['name']} is missing {d['type']}"
        for d in documents
    )

    # Format upcoming appointments
    appt_text = "\n".join(
        f"{a['name']} – {a['title']} at {a['datetime']}"
        for a in appointments
    )

    # Step 3: Construct the full LLM prompt using the gathered data
    prompt = f"""
You are a digital assistant for a mortgage broker.

Your job is to recommend today's top 3 tasks based on:

=== Clients Needing Follow-Up ===
{followup_text or 'None'}

=== Missing Documents ===
{docs_text or 'None'}

=== Upcoming Appointments ===
{appt_text or 'None'}

Respond with exactly 3 tasks as actionable items.
"""

    # Step 4: Get response from the LLM model
    plan_text = run_llm(prompt)
    print("LLM Plan Response:", plan_text)  # Debug log

    # Step 5: Parse and return structured task data
    return parse_llm_tasks(plan_text)


def parse_llm_tasks(plan_text):
    """
    Parses the LLM's response into structured task dictionaries.

    Assumes each line contains a task and categorizes it based on keywords.

    Parameters:
        plan_text (str): Multiline string from the LLM listing tasks.

    Returns:
        list of dict: Each dict has a 'type' and 'content' field.
    """

    tasks = []

    # Process each line to detect task type and clean up text
    for line in plan_text.strip().split("\n"):

        # Determine task type based on keywords in the text
        if "email" in line.lower():
            task_type = "email"
        elif "call" in line.lower() or "meeting" in line.lower():
            task_type = "calendar"
        elif "update" in line.lower() or "log" in line.lower():
            task_type = "crm"
        else:
            task_type = "email"  # Default to email if unclear

        # Strip numbering/bullet formatting and surrounding whitespace
        cleaned_line = line.strip("-•123. ").strip()

        # Append parsed task to the task list
        tasks.append({
            "type": task_type,
            "content": cleaned_line
        })

    return tasks