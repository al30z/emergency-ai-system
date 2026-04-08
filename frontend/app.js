const API = "http://127.0.0.1:8000";
let queue = [];

const COLORS = {
  critical: "#ff3b30",
  urgent: "#ff9500",
  medium: "#f0b429",
  low: "#34c759"
};

async function checkHealth() {
  try {
    const r = await fetch(`${API}/health`);
    const data = await r.json();
    const pill = document.getElementById("statusPill");
    if (data.model_loaded) {
      pill.textContent = "● API Online";
      pill.classList.add("online");
    }
  } catch {
    document.getElementById("statusPill").textContent = "● API Offline";
  }
}

async function submitMessage() {
  const input = document.getElementById("messageInput");
  const msg = input.value.trim();
  if (!msg) return alert("Please enter a message.");

  try {
    const r = await fetch(`${API}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });
    const data = await r.json();
    addToQueue(data);
    input.value = "";
  } catch (e) {
    alert("Could not reach API. Make sure the backend is running on port 8000.");
  }
}

async function loadDemo() {
  try {
    const r = await fetch(`${API}/demo`);
    const data = await r.json();
    data.results.forEach(item => addToQueue(item));
  } catch {
    alert("API not reachable.");
  }
}

function addToQueue(item) {
  queue.push(item);
  queue.sort((a, b) => a.order - b.order);
  renderQueue();
  updateStats();
}

function renderQueue() {
  const el = document.getElementById("messageQueue");
  if (queue.length === 0) {
    el.innerHTML = `<div class="empty-state">No messages yet. Submit a message or load the demo.</div>`;
    return;
  }
  el.innerHTML = queue.map((item, i) => `
    <div class="msg-card" style="border-left-color: ${COLORS[item.priority]}">
      <span class="msg-badge" style="background:${COLORS[item.priority]}20; color:${COLORS[item.priority]}">
        ${item.priority}
      </span>
      <span class="msg-text">${item.message}</span>
      <span class="msg-confidence">${item.confidence}% confidence</span>
      <button onclick="removeItem(${i})" style="background:none;border:none;color:#8b949e;cursor:pointer;font-size:1rem;">✕</button>
    </div>
  `).join("");
}

function removeItem(index) {
  queue.splice(index, 1);
  renderQueue();
  updateStats();
}

function clearQueue() {
  queue = [];
  renderQueue();
  updateStats();
}

function updateStats() {
  const counts = { critical: 0, urgent: 0, medium: 0, low: 0 };
  queue.forEach(item => counts[item.priority]++);
  document.getElementById("criticalCount").textContent = counts.critical;
  document.getElementById("urgentCount").textContent = counts.urgent;
  document.getElementById("mediumCount").textContent = counts.medium;
  document.getElementById("lowCount").textContent = counts.low;
}

document.getElementById("messageInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    submitMessage();
  }
});

checkHealth();
setInterval(checkHealth, 10000);
