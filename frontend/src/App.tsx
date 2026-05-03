import { useState, useRef, useEffect } from "react"
import { Toaster, toast } from "sonner"
import DOMPurify from "dompurify"
import { MarkdownRenderer } from "@/components/markdown-renderer"
import { ErrorBoundary } from "@/components/error-boundary"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { ThemeToggle } from "@/components/theme-toggle"
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip"
import { useHistory } from "@/hooks/use-history"
import { generateIcon, chat } from "@/lib/api"
import type { IconStyle, IconSize, HistoryItem } from "@/types"
import {
  Sparkles,
  Palette,
  History,
  Download,
  Copy,
  Trash2,
  Maximize2,
  ZoomIn,
  ZoomOut,
  MessageSquare,
  Send,
  X,
  Loader2,
  Plus,
} from "lucide-react"

const SIZES = [16, 24, 32, 48, 64, 128, 256] as const
const STYLES = ["Flat", "Outline", "Duotone", "Gradient"] as const
const COLORS = ["#000000", "#2563eb", "#059669", "#d97706", "#dc2626", "#7c3aed"] as const
const SUGGESTIONS = ["home icon", "user avatar", "settings gear", "search", "shopping cart", "heart", "bell", "cloud", "star", "mail"]

function sanitize(svg: string): string {
  return DOMPurify.sanitize(svg, { USE_PROFILES: { svg: true, svgFilters: true } }) as string
}

