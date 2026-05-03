import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { ThemeToggle } from "@/components/theme-toggle"

describe("ThemeToggle", () => {
  it("renders the toggle button", () => {
    render(<ThemeToggle />)
    expect(screen.getByRole("button")).toBeInTheDocument()
  })

  it("renders with accessible label", () => {
    render(<ThemeToggle />)
    expect(screen.getByText("Toggle theme")).toBeInTheDocument()
  })
})
