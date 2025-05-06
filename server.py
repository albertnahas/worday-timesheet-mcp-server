#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from browser import run_browser_agent

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("worday_timesheet")

# In-memory storage for search results and timesheet status
timesheet_status = {}

@mcp.tool()
async def fill_timesheet(
    week_start_date: str = "this week",
    days_off: str = "",
    time_types: str = "Admin",
    context: Context = None
) -> str:
    """Fill out a Workday timesheet with the specified hours.
    
    Args:
        week_start_date: Start date of the week in YYYY-MM-DD format
        days_off: Days off in the week (e.g. "Monday, Tuesday")
        time_types: Time types to fill (e.g. "Admin, KITN-1937")
    """
    
    # Parse days off parameter
    days_off_instruction = ""
    if days_off:
        days_off_list = [day.strip() for day in days_off.split(",")]
        days_off_instruction = f" Skip the following days as they are days off: {', '.join(days_off_list)}."

    # Get Workday URL from environment variable with a fallback
    workday_url = os.getenv("WORKDAY_URL", "https://wd3.myworkday.com/company/d/home.htmld")

    task = f"""
    1. Go to {workday_url}
    2. Wait for the Workday dashboard to load fully
    3. Scroll down if needed to view all apps
    4. Navigate to Time app (from "View all apps")
    5. Find the week starting on {week_start_date} or this week
    6. Fill in each day (Monday to Friday except holidays) with 4 hours time type {time_types} and 4 hours time type Admin.{days_off_instruction}
    7. Click "save"
    """
    
    # Store initial status
    timesheet_status[context.request_id] = "Timesheet filling in progress. Please wait."
    
    # Start the background task
    asyncio.create_task(
        perform_timesheet_filling(week_start_date, task, context)
    )
    
    return f"Timesheet filling started for week of {week_start_date}. You can check the status using the resource URI: resource://timesheet_status/{context.request_id}. This process may take a few minutes."

async def perform_timesheet_filling(week_start_date: str, task: str, context: Context):
    """Perform the actual timesheet filling in the background."""
    try:
        step_count = 0
        
        async def step_handler(*args, **kwargs):
            nonlocal step_count
            step_count += 1
            await context.info(f"Timesheet step {step_count} completed")
            await context.report_progress(step_count)
        
        # Fall back to generic browser agent if workday module is not available
        await context.info("Specialized Workday agent not available, using generic browser agent")
        result = await run_browser_agent(task=task, on_step=step_handler, enable_memory=True)
        
        # Update status
        timesheet_status[context.request_id] = f"Timesheet for week of {week_start_date} has been successfully submitted."
        
        # Report completion
        await context.info(f"Timesheet has been successfully submitted!")
        return result
    
    except Exception as e:
        error_msg = f"Error filling timesheet: {str(e)}"
        timesheet_status[context.request_id] = error_msg
        await context.error(error_msg)
        return error_msg

@mcp.resource(uri="resource://timesheet_status/{request_id}")
async def get_timesheet_status(request_id: str) -> str:
    """Get the status of a timesheet filling request.
    
    Args:
        request_id: The ID of the request to get status for
    """
    # Check if the status exists
    if request_id not in timesheet_status:
        return f"No timesheet filling request found for ID: {request_id}"
    
    # Return the status
    return timesheet_status[request_id]

if __name__ == "__main__":
    mcp.run(transport='stdio')
