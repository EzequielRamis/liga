#!/usr/bin/env python
#
# usage: fontforge -lang=py ligate.py [options]
# Run with --help for detailed options.
#
# See config_sample.py for a complete configuration that will be copied.

import fontforge
import psMat
import os
from os import path
from glyphsLib import GSFont
import re
import importlib.util
import utils as u
from functools import reduce

# Constants
COPYRIGHT = """

Programming ligatures added by Ezequiel Ramis Folberg from FiraCode.
FiraCode Copyright (c) 2014 by Nikita Prokopov."""


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def get_ligature_source(fontname):
    # Become case-insensitive
    fontname = fontname.lower()
    ext = fontname[:-3]
    for weight in ["Bold", "Retina", "Medium", "Regular", "Light", "SemiBold"]:
        if fontname.endswith("-" + weight.lower()):
            # Exact match for one of the Fira Code weights
            return f"fira/FiraCode-{weight}.{ext}"
    return f"fira/FiraCode-Regular.{ext}"


def add_fira_prefix(code):
    print("foo")


def write_fira_feature_file(feats, output_file, firacode, font):
    file = open(output_file, "w")
    fira = GSFont("fira.glyphs")
    filtered_feats = [f for f in fira.features if f.name in feats]
    for feature in fira.featurePrefixes:
        file.write(feature.code)
    for _class in fira.classes:
        fcode = " ".join(
            set(
                filter(
                    lambda i: i[0] == "\\"
                    and firacode.__contains__(i[1:])
                    and font.__contains__(firacode[i[1:]].unicode),
                    [
                        ("\\" + cl if cl[0] != "@" else cl)
                        for cl in re.sub("\s+", " ", _class.code).split(" ")
                    ],
                )
            )
        )
        file.write(f"@{_class.name} = [{fcode}];\n")
    for feature in filtered_feats:
        code = "\n".join(
            [
                l
                for l in u.add_backslash_to_glyphs(feature.code).split("\n")
                if ("twoemdash" not in l and "threeemdash" not in l)
            ]
        )
        code = u.remove_fl_ft_sub(code)
        code = u.add_lookups_prefix(u.remove_last_newlines(code).replace("\n", "\n\t"))
        file.write(
            f"feature {feature.name} "
            + "{\n\t"
            + code
            + "\n}"
            + f" {feature.name};\n\n"
        )
    file.close()


def extract_tagged_glyphs(tmp_fea):
    content = open(tmp_fea, "r").read()
    res = re.findall(r"(?<=\\)(\w+(\.\w+)+)", content)
    return set([r[0] for r in res])


def correct_ligature_width(font, g, mult):
    if mult == 0:
        mult = 1.0
    scale = float(font["M"].width) / font[g].width
    font[g].transform(psMat.scale(scale * mult))


def paste_tagged_glyphs(fira, font, glyphs, scale):
    for g in glyphs:
        renamed_g = "fira_" + g

        fira.selection.none()
        fira.selection.select(g)
        fira.copy()

        font.createChar(-1, g)
        font.selection.none()
        font.selection.select(g)
        font.paste()
        font[g].glyphname = renamed_g
        correct_ligature_width(font, renamed_g, scale)


def paste_normal_glyphs(fira, font, glyphs, scale):
    for g in glyphs:
        fira.selection.none()
        fira.selection.select(g)
        fira.copy()
        uni = fira[g].unicode

        font.createChar(uni, g)
        font.selection.none()
        font.selection.select(g)
        font.paste()
        correct_ligature_width(font, g, scale)


def rename_tagged_glyphs(glyphs, tmp_fea):
    content = open(tmp_fea, "r").read()
    for g in glyphs:
        content = re.sub(f"(?<=\\\\){g}", f"fira_{g}", content)
    file = open(tmp_fea, "w")
    file.write(content)
    file.close()


