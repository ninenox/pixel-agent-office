# Claude Agent Office 🏢

Pixel-art office dashboard แสดง Claude AI team ทำงาน real-time
แต่ละ agent เดินไปโซนต่างๆ (โต๊ะ, กระดาน, break room) ตามสถานะงาน

![Claude Agent Office](images/example.png)

---

## Quick Start

```bash
git clone https://github.com/ninenox/claude-agent-office.git
cd claude-agent-office
bash install.sh
source .venv/bin/activate
```

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # ต้องมีสำหรับรัน task จริง (ไม่ต้องสำหรับ demo)
python main.py
```
เปิดเบราว์เซอร์: http://localhost:19000 แล้วส่ง task ผ่าน **⚡ TASK DISPATCH**

---

## วิธีใช้งาน

### กำหนด Task ผ่านหน้าเว็บ

เปิด dashboard แล้วดูที่ส่วน **⚡ TASK DISPATCH** ด้านล่าง:

- พิมพ์งานในช่อง input ของแต่ละ agent
- กด **▶ RUN** เพื่อส่งงาน agent ทีละตัว
- กด **🚀 DISPATCH ALL** เพื่อส่งงานทุก agent พร้อมกัน
- กด `Ctrl+Enter` ใน textarea เพื่อ dispatch agent นั้น

### กำหนด Task ผ่าน CLI

**ไฟล์ JSON:**
```bash
# สร้าง tasks.json
{
  "claude-opus":   "วิเคราะห์แนวโน้ม AI Agent ปี 2026",
  "claude-sonnet": "ออกแบบ REST API สำหรับ task management",
  "claude-haiku":  "สรุปข่าวเทคโนโลยีวันนี้",
  "claude-code":   "เขียน unit test สำหรับ authentication"
}

python main.py --tasks tasks.json
```

**Single agent:**
```bash
cd agents
python agent_runner.py claude-sonnet "ออกแบบ database schema สำหรับ blog"
python agent_runner.py claude-haiku "สรุป 3 เทคนิค prompt engineering" --stream
```

**Boss Router** (AI แจกงานให้ทีมเอง):
```bash
cd agents
python router.py "วิเคราะห์และออกแบบระบบ e-commerce ทั้งหมด"
```

---

## Agents

กำหนดได้ที่ `config/team.json`

| Agent | บทบาท | Model |
|-------|--------|-------|
| `claude-opus` | Lead Researcher — วิเคราะห์เชิงลึก | claude-opus-4-6 |
| `claude-sonnet` | Code Architect — ออกแบบระบบ เขียนโค้ด | claude-sonnet-4-6 |
| `claude-haiku` | Quick Responder — ตอบเร็ว งานเบา | claude-haiku-4-5 |
| `claude-code` | Dev Agent — debug, refactor, test | claude-sonnet-4-6 |

เพิ่ม/แก้ไข agent ได้โดยแก้ไฟล์ `config/team.json`

---

## CLI Options

```
python main.py
  (ไม่มี flag)       รัน server รอรับ task ผ่านหน้าเว็บ
  --agents-only      รัน agents อย่างเดียว (ไม่มี UI)
  --tasks <file>     ระบุไฟล์ JSON กำหนด tasks (ใช้กับ --agents-only)

python set_state.py <agent_id> <status> [detail]
  ตัวอย่าง: python set_state.py claude-opus writing "กำลังเขียนรายงาน"
```

---

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/status` | อ่านสถานะ agents ทั้งหมด |
| POST | `/status` | อัพเดตสถานะ agent |
| POST | `/run` | ส่ง tasks แล้วรัน agents ใน background |
| GET | `/health` | health check |

**POST `/run`:**
```json
{
  "tasks": {
    "claude-opus": "วิเคราะห์...",
    "claude-sonnet": "ออกแบบ..."
  }
}
```

---

## Status → Zone

| Status | โซน | Icon |
|--------|-----|------|
| `writing` | Desk 1 | ✍️ |
| `coding` | Desk 2 | 💻 |
| `researching` | Desk 3 | 🔍 |
| `thinking` / `planning` | Whiteboard | 🧠 |
| `idle` / `error` | Breakroom | ☕ |

---

## License

MIT
