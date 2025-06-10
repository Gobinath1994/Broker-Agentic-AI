import os

def log_event(message):
    """
    Appends a log message to the 'logs/execution.log' file.

    This function is useful for keeping a simple event trail
    for debugging or audit purposes.

    Args:
        message (str): The log message to be recorded.
    """

    # ✅ Create the "logs" directory if it doesn't already exist
    os.makedirs("logs", exist_ok=True)

    # ✅ Open (or create) the log file in append mode
    with open("logs/execution.log", "a") as log_file:
        # ✅ Write the message with a [LOG] tag prefix
        log_file.write(f"[LOG] {message}\n")