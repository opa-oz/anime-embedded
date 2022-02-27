import json
import pytest
from pathlib import Path
from core import GeneratorFactory, Config, resize, make_transparent

base_dir = Path().cwd() / 'example'

background_path = base_dir / 'small_bg.jpg'
sub_image_path = base_dir / 'wings.png'
logo_first_part_path = base_dir / 'shikimori-glyph.png'
logo_second_part_path = base_dir / 'shikimori-logo.png'

header_font = base_dir / 'Noto_Serif' / 'NotoSerif-Bold.ttf'
text_font = base_dir / 'Noto_Serif' / 'NotoSerif-Regular.ttf'
subheader_font = base_dir / 'Noto_Serif_JP' / 'NotoSerifJP-Bold.otf'

sub_image = resize(make_transparent(sub_image_path), 0.45)
logo_first_part = resize(make_transparent(logo_first_part_path), 0.2)
logo_second_part = resize(make_transparent(logo_second_part_path), 0.2)

average_anime = [
    {
        "score": 9.15,
        "name": "Fullmetal Alchemist: Brotherhood",
        "japanese_synonyms": "[\"\\u92fc\\u306e\\u932c\\u91d1\\u8853\\u5e2b FULLMETAL ALCHEMIST\"]"
    },
    {
        "score": 9.09,
        "name": "Gintama°",
        "japanese_synonyms": "[\"\\u9280\\u9b42\\u00b0\"]"
    },
    {
        "score": 9.09,
        "name": "Steins;Gate",
        "japanese_synonyms": "[\"STEINS;GATE\"]"
    },
    {
        "score": 9.09,
        "name": "Shingeki no Kyojin Season 3 Part 2",
        "japanese_synonyms": "[\"\\u9032\\u6483\\u306e\\u5de8\\u4eba Season3 Part.2\"]"
    },
    {
        "score": 9.06,
        "name": "Fruits Basket: The Final",
        "japanese_synonyms": "[\"\\u30d5\\u30eb\\u30fc\\u30c4\\u30d0\\u30b9\\u30b1\\u30c3\\u30c8 The Final\"]"
    },
    {
        "score": 9.06,
        "name": "Hunter x Hunter (2011)",
        "japanese_synonyms": "[\"HUNTER\\u00d7HUNTER\\uff08\\u30cf\\u30f3\\u30bf\\u30fc\\u00d7\\u30cf\\u30f3\\u30bf\\u30fc\\uff09\"]"
    },
    {
        "score": 9.06,
        "name": "Gintama'",
        "japanese_synonyms": "[\"\\u9280\\u9b42'\"]"
    },
    {
        "score": 9.05,
        "name": "Gintama: The Final",
        "japanese_synonyms": "[\"\\u9280\\u9b42 THE FINAL\"]"
    },
    {
        "score": 9.04,
        "name": "Ginga Eiyuu Densetsu",
        "japanese_synonyms": "[\"\\u9280\\u6cb3\\u82f1\\u96c4\\u4f1d\\u8aac\"]"
    },
    {
        "score": 9.04,
        "name": "Gintama': Enchousen",
        "japanese_synonyms": "[\"\\u9280\\u9b42' \\u5ef6\\u9577\\u6226\"]"
    }
]
shortest_anime = [
    {
        "name": "F",
        "japanese_synonyms": "[\"\\uff26-\\u30a8\\u30d5\"]",
        "l": 1
    },
    {
        "name": "X",
        "japanese_synonyms": "[\"X\\u2212\\u30a8\\u30c3\\u30af\\u30b9\\u2212\"]",
        "l": 1
    },
    {
        "name": "K",
        "japanese_synonyms": "[\"K\"]",
        "l": 1
    },
    {
        "name": "◯",
        "japanese_synonyms": "[\"\\u25ef\"]",
        "l": 1
    },
    {
        "name": "C³",
        "japanese_synonyms": "[\"\\u30b7\\u30fc\\u30ad\\u30e5\\u30fc\\u30d6\"]",
        "l": 2
    },
    {
        "name": "Yu",
        "japanese_synonyms": "[\"\\u9b5a\"]",
        "l": 2
    },
    {
        "name": "TO",
        "japanese_synonyms": "[\"\\u30c8\\u30a5\\u30fc\"]",
        "l": 2
    },
    {
        "name": "Ai",
        "japanese_synonyms": "[\"\\u611b\"]",
        "l": 2
    },
    {
        "name": "We",
        "japanese_synonyms": "[\"We\"]",
        "l": 2
    },
    {
        "name": "OZ",
        "japanese_synonyms": "[\"\\u30aa\\u30ba\"]",
        "l": 2
    }
]
longest_anime = [
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Seton Tankentai! Sumidagawa no Chikai - Omoide no Shiroi Kujira wo Sagase!",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240  \\u30b7\\u30fc\\u30c8\\u30f3\\u63a2\\u691c\\u968a!\\u9685\\u7530\\u5ddd\\u306e\\u8a93\\u3044\\u301c\\u601d\\u3044\\u51fa\\u306e\\u767d\\u3044\\u9be8\\u3092\\u63a2\\u305b!\\u301c\"]",
        "l": 124
    },
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Ryou-san to Chuuken Lucky Monogatari - Kameari Dai Houimou wo Kawase!!",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240  \\u4e21\\u3055\\u3093\\u3068\\u5fe0\\u72ac\\u30e9\\u30c3\\u30ad\\u30fc\\u7269\\u8a9e \\u301c\\u4e80\\u6709\\u5927\\u5305\\u56f2\\u7db2\\u3092\\u304b\\u308f\\u305b!!\"]",
        "l": 120
    },
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Ryoutsu no Asakusa Renewal Daisakusen!! - Aa, Omoide no Hanayashiki",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240  \\u4e21\\u6d25\\u306e\\u6d45\\u8349\\u30ea\\u30cb\\u30e5\\u30fc\\u30a2\\u30eb\\u5927\\u4f5c\\u6226!! \\u301c\\u3042\\u3041 \\u601d\\u3044\\u51fa\\u306e\\u82b1\\u3084\\u3057\\u304d\\u301c\"]",
        "l": 117
    },
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Ryoutsu vs. Nakimushi Idol!? Nihon 1-shuu Dai Sugoroku Game!!",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240 \\u4e21\\u6d25VS\\u6ce3\\u304d\\u866b\\u30a2\\u30a4\\u30c9\\u30eb!? \\u65e5\\u672c1\\u5468\\u5927\\u3059\\u3054\\u308d\\u304f\\u30b2\\u30fc\\u30e0!!\"]",
        "l": 111
    },
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Mezase! Kameari Superstar!! Ryoutsu-shiki Idol e no Michi!",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240 \\u76ee\\u6307\\u305b!\\u4e80\\u6709\\u30b9\\u30fc\\u30d1\\u30fc\\u30b9\\u30bf\\u30fc!!\\u4e21\\u6d25\\u5f0f\\u30a2\\u30a4\\u30c9\\u30eb\\u3078\\u306e\\u9053!\"]",
        "l": 108
    },
    {
        "name": "Shin no Nakama ja Nai to Yuusha no Party wo Oidasareta node, Henkyou de Slow Life suru Koto ni Shimashita",
        "japanese_synonyms": "[\"\\u771f\\u306e\\u4ef2\\u9593\\u3058\\u3083\\u306a\\u3044\\u3068\\u52c7\\u8005\\u306e\\u30d1\\u30fc\\u30c6\\u30a3\\u30fc\\u3092\\u8ffd\\u3044\\u51fa\\u3055\\u308c\\u305f\\u306e\\u3067\\u3001\\u8fba\\u5883\\u3067\\u30b9\\u30ed\\u30fc\\u30e9\\u30a4\\u30d5\\u3059\\u308b\\u3053\\u3068\\u306b\\u3057\\u307e\\u3057\\u305f\"]",
        "l": 105
    },
    {
        "name": "Maou Gakuin no Futekigousha: Shijou Saikyou no Maou no Shiso, Tensei shite Shison-tachi no Gakkou e Kayou",
        "japanese_synonyms": "[\"\\u9b54\\u738b\\u5b66\\u9662\\u306e\\u4e0d\\u9069\\u5408\\u8005 \\uff5e\\u53f2\\u4e0a\\u6700\\u5f37\\u306e\\u9b54\\u738b\\u306e\\u59cb\\u7956\\u3001\\u8ee2\\u751f\\u3057\\u3066\\u5b50\\u5b6b\\u305f\\u3061\\u306e\\u5b66\\u6821\\u3078\\u901a\\u3046\\uff5e\"]",
        "l": 105
    },
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Ryou-san no Sushi Kui Nee! - Choujou Maguro Taiketsu!!",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240 \\u4e21\\u3055\\u3093\\u306e\\u5bff\\u53f8\\u98df\\u3044\\u306d\\u3048!\\u301c\\u9802\\u4e0a\\u30de\\u30b0\\u30ed\\u5bfe\\u6c7a!!\\u301c\"]",
        "l": 104
    },
    {
        "name": "Kochira Katsushikaku Kameari Kouenmae Hashutsujo: Washi to Ore!? - Bokura wa Asakusa Shounen Tanteidan!",
        "japanese_synonyms": "[\"\\u3053\\u3061\\u3089\\u845b\\u98fe\\u533a\\u4e80\\u6709\\u516c\\u5712\\u524d\\u6d3e\\u51fa\\u6240  \\u30ef\\u30b7\\u3068\\u4ffa!?\\u301c\\u307c\\u304f\\u3089\\u306f\\u6d45\\u8349\\u5c11\\u5e74\\u63a2\\u5075\\u56e3!\\u301c\"]",
        "l": 103
    },
    {
        "name": "Tottoko Hamtarou OVA 2: Hamuchanzu no Takara Sagashi Daisaku - Hamuha! Suteki na Umi no Natsuyasumi",
        "japanese_synonyms": "[\"\\u30cf\\u30e0\\u3061\\u3083\\u3093\\u305a\\u306e\\u5b9d\\u3055\\u304c\\u3057\\u5927\\u4f5c\\u6226\\u301c\\u306f\\u3080\\u306f\\u30fc!\\u3059\\u3066\\u304d\\u306a\\u6d77\\u306e\\u306a\\u3064\\u3084\\u3059\\u307f\\u301c\"]",
        "l": 99
    }
]


