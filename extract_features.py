#!/usr/bin/env python

import fontforge


def update_features():
    font = fontforge.open("fira/FiraCode-Regular.ttf")
    for i, lookup in enumerate(font.gsub_lookups):
        font.generateFeatureFile(f"features/{i}.fea", lookup)


def main():
    update_features()


if __name__ == "__main__":
    main()
