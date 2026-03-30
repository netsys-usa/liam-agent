# xd-memory Skill — Installation Guide

xd-memory is a skill that gives OpenClaw persistent, searchable cloud memory. Once installed, the agent stores and retrieves memories automatically.

> **Before you begin:** See [liam-python-sdk/README.md](README.md) for account setup and configuration instructions.

---

## Your Setup

Pick the scenario that matches you:

- **Scenario A** — OpenClaw running locally on your Mac
- **Scenario B** — OpenClaw running on a Linux cloud VM, accessed from your Mac

---

## Step 1 — Install mcporter

**Scenario A (local Mac)**

Run on your Mac:

```bash
npm install -g mcporter
```

**Scenario B (Linux VM)**

Run on your Mac (where the browser is):

```bash
npm install -g mcporter
```

Also run on your Linux VM (where OpenClaw runs):

```bash
npm install -g mcporter
```

---

## Step 2 — Authenticate

Authentication opens a browser, so it must run on your Mac regardless of scenario.

```bash
npx mcporter auth https://web.askbuddy.ai/memory/mcp
```

- A browser tab opens → log in with your XD Memory account
- Once you see confirmation in the browser → press `Ctrl+C` in the terminal
- Credentials are saved to `~/.mcporter/credentials.json` on your Mac

**Verify:**

```bash
mcporter call 'https://web.askbuddy.ai/memory/mcp.ListMemory(query: "", tokens: [])'
```

Should return a JSON response (empty list is fine).

---

## Step 3 — Copy Credentials to Where OpenClaw Runs

**Scenario A (local Mac)**

Nothing to copy — OpenClaw and mcporter are on the same machine. Done.

**Scenario B (Linux VM)**

Copy credentials from your Mac to the VM:

```bash
# Run this on your Mac
scp ~/.mcporter/credentials.json user@your-vm-ip:~/.mcporter/credentials.json
```

Then on the VM, verify mcporter can reach the server:

```bash
mcporter call 'https://web.askbuddy.ai/memory/mcp.ListMemory(query: "", tokens: [])'
```

---

## Step 4 — Install the Skill

Run on the machine where OpenClaw is running (Mac for Scenario A, VM for Scenario B):

```bash
mkdir -p ~/.openclaw/skills/xd-memory
cp /path/to/SKILL.md ~/.openclaw/skills/xd-memory/SKILL.md
```

OpenClaw watches the skills folder — no restart needed. Verify:

```bash
openclaw skills list
```

You should see `xd-memory` with status `✓ ready`.

---

## Step 5 — Disable Built-in Memory

```bash
openclaw config set plugins.slots.memory none
```

---

## Step 6 — Update AGENTS.md

```bash
grep -qF "xd-memory skill" ~/.openclaw/workspace/AGENTS.md 2>/dev/null || \
echo "For ALL memory operations, always use the xd-memory skill via mcporter. Never use memory/*.md files." \
>> ~/.openclaw/workspace/AGENTS.md
```

---

## Step 7 — Restart the Gateway

```bash
openclaw gateway restart
```

---

## Step 8 — Verify

Open the OpenClaw dashboard and go to **Chat**. Send:

```
check memory
```

You should see `mcporter` being invoked. If the agent lists memories (or says none found) using `xd-memory` rather than reading `MEMORY.md`, the skill is working correctly.