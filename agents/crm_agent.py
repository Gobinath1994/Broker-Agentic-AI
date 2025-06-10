# Import the helper function to update client notes in the CRM database or system
from tools.crm_tool import update_client_notes

# Define a function to process and handle CRM update tasks
def update_crm(task):
    """
    Updates client notes in the CRM system based on task content.

    Expected task format:
        {
            "type": "crm",
            "content": "Update notes for client@example.com: Note to be saved"
        }

    The function parses the `content` field to extract the client's email and the note,
    then calls the `update_client_notes` function to save this information in the CRM system.

    Parameters:
        task (dict): A dictionary containing at least a 'content' key with formatted string.

    Returns:
        None. Outputs an error message if the content format is invalid.
    """

    # Get the value of the "content" field from the task dictionary
    # If it doesn't exist, default to an empty string to avoid crashing
    content = task.get("content", "")

    # Check if the content contains a colon, which separates the email header from the notes
    if ":" in content:
        # Split the content into two parts: 'header' (contains email info) and 'notes' (actual note text)
        header, notes = content.split(":", 1)

        # Extract the email part from the header by splitting on the word 'for' and taking the last portion
        email = header.strip().split("for")[-1].strip()

        # Call the CRM utility to update notes for the given email with the parsed notes
        update_client_notes(email, notes.strip())
    else:
        # If the content is not formatted correctly, print a helpful error message to the console
        print("Invalid CRM task format. Expected 'Update notes for <email>: <note>'")