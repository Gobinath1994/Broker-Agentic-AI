import sys
import os

# ✅ Add the parent directory to the Python path so internal modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import task-specific agents and utility modules
from agents.planner_agent import generate_daily_plan  # Plans daily tasks using LLM
from agents.email_agent import handle_emails          # Handles email-related tasks
from agents.calendar_agent import manage_calendar     # Manages calendar events
from agents.crm_agent import update_crm               # Updates CRM notes
from utils.logger import log_event                    # Logs key events to file
from utils.db import log_task_completion              # Logs completed tasks into DB

def run_agent():
    """
    Orchestrates the automation of daily broker tasks.

    This function:
    - Logs the start of the process
    - Generates a task list using LLM logic
    - Iterates through each task, delegates based on type
    - Logs execution and stores completion in DB
    """
    
    log_event("Starting Broker Task Automation Agent")

    # 🧠 Step 1: Generate today's task list via the planning agent
    tasks = generate_daily_plan()

    # 🔁 Step 2: Loop over each task and handle based on its type
    for task in tasks:
        log_event(f"Executing task: {task['type']}")

        if task["type"] == "email":
            handle_emails(task)           # Send email reminder
        elif task["type"] == "calendar":
            manage_calendar(task)         # Schedule an event
        elif task["type"] == "crm":
            update_crm(task)              # Update CRM system
        
        # ✅ Log the completed task in the database
        log_task_completion(task['type'], task['content'])

    # 📤 Return list of tasks executed
    return tasks

# ✅ Run this block only if this file is executed directly (not imported)
if __name__ == "__main__":
    run_agent()