# -*- coding: utf-8 -*-
from __future__ import absolute_import


class LavaUIFactory(object):

    # Colors
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    # Effects
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    FAST_BLINK = 6

    # Escape codes
    ESCAPE_SEQUENCE = "\033[%sm"
    END_SEQUENCE = "\033[0m"

    # Lavalamp color map
    lavalamp_color_map = {
        "█": [
            CYAN,
            BOLD
        ],
        "▄": [
            CYAN
        ],
        "▀": [
            CYAN
        ],
        "▐": [
            CYAN
        ],
        "▒": [
            RED,
            BOLD
        ],
        "▓": [
            RED,
            BOLD
        ],
        "░": [
            RED
        ]
    }

    # Lavalamp splash
    lavalamp_splash = '''

     ██▓     ▄▄▄       ██▒   █▓ ▄▄▄       ██▓     ▄▄▄       ███▄ ▄███▓ ██▓███
    ▓██▒    ▒████▄    ▓██░   █▒▒████▄    ▓██▒    ▒████▄    ▓██▒▀█▀ ██▒▓██░  ██▒
    ▒██░    ▒██  ▀█▄   ▓██  █▒░▒██  ▀█▄  ▒██░    ▒██  ▀█▄  ▓██    ▓██░▓██░ ██▓▒
    ▒██░    ░██▄▄▄▄██   ▒██ █░░░██▄▄▄▄██ ▒██░    ░██▄▄▄▄██ ▒██    ▒██ ▒██▄█▓▒ ▒
    ░██████▒ ▓█   ▓██▒   ▒▀█░   ▓█   ▓██▒░██████▒ ▓█   ▓██▒▒██▒   ░██▒▒██▒ ░  ░
    ░ ▒░▓  ░ ▒▒   ▓▒█░   ░ ▐░   ▒▒   ▓▒█░░ ▒░▓  ░ ▒▒   ▓▒█░░ ▒░   ░  ░▒▓▒░ ░  ░
    ░ ░ ▒  ░  ▒   ▒▒ ░   ░ ░░    ▒   ▒▒ ░░ ░ ▒  ░  ▒   ▒▒ ░░  ░      ░░▒ ░
      ░ ░     ░   ▒        ░░    ░   ▒     ░ ░     ░   ▒   ░      ░   ░░
        ░  ░      ░  ░      ░        ░  ░    ░  ░      ░  ░       ░
                           ░

'''

    @classmethod
    def apply_text_effects(cls, input_text, input_effects):
        """
        Colorize the contents of the given text based on the given text effects map.
        :param input_text: The text to colorize.
        :param input_effects: A dictionary mapping characters to the stylization to apply.
        :return: The stylized string.
        """
        effects = ";".join([str(x) for x in input_effects])
        begin_sequence = cls.ESCAPE_SEQUENCE % effects
        return begin_sequence + input_text + cls.END_SEQUENCE

    @classmethod
    def get_colorized_lavalamp_splash(cls):
        """
        Get a colorized version of self.lavalamp_splash.
        :return: A colorized version of self.lavalamp_splash.
        """
        to_return = cls.lavalamp_splash
        for cur_key in cls.lavalamp_color_map.keys():
            effect_char = cls.apply_text_effects(
                cur_key,
                cls.lavalamp_color_map[cur_key]
            )
            to_return = to_return.replace(cur_key, effect_char)
        return to_return
