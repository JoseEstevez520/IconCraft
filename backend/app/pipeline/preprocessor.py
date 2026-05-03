from io import BytesIO

from PIL import Image, ImageFilter

SUPPORTED_FORMATS = {"PNG", "JPEG", "WEBP", "BMP", "GIF"}
TARGET_SIZE = 512


def load_image(data: bytes) -> Image.Image:
    img = Image.open(BytesIO(data))
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    return img


def remove_background(img: Image.Image) -> Image.Image:
    try:
        from rembg import remove

        return remove(img)
    except ImportError:
        img = img.convert("RGBA")
        pixels = img.load()
        if pixels:
            edge_pixel = pixels[0, 0]
            threshold = 240
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = pixels[x, y]
                    if r > threshold and g > threshold and b > threshold:
                        pixels[x, y] = (r, g, b, 0)
        return img


def resize(img: Image.Image, size: int = TARGET_SIZE) -> Image.Image:
    original = img.size
    ratio = size / max(original)
    if ratio >= 1:
        return img
    new_size = (int(original[0] * ratio), int(original[1] * ratio))
    return img.resize(new_size, Image.LANCZOS)


def sharpen(img: Image.Image) -> Image.Image:
    return img.filter(ImageFilter.SHARPEN)


async def process_image(data: bytes) -> Image.Image:
    img = load_image(data)
    img = remove_background(img)
    img = resize(img)
    img = sharpen(img)
    return img
