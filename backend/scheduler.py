"""
Scheduler — APScheduler อ่าน config/schedules.json แล้วรัน agent ตามเวลา

- โหลด schedules ตอน start
- watch schedules.json ทุก 30s — ถ้าเปลี่ยนแปลงให้ reload อัตโนมัติ
- เมื่อถึงเวลา → run_agent_with_tools(agent_id, task)
"""

import json
import os
import sys
import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEDULES_FILE = os.path.join(BASE_DIR, "config", "schedules.json")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")

if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

_scheduler = BackgroundScheduler(timezone="Asia/Bangkok")
_last_mtime = 0


def _load_schedules() -> list:
    try:
        with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _run_scheduled_agent(agent_id: str, task: str, schedule_id: str):
    """รัน agent สำหรับ scheduled task"""
    print(f"[scheduler] ⏰ trigger schedule '{schedule_id}' → [{agent_id}] {task[:50]}")
    try:
        from agent_tools import run_agent_with_tools
        result = run_agent_with_tools(agent_id, task)
        if result:
            print(f"[scheduler] ✓ [{agent_id}] เสร็จ ({len(result)} chars)")
    except Exception as e:
        print(f"[scheduler] ✗ [{agent_id}] error: {e}")


def _reload_schedules():
    """sync jobs ใน scheduler ให้ตรงกับ schedules.json"""
    schedules = _load_schedules()
    enabled = [s for s in schedules if s.get("enabled", True)]

    # ลบ jobs เก่าทั้งหมดแล้วสร้างใหม่
    for job in _scheduler.get_jobs():
        if job.id.startswith("sched_"):
            job.remove()

    for s in enabled:
        job_id = f"sched_{s['id']}"
        try:
            _scheduler.add_job(
                _run_scheduled_agent,
                trigger=CronTrigger.from_crontab(s["cron"], timezone="Asia/Bangkok"),
                id=job_id,
                args=[s["agent_id"], s["task"], s["id"]],
                replace_existing=True,
                misfire_grace_time=300,
            )
            print(f"[scheduler] + job '{s['id']}' [{s['agent_id']}] cron={s['cron']}")
        except Exception as e:
            print(f"[scheduler] ✗ ไม่สามารถสร้าง job '{s['id']}': {e}")

    print(f"[scheduler] โหลด {len(enabled)} schedules")


def _watch_schedules_file():
    """background thread คอย watch schedules.json — reload เมื่อไฟล์เปลี่ยน"""
    global _last_mtime
    while True:
        try:
            if os.path.exists(SCHEDULES_FILE):
                mtime = os.path.getmtime(SCHEDULES_FILE)
                if mtime != _last_mtime:
                    _last_mtime = mtime
                    _reload_schedules()
        except Exception as e:
            print(f"[scheduler] watch error: {e}")
        time.sleep(30)


def start():
    """เริ่ม scheduler — เรียกครั้งเดียวตอน app start"""
    _reload_schedules()
    _scheduler.start()
    print("[scheduler] started")

    watcher = threading.Thread(target=_watch_schedules_file, daemon=True)
    watcher.start()


def stop():
    """หยุด scheduler gracefully"""
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
        print("[scheduler] stopped")


def get_jobs_info() -> list:
    """คืนรายการ jobs ที่กำลัง active"""
    jobs = []
    for job in _scheduler.get_jobs():
        if job.id.startswith("sched_"):
            jobs.append({
                "id": job.id.replace("sched_", ""),
                "next_run": str(job.next_run_time) if job.next_run_time else None,
            })
    return jobs
