from typing import Any

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "generate_icon",
        "description": "Generate an SVG icon from a text description",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Description of the icon"},
                "style": {
                    "type": "string",
                    "enum": ["Flat", "Outline", "Duotone", "Gradient"],
                    "description": "Icon style",
                },
                "color": {
                    "type": "string",
                    "description": "Primary color in hex format",
                },
                "size": {
                    "type": "integer",
                    "description": "Icon size in pixels",
                    "enum": [16, 24, 32, 48, 64, 128, 256],
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "optimize_svg",
        "description": "Optimize an SVG string to reduce file size",
        "input_schema": {
            "type": "object",
            "properties": {
                "svg": {"type": "string", "description": "Raw SVG content"},
            },
            "required": ["svg"],
        },
    },
    {
        "name": "list_styles",
        "description": "List all available icon styles",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def get_tool_definitions() -> list[dict[str, Any]]:
    return TOOL_DEFINITIONS
