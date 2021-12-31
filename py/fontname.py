#!/usr/bin/env python

import sys

old = sys.argv[1]
new = sys.argv[2]
type = sys.argv[3]


def camelcase(s):
    return "".join([ss[0].upper() + ss[1:] for ss in s.split(" ")])


def slice_postscript(s):
    sp = s.split("-")
    return (sp[:-1], sp[-1])


def slice_fullname(s):
    sp = s.split(" ")
    return (sp[:-1], sp[-1])


def add_postscript_weight(s, w):
    if w:
        return f"{s}-{w}"
    else:
        return s


def add_fullname_weight(s, w):
    if w:
        return f"{s} {w}"
    else:
        return s


# ["Font name", "Font name Weight", "FontName", "FontName-Weight"]
def fontnames(old_psname, name):
    family, weight = slice_postscript(old_psname)
    psname = camelcase(name)
    if len(family) > 0:
        name_weighted = add_fullname_weight(name, weight)
        psname_weighted = add_postscript_weight(psname, weight)
    else:
        name_weighted = name
        psname_weighted = psname
    return [name, name_weighted, psname, psname_weighted]


def main():
    print(fontnames(old, new)[int(type)])


if __name__ == "__main__":
    main()