def get_average_anime():
    for i in range(len(average_anime)):
        item = average_anime[i]
        japanese = json.loads(item['japanese_synonyms'])

        yield {'header': item['name'], 'subheader': japanese[0] or None,
               'main_text': f'#{i + 1} anime in history'}


def get_shortest_anime():
    for i in range(len(shortest_anime)):
        item = shortest_anime[i]
        japanese = json.loads(item['japanese_synonyms'])

        yield {'header': item['name'], 'subheader': japanese[0] or None,
               'main_text': f'#{i + 1} аниме с самым коротким названием'}


def get_longest_anime():
    for i in range(len(longest_anime)):
        item = longest_anime[i]
        japanese = json.loads(item['japanese_synonyms'])

        yield {'header': item['name'], 'subheader': japanese[0] or None,
               'main_text': f'#{i + 1} аниме с самым длинным названием'}


def test_full_case(image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        main_text='The best anime ever!',
        subheader='フルーツバスケット The Final',
        small_text='based on'
    )


def test_full_case_ru(image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        main_text='Лучшее аниме в истории!',
        subheader='フルーツバスケット The Final',
        small_text='по данным'
    )


@pytest.mark.parametrize('anime', get_average_anime())
def test_using_table(anime, image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header=anime['header'],
        main_text=anime['main_text'],
        subheader=anime['subheader'],
        small_text='по данным'
    )


