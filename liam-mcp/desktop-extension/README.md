# LIAM — Claude Desktop Extension (.mcpb)

A one-double-click installer for **Claude Desktop** that connects to the hosted
LIAM MCP server (`https://web.askbuddy.ai/memory/mcp`) with Google OAuth.

## How it works

`.mcpb` bundles only run **local stdio** servers — they can't point at a remote
HTTPS+OAuth server directly. So this bundle ships a tiny launcher
([`server/index.js`](./server/index.js)) that runs a **vendored copy of
[`mcp-remote`](https://www.npmjs.com/package/mcp-remote)** (bundled in
`node_modules/` — nothing is fetched at runtime). `mcp-remote` bridges Claude
Desktop's local stdio transport to the remote LIAM server and runs the standard
OAuth flow (Dynamic Client Registration + PKCE + refresh tokens) on first connect —
the same `/xdlogin/` flow used by the Connectors Directory listing.

**Runtime requirements:** just the Node runtime that Claude Desktop already ships.
No `npx`, no network fetch of dependencies — everything is in the bundle.

## Install (for end users)

1. Download `liam.mcpb`.
2. Double-click it (or drag it into **Claude Desktop → Settings → Extensions**).
3. Click **Install**.
4. On first use, a browser opens for **Google sign-in** — approve, and LIAM's
   tools are available in Claude Desktop.

## Distribute

Host `liam.mcpb` at a stable URL (e.g. `https://web.askbuddy.ai/liam.mcpb` or a
GitHub Release asset) and link to it from your site/onboarding. Users download
and double-click.

> Note: there is currently **no web deep link** that auto-installs a `.mcpb` —
> distribution is download-then-double-click. For a native one-click "Add" inside
> claude.ai and Desktop, that's the **Connectors Directory** listing (submitted
> separately), which needs no bundle at all.

## Rebuild

```bash
cd liam-mcp/desktop-extension
npm install                 # restore vendored deps (mcp-remote + transitive)
npx -y @anthropic-ai/mcpb@latest validate manifest.json
npx -y @anthropic-ai/mcpb@latest pack . liam.mcpb
```

Bump `version` in [`manifest.json`](./manifest.json) for each release. The server
URL lives in [`server/index.js`](./server/index.js) (`LIAM_URL`).
