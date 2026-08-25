function showPage(pageId, button) {
  document
    .querySelectorAll(".page")
    .forEach((p) => p.classList.remove("active"));
  document
    .querySelectorAll(".nav-item")
    .forEach((i) => i.classList.remove("active"));
  document.getElementById(pageId).classList.add("active");
  button.classList.add("active");
  if (pageId === "summary" || pageId === "compare") loadDocuments();
  if (pageId === "stats") loadStats();
}
function useQuestion(button) {
  document.getElementById("question").value = button.innerText;
  askQuestion();
}
async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value.trim();
  if (!question) return;
  addMessage(question, "user");
  input.value = "";
  addMessage("Thinking...", "assistant", "loading");
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();
    removeLoading();
    addMessage(data.answer, "assistant", "", data.sources);
  } catch (e) {
    removeLoading();
    addMessage("Unable to connect to the server.", "assistant");
  }
}
function addMessage(text, role, extraClass = "", sources = []) {
  const container = document.getElementById("chatMessages");
  const welcome = container.querySelector(".welcome");
  if (welcome) welcome.remove();
  const message = document.createElement("div");
  message.className = `message ${role} ${extraClass}`;
  message.innerText = text;
  if (role === "assistant" && sources && sources.length) {
    const sourceBox = document.createElement("div");
    sourceBox.className = "sources";
    sourceBox.innerText =
      "📚 Sources\n" +
      sources.map((s) => `${s.document} — Page ${s.page}`).join("\n");
    message.appendChild(sourceBox);
  }
  container.appendChild(message);
  container.scrollTop = container.scrollHeight;
}
function removeLoading() {
  const loading = document.querySelector(".message.loading");
  if (loading) loading.remove();
}
async function clearChat() {
  await fetch("/api/clear-chat", { method: "POST" });
  document.getElementById("chatMessages").innerHTML =
    `<div class="welcome"><div class="welcome-icon">✦</div><h2>How can I help you?</h2><p>Ask questions across your organizational knowledge.</p></div>`;
}
async function uploadFiles() {
  const input = document.getElementById("fileInput"),
    status = document.getElementById("uploadStatus");
  if (!input.files.length) {
    status.innerText = "Please select files.";
    return;
  }
  const formData = new FormData();
  for (const file of input.files) formData.append("files", file);
  status.innerText = "Processing documents...";
  try {
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    if (data.success) {
      status.innerText = `Knowledge base ready. ${data.documents} documents, ${data.chunks} chunks and ${data.vectors} vectors created.`;
      loadDocuments();
      loadStats();
    } else status.innerText = data.message;
  } catch (e) {
    status.innerText = "Upload failed.";
  }
}
async function loadDocuments() {
  const response = await fetch("/api/documents");
  const data = await response.json();
  ["summaryDocument", "documentA", "documentB"].forEach((id) => {
    const select = document.getElementById(id);
    if (!select) return;
    const first = select.options[0];
    select.innerHTML = "";
    select.appendChild(first);
    data.documents.forEach((name) => {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      select.appendChild(option);
    });
  });
}
async function summarize() {
  const document = document.getElementById("summaryDocument").value,
    result = document.getElementById("summaryResult");
  if (!document) {
    result.innerText = "Select a document.";
    return;
  }
  result.innerText = "Generating summary...";
  const response = await fetch("/api/summary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document }),
  });
  const data = await response.json();
  result.innerText = data.result;
}
async function compareDocuments() {
  const documentA = document.getElementById("documentA").value,
    documentB = document.getElementById("documentB").value,
    result = document.getElementById("compareResult");
  if (!documentA || !documentB) {
    result.innerText = "Select both documents.";
    return;
  }
  result.innerText = "Comparing documents...";
  const response = await fetch("/api/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_a: documentA, document_b: documentB }),
  });
  const data = await response.json();
  result.innerText = data.result;
}
async function analyzeDecision() {
  const situation = document.getElementById("situation").value.trim(),
    result = document.getElementById("decisionResult");
  if (!situation) {
    result.innerText = "Describe the business situation.";
    return;
  }
  result.innerText = "Analyzing decision...";
  const response = await fetch("/api/decision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ situation }),
  });
  const data = await response.json();
  result.innerText = data.answer;
}
async function loadStats() {
  const response = await fetch("/api/stats"),
    data = await response.json(),
    grid = document.getElementById("statsGrid");
  grid.innerHTML = "";
  [
    ["Status", data.status],
    ["Documents", data.documents],
    ["Sections", data.sections],
    ["Chunks", data.chunks],
    ["Vectors", data.vectors],
    ["Embedding Model", data.embedding_model],
    ["Reranker", data.reranker],
    ["LLM", data.llm],
  ].forEach((item) => {
    const card = document.createElement("div");
    card.className = "stat-card";
    card.innerHTML = `<span>${item[0]}</span><strong>${item[1]}</strong>`;
    grid.appendChild(card);
  });
}
document
  .getElementById("question")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  });
loadDocuments();
loadStats();
