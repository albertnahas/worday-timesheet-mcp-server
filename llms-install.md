# AI Agents -- Read this!

This guide provides instructions for AI agents to set up the Workday Timesheet MCP server on behalf of the user.

## Prerequisites

- Python 3.12 or higher
- Anthropic API key or other supported LLM provider

## Setup

1. Create and activate a virtual environment:

   ```
   uv venv
   source .venv/bin/activate  # On Unix/Mac
   ```

2. Install required packages:
   ```
   uv pip install -r requirements.txt
   playwright install
   ```

## MCP Configuration

To use this server with MCP-compatible applications, you need to add it to your MCP settings file:

**Important Notes:**

- Replace `/path/to/workday-timesheet-mcp-server` with the actual path to your installation
- Replace the censored `ANTHROPIC_API_KEY` with your actual Anthropic API key
- All environment variables can be set directly in the MCP settings JSON file, so you don't need to update the .env file separately
- The command uses `/bin/bash` to activate the virtual environment before running the server
- You may need to restart your application after updating the MCP settings

## Available Tools

This MCP server provides the following tools:

1. `fill_timesheet`: Fill out a Workday timesheet

   - Parameters: 
     - `week_start_date` (string) - Start date of the week in YYYY-MM-DD format
     - `days_off` (string, optional) - Days off in the week (e.g. "Monday, Tuesday")
     - `time_types` (string, optional) - Time types to fill (e.g. "Admin, KITN-1937")
   - Returns a resource URI that can be used to track the progress

## Example Usage

```python
# Fill out a timesheet for a specific week
result = await use_mcp_tool(
    server_name="github.com/user/workday-timesheet-mcp-server",
    tool_name="fill_timesheet",
    arguments={
        "week_start_date": "2025-05-05",
        "days_off": "Monday, Friday",
        "time_types": "Admin, KITN-1937"
    }
)

# Check the status of the timesheet submission
status = await access_mcp_resource(
    server_name="github.com/user/workday-timesheet-mcp-server",
    uri="resource://timesheet_status/{request_id}"  # request_id from the previous result
)
```

## Troubleshooting

If you encounter connection issues:

1. Make sure the virtual environment is activated in the MCP settings file command
2. Check that the paths in your MCP settings file are correct
3. Verify that your Anthropic API key is valid
4. Try adjusting the log levels in the env section of your MCP settings
5. Restart your application after making changes to the MCP settings
