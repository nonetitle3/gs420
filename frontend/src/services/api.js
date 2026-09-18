const API=import.meta.env.VITE_API_URL||"";
async function request(path,options={}){const r=await fetch(API+path,options);if(!r.ok)throw new Error("HTTP "+r.status);return r.json()}
export const chat=(message,session_id,task)=>request("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message,session_id,task})});
export const plan=task=>request("/api/agents/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({task})});
export const searchDocuments=q=>request("/api/documents/search?q="+encodeURIComponent(q));
export const models=()=>request("/api/models");
