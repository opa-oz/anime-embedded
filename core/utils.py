import textwrap

from PIL import Image, ImageFont
from PIL.Image import Image as ImageType
from pathlib import Path


def resize(img: ImageType, scale: float) -> ImageType:
    width, height = img.size

    return img.resize(
        (
            int(width * scale),
            int(height * scale)
        )
    )


def make_transparent(p: str or Path) -> ImageType:
    image = Image.open(p).convert("RGBA")

    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        image.putalpha(alpha)

    return image


def bruteforce(text, max_width, font, count=40):
    lines = textwrap.wrap(text, width=count)

    final_text = []

    for line in lines:
        width, height = font.getsize(line)

        if width >= max_width:
            return bruteforce(text, max_width, font, count - 10)
        else:
            final_text.append(line)

    return final_text


def find_suitable_fontsize(max_width: int, font: ImageFont, text: str, max_letters: int = 40) -> ImageFont:
    fontsize = 1
    font = ImageFont.truetype(font.path, fontsize)

    while font.getsize(text[0:max_letters])[0] < max_width:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font.path, fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    return ImageFont.truetype(font.path, fontsize)
