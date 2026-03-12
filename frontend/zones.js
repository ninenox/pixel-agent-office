/* ─── Zone Definitions ─── */
// Room layout: Research(x=10-258) | Dev(x=268-532) | Meeting(x=542-790) | Corridor(y=270-320) | Break(y=320-550)
const ZONES = {
  desk1:      { x: 140, y: 188, label: "Writing" },    // Research room
  desk2:      { x: 340, y: 188, label: "Coding" },     // Dev room
  desk3:      { x: 460, y: 188, label: "Research" },   // Dev room
  whiteboard: { x: 666, y: 148, label: "Planning" },   // Meeting room
  breakroom:  { x: 400, y: 430, label: "Break" },      // Break room
};

const STATUS_TO_ZONE = {
  writing:     "desk1",
  coding:      "desk2",
  researching: "desk3",
  thinking:    "whiteboard",
  planning:    "whiteboard",
  idle:        "breakroom",
  error:       "breakroom",
  syncing:     "desk1",
};

const STATUS_ICONS = {
  writing:     "✍️",
  coding:      "💻",
  researching: "🔍",
  thinking:    "🧠",
  idle:        "☕",
  error:       "⚠️",
  syncing:     "🔄",
  planning:    "📋",
};

const STATUS_COLORS = {
  writing:     "#f97316",
  coding:      "#8b5cf6",
  researching: "#3b82f6",
  thinking:    "#fbbf24",
  idle:        "#6b7280",
  error:       "#ef4444",
  syncing:     "#06b6d4",
  planning:    "#22c55e",
};
