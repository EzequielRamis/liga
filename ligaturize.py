import fontforge
import os


def ligaturize_font(
    input_font_file, output_dir, ligature_font_file, output_name, prefix, **kwargs
):
    font = fontforge.open(input_font_file)
    cls()
    for lookup in font.gsub_lookups:
        print(font.getLookupSubtables(lookup))


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "input_font_file", help="The TTF or OTF font to add ligatures to."
    )
    parser.add_argument(
        "--output-dir",
        help="The directory to save the ligaturized font in. The actual filename"
        " will be automatically generated based on the input font name and"
        " the --prefix and --output-name flags.",
    )
    parser.add_argument(
        "--ligature-font-file",
        type=str,
        default="",
        metavar="PATH",
        help="The file to copy ligatures from. If unspecified, ligaturize will"
        " attempt to pick a suitable one from fonts/fira/distr/otf/ based on the input"
        " font's weight.",
    )
    parser.add_argument(
        "--copy-character-glyphs",
        default=False,
        action="store_true",
        help="Copy glyphs for (some) individual characters from the ligature"
        " font as well. This will result in punctuation that matches the"
        " ligatures more closely, but may not fit in as well with the rest"
        " of the font.",
    )
    parser.add_argument(
        "--scale-character-glyphs-threshold",
        type=float,
        default=0.1,
        metavar="THRESHOLD",
        help="When copying character glyphs, if they differ in width from the"
        " width of the input font by at least this much, scale them"
        " horizontally to match the input font even if this noticeably"
        " changes their aspect ratio. The default (0.1) means to scale if"
        " they are at least 10%% wider or narrower. A value of 0 will scale"
        " all copied character glyphs; a value of 2 effectively disables"
        " character glyph scaling.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="Liga",
        help="String to prefix the name of the generated font with.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default="",
        help="Name of the generated font. Completely replaces the original.",
    )
    return parser.parse_args()


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    ligaturize_font(**vars(parse_args()))


if __name__ == "__main__":
    main()
