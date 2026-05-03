from typing import Literal

Style = Literal["Flat", "Outline", "Duotone", "Gradient"]

STYLE_PROMPTS: dict[Style, str] = {
    "Flat": "flat vector icon, solid colors, no shading, minimal design, clean bold shapes",
    "Outline": "outline vector icon, thin strokes, line art style, transparent background, detailed contours",
    "Duotone": "duotone vector icon, two-color gradient style, transparent overlapping layers, modern dual-tone effect",
    "Gradient": "gradient vector icon, smooth color transitions, vibrant gradients, glossy modern finish",
}

QUALITY_SUFFIX = "centered, square aspect ratio, transparent background, high contrast, crisp edges, isolated on transparent, no text, professional icon design"


def build_prompt(description: str, style: Style = "Flat", color: str = "#1e1e1e") -> str:
    style_desc = STYLE_PROMPTS.get(style, STYLE_PROMPTS["Flat"])
    return f"{description}. {style_desc}. {QUALITY_SUFFIX}. Use {color} as primary color."
