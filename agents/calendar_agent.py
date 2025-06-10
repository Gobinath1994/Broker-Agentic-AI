# Import the schedule_event function from the tools.calendar_tool module.
# This function is responsible for interacting with the Google Calendar API to schedule events.
from tools.calendar_tool import schedule_event

# Define a function named `manage_calendar` that takes one argument: `task`.
# The `task` parameter is expected to be a dictionary containing task details.
def manage_calendar(task):
    """
    This function handles scheduling a calendar event for a client task.
    Currently, it uses hardcoded data to demonstrate the scheduling logic.
    In production, event details should ideally be extracted from the `task` parameter.
    """

    # Create a dictionary called `event` that holds the event details.
    # The "title" key specifies the name of the calendar event.
    # The "time" key contains the date and time in ISO 8601 format (e.g., "YYYY-MM-DDTHH:MM:SS").
    event = {
        "title": "Client Call",          # Static event title for now, shown in the calendar
        "time": "2025-06-10T15:00:00"    # Static date/time string for the event
    }

    # Call the imported `schedule_event` function and pass the `event` dictionary to it.
    # This triggers the logic that sends the event to Google Calendar via the API.
    schedule_event(event)