def rename_normal_glyphs(firacode, font, tmp_fea):
    content = open(tmp_fea, "r").read()
    normal_glyphs = list(
        set(
            filter(
                lambda s: "." not in s,
                map(
                    lambda s: reduce(lambda z, i: z.replace(i, ""), ["'", ";", "]"], s),
                    re.findall(r"(?<=\\)(\S+)", content),
                ),
            )
        )
    )
    for g in normal_glyphs:
        uni = firacode[g].unicode
        # if it exists, it's only renamed
        font.createChar(uni, g)


class LigatureCreator(object):
    def __init__(
        self, font, firacode, scale_character_glyphs_threshold, copy_character_glyphs
    ):
        self.font = font
        self.firacode = firacode
        self.scale_character_glyphs_threshold = scale_character_glyphs_threshold
        self.should_copy_character_glyphs = copy_character_glyphs
        self._lig_counter = 0

        # Scale firacode to correct em height.
        self.firacode.em = self.font.em
        self.emwidth = self.font[ord("m")].width

    def copy_ligature_from_source(self, ligature_name):
        try:
            self.firacode.selection.none()
            self.firacode.selection.select(ligature_name)
            self.firacode.copy()
            return True
        except ValueError:
            return False

    def correct_character_width(self, glyph):
        """Width-correct copied individual characters (not ligatures!).

        This will correct the horizontal advance of characters to match the em
        width of the output font, and (depending on the width of the glyph, the
        em width of the output font, and the value of the command line option
        --scale-character-glyphs-threshold) optionally horizontally scale it.

        Glyphs that are not horizontally scaled, but which still need horizontal
        advance correction, will be centered instead.
        """

        if glyph.width == self.emwidth:
            # No correction needed.
            return

        widthdelta = float(abs(glyph.width - self.emwidth)) / self.emwidth
        if widthdelta >= self.scale_character_glyphs_threshold:
            # Character is too wide/narrow compared to output font; scale it.
            scale = float(self.emwidth) / glyph.width
            glyph.transform(psMat.scale(scale, 1.0))
        else:
            # Do not scale; just center copied characters in their hbox.
            # Fix horizontal advance first, to recalculate the bearings.
            glyph.width = self.emwidth
            # Correct bearings to center the glyph.
            glyph.left_side_bearing = (
                glyph.left_side_bearing + glyph.right_side_bearing
            ) / 2
            glyph.right_side_bearing = glyph.left_side_bearing

        # Final adjustment of horizontal advance to correct for rounding
        # errors when scaling/centering -- otherwise small errors can result
        # in visible misalignment near the end of long lines.
        glyph.width = self.emwidth

    def copy_character_glyphs(self, chars):
        """Copy individual (non-ligature) characters from the ligature font."""
        if not self.should_copy_character_glyphs:
            return
        print("    ...copying %d character glyphs..." % (len(chars)))

        for char in chars:
            self.firacode.selection.none()
            self.firacode.selection.select(char)
            self.firacode.copy()
            self.font.selection.none()
            self.font.selection.select(char)
            self.font.paste()
            # self.correct_character_width(self.font[ord(char_dict[char])])

    def correct_ligature_width(self, glyph):
        """Correct the horizontal advance and scale of a ligature."""

        if glyph.width == self.emwidth:
            return

        # TODO: some kind of threshold here, similar to the character glyph
        # scale threshold? The largest ligature uses 0.956 of its hbox, so if
        # the target font is within 4% of the source font size, we don't need to
        # resize -- but we may want to adjust the bearings. And we can't just
        # center it, because ligatures are characterized by very large negative
        # left bearings -- they advance 1em, but draw from (-(n-1))em to +1em.
        scale = float(self.emwidth) / glyph.width
        glyph.transform(psMat.scale(scale, 1.0))
        glyph.width = self.emwidth


def replace_sfnt(font, key, value):
    font.sfnt_names = tuple(
        (row[0], key, value) if row[1] == key else row for row in font.sfnt_names
    )


