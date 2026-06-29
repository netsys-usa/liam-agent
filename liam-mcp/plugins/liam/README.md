# LIAM — Large Intelligent Agentic Memory

> Give Claude a persistent personal memory: save & recall notes, contacts, recipes, and food/receipt logs — by text **or by uploading a photo**. By [NetXD](https://netxd.com).

This plugin connects Claude Code (and Cowork) to the LIAM MCP server over HTTP, so its tools are available automatically once installed — no manual MCP setup. The server is protected by **Google OAuth**; the first time you use it, Claude walks you through sign-in.

You can type a request, or just drop in a photo — a receipt, meal, business card, or
handwritten note is read and filed to the right place automatically (a restaurant
receipt is logged as both an expense **and** a meal). Only the extracted text/values are
stored — never the raw image.

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
/plugin marketplace add netsys-usa/liam-agent
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
  account. When you upload an image, only the **extracted text/values** are stored —
  not the raw image. Tools like `ForgetMemory`, and the XD Brain web app, let you
  view and delete your data.
- **Policies:** see the [Privacy Policy](https://web.askbuddy.ai/brain/#/privacy-policy/sh)
  and [Terms of Service](https://web.askbuddy.ai/brain/#/terms/sh).

## Links

- **Website:** https://web.askbuddy.ai
- **Manage your data (XD Brain):** https://web.askbuddy.ai/brain/#/login
- **Support / contact:** https://web.askbuddy.ai/contact/
- **Privacy Policy:** https://web.askbuddy.ai/brain/#/privacy-policy/sh
- **Terms of Service:** https://web.askbuddy.ai/brain/#/terms/sh

## License

MIT — see [LICENSE](../../LICENSE).
