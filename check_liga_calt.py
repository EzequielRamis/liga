#!/usr/bin/env python

from glyphsLib import GSFont
import re
from features_sample import features


def check():
    font = GSFont("fira.glyphs")
    liga_feature = font.features["liga"]
    ligas = set(re.findall("(?<=by )([\s\S]*?)(?=.liga)", liga_feature.code))
    calts = set(features["calt"])
    if ligas.issubset(calts):
        print("OK")
    else:
        print("ERROR")
        print(ligas.symmetric_difference(calts))


def main():
    check()


if __name__ == "__main__":
    main()
