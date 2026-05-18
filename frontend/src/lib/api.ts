const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8765";
const FETCH_TIMEOUT = 5000; // 5 second timeout

async function fetchWithTimeout(url: string, options: RequestInit = {}): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    return res;
  } finally {
    clearTimeout(timer);
  }
}

// Retry fetch up to maxRetries times with delay
async function fetchRetry(url: string, options: RequestInit = {}, maxRetries = 3, delayMs = 2000): Promise<Response> {
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fetchWithTimeout(url, options);
    } catch (e) {
      if (i === maxRetries) throw e;
      await new Promise(r => setTimeout(r, delayMs));
    }
  }
  throw new Error("unreachable");
}

export interface CatalogApp {
  app_id: string;
  name: string;
  tagline: string;
  description: string;
  icon: string;
  category: string;
  color: string;
  author: string;
  is_builtin: boolean;
}

export interface InstalledApp {
  id: number;
  app_id: string;
  display_name: string;
  icon: string;
  category: string;
  color: string;
  installed_at: string;
}

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatSession {
  session_id: string;
  created_at: string;
  message_count: number;
  preview: string;
}

export async function waitForBackend(maxWaitMs = 15000): Promise<boolean> {
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    try {
      const res = await fetchWithTimeout(`${API_BASE}/api/health`);
      if (res.ok) return true;
    } catch {
      // not ready yet
    }
    await new Promise(r => setTimeout(r, 800));
  }
  return false;
}

export async function fetchCatalog(): Promise<CatalogApp[]> {
  const res = await fetchRetry(`${API_BASE}/api/apps/catalog`);
  if (!res.ok) throw new Error(`Failed to fetch catalog: ${res.statusText}`);
  return res.json();
}

export async function fetchInstalled(): Promise<InstalledApp[]> {
  const res = await fetchRetry(`${API_BASE}/api/apps/installed`);
  if (!res.ok) throw new Error(`Failed to fetch installed: ${res.statusText}`);
  return res.json();
}

export async function installApp(appId: string): Promise<any> {
  const res = await fetchWithTimeout(`${API_BASE}/api/apps/install?app_id=${appId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Failed to install: ${res.statusText}`);
  return res.json();
}

export async function uninstallApp(appId: string): Promise<any> {
  const res = await fetchWithTimeout(`${API_BASE}/api/apps/uninstall?app_id=${appId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Failed to uninstall: ${res.statusText}`);
  return res.json();
}

export async function sendChatMessage(
  appId: string,
  message: string,
  sessionId?: string
): Promise<Response> {
  const res = await fetchWithTimeout(`${API_BASE}/api/chat/send`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ app_id: appId, message, session_id: sessionId || undefined }),
  });
  return res;
}

export async function fetchChatSessions(appId: string): Promise<ChatSession[]> {
  const res = await fetchWithTimeout(`${API_BASE}/api/chat/sessions/${appId}`);
  if (!res.ok) throw new Error(`Failed to fetch sessions: ${res.statusText}`);
  return res.json();
}

export async function fetchChatHistory(appId: string, sessionId: string): Promise<{ messages: ChatMessage[] }> {
  const res = await fetchWithTimeout(`${API_BASE}/api/chat/history/${appId}/${sessionId}`);
  if (!res.ok) throw new Error(`Failed to fetch history: ${res.statusText}`);
  return res.json();
}