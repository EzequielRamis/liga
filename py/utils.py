import re
import os
from pathlib import Path

def relative_from_project(p):
    liga = Path(__file__).resolve().parent.parent
    return os.path.relpath(p, liga)


def lookups(s):
    return re.findall("(?<=lookup )([\s\S]*?)(?= \{)", s)


def remove_last_newlines(s):
    while s[-1:] == "\n" and len(s) > 0:
        s = s[:-1]
    return s


def remove_duplicates(l):
    return list(dict.fromkeys(l))


def add_lookups_prefix(code):
    return re.sub(
        "(?<=\})\s+(?=\w+;)", " fira_", re.sub("lookup ", "lookup fira_", code)
    )


def add_backslash_to_glyphs(code):
    splitted_code = code.split("\n")
    new_code = []
    for line in splitted_code:
        if re.search("(sub|by)\s+", line) is not None:
            splitted_line = re.split("\s+", re.sub("#.+", "", line))
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


def uni(number):
    return hex(number).upper().replace("0X", "uni")


def uni_range(start, end):
    return "\n".join([f'        "{uni(u)}",' for u in range(start, end + 1)])