@pytest.mark.parametrize('s_anime', get_shortest_anime())
def test_shortest_anime(s_anime, image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header=s_anime['header'],
        main_text=s_anime['main_text'],
        subheader=s_anime['subheader']
    )


@pytest.mark.parametrize('l_anime', get_longest_anime())
def test_longest_anime(l_anime, image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header=l_anime['header'],
        main_text=l_anime['main_text'],
        subheader=l_anime['subheader']
    )


def test_without_site(image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        main_text='Лучшее аниме в истории!',
        subheader='フルーツバスケット The Final',
        small_text='по данным'
    )


def test_without_small_text(image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        main_text='Лучшее аниме в истории!',
        subheader='フルーツバスケット The Final',
    )


def test_without_subheader(image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        logo_first_part=logo_first_part,
        logo_second_part=logo_second_part,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        main_text='Лучшее аниме в истории!',
        small_text='по данным'
    )


def test_without_logo(image_similarity):
    config = Config(
        background=background_path,
        sub_image=sub_image,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        subheader='フルーツバスケット The Final',
        main_text='Лучшее аниме в истории!',
        small_text='по данным'
    )


def test_without_logo_and_subimage(image_similarity):
    config = Config(
        background=background_path,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        subheader='フルーツバスケット The Final',
        main_text='Лучшее аниме в истории!',
    )


def test_minimal_setup(image_similarity):
    config = Config(
        background=background_path,
        header_font=header_font,
        text_font=text_font,
        small_text_font=text_font,
        subheader_font=subheader_font,
        main_font=text_font,
        site='anime-recommend.ru',
    )

    banner_factory = GeneratorFactory.banner(config)
    fname = image_similarity['filename']

    banner_factory.generate_file(
        fname,
        header='Fruits Basket: The Final',
        main_text='Лучшее аниме в истории!',
    )
