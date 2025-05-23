# Workday Timesheet MCP Server

A server for automatically filling Workday timesheets.

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
   
4. Add Your organization's Workday URL (e.g., https://wd3.myworkday.com/company/d/home.htmld)

   Example:
   ```
   WORKDAY_URL=https://wd3.myworkday.com/company/d/home.htmld
   ```

## Note

Since we're using stdio as MCP transport, we have disable all output from browser use

## Debugging

You can run the MCP inspector tool with this command

```bash
uv run mcp dev server.py
```

You may need to launch a Chrome instance with remote debugging enabled:

```bash
/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

This allows the automation tools to connect to an existing Chrome instance.

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
