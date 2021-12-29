#!/usr/bin/env python
#
# usage: fontforge -lang=py ligate.py [options]
# Run with --help for detailed options.
#
# See config_sample.py for a complete configuration that will be copied.

import fontforge
import psMat
from os import path
from glyphsLib import GSFont
import re
import importlib.util
from py.fontname import fontname, wo_ws
import py.utils as u
from functools import reduce
import warnings as w
import sys

# Constants
COPYRIGHT = """

Programming ligatures added with https://github.com/EzequielRamis/liga
FiraCode Copyright (c) 2014 Nikita Prokopov."""


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
                # remove lines which wouldn't be here
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
    res = []
    [res.append(x) for x in [r[0] for r in ref] if x not in res]
    return res


def correct_ligature_width(font, g, mult):
    if mult == 0:
        mult = 1.0
    scale = float(font["M"].width) / font[g].width
    font[g].transform(psMat.scale(scale * mult))


def paste_glyphs(fira, font, glyphs, scale, prefix, isLigature):
    fira.selection.none()
    fira.selection.select(*glyphs)
    fira.copy()
    for g in glyphs:
        if isLigature:
            uni = -1
        else:
            uni = fira[g].unicode
        font.createChar(uni, g)
    font.selection.none()
    font.selection.select(*glyphs)
    font.paste()
    for g in glyphs:
        renamed_g = prefix + g
        font[g].glyphname = renamed_g
        correct_ligature_width(font, renamed_g, scale)


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


def replace_sfnt(font, key, value):
    font.sfnt_names = tuple(
        (row[0], key, value) if row[1] == key else row for row in font.sfnt_names
    )


def update_font_metadata(font, prefix, suffix):
    # Figure out the input font's real name (i.e. without a hyphenated suffix)
    # and hyphenated suffix (if present)
    old_familyname = font.familyname
    old_fontname = font.fontname

    old_fontname_spl = font.fontname.split("-")
    if len(old_fontname_spl) > 1:
        weight = old_fontname_spl[-1]
    else:
        weight = None

    new_name = prefix + old_familyname + suffix
    new_name_w = fontname(font.fontname, prefix, suffix)

    font.familyname = new_name
    font.fontname = new_name_w
    # Replace the old name with the new name whether or not a weight was present.
    # If a weight was present, append it accordingly.
    if weight:
        font.fullname = "%s %s" % (new_name, weight)
    else:
        font.fullname = new_name

    print(
        "Ligating font %s (%s) as '%s'"
        % (path.basename(font.path), old_fontname, new_name_w)
    )

    font.copyright = (font.copyright or "") + COPYRIGHT
    replace_sfnt(font, "UniqueID", "%s; Ligated" % font.fullname)
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
    prefix,
    suffix,
):
    font = fontforge.open(input_font_file)
    config_file_name = path.splitext(path.basename(config_file))[0]
    try:
        spec = importlib.util.spec_from_file_location(config_file_name, config_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        config = mod.config
    except Exception as e:
        w.warn(f"Error with config_file: {e}\n...using config from config_sample.py")
        spec = importlib.util.spec_from_file_location("default", "config_sample.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        config = mod.config

    if not ligature_font_file:
        ligature_font_file = get_ligature_source(font.fontname)

    update_font_metadata(font, prefix, suffix)

    print("    ...using ligatures from %s" % ligature_font_file)
    print("    ...using config    from %s" % config_file)
    firacode = fontforge.open(ligature_font_file)

    tmp_fea = "tmp.fea"
    write_fira_feature_file(config["features"], tmp_fea, firacode, font)
    tmp_glyphs = extract_tagged_glyphs(tmp_fea)
    paste_glyphs(firacode, font, tmp_glyphs, config["scale"], "fira_", True)
    if copy_character_glyphs:
        paste_glyphs(firacode, font, config["glyphs"], config["scale"], "", False)
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
    print("\n    ...saving\t       to   %s (%s)" % (output_font_file, font.fullname))
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
        "--suffix",
        type=str,
        default="",
        help="String to suffix the name of the generated font with.",
    )
    return parser.parse_args()


def main():
    try:
        ligate_font(**vars(parse_args()))
    except Exception as e:
        w.warn(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
