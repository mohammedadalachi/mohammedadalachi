import io

import requests
from PIL import Image, ImageDraw, ImageFilter

# Model: "Vegeta From Dragon Ball - Textured and Rigged" by Light.k
# License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
# Source: https://sketchfab.com/3d-models/none-41a0b494147e4bf4a3b2b2645d4156c6
IMAGE_URL = "https://media.sketchfab.com/models/41a0b494147e4bf4a3b2b2645d4156c6/thumbnails/745f801505674706aa85fd7246aa8925/f1cb31b734c14bc9936be8e4601f1cf7.jpeg"
response = requests.get(IMAGE_URL, timeout=30)
if response.status_code != 200:
    raise ConnectionError(f"Download failed with status: {response.status_code}")
image = Image.open(io.BytesIO(response.content)).convert("RGB")
scale = image.width / 720
image = image.crop((int(200 * scale), int(5 * scale), int(515 * scale), int(400 * scale)))
width, height = image.size
work = image.copy()
marker = (255, 0, 255)
for point in [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1), (width // 2, 0), (width // 2, height - 1)]:
    ImageDraw.floodfill(work, point, marker, thresh=16)
alpha = Image.new("L", (width, height), 255)
work_pixels = work.load()
alpha_pixels = alpha.load()
for y in range(height):
    for x in range(width):
        if work_pixels[x, y] == marker:
            alpha_pixels[x, y] = 0
alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
result = image.convert("RGBA")
result.putalpha(alpha)
result = result.crop(result.getbbox())
new_height = 252
result = result.resize((round(result.width * new_height / result.height), new_height), Image.LANCZOS)
result.save("saiyan/vegeta.png", optimize=True)
print(f"Saved saiyan/vegeta.png, size {result.size}")