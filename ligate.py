#!/usr/bin/env python
#
# usage: fontforge -lang=py ligate.py [options]
# Run with --help for detailed options.
#
# See config_sample.py for a complete configuration that will be used.

import fontforge
import psMat
from os import path
from glyphsLib import GSFont
import re
import importlib.util
import py.utils as u
from functools import reduce
import sys
from pathlib import Path
import faulthandler
import py.fontname as f

# Constants
COPYRIGHT = """

Programming ligatures from FiraCode added with https://github.com/EzequielRamis/liga
FiraCode Copyright (c) 2014 Nikita Prokopov."""


def get_ligature_source(font):
    WEIGHT = {
        300: "Light",
        400: "Regular",
        450: "Retina",
        500: "Medium",
        600: "SemiBold",
        700: "Bold",
    }
    ext = font.path.lower().split(".")[-1]
    # closest key
    matched_key = min(WEIGHT.keys(), key=lambda x: abs(x - font.os2_weight))
    return f"fira/FiraCode-{WEIGHT[matched_key]}.{ext}"


def write_fira_feature_file(feats, output_file, firacode, font):
    file = open(output_file, "w")
    fira = GSFont("fira.glyphs")
    filtered_feats = [f for f in fira.features if f.name in feats]
    for feature in fira.featurePrefixes:
        file.write(feature.code)
    for _class in fira.classes:
        fcode = " ".join(
            u.remove_duplicates(
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
                # remove .fea lines which wouldn't be here
                if (
                    all(
                        [
                            s not in l
                            for s in [
                                "twoemdash",
                                "threeemdash",
                                r"\f \i.salt_low \j.salt_low",
                                r"\F \T \I \l.salt_low",
                            ]
                        ]
                    )
                )
            ]
        )
        filtered_code = []
        inside_lookup = False
        chosen_lookup = False
        for l in code.split("\n"):
            lookup_start = re.findall(r"(lookup\s+)(\S+)(\s+{)", l)
            lookup_end = re.findall(r"(}\s+)(\S+)(\s*;)", l)
            if len(lookup_start) != 0:
                inside_lookup = True
                if lookup_start[0][1] in feats[feature.name]:
                    chosen_lookup = True
                    filtered_code.append(l)
            else:
                if len(lookup_end) != 0:
                    inside_lookup = False
                    chosen_lookup = False
                    if lookup_end[0][1] in feats[feature.name]:
                        filtered_code.append(l)
                else:
                    if not inside_lookup or chosen_lookup:
                        filtered_code.append(l)
        code = u.add_lookups_prefix(
            u.remove_last_newlines("\n".join(filtered_code)).replace("\n", "\n\t")
        )
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
    ref = re.findall(r"(?<=\\)(\w+(\.\w+)+)", content)
    return u.remove_duplicates([r[0] for r in ref])


def correct_ligature_width(font, g, mult):
    if mult <= 0:
        mult = 1.0
    scale = float(font["M"].width) / font[g].width
    font[g].transform(psMat.scale(scale * mult))


def paste_glyphs(fira, font, glyphs, scale, prefix):
    for g in glyphs:
        fira.selection.none()
        fira.selection.select(g)
        fira.copy()

        uni = fira[g].unicode
        font.createChar(uni, g)
        font.selection.none()
        font.selection.select(g)
        font.paste()
        renamed_g = prefix + g
        font[g].glyphname = renamed_g
        correct_ligature_width(font, renamed_g, scale)


def rename_tagged_glyphs_from_fea(glyphs, tmp_fea, prefix):
    content = open(tmp_fea, "r").read()
    for g in glyphs:
        content = re.sub(f"(?<=\\\\){g}", f"{prefix}{g}", content)
    file = open(tmp_fea, "w")
    file.write(content)
    file.close()


def rename_normal_glyphs_from_font(firacode, font, tmp_fea):
    content = open(tmp_fea, "r").read()
    normal_glyphs = u.remove_duplicates(
        filter(
            lambda s: "." not in s,
            map(
                lambda s: reduce(lambda z, i: z.replace(i, ""), ["'", ";", "]"], s),
                re.findall(r"(?<=\\)(\S+)", content),
            ),
        )
    )
    for g in normal_glyphs:
        uni = firacode[g].unicode
        # if it exists, it's only renamed
        font.createChar(uni, g)


