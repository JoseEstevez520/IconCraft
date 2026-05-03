export type IconStyle = "Flat" | "Outline" | "Duotone" | "Gradient"

export const SIZES = [16, 24, 32, 48, 64, 128, 256] as const
export type IconSize = (typeof SIZES)[number]

export interface GenerateRequest {
  prompt: string
  style: IconStyle
  color: string
  size: IconSize
}

export interface GenerateResponse {
  svg: string
  size: number
}

export interface ChatRequest {
  message: string
}

export interface ChatResponse {
  reply: string
}

export interface HistoryItem {
  id: string
  svg: string
  prompt: string
  style: IconStyle
  color: string
  size: IconSize
  createdAt: string
}
