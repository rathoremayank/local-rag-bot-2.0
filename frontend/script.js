const BACKEND = "http://localhost:8000";

async function post(url, data) {
  let res = await fetch(BACKEND + url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });
  return res.json();
}

async function ingest() {
  let path = document.getElementById("docsPath").value || null;
  document.getElementById("ingestStatus").textContent = "Ingesting...";
  let res = await post("/ingest", {docs_path: path});
  document.getElementById("ingestStatus").textContent = JSON.stringify(res, null, 2);
}

async function ask() {
  let q = document.getElementById("question").value;
  let k = parseInt(document.getElementById("topK").value);
  document.getElementById("answer").textContent = "Thinking...";
  let res = await post("/query", {question: q, k: k});
  document.getElementById("answer").textContent = res.answer;
  let ul = document.getElementById("sources");
  ul.innerHTML = "";
  (res.sources || []).forEach(s => {
    let li = document.createElement("li");
    li.textContent = `${s.source} (chunk ${s.chunk_id})`;
    ul.appendChild(li);
  });
}
