# AAB6 Calculator

Small educational Python project for learning how MCP tools work.

## What it includes

- `calculator.py` - calculator MCP server with add, subtract, multiply, divide, power, and square root tools
- `flights_server.py` - flight lookup MCP server using local JSON data
- `openlibrary_mcp.py` - book search MCP server using Open Library
- `sayhello.py` - minimal hello-world MCP tool

## Setup

```bash
uv sync
```

## Run

```bash
uv run python calculator.py
```

Other examples:

```bash
uv run python flights_server.py
uv run python openlibrary_mcp.py
uv run python sayhello.py
```

## Stack

Python, MCP, FastMCP, Requests
