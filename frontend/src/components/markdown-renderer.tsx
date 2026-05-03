export function MarkdownRenderer({ content }: { content: string }) {
  const html = content
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre class="my-1 rounded-md bg-muted-foreground/10 p-2 text-xs overflow-x-auto"><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code class="rounded bg-muted-foreground/10 px-1 py-0.5 text-xs">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/^### (.+)$/gm, "<strong class='block text-xs font-semibold'>$1</strong>")
    .replace(/^## (.+)$/gm, "<strong class='block text-sm font-semibold'>$1</strong>")
    .replace(/^# (.+)$/gm, "<strong class='block text-base font-semibold'>$1</strong>")
    .replace(/^- (.+)$/gm, '<span class="block pl-3 -indent-3">$1</span>')
    .replace(/^\d+\. (.+)$/gm, '<span class="block pl-3 -indent-3">$1</span>')
    .replace(/\n/g, "<br/>")

  return <span dangerouslySetInnerHTML={{ __html: html }} />
}
