import pytest

from app.pipeline.prompt_builder import build_prompt, STYLE_PROMPTS


class TestPromptBuilder:
    def test_build_prompt_default_style(self):
        result = build_prompt("a home icon")
        assert "a home icon" in result
        assert STYLE_PROMPTS["Flat"] in result
        assert "#1e1e1e" in result

    def test_build_prompt_outline(self):
        result = build_prompt("a star", "Outline", "#ff0000")
        assert "a star" in result
        assert STYLE_PROMPTS["Outline"] in result
        assert "#ff0000" in result

    def test_build_prompt_unknown_style_falls_back_to_flat(self):
        result = build_prompt("test", "UnknownStyle")  # type: ignore
        assert STYLE_PROMPTS["Flat"] in result

    def test_all_styles_defined(self):
        for style in ("Flat", "Outline", "Duotone", "Gradient"):
            assert style in STYLE_PROMPTS
            assert STYLE_PROMPTS[style]
