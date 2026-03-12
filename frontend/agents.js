/* ─── Agent Definitions ─── */
const AGENTS_CONFIG = [
  {
    id: "claude-opus",
    name: "Claude Opus",
    role: "Lead Researcher",
    color: "#f97316",
    skinColor: "#fcd5b5",
    hairColor: "#4a3728",
    shirtColor: "#f97316",
    pantsColor: "#374151",
  },
  {
    id: "claude-sonnet",
    name: "Claude Sonnet",
    role: "Code Architect",
    color: "#8b5cf6",
    skinColor: "#e8c4a0",
    hairColor: "#1a1a2e",
    shirtColor: "#8b5cf6",
    pantsColor: "#1f2937",
  },
  {
    id: "claude-haiku",
    name: "Claude Haiku",
    role: "Quick Responder",
    color: "#06b6d4",
    skinColor: "#f5d6b8",
    hairColor: "#92400e",
    shirtColor: "#06b6d4",
    pantsColor: "#374151",
  },
  {
    id: "claude-code",
    name: "Claude Code",
    role: "Dev Agent",
    color: "#22c55e",
    skinColor: "#deb896",
    hairColor: "#1e293b",
    shirtColor: "#22c55e",
    pantsColor: "#1e293b",
  },
];

const ACTIVITIES = {
  writing:     ["Drafting report...", "Editing document", "Writing summary", "Composing email"],
  coding:      ["Fixing bug #42", "Writing tests", "Code review", "Refactoring..."],
  researching: ["Reading papers", "Analyzing data", "Web search...", "Deep research"],
  thinking:    ["Brainstorming", "Processing...", "Evaluating...", "Reasoning..."],
  idle:        ["Coffee break!", "Stretching...", "Chatting", "Taking a break"],
  planning:    ["Roadmap review", "Sprint plan", "Architecture", "Diagramming"],
};

/* ─── Runtime Agent State ─── */
let agents = AGENTS_CONFIG.map((a, i) => ({
  ...a,
  x: 200 + i * 150,
  y: 300,
  targetX: 200 + i * 150,
  targetY: 300,
  status: ["writing", "coding", "researching", "idle"][i],
  detail: "",
  facing: "right",
  isWalking: false,
  bubbleText: "",
  bubbleTimer: 0,
}));

let selectedAgentId = null;
let activityLogs = [];

/* ─── Pixel Character Drawing ─── */
const S = 2; // pixel scale

function drawRect(ctx, x, y, w, h, color) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), w, h);
}

