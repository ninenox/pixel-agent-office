# Claude Agent Office 🏢

A pixel-art office dashboard that visualizes your Claude AI team working in real-time. Inspired by [Star-Office-UI](https://github.com/ringhyacinth/Star-Office-UI).

Each Claude agent appears as a pixel character that walks between office zones (desk, whiteboard, breakroom) based on their current task status.

## Features

- **Pixel Office Canvas** — hand-drawn office with desks, whiteboard, bookshelf, coffee machine
- **4 AI Agents** — Opus (research), Sonnet (code), Haiku (quick tasks), Code (dev)
- **Real-time Status** — agents move to zones matching their work status
- **Activity Log** — sidebar shows all status changes with timestamps
- **Multi-Agent** — run multiple Claude instances simultaneously via API
- **Boss Router** — auto-delegate tasks to the right agent
- **Demo Mode** — works without API key (auto-simulates activity)

## Quick Start

### 1. Install

```bash
git clone https://github.com/ninenox/claude-agent-office.git
cd claude-agent-office
pip install -r backend/requirements.txt
```

### 2. Run (Demo Mode — no API key needed)

```bash
cp state.sample.json state.json
cd backend && python app.py
```

Open http://localhost:19000 — agents will auto-simulate.

### 3. Run with Claude API

```bash
cp .env.example .env
# Edit .env → add your ANTHROPIC_API_KEY

# Run everything (server + agents)
python main.py

# Or server only
python main.py --server-only
```

### 4. Manual Status Control

```bash
python set_state.py claude-opus writing "Drafting report"
python set_state.py claude-haiku idle "Coffee break"
python set_state.py claude-sonnet coding "Fixing bug #42"
python set_state.py claude-code error "Build failed"
```

## Architecture

```
main.py (orchestrator)
    │
    ├─ Thread 1 → claude-opus   → Anthropic API ─┐
    ├─ Thread 2 → claude-sonnet → Anthropic API ─┤
    ├─ Thread 3 → claude-haiku  → Anthropic API ─┤  write
    └─ Thread 4 → claude-code   → Anthropic API ─┤
                                                   ▼
                                             state.json
                                                   │
                                  Flask (app.py) ◀─┘
                                    GET /status
                                         │
                                         ▼
                                  Browser Canvas 🎮
                                  (poll every 2s)
```

## Agent Modes

| Mode | File | Description |
|------|------|-------------|
| Basic | `agents/agent_runner.py` | Simple API call + status update |
| Stream | `agents/agent_runner.py` | Streaming with real-time preview |
| Tools | `agents/agent_tools.py` | Agent with tool use (search, file I/O) |
| Multi | `agents/orchestrator.py` | Run all agents in parallel |
| Router | `agents/router.py` | Boss agent auto-delegates tasks |

## Configuration

- `config/team.json` — agent names, roles, models
- `config/zones.json` — map status → office zone position
- `state.sample.json` — initial state template

## Valid Statuses

`writing` · `coding` · `researching` · `thinking` · `planning` · `idle` · `error` · `syncing`

## License

MIT
