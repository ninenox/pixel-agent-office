"""
Tool: create_schedule — ให้ agent สร้าง/ดู/ลบ schedule ได้เอง

agent สามารถรับ prompt เช่น "ทุกวัน 10 โมงเช้าดูนัดหมาย"
แล้วเรียก tool นี้เพื่อสร้าง recurring task โดยอัตโนมัติ
"""

import json
import os
import uuid
from datetime import datetime
from .base import BaseTool

SCHEDULES_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "config", "schedules.json")
)

# cron shorthand ที่ใช้บ่อย
CRON_PRESETS = {
    "ทุกวัน 9 โมง":     "0 9 * * *",
    "ทุกวัน 10 โมง":    "0 10 * * *",
    "ทุกวัน 8 โมงเช้า": "0 8 * * *",
    "ทุกวันเที่ยง":     "0 12 * * *",
    "ทุกวัน 18:00":     "0 18 * * *",
    "ทุกชั่วโมง":       "0 * * * *",
    "ทุกวันจันทร์ 9 โมง": "0 9 * * 1",
}


def _load() -> list:
    try:
        with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(schedules: list) -> None:
    with open(SCHEDULES_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, ensure_ascii=False, indent=2)


class CreateScheduleTool(BaseTool):
    name = "create_schedule"
    description = (
        "สร้าง, ดู หรือลบ scheduled task ที่จะรันซ้ำตามเวลาที่กำหนด "
        "ใช้เมื่อผู้ใช้ขอให้ทำงานซ้ำอัตโนมัติ เช่น 'ทุกวัน 10 โมงเช้าดูนัดหมาย' "
        "action: 'create' | 'list' | 'delete'"
    )
    input_schema = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["create", "list", "delete"],
                "description": "'create' = สร้าง schedule ใหม่, 'list' = ดู schedules ทั้งหมด, 'delete' = ลบ",
            },
            "cron": {
                "type": "string",
                "description": (
                    "Cron expression เช่น '0 10 * * *' = ทุกวัน 10:00 "
                    "หรือ shorthand: 'ทุกวัน 10 โมง', 'ทุกวัน 9 โมง', 'ทุกชั่วโมง'"
                ),
            },
            "agent_id": {
                "type": "string",
                "description": "Agent ที่จะรัน task (เช่น 'research-agent') — จำเป็นเมื่อ action='create'",
            },
            "task": {
                "type": "string",
                "description": "Task ที่ต้องการให้ agent ทำ — จำเป็นเมื่อ action='create'",
            },
            "schedule_id": {
                "type": "string",
                "description": "ID ของ schedule ที่ต้องการลบ — จำเป็นเมื่อ action='delete'",
            },
        },
        "required": ["action"],
    }

    def run(
        self,
        action: str,
        cron: str = None,
        agent_id: str = None,
        task: str = None,
        schedule_id: str = None,
    ) -> str:
        if action == "list":
            return self._list()
        elif action == "create":
            return self._create(cron, agent_id, task)
        elif action == "delete":
            return self._delete(schedule_id)
        return f"[error] action ไม่รู้จัก: {action}"

    def _create(self, cron: str, agent_id: str, task: str) -> str:
        if not cron or not agent_id or not task:
            return "[error] ต้องระบุ cron, agent_id และ task"

        # แปลง shorthand → cron expression
        resolved_cron = CRON_PRESETS.get(cron.strip(), cron.strip())

        # ตรวจ cron format เบื้องต้น
        parts = resolved_cron.split()
        if len(parts) != 5:
            return f"[error] cron ไม่ถูกต้อง: '{resolved_cron}' ต้องมี 5 ส่วน เช่น '0 10 * * *'"

        schedules = _load()
        new_schedule = {
            "id": str(uuid.uuid4())[:8],
            "cron": resolved_cron,
            "agent_id": agent_id,
            "task": task,
            "enabled": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        schedules.append(new_schedule)
        _save(schedules)

        # แปลง cron กลับเป็นภาษาคนอ่านง่าย
        cron_desc = {v: k for k, v in CRON_PRESETS.items()}.get(resolved_cron, resolved_cron)
        return (
            f"✓ สร้าง schedule สำเร็จ\n"
            f"ID: {new_schedule['id']}\n"
            f"เวลา: {cron_desc}\n"
            f"Agent: {agent_id}\n"
            f"Task: {task}"
        )

    def _list(self) -> str:
        schedules = _load()
        if not schedules:
            return "ยังไม่มี schedule ที่กำหนดไว้"
        lines = [f"Schedules ทั้งหมด ({len(schedules)} รายการ):\n"]
        for s in schedules:
            status = "✓" if s.get("enabled") else "✗"
            cron_desc = {v: k for k, v in CRON_PRESETS.items()}.get(s["cron"], s["cron"])
            lines.append(
                f"{status} [{s['id']}] {cron_desc}\n"
                f"   Agent: {s['agent_id']}\n"
                f"   Task: {s['task'][:60]}{'...' if len(s['task'])>60 else ''}"
            )
        return "\n".join(lines)

    def _delete(self, schedule_id: str) -> str:
        if not schedule_id:
            return "[error] ต้องระบุ schedule_id"
        schedules = _load()
        original_len = len(schedules)
        schedules = [s for s in schedules if s["id"] != schedule_id]
        if len(schedules) == original_len:
            return f"[error] ไม่พบ schedule ID: {schedule_id}"
        _save(schedules)
        return f"✓ ลบ schedule '{schedule_id}' สำเร็จ"
