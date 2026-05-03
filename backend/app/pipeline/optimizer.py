import re


def _strip_comments(svg: str) -> str:
    return re.sub(r"<!--.*?-->", "", svg, flags=re.DOTALL)


def _collapse_whitespace(svg: str) -> str:
    svg = re.sub(r">\s+<", "><", svg)
    svg = re.sub(r"\s{2,}", " ", svg)
    svg = re.sub(r"\n\s*", "", svg)
    return svg.strip()


def _remove_unused_defs(svg: str) -> str:
    defs_pattern = re.compile(r"<defs>.*?</defs>", re.DOTALL)
    used_ids = set(re.findall(r'url\(#([^)]+)\)', svg))
    if used_ids:
        return svg

    return defs_pattern.sub("", svg)


def _round_coordinates(svg: str, precision: int = 2) -> str:
    def _round_match(m: re.Match) -> str:
        num = float(m.group(0))
        return f"{num:.{precision}f}".rstrip("0").rstrip(".")

    return re.sub(r"(?<!\w)-?\d+\.\d+", _round_match, svg)


async def optimize(svg: str) -> str:
    try:
        from scour.scour import parse_args, scourString

        options = parse_args([
            "--enable-comment-stripping",
            "--enable-id-stripping",
            "--shorten-ids",
            "--indent=none",
            "--strip-xml-prolog",
            "--remove-descriptive-elements",
            "--create-groups",
        ])
        result = scourString(svg, options)
        return str(result) if result is not None else _optimize_fallback(svg)
    except ImportError:
        return _optimize_fallback(svg)


def _optimize_fallback(svg: str) -> str:
    svg = _strip_comments(svg)
    svg = _remove_unused_defs(svg)
    svg = _round_coordinates(svg)
    svg = _collapse_whitespace(svg)
    return svg
