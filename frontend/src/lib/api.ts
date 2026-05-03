import type { GenerateRequest, GenerateResponse, ChatRequest, ChatResponse } from "@/types"

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

async function request<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? `Request failed: ${res.status}`)
  }
  return res.json()
}

export async function generateIcon(req: GenerateRequest): Promise<GenerateResponse> {
  return request<GenerateResponse>("/api/generate", req)
}

export async function chat(req: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat", req)
}

export async function healthCheck(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`)
    return res.ok
  } catch {
    return false
  }
}