def replace_sfnt(font, key, value):
    font.sfnt_names = tuple(
        (row[0], key, value) if row[1] == key else row for row in font.sfnt_names
    )


def update_font_metadata(font, name):
    old_fullname = font.fullname
    old_postscript = font.fontname

    flname_weighted = f.safe_add_fullname_style(old_fullname, name)
    psname_weighted = f.safe_add_postname_style(old_postscript, name)

    font.familyname = name
    font.fontname = psname_weighted
    font.fullname = flname_weighted

    print(
        "Ligating font '%s' (%s) as '%s'"
        % (old_fullname, path.basename(font.path), flname_weighted)
    )

    font.copyright = (font.copyright or "") + COPYRIGHT
    replace_sfnt(font, "UniqueID", "%s; Ligated" % flname_weighted)
    replace_sfnt(font, "Fullname", flname_weighted)
    replace_sfnt(font, "Preferred Family", name)
    replace_sfnt(font, "Compatible Full", name)
    replace_sfnt(font, "Family", name)
    replace_sfnt(font, "WWS Family", name)


def ligate_font(
    input_font_file,
    output_dir,
    ligature_font_file,
    config_file,
    copy_character_glyphs,
    prefix,
    output_name,
):
    faulthandler.enable()
    font = fontforge.open(input_font_file)
    config_file_name = path.splitext(path.basename(config_file))[0]
    try:
        spec = importlib.util.spec_from_file_location(config_file_name, config_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        config = mod.config
    except Exception as e:
        sys.stderr.write(
            f"Error with config_file: {e}\n    · Using config from config_sample.py"
        )
        spec = importlib.util.spec_from_file_location("default", "config_sample.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        config = mod.config

    if not ligature_font_file:
        ligature_font_file = get_ligature_source(font)

    if output_name:
        output_basename = f.safe_add_postname_style(Path(font.path).stem, output_name)
    else:
        output_name = prefix + font.familyname
        output_basename = prefix + Path(font.path).stem

    update_font_metadata(font, output_name)

    print("    · Using ligatures from %s" % ligature_font_file)
    print("    · Using config    from %s" % config_file)
    firacode = fontforge.open(ligature_font_file)

    # For logging purposes
    sys.stderr.write("====\n")

    # This removes unnecessary stderr output.
    # Also, firacode gpos lookups are only about diacritical marks
    for look in firacode.gpos_lookups:
        firacode.removeLookup(look, 1)

    tmp_fea = "tmp.fea"
    write_fira_feature_file(config["features"], tmp_fea, firacode, font)
    tmp_glyphs = extract_tagged_glyphs(tmp_fea)

    tagged_prefix = "fira_"

    paste_glyphs(firacode, font, tmp_glyphs, config["scale"], tagged_prefix)
    if copy_character_glyphs:
        paste_glyphs(firacode, font, config["glyphs"], config["scale"], "")
    rename_tagged_glyphs_from_fea(tmp_glyphs, tmp_fea, tagged_prefix)
    rename_normal_glyphs_from_font(firacode, font, tmp_fea)

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
    output_font_file = path.join(output_dir, output_basename + output_font_type)
    print("    · Saving\t      to   %s (%s)" % (output_font_file, font.fontname))
    font.generate(output_font_file)
    font.close()
    firacode.close()


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "input_font_file", help="The TTF or OTF font to add ligatures to."
    )
    parser.add_argument(
        "--output-dir",
        help="The directory to save the ligated font in.",
    )
    parser.add_argument(
        "--ligature-font-file",
        type=str,
        default="",
        metavar="PATH",
        help="The file to copy ligatures from. If unspecified, ligate will"
        " attempt to pick a suitable one from fira/ based on the input"
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
        default="Liga ",
        help="String to prefix the name of the generated font with.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=None,
        help="Name of the generated font. Completely replaces the original"
        " and prefix flag will be ignored.",
    )
    return parser.parse_args()


def main():
    ligate_font(**vars(parse_args()))


if __name__ == "__main__":
    main()
