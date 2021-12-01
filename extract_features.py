#!/usr/bin/env python

import fontforge


def update_features():
    font = fontforge.open("fira/FiraCode-Regular.ttf")
    lookups = font.gsub_lookups
    pad = len(str(len(lookups)))
    for i, lookup in enumerate(lookups):
        font.generateFeatureFile(f"features/{str(i).zfill(pad)}.fea", lookup)


def main():
    update_features()


if __name__ == "__main__":
    main()
