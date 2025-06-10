"""
Database Utility Functions for Broker AI System

This module provides database interaction functions using `mysql.connector`.
It allows querying and updating client, document, task, and appointment data
used by the automation agent.

Author: [Your Name]
Date: [YYYY-MM-DD]
"""

import mysql.connector  # Import MySQL connector to interact with MySQL DB

def run_query(query, params=None):
    """
    Execute a SQL query and return the results as a list of dictionaries.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to be safely substituted into the query.

    Returns:
        list: List of result rows as dictionaries.
    """
    conn = mysql.connector.connect(
        host='127.0.0.1',       # Localhost database connection
        user='root',            # Your DB username
        password='Gopinath',    # Your DB password
        database='broker_ai'    # Target database
    )
    cursor = conn.cursor(dictionary=True)  # Use dict cursor to return rows as dicts
    cursor.execute(query, params or ())    # Execute with parameters (or empty tuple)
    result = cursor.fetchall()             # Fetch all rows
    conn.commit()                          # Commit (required for INSERT/UPDATE/DELETE)
    cursor.close()
    conn.close()
    return result                          # Return result as list of dictionaries


def fetch_clients_for_followup():
    """
    Fetch clients who are not marked as 'Closed' or 'Completed',
    ordered by how long it's been since last contacted.

    Returns:
        list: Clients needing follow-up.
    """
    query = """
    SELECT name, email, status, last_contacted
    FROM clients
    WHERE status NOT IN ('Closed', 'Completed')
    ORDER BY last_contacted ASC
    """
    return run_query(query)


def fetch_missing_documents():
    """
    Fetch list of missing documents per client.

    Returns:
        list: Each row includes client's name and missing document type.
    """
    query = """
        SELECT c.name, d.type
        FROM documents d
        JOIN clients c ON d.client_id = c.id
        WHERE d.received = FALSE
    """
    return run_query(query)


def fetch_upcoming_appointments():
    """
    Fetch client appointments scheduled within the next 3 days.

    Returns:
        list: Appointments including ID, title, datetime, and client name.
    """
    query = """
        SELECT a.id, a.title, a.datetime, c.name
        FROM appointments a
        JOIN clients c ON a.client_id = c.id
        WHERE a.datetime BETWEEN NOW() AND NOW() + INTERVAL 3 DAY
    """
    return run_query(query)


def log_task_completion(task_type, content, notes="", status="completed"):
    """
    Log a task that has been completed into the completed_tasks table.

    Args:
        task_type (str): Type of task (e.g. 'email', 'calendar', 'crm').
        content (str): Summary or details of the task.
        notes (str): Optional additional notes.
        status (str): Task status, defaults to 'completed'.
    """
    query = """
    INSERT INTO completed_tasks (type, content, notes, status)
    VALUES (%s, %s, %s, %s)
    """
    return run_query(query, (task_type, content, notes, status))


def fetch_task_log():
    """
    Fetch the task completion log.

    Returns:
        list: Completed tasks with type, content, and completion timestamp.
    """
    query = "SELECT type, content, completed_at FROM completed_tasks ORDER BY completed_at DESC"
    return run_query(query)


def fetch_client_emails():
    """
    Fetch all distinct client emails that are not NULL.

    Returns:
        list: List of client email addresses.
    """
    query = "SELECT DISTINCT email FROM clients WHERE email IS NOT NULL"
    rows = run_query(query)
    return [r["email"] for r in rows]


def get_client_email_by_name(name):
    """
    Get a client email by their name.

    Args:
        name (str): Full name of the client.

    Returns:
        str: Email address if found, else a default placeholder email.
    """
    query = "SELECT email FROM clients WHERE name = %s"
    result = run_query(query, (name,))
    return result[0]["email"] if result else "client@example.com"