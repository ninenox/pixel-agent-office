#!/usr/bin/env python3
"""
CLI สำหรับเปลี่ยนสถานะ agent ด้วยมือ

Usage:
  python set_state.py <agent_id> <status> [detail]

Examples:
  python set_state.py claude-opus writing "กำลังเขียนรายงาน"
  python set_state.py claude-haiku idle "พักเบรก"
  python set_state.py claude-sonnet coding "Refactoring auth module"
  python set_state.py claude-code error "Build failed"

Valid statuses: writing, coding, researching, thinking, planning, idle, error, syncing
"""

import json
import os
import sys
import time

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

VALID_STATUSES = ["writing", "coding", "researching", "thinking", "planning", "idle", "error", "syncing"]

VALID_AGENTS = ["claude-opus", "claude-sonnet", "claude-haiku", "claude-code"]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    agent_id = sys.argv[1]
    status = sys.argv[2]
    detail = sys.argv[3] if len(sys.argv) > 3 else ""

    if agent_id not in VALID_AGENTS:
        print(f"Error: Unknown agent '{agent_id}'")
        print(f"Valid agents: {', '.join(VALID_AGENTS)}")
        sys.exit(1)

    if status not in VALID_STATUSES:
        print(f"Error: Unknown status '{status}'")
        print(f"Valid statuses: {', '.join(VALID_STATUSES)}")
        sys.exit(1)

    # Read current state
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {"agents": {}}

    if "agents" not in state:
        state["agents"] = {}

    # Update
    state["agents"][agent_id] = {
        "status": status,
        "detail": detail,
        "updated_at": time.strftime("%H:%M:%S"),
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f"✓ [{agent_id}] → {status}: {detail}")


if __name__ == "__main__":
    main()
