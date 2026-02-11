# Conversations MCP Server

## What it does

Stores and retrieves chat transcripts as JSON on disk, and can search across saved conversations.

## When to use it

- Persist conversation context across sessions.
- Retrieve a past transcript to summarize or continue work.

## Tools

- `save_conversation`
- `load_conversation`
- `list_conversations`
- `search_conversations`

## How to run

```bash
uv run conversations
```