function App() {
  const [prompt, setPrompt] = useState("")
  const [size, setSize] = useState<IconSize>(64)
  const [style, setStyle] = useState<IconStyle>("Flat")
  const [color, setColor] = useState("#000000")
  const [colorInput, setColorInput] = useState("#000000")
  const [svg, setSvg] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [chatOpen, setChatOpen] = useState(false)
  const [chatMsg, setChatMsg] = useState("")
  const [chatReplies, setChatReplies] = useState<{ role: "user" | "assistant"; text: string }[]>([])
  const [chatLoading, setChatLoading] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [zoom, setZoom] = useState(1)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const { items: historyItems, add: addHistory, remove: removeHistory, clear: clearHistory } = useHistory()

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }) }, [chatReplies, chatLoading])

  function handleZoomIn() { setZoom((z) => Math.min(z + 0.25, 4)) }
  function handleZoomOut() { setZoom((z) => Math.max(z - 0.25, 0.25)) }
  function handleZoomFit() { setZoom(1) }

  async function handleGenerate() {
    if (!prompt.trim()) return
    setLoading(true)
    setSvg(null)
    try {
      const res = await generateIcon({ prompt: prompt.trim(), style, color, size })
      setSvg(sanitize(res.svg))
      addHistory({ svg: res.svg, prompt: prompt.trim(), style, color, size })
      toast.success("Icon generated")
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Generation failed")
    } finally {
      setLoading(false)
    }
  }

  async function handleSendChat() {
    if (!chatMsg.trim()) return
    const text = chatMsg.trim()
    setChatMsg("")
    setChatReplies((p) => [...p, { role: "user", text }])
    setChatLoading(true)
    try {
      const res = await chat({ message: text })
      setChatReplies((p) => [...p, { role: "assistant", text: res.reply }])
    } catch {
      setChatReplies((p) => [...p, { role: "assistant", text: "Sorry, something went wrong." }])
    } finally {
      setChatLoading(false)
    }
  }

  function handleDownload() {
    if (!svg) { toast.error("Generate an icon first"); return }
    const blob = new Blob([svg], { type: "image/svg+xml" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `icon-${prompt.slice(0, 20).replace(/\s+/g, "-")}.svg`
    a.click()
    URL.revokeObjectURL(url)
  }

  async function handleCopy() {
    if (!svg) { toast.error("Generate an icon first"); return }
    try {
      await navigator.clipboard.writeText(svg)
      toast.success("Copied to clipboard")
    } catch {
      toast.error("Failed to copy")
    }
  }

  function handleSelectHistory(item: HistoryItem) {
    setSvg(sanitize(item.svg))
    setPrompt(item.prompt)
    setStyle(item.style)
    setColor(item.color)
    setColorInput(item.color)
    setSize(item.size)
    setHistoryOpen(false)
    toast.success("History item restored")
  }

  function handleColorChange(hex: string) {
    setColorInput(hex)
    if (/^#[0-9a-fA-F]{6}$/.test(hex)) setColor(hex)
  }

  return (
    <TooltipProvider>
      <div className="flex h-screen flex-col bg-background">
        <Toaster position="bottom-right" richColors />

        {/* Header */}
        <header className="flex h-10 items-center justify-between border-b bg-background px-5">
          <div className="flex items-center gap-2.5">
            <div className="flex h-5 w-5 items-center justify-center rounded bg-primary">
              <Palette className="h-3 w-3 text-primary-foreground" />
            </div>
            <span className="text-xs font-semibold">IconCraft</span>
          </div>
          <div className="flex items-center gap-1">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => setChatOpen(!chatOpen)}>
                  <MessageSquare className="h-3.5 w-3.5 text-muted-foreground" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="bottom">Chat</TooltipContent>
            </Tooltip>
            <ThemeToggle />
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => { setSvg(null); setPrompt("") }}>
                  <Plus className="h-3.5 w-3.5 text-muted-foreground" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="bottom">New</TooltipContent>
            </Tooltip>
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          {/* Left sidebar */}
          <aside className="flex w-64 shrink-0 flex-col bg-muted/20">
            <div className="flex flex-1 flex-col gap-4 p-5">
              {/* Prompt */}
              <div>
                <div className="relative">
                  <Sparkles className="absolute left-3 top-3.5 h-4 w-4 text-muted-foreground" />
                  <textarea
                    value={prompt}
                    onChange={(e) => { setPrompt(e.target.value); e.target.style.height = "auto"; e.target.style.height = e.target.scrollHeight + "px" }}
                    placeholder="Describe your icon..."
                    rows={3}
                    className="min-h-[80px] w-full resize-none rounded-lg border border-input bg-background px-3 py-3 pl-9 text-sm placeholder:text-muted-foreground/50 focus:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                    onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) handleGenerate() }}
                  />
                </div>
              </div>

              {/* Suggestions */}
              <div>
                <p className="mb-2 text-[11px] font-medium text-muted-foreground/70">Suggestions</p>
                <div className="flex flex-wrap gap-1.5">
                  {SUGGESTIONS.slice(0, 6).map((s) => (
                    <button
                      key={s}
                      onClick={() => setPrompt(s)}
                      className="rounded-md bg-muted/60 px-2.5 py-1 text-[12px] text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              <Separator className="bg-border/50" />

              <Button
                className="w-full gap-2 bg-primary text-primary-foreground shadow-sm hover:bg-primary/90"
                disabled={!prompt.trim() || loading}
                onClick={handleGenerate}
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                {loading ? "Generating..." : "Generate"}
              </Button>

              <Dialog open={historyOpen} onOpenChange={setHistoryOpen}>
                <DialogTrigger asChild>
                  <Button variant="ghost" size="sm" className="w-full gap-2 text-muted-foreground">
                    <History className="h-4 w-4" />
                    History
                    {historyItems.length > 0 && (
                      <span className="ml-auto rounded-full bg-muted px-1.5 py-0.5 text-[10px] font-medium">{historyItems.length}</span>
                    )}
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-md">
                  <DialogHeader>
                    <DialogTitle>History</DialogTitle>
                  </DialogHeader>
                  <div className="flex max-h-80 flex-col gap-2 overflow-y-auto">
                    {historyItems.length === 0 && (
                      <p className="py-8 text-center text-sm text-muted-foreground">No icons generated yet</p>
                    )}
                    {historyItems.map((item) => (
                      <div
                        key={item.id}
                        className="flex cursor-pointer items-center gap-3 rounded-lg border p-2.5 transition-colors hover:bg-muted/50"
                        onClick={() => handleSelectHistory(item)}
                      >
                        <div
                          className="flex size-10 shrink-0 items-center justify-center overflow-hidden rounded-md border bg-muted"
                          dangerouslySetInnerHTML={{ __html: sanitize(item.svg) }}
                        />
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-medium">{item.prompt}</p>
                          <p className="text-xs text-muted-foreground">{item.style} &middot; {item.size}&times;{item.size}</p>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="size-7 shrink-0 text-muted-foreground hover:text-foreground"
                          onClick={(e) => { e.stopPropagation(); removeHistory(item.id) }}
                        >
                          <X className="size-3" />
                        </Button>
                      </div>
                    ))}
                  </div>
                  {historyItems.length > 0 && (
                    <Button variant="outline" size="sm" className="w-full" onClick={clearHistory}>
                      <Trash2 className="mr-2 h-3.5 w-3.5" />
                      Clear all
                    </Button>
                  )}
                </DialogContent>
              </Dialog>
            </div>
          </aside>

          {/* Canvas */}
          <main className="flex flex-1 flex-col bg-muted/10 p-6">
            <div className="flex w-full flex-1 items-center justify-center rounded-xl border bg-card shadow-sm">
              {loading ? (
                <div className="flex flex-col items-center gap-4">
                  <div className="relative flex items-center justify-center" style={{ width: size * 2, height: size * 2 }}>
                    <Skeleton className="absolute inset-0 rounded-lg" />
                    <Loader2 className="relative h-6 w-6 animate-spin text-muted-foreground" />
                  </div>
                  <Skeleton className="h-4 w-20 rounded-md" />
                </div>
              ) : svg ? (
                <div
                  className="flex items-center justify-center transition-transform duration-200"
                  style={{ width: size * 2, height: size * 2, transform: `scale(${zoom})` }}
                >
                  <div
                    className="flex items-center justify-center"
                    style={{ width: size, height: size }}
                    dangerouslySetInnerHTML={{ __html: sanitize(svg) }}
                  />
                </div>
              ) : (
                <div className="flex flex-col items-center gap-4">
                  <div
                    className="flex items-center justify-center rounded-xl border-2 border-dashed border-border bg-muted/20"
                    style={{ width: 180, height: 180 }}
                  >
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="hsl(240 4% 46% / 0.35)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="px-2 py-0.5 text-[11px] font-normal">{style}</Badge>
                    <span className="text-xs tabular-nums text-muted-foreground">{size}&times;{size}px</span>
                  </div>
                </div>
              )}
            </div>

            {/* Toolbar */}
            <div className="mt-3 flex items-center justify-center">
              <div className="inline-flex items-center gap-0.5 rounded-lg border bg-card px-1 py-1 shadow-sm">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground" onClick={handleZoomOut}>
                      <ZoomOut className="h-3.5 w-3.5" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="top">Zoom out</TooltipContent>
                </Tooltip>
                <button onClick={handleZoomFit} className="min-w-9 rounded px-1 py-0.5 text-xs tabular-nums text-muted-foreground transition-colors hover:text-foreground select-none">
                  {Math.round(zoom * 100)}%
                </button>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground" onClick={handleZoomIn}>
                      <ZoomIn className="h-3.5 w-3.5" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="top">Zoom in</TooltipContent>
                </Tooltip>
                <Separator orientation="vertical" className="mx-1 h-4 bg-border/50" />
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground" onClick={handleZoomFit}>
                      <Maximize2 className="h-3.5 w-3.5" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="top">Fit</TooltipContent>
                </Tooltip>
                <Separator orientation="vertical" className="mx-1 h-4 bg-border/50" />
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground" disabled={!svg} onClick={handleCopy}>
                      <Copy className="h-3.5 w-3.5" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="top">Copy SVG</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground" disabled={!svg} onClick={handleDownload}>
                      <Download className="h-3.5 w-3.5" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="top">Download SVG</TooltipContent>
                </Tooltip>
              </div>
            </div>

          </main>

          {/* Right sidebar */}
          <aside className="flex w-56 shrink-0 flex-col bg-muted/20 p-5">
            <h3 className="mb-5 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground/60">Properties</h3>

            <div className="space-y-5">
              {/* Size */}
              <div>
                <label className="mb-2 block text-[11px] font-medium text-muted-foreground/70">Size</label>
                <div className="flex flex-wrap gap-1">
                  {SIZES.filter(s => s >= 24).map((s) => (
                    <button
                      key={s}
                      onClick={() => setSize(s)}
                      className={`rounded-md px-2 py-1 text-xs font-medium transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-ring ${
                        size === s
                          ? "bg-primary text-primary-foreground shadow-sm"
                          : "bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground"
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              <Separator className="bg-border/50" />

              {/* Style */}
              <div>
                <label className="mb-2 block text-[11px] font-medium text-muted-foreground/70">Style</label>
                <div className="grid grid-cols-2 gap-1.5">
                  {STYLES.map((s) => (
                    <button
                      key={s}
                      onClick={() => setStyle(s)}
                      className={`rounded-md px-2 py-1.5 text-xs font-medium transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-ring ${
                        style === s
                          ? "bg-primary text-primary-foreground shadow-sm"
                          : "bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground"
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              <Separator className="bg-border/50" />

              {/* Color */}
              <div>
                <label className="mb-2 block text-[11px] font-medium text-muted-foreground/70">Color</label>
                <div className="flex flex-wrap gap-1.5">
                  {COLORS.map((c) => (
                    <button
                      key={c}
                      onClick={() => { setColor(c); setColorInput(c) }}
                      className={`h-5 w-5 rounded-full border transition-all hover:scale-110 focus:outline-none focus-visible:ring-2 focus-visible:ring-ring ${
                        color === c ? "scale-110 border-primary ring-2 ring-primary/20" : "border-border"
                      }`}
                      style={{ backgroundColor: c }}
                    />
                  ))}
                </div>
                <div className="relative mt-2">
                  <span className="absolute left-2 top-1/2 -translate-y-1/2 text-xs text-muted-foreground/50">#</span>
                  <input
                    value={colorInput.replace("#", "")}
                    onChange={(e) => handleColorChange("#" + e.target.value)}
                    className="h-7 w-full rounded-md border border-input bg-background pl-4 pr-2 text-xs font-mono focus:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                    placeholder="000000"
                    maxLength={6}
                  />
                </div>
              </div>
              <Separator className="bg-border/50" />
              <div className="flex flex-col gap-2">
                <Button variant="default" size="sm" className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90" onClick={handleDownload}>
                  <Download className="h-4 w-4" />
                  Export SVG
                </Button>
                <Button variant="ghost" size="sm" className="w-full gap-2 text-muted-foreground" onClick={handleCopy}>
                  <Copy className="h-4 w-4" />
                  Copy code
                </Button>
              </div>
            </div>
          </aside>
        </div>

        {/* Chat */}
        {chatOpen && (
          <div className="fixed bottom-4 right-4 z-50 flex w-80 flex-col rounded-xl border bg-card shadow-lg">
            <div className="flex items-center justify-between border-b px-4 py-2.5">
              <div className="flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-primary" />
                <span className="text-xs font-semibold">Assistant</span>
              </div>
              <Button variant="ghost" size="icon" className="h-6 w-6 text-muted-foreground" onClick={() => setChatOpen(false)}>
                <X className="h-3.5 w-3.5" />
              </Button>
            </div>
            <div className="flex h-64 flex-col gap-3 overflow-y-auto p-4">
              {chatReplies.length === 0 && (
                <div className="mt-8 space-y-2 text-center">
                  <MessageSquare className="mx-auto h-5 w-5 text-muted-foreground/30" />
                  <p className="text-xs text-muted-foreground/60">Ask me anything</p>
                </div>
              )}
              {chatReplies.map((r, i) => (
                <div key={i} className={`flex ${r.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[85%] rounded-xl px-3 py-2 text-xs leading-relaxed ${
                      r.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted text-foreground"
                    }`}
                  >
                    {r.role === "user" ? (
                      r.text
                    ) : (
                      <ErrorBoundary fallback={<span>{r.text}</span>}>
                        <MarkdownRenderer content={r.text} />
                      </ErrorBoundary>
                    )}
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="flex justify-start">
                  <div className="rounded-xl bg-muted px-4 py-3">
                    <div className="flex gap-1">
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground/50" style={{ animationDelay: "0ms" }} />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground/50" style={{ animationDelay: "150ms" }} />
                      <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground/50" style={{ animationDelay: "300ms" }} />
                    </div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="flex items-center gap-2 border-t p-3">
              <Input
                value={chatMsg}
                onChange={(e) => setChatMsg(e.target.value)}
                placeholder="Type a message..."
                className="h-9 text-xs"
                onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSendChat() } }}
              />
              <Button variant="default" size="icon" className="h-9 w-9 shrink-0 bg-primary text-primary-foreground hover:bg-primary/90" onClick={handleSendChat} disabled={!chatMsg.trim() || chatLoading}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>
    </TooltipProvider>
  )
}

export default App
