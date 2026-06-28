# liam-mcp

A Claude Code / Cowork plugin that wraps the **LIAM** remote MCP server — a
personal memory assistant (memories, contacts, recipes, food & receipt logs)
served over HTTP with Google OAuth.

This repo is both the **plugin source** and a small **development marketplace**,
so you can install and test the plugin straight from the repo before submitting it
to the public directory.

## Layout

```
liam-mcp/
├── .claude-plugin/
│   └── marketplace.json        # dev marketplace catalog (lists the plugin)
├── plugins/
│   └── liam/
│       ├── .claude-plugin/
│       │   └── plugin.json      # plugin manifest (required)
│       ├── .mcp.json            # remote HTTP MCP server config
│       └── README.md            # user-facing docs / directory listing
├── LICENSE
└── README.md                    # you are here
```

## Test it locally

1. Set the real server URL in `plugins/liam/.mcp.json`.
2. Validate the structure:
   ```
   claude plugin validate plugins/liam --strict
   ```
3. Register this repo as a marketplace and install:
   ```
   /plugin marketplace add ./           # or NetXD/liam-mcp once pushed to GitHub
   /plugin install liam@liam
   ```
4. Confirm the server connects:
   ```
   /mcp
   ```

## Submit to the Claude plugin directory

1. Fill in every `REPLACE ME` field (description, author, repo URL, security notes).
2. Push to a **public** GitHub repo.
3. Submit via one of the in-app forms:
   - claude.ai: `https://claude.ai/admin-settings/directory/submissions/plugins/new` (Team/Enterprise)
   - Console: `https://platform.claude.com/plugins/submit` (individual authors)
   Or start from `https://claude.com/plugins`.

Do **not** open a pull request against `anthropics/claude-plugins-community` — those
are closed automatically; everything flows through the submission form + review
pipeline. After approval, pushes to your repo are mirrored automatically, so you
don't resubmit for updates.
