import re


def lookups(s):
    return re.findall("(?<=lookup )([\s\S]*?)(?= \{)", s)


def remove_last_newlines(s):
    while s[-1:] == "\n" and len(s) > 0:
        s = s[:-1]
    return s


def add_backslash_to_glyphs(code):
    splitted_code = code.split("\n")
    new_code = []
    for line in splitted_code:
        if re.search("sub\s+", line) is not None:
            splitted_line = re.split("\s+", line)
            line_res = []
            for token in splitted_line:
                if token != "":
                    if token not in ["sub", "ignore", "by", ";"] and (
                        (token[0] == "[" and token[1] not in ["@", "\\"])
                        or (token[0] not in ["[", "@", "\\"])
                    ):
                        if token[0] != "[":
                            line_res.append("\\" + token)
                        else:
                            line_res.append("[\\" + token[1:])
                    else:
                        line_res.append(token)
                else:
                    line_res.append("   ")
            new_line = " ".join(line_res)
        else:
            new_line = line
        new_code.append(new_line)
    return "\n".join(new_code)
