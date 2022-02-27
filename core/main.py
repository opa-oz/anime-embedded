from typing import Optional, Union, Tuple
from colour import Color
from PIL import ImageFont, Image, ImageDraw
from PIL.Image import Image as ImageType
from pathlib import Path
import re

from core.utils import bruteforce, find_suitable_fontsize

DEFAULT_MAX_TEXT_WIDTH = 500
DEFAULT_MAX_HEADER_WIDTH = 730

DEFAULT_PADDING = 70
DEFAULT_BOTTOM_PADDING = 45

DEFAULT_TEXT_COLOR = Color('#ffffff')

DEFAULT_HEADER_FONTSIZE = 64
DEFAULT_MAIN_FONTSIZE = 40
DEFAULT_TEXT_FONTSIZE = 32
DEFAULT_SMALL_TEXT_FONTSIZE = 20
DEFAULT_SUBHEADER_FONTSIZE = 32

DEFAULT_LENGTH = 40

DEFAULT_FONT = 'arial.ttf'

ru_re = re.compile(r'^[а-яёА-ЯЁ\s]+$')


class Config:
    max_text_width: int
    max_header_width: int

    length: int

    text_color: Color

    padding: int
    bottom_padding: int

    header_fontsize: int
    header_font: ImageFont

    subheader_fontsize: int
    subheader_font: ImageFont

    main_fontsize: int
    main_font: ImageFont

    text_fontsize: int
    text_font: ImageFont

    small_text_fontsize: int
    small_text_font: ImageFont

    background: ImageType

    logo_first_part: Optional[ImageType]
    logo_second_part: Optional[ImageType]

    sub_image: Optional[ImageType]

    site: str

    def __init__(
        self,
        max_text_width: int = DEFAULT_MAX_TEXT_WIDTH,
        max_header_width: int = DEFAULT_MAX_HEADER_WIDTH,
        text_color: int or Color = DEFAULT_TEXT_COLOR,
        padding: int = DEFAULT_PADDING,
        bottom_padding: int = DEFAULT_BOTTOM_PADDING,
        header_fontsize: int = DEFAULT_HEADER_FONTSIZE,
        header_font: str or Path = DEFAULT_FONT,
        subheader_fontsize: int = DEFAULT_SUBHEADER_FONTSIZE,
        subheader_font: str or Path = DEFAULT_FONT,
        main_fontsize: int = DEFAULT_MAIN_FONTSIZE,
        main_font: str or Path = DEFAULT_FONT,
        text_fontsize: int = DEFAULT_TEXT_FONTSIZE,
        text_font: str or Path = DEFAULT_FONT,
        small_text_fontsize: int = DEFAULT_SMALL_TEXT_FONTSIZE,
        small_text_font: str or Path = DEFAULT_FONT,
        background: str or Path or ImageType = None,
        logo_first_part: str or Path or ImageType = None,
        logo_second_part: str or Path or ImageType = None,
        sub_image: str or Path or ImageType = None,
        site: str = '',
        length: int = DEFAULT_LENGTH
    ):
        self.max_text_width = max_text_width
        self.max_header_width = max_header_width

        if isinstance(text_color, Color):
            self.text_color = text_color
        elif isinstance(text_color, str):
            self.text_color = Color(text_color)

        self.padding = padding
        self.bottom_padding = bottom_padding

        self.header_fontsize = header_fontsize

        if isinstance(header_font, Path):
            header_font = str(header_font)

        self.header_font = ImageFont.truetype(header_font, size=self.header_fontsize)

        self.subheader_fontsize = subheader_fontsize

        if isinstance(subheader_font, Path):
            subheader_font = str(subheader_font)

        self.subheader_font = ImageFont.truetype(subheader_font, size=self.subheader_fontsize)

        self.main_fontsize = main_fontsize

        if isinstance(main_font, Path):
            main_font = str(main_font)

        self.main_font = ImageFont.truetype(main_font, size=self.main_fontsize)

        self.text_fontsize = text_fontsize

        if isinstance(text_font, Path):
            text_font = str(text_font)

        self.text_font = ImageFont.truetype(text_font, size=self.text_fontsize)

        self.small_text_fontsize = small_text_fontsize

        if isinstance(small_text_font, Path):
            small_text_font = str(small_text_font)

        self.small_text_font = ImageFont.truetype(small_text_font, size=self.small_text_fontsize)

        self.length = length

        if background is not None:
            if isinstance(background, ImageType):
                self.background = background
            else:
                if isinstance(background, Path):
                    background = str(background)
                self.background = Image.open(background)

        if logo_first_part is not None:
            if isinstance(logo_first_part, ImageType):
                self.logo_first_part = logo_first_part
            else:
                if isinstance(logo_first_part, Path):
                    logo_first_part = str(logo_first_part)
                self.logo_first_part = Image.open(logo_first_part)
        else:
            self.logo_first_part = None

        if logo_second_part is not None:
            if isinstance(logo_second_part, ImageType):
                self.logo_second_part = logo_second_part
            else:
                if isinstance(logo_second_part, Path):
                    logo_second_part = str(logo_second_part)
                self.logo_second_part = Image.open(logo_second_part)
        else:
            self.logo_second_part = None

        if sub_image is not None:
            if isinstance(sub_image, ImageType):
                self.sub_image = sub_image
            else:
                if isinstance(sub_image, Path):
                    sub_image = str(sub_image)
                self.sub_image = Image.open(sub_image)
        else:
            self.sub_image = None

        self.site = site


