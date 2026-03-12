# Claude Agent Office 🏢

> [🇹🇭 ภาษาไทย](README.th.md)

Pixel-art office dashboard showing a Claude AI team working in real-time.
Each agent walks to different zones (desk, whiteboard, break room) based on their current task status — with waypoint pathfinding to navigate around room walls.

**Two modes:**
- **Manual** — assign tasks to each agent individually
- **Auto** — describe a goal once; the Boss AI analyzes and distributes work automatically

![Claude Agent Office](examples/example.gif)

---

## Quick Start

```bash
git clone https://github.com/ninenox/claude-agent-office.git
cd claude-agent-office
bash install.sh
source .venv/bin/activate
```

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python main.py
```

Open browser: http://localhost:19000

---

## Usage

### ⚡ MANUAL Mode

Click **⚡ TASK DISPATCH** at the top → select the **⚙ MANUAL** tab.

- Type a task in each agent's input box
- Click **▶ RUN** to send a task to one agent, or press `Ctrl+Enter`
- Click **🚀 DISPATCH ALL** to send tasks to all agents simultaneously
- Click **■ STOP** next to an agent name to stop that agent, or **■ STOP ALL** to stop everyone

### ✦ AUTO Mode (Brainstorm)

Select the **✦ AUTO** tab in TASK DISPATCH:

- Describe your goal in a single text box
- Click **✦ BRAINSTORM** — the Boss AI analyzes and assigns tasks automatically
- All agents walk to the whiteboard first, then Boss distributes work
- The Boss's plan and per-agent assignments appear below the button

### CLI

**Run agents without the UI:**
```bash
python main.py --agents-only --tasks tasks.json
```

Example `tasks.json`:
```json
{
  "claude-opus":   "Analyze AI Agent trends for 2026",
  "claude-sonnet": "Design a REST API for task management",
  "claude-haiku":  "Summarize today's tech news",
  "claude-code":   "Write unit tests for user authentication"
}
```

**Single agent:**
```bash
cd agents
python agent_runner.py claude-sonnet "Design a database schema for a blog"
python agent_runner.py claude-haiku "List 3 prompt engineering techniques" --stream
```

---

## Agents

Configured in `config/team.json`

| Agent | Role | Model |
|-------|------|-------|
| `claude-opus` | Lead Researcher — deep analysis | claude-opus-4-6 |
| `claude-sonnet` | Code Architect — system design & coding | claude-sonnet-4-6 |
| `claude-haiku` | Quick Responder — fast, lightweight tasks | claude-haiku-4-5 |
| `claude-code` | Dev Agent — debug, refactor, test | claude-sonnet-4-6 |

Add or modify agents by editing `config/team.json`.

---

## CLI Options

```
python main.py
  (no flags)                      Start server; assign tasks via the web UI
  --agents-only --tasks <file>    Run agents from a JSON file (no UI)
```

---

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/status` | Get all agent statuses |
| POST | `/status` | Update a single agent's status |
| POST | `/run` | Send tasks and run agents in the background |
| POST | `/brainstorm` | Boss analyzes a goal and assigns work (AUTO mode) |
| POST | `/stop` | Stop agent(s) and set status to idle |
| GET | `/health` | Health check |

**POST `/run`:**
```json
{ "tasks": { "claude-opus": "Analyze...", "claude-sonnet": "Design..." } }
```

**POST `/brainstorm`:**
```json
{ "task": "Analyze and design a complete e-commerce system" }
```

**POST `/stop`:**
```json
{ "agent_id": "claude-opus" }   // omit to stop all agents
```

---

## Status → Zone

| Status | Room | Zone |
|--------|------|------|
| `writing` | Research | Desk |
| `coding` | Dev | Desk 1 |
| `researching` | Dev | Desk 2 |
| `thinking` / `planning` | Meeting | Whiteboard |
| `idle` / `error` | Break Room | — |

---

## License

MIT
