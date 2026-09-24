import { Client } from "@gradio/client";

const API = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");
const GRADIO = (import.meta.env.VITE_GRADIO_URL || "").replace(/\/$/, "");
const RUNTIME = import.meta.env.VITE_RUNTIME_MODE || (GRADIO ? "gradio" : "fastapi");

async function request(path, options = {}) {
  if (!API) throw new Error("FastAPI URL is not configured. Set VITE_API_URL.");
  try {
    const response = await fetch(API + path, { ...options, signal: AbortSignal.timeout(30000) });
    if (!response.ok) throw new Error(`Backend HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    if (error?.name === "TimeoutError") throw new Error("Backend request timed out.");
    if (error instanceof TypeError) throw new Error("Backend unavailable or blocked by CORS.");
    throw error;
  }
}

let gradioClientPromise;
async function getGradioClient() {
  if (!GRADIO) throw new Error("ZeroGPU URL is not configured. Set VITE_GRADIO_URL.");
  if (!gradioClientPromise) {
    gradioClientPromise = Client.connect(GRADIO, {
      status_callback: (status) => console.info("GS420 ZeroGPU status:", status),
    });
  }
  return gradioClientPromise;
}

export async function health() {
  if (RUNTIME === "gradio") {
    const client = await getGradioClient();
    return { status: "ok", runtime: "gradio-zerogpu", endpoint: !!client };
  }
  return request("/health");
}

export async function chat(message, session_id, task) {
  if (RUNTIME === "gradio") {
    const client = await getGradioClient();
    const result = await client.predict("/chat", { message, session_id: session_id || null, task: task || null });
    return { answer: result.data, runtime: "gradio-zerogpu", model: "Auto" };
  }
  return request("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id, task }),
  });
}

export const plan = task => request("/api/agents/plan", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ task }),
});
export const searchDocuments = q => request("/api/documents/search?q=" + encodeURIComponent(q));
export const models = () => request("/api/models");
