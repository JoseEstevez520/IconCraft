import { useEffect, useState } from "react"

type Theme = "light" | "dark"

function getStoredTheme(): Theme {
  if (typeof window === "undefined") return "light"
  return (localStorage.getItem("theme") as Theme) || "light"
}

export function useTheme() {
  const [theme, setThemeState] = useState<Theme>(getStoredTheme)

  useEffect(() => {
    const root = document.documentElement
    root.classList.remove("light", "dark")
    root.classList.add(theme)
    localStorage.setItem("theme", theme)
  }, [theme])

  const toggleTheme = () => setThemeState((t) => (t === "dark" ? "light" : "dark"))

  return { theme, toggleTheme }
}