class BaseGenerator:
    config: Config

    def __init__(self, config: Config = None):
        if config is None:
            self.config = Config()

    @staticmethod
    def _draw_two_part_logo(
        x: int, y: int,
        image: ImageType,
        second_part: ImageType, first_part: ImageType
    ) -> Tuple[int, int]:
        image.paste(first_part, (x, y), first_part)
        image.paste(second_part, (x + first_part.width + 5, y), second_part)

        return first_part.width + 5 + second_part.width, max(second_part.height, first_part.height)


class BannerGenerator(BaseGenerator):
    config: Config

    def __init__(self, config: Config = None):
        super().__init__(config=config)

        self.config = config

    def generate(self, header: str, main_text: str, subheader: Optional[str] = None, small_text: Optional[str] = None):
        return self.__gen(header, main_text, subheader, small_text)

    def generate_file(self, fp: Union[str, bytes, Path], header: str, main_text: str, subheader: Optional[str] = None,
                      small_text: Optional[str] = None):
        image = self.__gen(header, main_text, subheader, small_text)

        image.save(fp)

    def __gen(self, header: str, main_text: str, subheader: Optional[str] = None,
              small_text: Optional[str] = None) -> ImageType:
        image = self.config.background
        image_editable = ImageDraw.Draw(image)

        image_height = image.height

        start_y = self.config.padding - 30

        sub_image = self.config.sub_image

        header_font = self.config.header_font

        if len(header) > 60:
            header_font = find_suitable_fontsize(self.config.max_header_width, header_font, header, self.config.length)

        header_text = bruteforce(header, self.config.max_header_width, header_font,
                                 count=self.config.length)
        header_line_height = header_font.getsize(header_text[0])[1]

        pattern = []
        for i in range(len(header_text)):
            text = header_text[i]

            if i == 0:
                padding_y = start_y
            else:
                padding_y = start_y + i * header_line_height

            pattern.append((text, (self.config.padding, padding_y)))

        for text, bounds in pattern:
            image_editable.text(bounds, text, self.config.text_color.hex, font=header_font)

        height = pattern[-1][1][1] + header_line_height

        if subheader is not None and len(subheader) > 0:
            subheader_y = height + 20

            subheader_font = self.config.subheader_font
            if self.config.subheader_font.getsize(subheader)[0] > self.config.max_header_width:
                subheader_font = find_suitable_fontsize(self.config.max_header_width, subheader_font, subheader,
                                                        len(subheader))

            image_editable.text((self.config.padding, subheader_y), subheader, self.config.text_color.hex,
                                font=subheader_font)

            line_y = subheader_y + subheader_font.getsize(subheader)[1] + 4
            image_editable.line(
                [
                    (self.config.padding, line_y),
                    (self.config.padding + subheader_font.getsize(subheader)[0], line_y),
                ],
                fill=self.config.text_color.hex,
                width=3
            )

            height = line_y + 5

        logoless = False

        if self.config.logo_first_part is not None and self.config.logo_second_part is not None:
            logo_y = image_height - self.config.bottom_padding - self.config.logo_second_part.height
            logo_width, logo_height = BaseGenerator._draw_two_part_logo(self.config.padding, logo_y, image,
                                                                        self.config.logo_second_part,
                                                                        self.config.logo_first_part)
        else:
            logo_y = image_height - self.config.bottom_padding
            logo_width = 0
            logoless = True

        based_x = self.config.padding + logo_width
        based_y = logo_y - 5

        if small_text is not None and len(small_text) > 0 and not logoless:
            print(ru_re.fullmatch(small_text), small_text)
            corrector = 0 if ru_re.fullmatch(small_text) is not None else 5
            based_y = logo_y - self.config.small_text_font.getsize(small_text)[1] - corrector
            b_w = self.config.small_text_font.getsize(small_text)[0]
            based_x = based_x - b_w
            image_editable.text((based_x, based_y), small_text, self.config.text_color.hex,
                                font=self.config.small_text_font)

        bottom_height = image_height - based_y

        if self.config.site is not None and len(self.config.site) > 0:
            corrector = 0 if logoless else 40

            image_editable.text((self.config.padding + logo_width + corrector, logo_y - 15), self.config.site,
                                self.config.text_color.hex,
                                font=self.config.text_font)

        main_text = bruteforce(main_text, self.config.max_text_width, self.config.main_font, count=self.config.length)
        ru_line_height = self.config.main_font.getsize(main_text[0])[1]

        pattern = []
        for i in range(len(main_text)):
            text = main_text[i]

            if i == 0:
                padding_y = 0
            else:
                padding_y = i * ru_line_height

            pattern.append((text, (self.config.padding, padding_y)))

        main_text_height = pattern[-1][1][1]

        available_h = (image_height - bottom_height) - height
        middle = int(available_h / 2)

        save_zone = 5

        no_need_sub_image = False

        if sub_image is None or middle < sub_image.height + save_zone or main_text_height > middle:
            no_need_sub_image = True

        if no_need_sub_image:
            half = int(len(pattern)) / 2
            start_y = height + middle - half * ru_line_height
            for text, bounds in pattern:
                image_editable.text((bounds[0], start_y + bounds[1]), text, self.config.text_color.hex,
                                    font=self.config.subheader_font)
        else:
            start_y = height + middle + 10
            for text, bounds in pattern:
                image_editable.text((bounds[0], start_y + bounds[1]), text, self.config.text_color.hex,
                                    font=self.config.subheader_font)

            image.paste(sub_image, (self.config.padding, height + middle - 10 - sub_image.height), sub_image)

        return image


class GeneratorFactory:
    @staticmethod
    def banner(config: Config) -> BannerGenerator:
        return BannerGenerator(config)
