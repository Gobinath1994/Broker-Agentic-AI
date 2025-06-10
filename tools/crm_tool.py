# tools/crm_tool.py

"""
This module provides functions to interact with the CRM-related 
client data stored in the database, specifically for updating notes.
"""

from utils.db import run_query  # Import the utility function to execute DB queries

def update_client_notes(client_email, notes):
    """
    Updates the notes field for a specific client in the database.

    Args:
        client_email (str): The email address of the client.
        notes (str): The note content to be updated in the client's record.

    Returns:
        None
    """

    # SQL query to update the 'notes' column in the 'clients' table where the email matches
    query = """
        UPDATE clients
        SET notes = %s
        WHERE email = %s
    """

    # Execute the query with the provided parameters (note content and client email)
    run_query(query, (notes, client_email))

    # Confirm the update in the console/log
    print(f"✅ Updated CRM notes for {client_email}")