function drawPixelChar(ctx, agent, x, y, frame) {
  const bobY = Math.sin(frame * 0.15) * 1.5;
  const legFrame = agent.isWalking ? Math.floor(frame * 0.2) % 4 : 0;
  const facing = agent.facing;

  // Shadow
  ctx.fillStyle = "rgba(0,0,0,0.15)";
  ctx.beginPath();
  ctx.ellipse(x, y + 18 * S, 5 * S, 2 * S, 0, 0, Math.PI * 2);
  ctx.fill();

  // Legs
  const legOff = [[0,0],[-1,1],[0,0],[1,-1]];
  const [lO, rO] = [legOff[legFrame], legOff[(legFrame+2)%4]];
  drawRect(ctx, x-3*S, y+10*S+lO[0], 2*S, 8*S, agent.pantsColor);
  drawRect(ctx, x+1*S, y+10*S+rO[0], 2*S, 8*S, agent.pantsColor);
  drawRect(ctx, x-3*S, y+17*S+lO[0], 3*S, 2*S, "#1a1a2e");
  drawRect(ctx, x+1*S, y+17*S+rO[0], 3*S, 2*S, "#1a1a2e");

  // Body
  drawRect(ctx, x-4*S, y+2*S+bobY, 8*S, 9*S, agent.shirtColor);
  const armBob = agent.isWalking ? Math.sin(frame*0.2)*2 : 0;
  drawRect(ctx, x-6*S, y+3*S+bobY+armBob, 2*S, 6*S, agent.shirtColor);
  drawRect(ctx, x+4*S, y+3*S+bobY-armBob, 2*S, 6*S, agent.shirtColor);
  drawRect(ctx, x-6*S, y+8*S+bobY+armBob, 2*S, 2*S, agent.skinColor);
  drawRect(ctx, x+4*S, y+8*S+bobY-armBob, 2*S, 2*S, agent.skinColor);

  // Head
  drawRect(ctx, x-4*S, y-7*S+bobY, 8*S, 9*S, agent.skinColor);
  drawRect(ctx, x-4*S, y-8*S+bobY, 8*S, 4*S, agent.hairColor);
  if (facing === "left") {
    drawRect(ctx, x-5*S, y-7*S+bobY, 2*S, 6*S, agent.hairColor);
  } else {
    drawRect(ctx, x+4*S, y-7*S+bobY, 2*S, 6*S, agent.hairColor);
  }

  // Eyes
  const eX = facing === "left" ? -2 : 1;
  drawRect(ctx, x+(eX-1)*S, y-3*S+bobY, 1.5*S, 2*S, "#1a1a2e");
  drawRect(ctx, x+(eX+2)*S, y-3*S+bobY, 1.5*S, 2*S, "#1a1a2e");
  drawRect(ctx, x+(eX-0.5)*S, y-3*S+bobY, 0.8*S, 0.8*S, "#fff");
  drawRect(ctx, x+(eX+2.5)*S, y-3*S+bobY, 0.8*S, 0.8*S, "#fff");

  // Name
  ctx.fillStyle = agent.color;
  ctx.font = "bold 10px 'Press Start 2P', monospace";
  ctx.textAlign = "center";
  ctx.fillText(agent.name.split(" ")[1] || agent.name, x, y - 14*S + bobY);
}

function drawBubble(ctx, x, y, text, color) {
  const pad = 8;
  ctx.font = "9px 'Press Start 2P', monospace";
  const tw = ctx.measureText(text).width;
  const bw = tw + pad*2;
  const bh = 22;
  const bx = x - bw/2;
  const by = y - 50;

  ctx.fillStyle = "rgba(0,0,0,0.7)";
  ctx.beginPath(); ctx.roundRect(bx-1, by-1, bw+2, bh+2, 4); ctx.fill();
  ctx.fillStyle = "#fff";
  ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 3); ctx.fill();

  ctx.fillStyle = "#fff";
  ctx.beginPath();
  ctx.moveTo(x-4, by+bh); ctx.lineTo(x, by+bh+6); ctx.lineTo(x+4, by+bh);
  ctx.fill();

  ctx.fillStyle = color || "#1a1a2e";
  ctx.textAlign = "center";
  ctx.fillText(text, x, by + 15);
}

/* ─── Update Agent from Server ─── */
function applyServerState(serverState) {
  if (!serverState || !serverState.agents) return;

  for (const [agentId, data] of Object.entries(serverState.agents)) {
    const agent = agents.find(a => a.id === agentId);
    if (!agent) continue;

    const oldStatus = agent.status;
    agent.status = data.status || "idle";
    agent.detail = data.detail || "";

    // ถ้าสถานะเปลี่ยน → เดินไปโซนใหม่
    if (oldStatus !== agent.status) {
      const zoneName = STATUS_TO_ZONE[agent.status] || "breakroom";
      const zone = ZONES[zoneName];
      if (zone) {
        const jitter = () => (Math.random() - 0.5) * 60;
        agent.targetX = zone.x + jitter();
        agent.targetY = zone.y + jitter() + 40;
        agent.bubbleText = agent.detail || agent.status;
        agent.bubbleTimer = 180;
      }

      activityLogs.unshift({
        time: new Date(),
        agent: agent.name,
        color: agent.color,
        status: agent.status,
        detail: agent.detail,
      });
      if (activityLogs.length > 30) activityLogs.pop();
    }
  }
}
