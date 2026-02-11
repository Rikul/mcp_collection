# MCP Collection

A grab-bag of small **MCP (Model Context Protocol) servers**.

Each folder is an independent server (usually a tiny Python package) exposing a handful of tools.

## Quick start

Most servers can be run with `uv`:

```bash
# from within a server directory
uv run <script-name>
```

Example:

```bash
cd conversations
uv run conversations
```

If you don’t have `uv` installed:

```bash
python -m pip install uv
```

## What’s in here

Use the helper to list servers and their runnable entrypoints:

```bash
python3 scripts/list_servers.py
```

Or list just a couple:

```bash
python3 scripts/list_servers.py current_date_time wikipedia_mcp
```

## Development helpers

Validate the collection structure (missing READMEs, missing entrypoints, etc.):

```bash
python3 scripts/validate_collection.py
```

## Notes

- Each server manages its own dependencies via its `pyproject.toml`.
- This repo intentionally avoids forcing a single monorepo-style build system.
