#!/usr/bin/env python

import sys

f = sys.argv[1]
p = sys.argv[2]
s = sys.argv[3]


# without whitespace
def wo_ws(s):
    return s.replace(" ", "")


def fontname(font_fontname, prefix, suffix):
    prefix_w = wo_ws(prefix)
    suffix_w = wo_ws(suffix)

    old_fontname_spl = font_fontname.split("-")
    if len(old_fontname_spl) > 1:
        old_fontname = "-".join(old_fontname_spl[:-1])
        weight = old_fontname_spl[-1]
    else:
        old_fontname = font_fontname
        weight = None

    new_name_w = prefix_w + old_fontname + suffix_w

    # Replace the old name with the new name whether or not a weight was present.
    # If a weight was present, append it accordingly.
    if weight:
        return "%s-%s" % (new_name_w, weight)
    else:
        return new_name_w


def main():
    print(fontname(f, p, s))


if __name__ == "__main__":
    main()
