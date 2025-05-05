# Workday Timesheet MCP Server

This is a POC of how you can build MCP servers on top of web services like Workday.

https://github.com/user-attachments/assets/05efbf51-1b95-4bd2-a327-55f1fe2f958b

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol that enables seamless integration between LLM applications and external tools.

## Features

### Workday Timesheets
- Fill out and submit timesheets automatically
- Track timesheet submission status

## Prerequisites

- Python 3.12 or higher
- Anthropic API key or other supported LLM provider

## Setup

1. Ensure you have a virtual environment activated:
   ```
   uv venv
   source .venv/bin/activate  # On Unix/Mac
   ```

2. Install required packages:
   ```
   uv pip install -r requirements.txt
   playwright install
   ```

3. Update the `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your_openai_api_key_here
   ```

## Note

Since we're using stdio as MCP transport, we have disable all output from browser use

## Debugging

You can run the MCP inspector tool with this command

```bash
uv run mcp dev server.py
```

## Usage Examples

### Workday Timesheets

Fill out a timesheet:
```
await fill_timesheet(
    week_start_date="2025-05-05",
    days_off="Monday"
    time_types="Admin",
)
```

Check timesheet submission status:
```
resource://timesheet_status/request_id
```
