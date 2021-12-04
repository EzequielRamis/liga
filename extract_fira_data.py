#!/usr/bin/env python

from glyphsLib import GSFont
import utils as u


def extract_features():
    file = open("fira.fea", "w")
    font = GSFont("fira.glyphs")
    for feature in font.features:
        code = u.add_backslash_to_glyphs(feature.code)
        file.write(
            f"feature {feature.name} "
            + "{\n\t"
            + u.remove_last_newlines(code).replace("\n", "\n\t")
            + "\n}"
            + f" {feature.name};\n\n"
        )
    file.close()


def extract_classes():
    font = GSFont("fira.glyphs")
    for _class in font.classes:
        file = open(f"classes/{_class.name}.fea", "w")
        file.write(_class.code)
        file.close()


FEAT_FILE_COMMENT = """
    This is an autogenerated set of curated features that ligaturize.py will
    attempt to copy from Fira Code to your output font. Each feature may have
    a list of lookups. Features/lookups that aren't present in the version of
    Fira Code you're using will be skipped. To disable features/lookups,
    simply comment them out in this file.
"""

FEAT_BLACKLIST = {
    "aalt",
    "subs",
    "sups",
    "numr",
    "dnom",
    "frac",
    "ordn",
    "tnum",
    "onum",
    "case",
    "liga",
    "locl",
    "zero",
    "salt",
    "ccmp",
    "sinf",
    "hwid",
}


def create_feature_set_file():
    font = GSFont("fira.glyphs")
    file = open("features_sample.py", "w")
    file.write(f'"""{FEAT_FILE_COMMENT}"""' + "\n\nfeatures = {\n")
    for feature in font.features:
        if feature.name not in FEAT_BLACKLIST:
            ls = u.lookups(feature.code)
            if len(ls) > 0:
                fls = "[\n"
                for i in range(len(ls)):
                    fls += f'\t\t"{ls[i]}",\n'
                fls += "\t]"
            else:
                fls = "[]"
            file.write(f'\t"{feature.name}": {fls},\n')
    file.write("}")
    file.close()


def main():
    extract_features()
    extract_classes()
    create_feature_set_file()


if __name__ == "__main__":
    main()
