const KEY="gs420-chat-cache";
export function loadMessages(){try{return JSON.parse(localStorage.getItem(KEY)||"[]")}catch{return []}}
export function saveMessages(messages){localStorage.setItem(KEY,JSON.stringify(messages.slice(-100)))}
