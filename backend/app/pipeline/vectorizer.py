from io import BytesIO

from PIL import Image

TARGET_SIZE = 256
GRADIENT_STEPS = 8


def _to_bilevel(img: Image.Image, threshold: int = 128) -> Image.Image:
    gray = img.convert("L")
    return gray.point(lambda x: 255 if x > threshold else 0, mode="1")


async def vectorize(img: Image.Image) -> str:
    img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)
    try:
        import vtracer

        bw = _to_bilevel(img)
        buf = BytesIO()
        bw.save(buf, format="PNG")
        buf.seek(0)

        svg_bytes = vtracer.convert_image_to_svg_py(
            buf.read(),
            colormode="binary",
            hierarchy="stacked",
            mode="spline",
            filter_speckle=4,
            color_precision=6,
            layer_difference=16,
            corner_threshold=60,
            length_threshold=4.0,
            max_iterations=10,
            splice_threshold=45,
            path_precision=8,
        )
        return svg_bytes.decode("utf-8") if isinstance(svg_bytes, bytes) else svg_bytes
    except ImportError:
        return _fallback_svg(img)


def _fallback_svg(img: Image.Image) -> str:
    w, h = img.size
    paths = []
    threshold = 128
    pixels = img.convert("L").load()
    if not pixels:
        return _empty_svg(w, h)

    visited = [[False] * h for _ in range(w)]

    for y in range(h):
        for x in range(w):
            if pixels[x, y] < threshold and not visited[x][y]:
                x0, y0 = x, y
                x1, y1 = x + 1, y + 1

                stack = [(x, y)]
                visited[x][y] = True
                while stack:
                    cx, cy = stack.pop()
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny] and pixels[nx, ny] < threshold:
                            visited[nx][ny] = True
                            x0 = min(x0, nx)
                            y0 = min(y0, ny)
                            x1 = max(x1, nx + 1)
                            y1 = max(y1, ny + 1)
                            stack.append((nx, ny))

                paths.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="currentColor"/>')

    return _wrap_svg(w, h, paths)


def _wrap_svg(w: int, h: int, paths: list[str]) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{"".join(paths)}</svg>'


def _empty_svg(w: int, h: int) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"/>'
