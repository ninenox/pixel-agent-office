/* ─── Zone Definitions ─── */
const ZONES = {
  desk1:      { x: 120, y: 180, label: "Writing" },
  desk2:      { x: 320, y: 180, label: "Coding" },
  desk3:      { x: 520, y: 180, label: "Research" },
  whiteboard: { x: 400, y: 80,  label: "Planning" },
  breakroom:  { x: 640, y: 400, label: "Break" },
  bookshelf:  { x: 80,  y: 400, label: "Reading" },
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
