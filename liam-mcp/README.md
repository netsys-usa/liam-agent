# liam-mcp

A Claude Code / Cowork plugin that wraps the **LIAM** remote MCP server — a
personal memory assistant (memories, contacts, recipes, food & receipt logs)
served over HTTP with Google OAuth.

The plugin itself lives in [`plugins/liam/`](./plugins/liam). The repo's
**development marketplace** is the `.claude-plugin/marketplace.json` at the
`liam-agent` **repo root**, which lists this plugin — so you can install and test
straight from the repo before submitting it to the public directory.

## Layout

```
liam-agent/                          # repo root (github.com/netsys-usa/liam-agent)
├── .claude-plugin/
│   └── marketplace.json             # marketplace catalog → source: ./liam-mcp/plugins/liam
└── liam-mcp/
    ├── plugins/
    │   └── liam/
    │       ├── .claude-plugin/
    │       │   └── plugin.json       # plugin manifest (required)
    │       ├── .mcp.json             # remote HTTP MCP server config
    │       └── README.md             # user-facing docs / directory listing
    ├── LICENSE
    └── README.md                     # you are here
```

## Test it locally

1. Validate the plugin structure (run from the repo root):
   ```
   claude plugin validate liam-mcp/plugins/liam
   ```
2. Register this repo as a marketplace and install:
   ```
   /plugin marketplace add netsys-usa/liam-agent
   /plugin install liam@liam
   ```
3. Authenticate and confirm the server connects:
   ```
   /mcp        # choose liam → Authenticate, complete Google sign-in
   ```

## Submit to the Claude plugin directory

1. Push to the **public** `netsys-usa/liam-agent` repo (the `.claude-plugin/marketplace.json`
   must be readable at the repo root).
2. Submit via one of the in-app forms:
   - claude.ai: `https://claude.ai/admin-settings/directory/submissions/plugins/new` (Team/Enterprise)
   - Console: `https://platform.claude.com/plugins/submit` (individual authors)
   Or start from `https://claude.com/plugins`.

Do **not** open a pull request against `anthropics/claude-plugins-community` — those
are closed automatically; everything flows through the submission form + review
pipeline. After approval, pushes to your repo are mirrored automatically, so you
don't resubmit for updates.