def update_font_metadata(font, new_name):
    # Figure out the input font's real name (i.e. without a hyphenated suffix)
    # and hyphenated suffix (if present)
    old_name = font.familyname
    try:
        suffix = font.fontname.split("-")[1]
    except IndexError:
        suffix = None

    # Replace the old name with the new name whether or not a suffix was present.
    # If a suffix was present, append it accordingly.
    font.familyname = new_name
    if suffix:
        font.fullname = "%s %s" % (new_name, suffix)
        font.fontname = "%s-%s" % (new_name, suffix)
    else:
        font.fullname = new_name
        font.fontname = new_name

    print(
        "Ligating font %s (%s) as '%s'" % (path.basename(font.path), old_name, new_name)
    )

    font.copyright = (font.copyright or "") + COPYRIGHT
    replace_sfnt(font, "UniqueID", "%s; ligated" % font.fullname)
    replace_sfnt(font, "Preferred Family", new_name)
    replace_sfnt(font, "Compatible Full", new_name)
    replace_sfnt(font, "Family", new_name)
    replace_sfnt(font, "WWS Family", new_name)


def ligate_font(
    input_font_file,
    output_dir,
    ligature_font_file,
    config_file,
    copy_character_glyphs,
    output_name,
    prefix,
):
    font = fontforge.open(input_font_file)
    cls()
    config_file_name = path.splitext(path.basename(config_file))[0]
    try:
        spec = importlib.util.spec_from_file_location(config_file_name, config_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        config = mod.config
    except:
        spec = importlib.util.spec_from_file_location("default", "config_sample.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        config = mod.config

    if not ligature_font_file:
        ligature_font_file = get_ligature_source(font.fontname)

    if output_name:
        name = output_name
    else:
        name = font.familyname
    if prefix:
        name = "%s%s" % (prefix, name)

    update_font_metadata(font, name)

    print("    ...using ligatures from %s" % ligature_font_file)
    print("    ...using features from %s" % config_file)
    firacode = fontforge.open(ligature_font_file)

    tmp_fea = "tmp.fea"
    write_fira_feature_file(config["features"], tmp_fea, firacode, font)
    tmp_glyphs = extract_tagged_glyphs(tmp_fea)
    paste_tagged_glyphs(firacode, font, tmp_glyphs, config["scale"])
    paste_normal_glyphs(firacode, font, config["glyphs"], config["scale"])
    rename_tagged_glyphs(tmp_glyphs, tmp_fea)
    rename_normal_glyphs(firacode, font, tmp_fea)
    font.mergeFeature(tmp_fea)

    # Work around a bug in Fontforge where the underline height is subtracted from
    # the underline width when you call generate().
    # font.upos += font.uwidth

    # Generate font type (TTF or OTF) corresponding to input font extension
    # (defaults to TTF)
    if input_font_file[-4:].lower() == ".otf":
        output_font_type = ".otf"
    else:
        output_font_type = ".ttf"

    # Generate font & move to output directory
    output_font_file = path.join(output_dir, font.fontname + output_font_type)
    print("\n    ...saving to '%s' (%s)" % (output_font_file, font.fullname))
    font.generate(output_font_file)


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "input_font_file", help="The TTF or OTF font to add ligatures to."
    )
    parser.add_argument(
        "--output-dir",
        help="The directory to save the ligated font in. The actual filename"
        " will be automatically generated based on the input font name and"
        " the --prefix and --output-name flags.",
    )
    parser.add_argument(
        "--ligature-font-file",
        type=str,
        default="",
        metavar="PATH",
        help="The file to copy ligatures from. If unspecified, ligate will"
        " attempt to pick a suitable one from fonts/fira/distr/otf/ based on the input"
        " font's weight.",
    )
    parser.add_argument(
        "--config-file",
        type=str,
        default="config_sample.py",
        metavar="PATH",
        help="The python file to copy the config from.",
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
        "--prefix",
        type=str,
        default="Liga-",
        help="String to prefix the name of the generated font with.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default="",
        help="Name of the generated font. Completely replaces the original.",
    )
    return parser.parse_args()


def main():
    ligate_font(**vars(parse_args()))


if __name__ == "__main__":
    main()
