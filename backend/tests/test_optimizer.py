import pytest

from app.pipeline.optimizer import optimize


class TestOptimizer:
    @pytest.mark.anyio
    async def test_optimize_empty_svg(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
        result = await optimize(svg)
        assert "<svg" in result
        assert "xmlns" in result

    @pytest.mark.anyio
    async def test_optimize_strips_comments(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><!-- comment --><rect width="10" height="10"/></svg>'
        result = await optimize(svg)
        assert "<!--" not in result

    @pytest.mark.anyio
    async def test_optimize_removes_unused_defs(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g"/></defs><rect width="10" height="10"/></svg>'
        result = await optimize(svg)
        assert "<defs>" not in result

    @pytest.mark.anyio
    async def test_optimize_keeps_used_defs(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g"><stop offset="0%"/></linearGradient></defs><rect fill="url(#g)" width="10" height="10"/></svg>'
        result = await optimize(svg)
        assert "<defs>" in result

    @pytest.mark.anyio
    async def test_optimize_collapses_whitespace(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg">\n  <rect width="10" height="10"/>\n</svg>'
        result = await optimize(svg)
        leading_spaces = sum(1 for line in result.split("\n") if line.startswith("  "))
        assert leading_spaces == 0
        assert "width" in result and "height" in result
