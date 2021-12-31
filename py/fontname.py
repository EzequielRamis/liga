def camelcase(s):
    return "".join([ss[0].upper() + ss[1:] for ss in s.split(" ") if len(ss) > 0])


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


def safe_add_fullname_weight(old_flname, name):
    family, weight = slice_fullname(old_flname)
    if len(family) > 0:
        name_weighted = add_fullname_weight(name, weight)
    else:
        name_weighted = name
    return name_weighted


def safe_add_postname_weight(old_psname, name):
    family, weight = slice_postscript(old_psname)
    psname = camelcase(name)
    if len(family) > 0:
        psname_weighted = add_postscript_weight(psname, weight)
    else:
        psname_weighted = psname
    return psname_weighted
