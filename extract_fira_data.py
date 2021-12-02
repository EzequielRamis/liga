#!/usr/bin/env python

from glyphsLib import GSFont


def remove_last_newlines(s):
    while s[-1:] == "\n" and s != "\n":
        s = s[: -1 or None]
    return s


def extract_features():
    file = open("fira.fea", "w")
    font = GSFont("fira.glyphs")
    for feature in font.features:
        file.write(
            f"feature {feature.name} "
            + "{\n\t"
            + remove_last_newlines(feature.code).replace("\n", "\n\t")
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


def main():
    extract_features()
    extract_classes()


if __name__ == "__main__":
    main()
