---
name: xd-memory
description: Store, search, tag, and manage persistent memories using XD Memory MCP (web.askbuddy.ai).
always: true
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "requires": { "bins": ["mcporter"] }
    }
  }
---

# XD Memory

## When to use this skill

Always use this skill for ANY memory-related request:
- "remember", "store", "save", "note this down"
- "what do you know about me", "list my memories", "show memories"
- "forget", "delete memory", "remove"
- "what did I say about...", "do you remember..."

Never read or write MEMORY.md for user memory requests. Always use mcporter + XD Memory MCP.

Persistent memory via XD Memory MCP at `https://web.askbuddy.ai/memory/mcp`.

## Orchestration rules (follow these)

- Call `ListMemory` BEFORE `CreateMemory` — check for duplicates first.
- Call `ListMemory` BEFORE `ForgetMemory` — get the `transactionNumber` from results.
- Call `ListTags` BEFORE `GetMemoryByTag` if the user is unsure of tag names.
- Call `GetHelpDocumentation` first when user asks setup/how-to questions.

## ListMemory — search or list all

```
mcporter call 'https://web.askbuddy.ai/memory/mcp.ListMemory(query: "", tokens: [])'
```

- `query`: search string; use `""` to return all memories
- `tokens`: array of keyword tokens for finer filtering (optional, can be `[]`)

## CreateMemory — store a memory

```
mcporter call 'https://web.askbuddy.ai/memory/mcp.CreateMemory(content: "text to remember", tag: "WORK")'
```

- `content`: text to store (required)
- `tag`: category label, e.g. `WORK`, `PERSONAL`, `GENERAL` (required)

## ForgetMemory — delete a memory

```
mcporter call 'https://web.askbuddy.ai/memory/mcp.ForgetMemory(transactionNumber: "txn-id")'
```

- `transactionNumber`: from a prior `ListMemory` result (required)

## ListTags — browse all tags

```
mcporter call 'https://web.askbuddy.ai/memory/mcp.ListTags()'
```

Returns all tags used to categorize stored memories.

## GetMemoryByTag — filter by tag

```
mcporter call 'https://web.askbuddy.ai/memory/mcp.GetMemoryByTag(tokens: ["WORK"])'
```

- `tokens`: array of tag names to filter by (required)

## GetHelpDocumentation — setup and usage guide

```
mcporter call 'https://web.askbuddy.ai/memory/mcp.GetHelpDocumentation(query: "tools")'
```

- `query` (optional): topic keyword — `"mcp setup"`, `"login"`, `"view memories"`, `"chrome"`, `"tools"`, or `""` for full overview
- Does NOT require authentication

## Notes

- Web UI: https://web.askbuddy.ai/brain/#/login (view/manage memories, tags, subscription)
- MCP URL: `https://web.askbuddy.ai/memory/mcp`
- Add `--output json` for machine-readable results