import base64

from PIL import Image, ImageOps

def preprocess_for_white_text(image_path):
    img = Image.open(image_path).convert('L')  # grayscale
    img = ImageOps.invert(img)  # white → black
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            if pixels[x, y] <= 55:  # pure black
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255
    img.save("temp/temp1.png")

    return "temp/temp1.png"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")