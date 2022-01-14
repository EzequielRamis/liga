# This is an autogenerated configuration that includes, principally, a set of
# curated features that ligate.py will attempt to copy from Fira Code to your
# output font. Each feature may have a list of lookups (it can also have an
# empty list). Features/lookups that aren't present in the version of Fira Code
# you're using will be skipped. To disable features/lookups, simply comment
# them out in this file.
#
# If you don't know what are these features, take a look at https://github.com/tonsky/FiraCode#readme.

config = {
    # When copying character glyphs from FiraCode, sometimes it is necessary to
    # adjust manually the glyph size by a scale factor. It will be ignored if
    # it's less than or equal to 0.
    "scale": 0.95,
    # Like above, sometimes it is necessary to translate it vertically by a
    # factor and direction. It can be any float, including zero and negatives.
    "yTranslate": 0.0,
    # Copy glyphs for individual characters from the ligature font as well.
    # Each item value is a postscript name from the FiraCode family, that can
    # be queried from the FontForge's GUI. It's also useful for characters
    # outside ligature contexts.
    "glyphs": [
        # "ampersand",
        "asciicircum",
        "asciitilde",
        "asterisk",
        "asteriskmath",
        "backslash",
        "bar",
        # "colon",
        # "equal",
        "exclam",
        "greater",
        # "hyphen",
        "less",
        "numbersign",
        # "percent",
        "period",
        "plus",
        "question",
        # "semicolon",
        "slash",
        "underscore",
        # "at",
        # "braceleft",
        # "braceright",
        # "bracketleft",
        # "bracketright",
        # "dollar",
        # "parenleft",
        # "parenright",
    ],
    "features": {
        "calt": [
            "less_bar_greater",
            "bar_bar_bar_greater",
            "less_bar_bar_bar",
            "bar_bar_greater",
            "less_bar_bar",
            "bar_greater",
            "less_bar",
            "bar_bar_bar",
            "greater_greater_greater",
            "less_less_less",
            "bar_bar",
            "greater_greater",
            "less_less",
            "less_exclam_hyphen_hyphen",
            "asciitilde_asciitilde_greater",
            "asterisk_asterisk_asterisk",
            "colon_colon_colon",
            "colon_colon_equal",
            "equal_equal_equal",
            "exclam_equal_equal",
            "exclam_exclam_period",
            "less_asciitilde_asciitilde",
            "less_asciitilde_greater",
            "less_asterisk_greater",
            "less_dollar_greater",
            "less_plus_greater",
            "less_slash_greater",
            "numbersign_underscore_parenleft",
            "period_period_equal",
            "period_period_less",
            "period_period_period",
            "plus_plus_plus",
            "slash_slash_slash",
            "w_w_w",
            # "ampersand_ampersand",
            "asciicircum_equal",
            "asciitilde_asciitilde",
            "asciitilde_at",
            "asciitilde_greater",
            "asciitilde_hyphen",
            "asterisk_asterisk",
            "asterisk_greater",
            "asterisk_slash",
            "bar_braceright",
            "bar_bracketright",
            "braceleft_bar",
            "bracketleft_bar",
            "bracketright_numbersign",
            "colon_colon",
            "colon_equal",
            "dollar_greater",
            "equal_equal",
            "exclam_equal",
            "exclam_exclam",
            "greater_equal",
            "hyphen_asciitilde",
            "hyphen_hyphen",
            "less_asciitilde",
            "less_asterisk",
            "less_dollar",
            "less_equal",
            "less_greater",
            "less_plus",
            "less_slash",
            "numbersign_braceleft",
            "numbersign_bracketleft",
            "numbersign_colon",
            "numbersign_equal",
            "numbersign_exclam",
            "numbersign_parenleft",
            "numbersign_question",
            "numbersign_underscore",
            # "percent_percent",
            "period_period",
            "period_question",
            "plus_greater",
            "plus_plus",
            "question_equal",
            "question_period",
            "question_question",
            # "semicolon_semicolon",
            "slash_asterisk",
            "slash_greater",
            "slash_slash",
            "center",
            "slash_backslash",
            "backslash_slash",
            "hexadecimal_x",
            "equal_arrows",
            "hyphen_arrows",
            # "lowercase_hyphen",
            # "lowercase_plus",
            "lowercase_asterisk",
            "lowercase_asteriskmath",
            # "uppercase_colon",
            "numbersigns",
            "underscores",
        ],
        "ss02": [],
        "ss03": [],
        "ss04": [],
        "ss05": [],
        "ss06": [
            "backslash_thin",
        ],
        "ss07": [
            "equal_asciitilde",
            "exclam_asciitilde",
        ],
        "ss08": [],
        "ss09": [
            "restore_greater_greater_equal",
            "restore_less_less_equal",
            "restore_bar_bar_equal",
            "restore_bar_equal",
        ],
        "cv15": [],
        "cv16": [],
        "cv17": [],
        "cv18": [],
        "cv19": [],
        "cv20": [
            "less_equal_cv20",
        ],
        "cv21": [
            "equal_less_cv21",
        ],
        "cv22": [
            "equal_less_cv22",
        ],
        "cv23": [],
        "cv24": [
            "slash_equal_as_not_equal",
        ],
        "cv25": [
            "period_hyphen",
        ],
        "cv26": [
            "colon_hyphen",
        ],
        "cv27": [
            "bracketleft_bracketright",
        ],
        "cv28": [],
        "cv29": [],
        "cv30": [],
        "cv31": [],
        "cv32": [
            "period_equal",
        ],
    },
}
