# NotebookLM Integration Guide

This guide describes how to connect, authenticate, and query the NotebookLM MCP server to perform semantic searches over your study notebooks.

---

## 1. Authentication Flow

The NotebookLM MCP server uses active browser session cookies extracted from Chrome.

### How it was authenticated:
1. Ran `notebooklm-mcp-auth --file` to show cookie extraction steps.
2. Extracted the `cookie:` header value from a `batchexecute` Network request on [notebooklm.google.com](https://notebooklm.google.com).
3. Saved the tokens via the `save_auth_tokens` tool:
   - Config file: `C:\Users\Parth\.notebooklm-mcp\auth.json`

### If Authentication Expires (RPC Error 16):
Run the interactive CLI in your terminal:
```bash
notebooklm-mcp-auth --file
```
Or paste the updated cookie string directly in chat and run the `save_auth_tokens` tool.

---

## 2. MCP Tool Reference

The following tools are available via the `notebooklm` MCP server:

| Tool Name | Description | Key Arguments |
|---|---|---|
| `notebook_list` | List all available notebooks. | `max_results` |
| `notebook_create` | Create a new notebook. | `title` |
| `notebook_get` | Get details of a notebook. | `notebook_id` |
| `notebook_query` | Query a notebook using natural language (semantic search). | `notebook_id`, `query` |
| `notebook_add_text` | Add a plain text source to a notebook. | `notebook_id`, `title`, `content` |
| `notebook_add_url` | Add a web URL source to a notebook. | `notebook_id`, `url` |
| `source_get_content` | Fetch raw content of a source. | `notebook_id`, `source_id` |
| `source_delete` | Delete a source from a notebook. | `notebook_id`, `source_id` |
| `notebook_delete` | Delete a notebook. | `notebook_id` |

---

## 3. Example Usage

### Listing notebooks:
```python
# MCP call: notebook_list
arguments = {"max_results": 10}
```

### Querying a notebook:
```python
# MCP call: notebook_query
arguments = {
    "notebook_id": "9be9c063-dbf9-4492-bdc9-87ce0a441219",
    "query": "What is vibe coding?"
}
```
