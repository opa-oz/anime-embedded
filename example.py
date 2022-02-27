import argparse
import sys

from core import GeneratorFactory, Config, resize, make_transparent


def main(args):
    ap = argparse.ArgumentParser()

    ap.add_argument("-bg", "--background", required=True,
                    help="Background")
    ap.add_argument("-si", "--sub_image", help="Sub image")

    ap.add_argument("-l1", "--logo_first_part",
                    help="First part of logo")
    ap.add_argument("-l2", "--logo_second_part",
                    help="First part of logo")

    ap.add_argument("-he", "--header_font",
                    help="Header font")
    ap.add_argument("-t", "--text_font",
                    help="Text font")
    ap.add_argument("-s", "--subheader_font",
                    help="Subheader font")

    ap.add_argument("-out", "--output", required=True,
                    help="Banner path")

    args, unknown = ap.parse_known_args(args[1:])
    args = vars(args)

    print(args)

    sub_image = resize(make_transparent(args['sub_image']), 0.45)
    logo_first_part = resize(make_transparent(args['logo_first_part']), 0.2)
    logo_second_part = resize(make_transparent(args['logo_second_part']), 0.2)

    config = Config(
        background=args['background'],
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=args['header_font'],
        text_font=args['text_font'],
        small_text_font=args['text_font'],
        subheader_font=args['subheader_font'],
        main_font=args['text_font'],
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)

    banner_factory.generate_file(
        args['output'],
        header='Fruits Basket: The Final',
        main_text='The best anime ever!',
        subheader='フルーツバスケット The Final',
        small_text='based_on'
    )


main(sys.argv)
