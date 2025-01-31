from PIL import ImageEnhance, ImageFilter
from PIL.Image import Image
from PIL import Image as Img
from random import randint

def enhance_color(image: Image, factor: float) -> Image:
    if factor < 0:
        raise ValueError("Color enhancement factor must be greater than or equal to 0.")
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def enhance_contrast(image: Image, factor: float) -> Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def enhance_blur(image: Image, radius: float) -> Image:

    return image.filter(ImageFilter.GaussianBlur(radius))


def add_noise(image: Image, noise_factor: int = 30):

    noise = Img.new("RGB", image.size)
    px = image.load()

    for x in range(image.width):
        for y in range(image.height):
            r, g, b = px[x, y]
            r = min(255, max(0, r + randint(-noise_factor, noise_factor)))
            g = min(255, max(0, g + randint(-noise_factor, noise_factor)))
            b = min(255, max(0, b + randint(-noise_factor, noise_factor)))
            noise.putpixel((x,y),(r, g, b))

    return noise