# Import the function to send emails using Gmail API
from tools.gmail_tool import send_email

# Import helper to fetch client email by name and to log completed tasks into the DB
from utils.db import get_client_email_by_name, log_task_completion


def extract_client_name(content):
    """
    Extracts the client's name from the task content string using a regular expression.

    Parameters:
        content (str): The content string, expected to contain something like
                       'Follow up with <Name> to request ...'

    Returns:
        str: Extracted client name, or "Client" if no match is found.
    """
    import re  # Import regex module for pattern matching
    match = re.search(r"with ([A-Za-z ]+?) to request", content)
    return match.group(1) if match else "Client"


def handle_emails(task):
    """
    Handles an email task by:
    1. Extracting the client name from the task content.
    2. Retrieving the associated client email from the database.
    3. Constructing and sending a reminder email.
    4. Logging the completion of the email task.

    Parameters:
        task (dict): Dictionary with at least a "content" field describing the task.
                     Example: { "type": "email", "content": "Follow up with John Doe to request ..." }

    Returns:
        None
    """

    # Extract the client's name from the task content string
    name = extract_client_name(task["content"])

    # Fetch the client's email address using the extracted name
    client_email = get_client_email_by_name(name)

    # Define the email body using a formatted multi-line string
    body = f"""
Hi {name},

This is a reminder to send the following documents needed for your pre-approval:

- ID proof
- Bank statement
- Payslip

Please reply to this email or upload them via the Broker Portal.

Regards,  
Broker AI Assistant
    """

    # Send the constructed email to the retrieved client email address
    send_email(client_email, "Follow-up Required for Pre-Approval", body)

    # Create a summary to log the completion of this email task
    summary = f"Sent follow-up email to {name} for missing documents."

    # Log the task as completed in the database with type 'email'
    log_task_completion("email", summary)