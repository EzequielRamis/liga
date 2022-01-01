def camelcase(s):
    return "".join([ss[0].upper() + ss[1:] for ss in s.split(" ") if len(ss) > 0])


def slice_postscript(s):
    sp = s.split("-")
    return (sp[:-1], sp[-1])


def slice_fullname(s):
    sp = s.split(" ")
    return (sp[:-1], sp[-1])


def add_postscript_style(s, w):
    if w:
        return f"{s}-{w}"
    else:
        return s


def add_fullname_style(s, w):
    if w:
        return f"{s} {w}"
    else:
        return s


# Assume that a general fullname has this pattern:
# "FAMILY [STYLE]" where STYLE is an optional set of words separated (or not)
# by a space.
# The STYLE set is a permutation whose elements must be:
# - Only a one WEIGHT_WORD
# - Zero or more words defined in STYLE_WORDS
# This would avoid some naming bugs that appear generally in italic fonts.

STYLE_WORDS = [
    "italic",
    "normal",
]

WEIGHT_WORDS = [
    "ultralight",
    "ultlt",
    "extralight",
    "extlt",
    "thin",
    "light",
    "regular",
    "retina",
    "text",
    "medium",
    "medm",
    "semibold",
    "semibld",
    "smbld",
    "demibold",
    "demibld",
    "dmbld",
    "bld",
    "bold",
    "heavy",
    "extrabold",
    "extbld",
    "ultrabold",
    "ultbld",
    "black",
]


def split_family_style(old_name, separator):
    words = old_name.split(separator)
    k = len(words) - 1
    while k >= 0 and (
        words[k].lower() in STYLE_WORDS
        or words[k].lower() in WEIGHT_WORDS
        # Cartesian products
        or words[k].lower() in [i + j for i in STYLE_WORDS for j in WEIGHT_WORDS]
        or words[k].lower() in [j + i for i in STYLE_WORDS for j in WEIGHT_WORDS]
    ):
        k -= 1
    count = k + 1
    return (separator.join(words[:count]), separator.join(words[count:]))


def safe_add_fullname_style(old_flname, name):
    family, style = split_family_style(old_flname, " ")
    if len(family) > 0:
        name_styled = add_fullname_style(name, style)
    else:
        name_styled = name
    return name_styled


# A postscript has the same pattern but its words are separated by a hypen


def safe_add_postname_style(old_psname, name):
    name = camelcase(name)
    family, style = split_family_style(old_psname, "-")
    if len(family) > 0:
        name_styled = add_postscript_style(name, style)
    else:
        name_styled = name
    return name_styled
