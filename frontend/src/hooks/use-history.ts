import { useCallback, useSyncExternalStore } from "react"
import type { HistoryItem } from "@/types"

const STORAGE_KEY = "iconcraft-history"

let cached: HistoryItem[] = []
const listeners = new Set<() => void>()

function read(): HistoryItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as HistoryItem[]) : []
  } catch {
    return []
  }
}

function emit() {
  listeners.forEach((l) => l())
}

function subscribe(callback: () => void) {
  listeners.add(callback)

  const onStorage = (e: StorageEvent) => {
    if (e.key === STORAGE_KEY) {
      cached = read()
      emit()
    }
  }
  window.addEventListener("storage", onStorage)

  return () => {
    listeners.delete(callback)
    window.removeEventListener("storage", onStorage)
  }
}

function getSnapshot(): HistoryItem[] {
  return cached
}

export function useHistory() {
  const items = useSyncExternalStore(subscribe, getSnapshot, getSnapshot)

  const add = useCallback((item: Omit<HistoryItem, "id" | "createdAt">) => {
    const entry: HistoryItem = {
      ...item,
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
    }
    cached = [entry, ...read()].slice(0, 50)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cached))
    emit()
  }, [])

  const remove = useCallback((id: string) => {
    cached = read().filter((i) => i.id !== id)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cached))
    emit()
  }, [])

  const clear = useCallback(() => {
    cached = []
    localStorage.removeItem(STORAGE_KEY)
    emit()
  }, [])

  return { items, add, remove, clear }
}
