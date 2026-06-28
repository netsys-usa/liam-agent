# LIAM

> Your personal memory assistant in Claude — capture memories, contacts, recipes, and daily food & receipt logs, then recall them on demand.

This plugin connects Claude Code (and Cowork) to the LIAM MCP server over HTTP, so its tools are available automatically once installed — no manual MCP setup. The server is protected by **Google OAuth**; the first time you use it, Claude walks you through sign-in.

## What you get

The `liam` MCP server, exposing these tools to Claude:

**Memory**
- `CreateMemory` — save a note/memory, optionally tagged
- `ListMemory` — list saved memories
- `GetMemoryByTag` — recall memories filed under a tag
- `ListTags` — see all tags in use
- `ForgetMemory` — delete a memory

**Contacts**
- `CreateContact` / `UpdateContact` — add or edit a contact
- `GetContactById` — fetch one contact
- `ListContacts` — list all contacts
- `ListContactsByOrganization` / `ListContactsByIndustry` — filter contacts
- `SearchContactByFullText` — free-text contact search

**Recipes**
- `CreateRecipe` — save a recipe
- `ListRecipe` — list saved recipes

**Food & receipt logging**
- `LogFood` — log a meal/food item
- `GetDailyFoodSummary` — daily food summary
- `LogReceipt` — log a purchase receipt
- `GetDailyReceiptSummary` — daily spending summary

**Account**
- `WhoAmI` — show the signed-in account
- `GetHelpDocumentation` — built-in help

## Install

From the official directory (once approved):

```
/plugin install liam@claude-plugins-official
```

Directly from this repo while testing or self-hosting:

```
/plugin marketplace add NetXD/liam-mcp
/plugin install liam@liam
```

After installing, run `/mcp` and choose **liam → Authenticate**. Claude opens a
browser for Google sign-in (scopes: `openid` and your email address). Once you
approve, `/mcp` shows the `liam` server as **connected**.

## Configuration

The server endpoint is defined in [`.mcp.json`](./.mcp.json):

```json
{
  "mcpServers": {
    "liam": {
      "type": "http",
      "url": "https://web.askbuddy.ai/memory/mcp"
    }
  }
}
```

No API key or header is needed — authentication is handled entirely through the
OAuth 2.0 flow that Claude runs via `/mcp`. Never add a long-lived secret here.

## Security & data

- **Authentication:** Google OAuth 2.0 (Authorization Code + PKCE), brokered by
  the server's authorization endpoints under `https://web.askbuddy.ai/memory/`.
  Claude registers dynamically and stores the resulting token securely; no
  credentials are committed to this repo.
- **Scopes requested:** `openid` and `https://www.googleapis.com/auth/userinfo.email`
  (identity + email only — no access to Gmail, Drive, or other Google data).
- **Data handled:** the notes, contacts, recipes, and food/receipt entries you
  create are sent to and stored on the LIAM server (`web.askbuddy.ai`) under your
  account. Tools like `ForgetMemory` let you delete data you've stored.

## License

MIT — see [LICENSE](../../LICENSE).
