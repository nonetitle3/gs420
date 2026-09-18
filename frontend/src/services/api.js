const API=import.meta.env.VITE_API_URL||"";
export async function chat(message,session_id){const r=await fetch(API+"/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message,session_id})});if(!r.ok)throw new Error("HTTP "+r.status);return r.json();}
export async function uploadDocument(file){const f=new FormData();f.append("file",file);const r=await fetch(API+"/api/documents/upload",{method:"POST",body:f});if(!r.ok)throw new Error("HTTP "+r.status);return r.json();}
