import React, { useEffect, useState } from "react";
import { chat, plan, searchDocuments, models, health } from "./services/api";
import { loadMessages, saveMessages } from "./stores/offline";

const tabs = ["Chat", "Coding", "Vision", "Image", "Video", "Voice", "Agents", "Documents", "Memory", "Settings"];

export default function App() {
  const [tab, setTab] = useState("Chat");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState(loadMessages());
  const [busy, setBusy] = useState(false);
  const [modelList, setModelList] = useState([]);
  const [runtime, setRuntime] = useState("CHECKING");
  const [backendError, setBackendError] = useState("");

  useEffect(() => saveMessages(messages), [messages]);

  useEffect(() => {
    health().then((r) => {
      setRuntime(r.runtime === "gradio-zerogpu" ? "ONLINE AI · ZeroGPU" : "ONLINE AI · FastAPI");
      setBackendError("");
    }).catch((e) => {
      setRuntime("OFFLINE/FALLBACK");
      setBackendError(e.message);
    });
    if ((import.meta.env.VITE_RUNTIME_MODE || "fastapi") !== "gradio") {
      models().then(setModelList).catch(() => {});
    }
  }, []);

  async function send() {
    if (!input.trim() || busy) return;
    const q = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", text: q }]);
    setBusy(true);
    try {
      const r = tab === "Agents" ? await plan(q) : tab === "Documents" ? await searchDocuments(q) : await chat(q);
      setMessages((m) => [...m, { role: "assistant", text: typeof r.answer === "string" ? r.answer : JSON.stringify(r, null, 2) }]);
      setBackendError("");
    } catch (e) {
      setRuntime("OFFLINE/FALLBACK");
      setBackendError(e.message);
      setMessages((m) => [...m, { role: "system", text: "AI runtime unavailable: " + e.message }]);
    } finally {
      setBusy(false);
    }
  }

  return <main>
    <header>
      <div><h1>GS420 AI</h1><p>Model: Auto · Memory: Enabled · {modelList.length || "—"} registered models</p></div>
      <span>{runtime}</span>
    </header>
    {backendError && <div className="error" role="alert">{backendError}</div>}
    <nav>{tabs.map((x) => <button className={tab === x ? "active" : ""} onClick={() => setTab(x)} key={x}>{x}</button>)}</nav>
    <section className="panel">
      <h2>{tab}</h2>
      {tab === "Settings" && <pre>{JSON.stringify(modelList, null, 2)}</pre>}
      <div className="messages">{messages.map((m, i) => <article className={m.role} key={i}>{m.text}</article>)}</div>
      <textarea value={input} onChange={(e) => setInput(e.target.value)} placeholder={tab === "Documents" ? "Search documents…" : "Ask anything…"}/>
      <button onClick={send} disabled={busy}>{busy ? "Processing…" : "Send"}</button>
    </section>
  </main>;
}
