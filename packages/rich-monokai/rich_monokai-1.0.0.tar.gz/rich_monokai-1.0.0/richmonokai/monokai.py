#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2021 Matt Doyle

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import types

from rich.color import Color
from rich.console import Console as DefaultConsole
from rich.progress import Progress
from rich.style import Style
from rich.text import Text
from rich.theme import Theme


COLOR = types.SimpleNamespace(
    BLACK=Color.from_ansi(235),
    BLUE=Color.from_ansi(81),
    BROWN=Color.from_ansi(95),
    DARK_GRAY=Color.from_ansi(237),
    GREEN=Color.from_ansi(148),
    LIGHT_GRAY=Color.from_ansi(238),
    ORANGE=Color.from_ansi(208),
    PURPLE=Color.from_ansi(141),
    RED=Color.from_ansi(197),
    WHITE=Color.from_ansi(231),
    YELLOW=Color.from_ansi(222),
)


BACKGROUND = types.SimpleNamespace(
    BLACK=Style(bgcolor=COLOR.BLACK),
    BLUE=Style(bgcolor=COLOR.BLUE),
    BROWN=Style(bgcolor=COLOR.BROWN),
    DARK_GRAY=Style(bgcolor=COLOR.DARK_GRAY),
    GREEN=Style(bgcolor=COLOR.GREEN),
    LIGHT_GRAY=Style(bgcolor=COLOR.LIGHT_GRAY),
    ORANGE=Style(bgcolor=COLOR.ORANGE),
    PURPLE=Style(bgcolor=COLOR.PURPLE),
    RED=Style(bgcolor=COLOR.RED),
    WHITE=Style(bgcolor=COLOR.WHITE),
    YELLOW=Style(bgcolor=COLOR.YELLOW),
)


FOREGROUND = types.SimpleNamespace(
    BLACK=Style(color=COLOR.BLACK),
    BLUE=Style(color=COLOR.BLUE),
    BROWN=Style(color=COLOR.BROWN),
    DARK_GRAY=Style(color=COLOR.DARK_GRAY),
    GREEN=Style(color=COLOR.GREEN),
    LIGHT_GRAY=Style(color=COLOR.LIGHT_GRAY),
    ORANGE=Style(color=COLOR.ORANGE),
    PURPLE=Style(color=COLOR.PURPLE),
    RED=Style(color=COLOR.RED),
    WHITE=Style(color=COLOR.WHITE),
    YELLOW=Style(color=COLOR.YELLOW),
)


ATTRIBUTE = types.SimpleNamespace(
    BLINK=Style(blink=True),
    BLINK2=Style(blink2=True),
    BOLD=Style(bold=True),
    CONCEAL=Style(conceal=True),
    DIM=Style(dim=True),
    ENCIRCLE=Style(encircle=True),
    FRAME=Style(frame=True),
    ITALIC=Style(italic=True),
    NOT_BOLD=Style(bold=False),
    NOT_DIM=Style(dim=False),
    NOT_ITALIC=Style(italic=False),
    OVERLINE=Style(overline=True),
    REVERSE=Style(reverse=True),
    STRIKE=Style(strike=True),
    UNDERLINE=Style(underline=True),
    UNDERLINE2=Style(underline2=True),
    RESET=Style(
        bold=False,
        dim=False,
        italic=False,
        underline=False,
        blink=False,
        blink2=False,
        reverse=False,
        conceal=False,
        strike=False,
        underline2=False,
        frame=False,
        encircle=False,
        overline=False,
    ),
)


class MonokaiTheme(Theme):

    def __init__(self):
        super().__init__(
            styles={
                "bar.back": FOREGROUND.LIGHT_GRAY,
                "bar.complete": FOREGROUND.GREEN,
                "bar.finished": FOREGROUND.GREEN,
                "bar.pulse": FOREGROUND.ORANGE,
                "black": FOREGROUND.BLACK,
                "blink": ATTRIBUTE.BLINK,
                "blink2": ATTRIBUTE.BLINK2,
                "bold": ATTRIBUTE.BOLD,
                "bright": ATTRIBUTE.NOT_DIM,
                "code": ATTRIBUTE.BOLD + ATTRIBUTE.REVERSE,
                "cyan": FOREGROUND.BLUE,
                "dim": ATTRIBUTE.DIM,
                "emphasize": ATTRIBUTE.ITALIC,
                "green": FOREGROUND.GREEN,
                "inspect.async_def": FOREGROUND.BLUE + ATTRIBUTE.ITALIC,
                "inspect.attr.dunder": FOREGROUND.YELLOW
                + ATTRIBUTE.DIM
                + ATTRIBUTE.ITALIC,
                "inspect.attr": FOREGROUND.YELLOW + ATTRIBUTE.ITALIC,
                "inspect.callable": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "inspect.class": FOREGROUND.BLUE + ATTRIBUTE.ITALIC,
                "inspect.def": FOREGROUND.BLUE + ATTRIBUTE.ITALIC,
                "inspect.doc": ATTRIBUTE.DIM,
                "inspect.equals": "none",
                "inspect.error": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "inspect.help": FOREGROUND.BLUE,
                "inspect.value.border": FOREGROUND.GREEN,
                "iso8601.date": FOREGROUND.BLUE,
                "iso8601.time": FOREGROUND.RED,
                "iso8601.timezone": FOREGROUND.YELLOW,
                "italic": ATTRIBUTE.ITALIC,
                "json.bool_false": FOREGROUND.RED + ATTRIBUTE.ITALIC,
                "json.bool_true": FOREGROUND.GREEN + ATTRIBUTE.ITALIC,
                "json.brace": ATTRIBUTE.BOLD,
                "json.key": FOREGROUND.BLUE + ATTRIBUTE.BOLD,
                "json.null": FOREGROUND.RED + ATTRIBUTE.ITALIC,
                "json.number": FOREGROUND.BLUE + ATTRIBUTE.BOLD + ATTRIBUTE.NOT_ITALIC,
                "json.str": FOREGROUND.GREEN
                + ATTRIBUTE.NOT_BOLD
                + ATTRIBUTE.NOT_ITALIC,
                "layout.tree.column": FOREGROUND.BLUE + ATTRIBUTE.NOT_DIM,
                "layout.tree.row": FOREGROUND.RED + ATTRIBUTE.NOT_DIM,
                "live.ellipsis": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "log.level": "none",
                "log.message": "none",
                "log.path": ATTRIBUTE.DIM,
                "log.time": FOREGROUND.BLUE + ATTRIBUTE.DIM,
                "logging.keyword": FOREGROUND.YELLOW + ATTRIBUTE.BOLD,
                "logging.level.critical": FOREGROUND.RED
                + ATTRIBUTE.BOLD
                + ATTRIBUTE.REVERSE,
                "logging.level.debug": FOREGROUND.GREEN,
                "logging.level.error": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "logging.level.info": FOREGROUND.BLUE,
                "logging.level.notset": ATTRIBUTE.DIM,
                "logging.level.warning": FOREGROUND.YELLOW,
                "magenta": FOREGROUND.RED,
                "markdown.block_quote": FOREGROUND.RED,
                "markdown.code_block": FOREGROUND.BLUE + BACKGROUND.BLACK,
                "markdown.code": FOREGROUND.BLUE + BACKGROUND.BLACK + ATTRIBUTE.BOLD,
                "markdown.em": ATTRIBUTE.ITALIC,
                "markdown.emph": ATTRIBUTE.ITALIC,
                "markdown.h1.border": "none",
                "markdown.h1": ATTRIBUTE.BOLD,
                "markdown.h2": ATTRIBUTE.BOLD + ATTRIBUTE.UNDERLINE,
                "markdown.h3": ATTRIBUTE.BOLD,
                "markdown.h4": ATTRIBUTE.BOLD + ATTRIBUTE.DIM,
                "markdown.h5": ATTRIBUTE.UNDERLINE,
                "markdown.h6": ATTRIBUTE.ITALIC,
                "markdown.h7": ATTRIBUTE.DIM + ATTRIBUTE.ITALIC,
                "markdown.hr": FOREGROUND.YELLOW,
                "markdown.item.bullet": FOREGROUND.YELLOW + ATTRIBUTE.BOLD,
                "markdown.item.number": FOREGROUND.YELLOW + ATTRIBUTE.BOLD,
                "markdown.item": "none",
                "markdown.link_url": FOREGROUND.BLUE + ATTRIBUTE.UNDERLINE,
                "markdown.link": FOREGROUND.BLUE + ATTRIBUTE.NOT_DIM,
                "markdown.list": FOREGROUND.BLUE,
                "markdown.paragraph": "none",
                "markdown.s": ATTRIBUTE.STRIKE,
                "markdown.strong": ATTRIBUTE.BOLD,
                "markdown.text": "none",
                "none": "none",
                "pretty": "none",
                "progress.data.speed": FOREGROUND.RED,
                "progress.description": FOREGROUND.WHITE,
                "progress.download": FOREGROUND.GREEN,
                "progress.elapsed": FOREGROUND.YELLOW,
                "progress.filesize.total": FOREGROUND.GREEN,
                "progress.filesize": FOREGROUND.GREEN,
                "progress.percentage": FOREGROUND.RED,
                "progress.remaining": FOREGROUND.BLUE,
                "progress.spinner": FOREGROUND.GREEN,
                "prompt.choices": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "prompt.default": FOREGROUND.BLUE + ATTRIBUTE.BOLD,
                "prompt.invalid.choice": FOREGROUND.RED,
                "prompt.invalid": FOREGROUND.RED,
                "prompt": FOREGROUND.WHITE,
                "red": FOREGROUND.RED,
                "repr.attrib_equal": ATTRIBUTE.BOLD,
                "repr.attrib_name": FOREGROUND.YELLOW + ATTRIBUTE.NOT_ITALIC,
                "repr.attrib_value": FOREGROUND.RED + ATTRIBUTE.NOT_ITALIC,
                "repr.bool_false": FOREGROUND.RED + ATTRIBUTE.ITALIC,
                "repr.bool_true": FOREGROUND.GREEN + ATTRIBUTE.ITALIC,
                "repr.brace": ATTRIBUTE.BOLD,
                "repr.call": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "repr.comma": ATTRIBUTE.BOLD,
                "repr.ellipsis": FOREGROUND.YELLOW,
                "repr.error": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "repr.eui48": FOREGROUND.GREEN + ATTRIBUTE.BOLD,
                "repr.eui64": FOREGROUND.GREEN + ATTRIBUTE.BOLD,
                "repr.filename": FOREGROUND.RED + ATTRIBUTE.NOT_DIM,
                "repr.indent": FOREGROUND.DARK_GRAY,
                "repr.ipv4": FOREGROUND.GREEN + ATTRIBUTE.BOLD,
                "repr.ipv6": FOREGROUND.GREEN + ATTRIBUTE.BOLD,
                "repr.none": FOREGROUND.RED + ATTRIBUTE.ITALIC,
                "repr.number_complex": FOREGROUND.BLUE
                + ATTRIBUTE.BOLD
                + ATTRIBUTE.NOT_ITALIC,
                "repr.number": FOREGROUND.BLUE + ATTRIBUTE.BOLD + ATTRIBUTE.NOT_ITALIC,
                "repr.path": FOREGROUND.RED,
                "repr.str": FOREGROUND.GREEN
                + ATTRIBUTE.NOT_BOLD
                + ATTRIBUTE.NOT_ITALIC,
                "repr.tag_contents": "none",
                "repr.tag_end": ATTRIBUTE.BOLD,
                "repr.tag_name": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "repr.tag_start": ATTRIBUTE.BOLD,
                "repr.url": FOREGROUND.BLUE
                + ATTRIBUTE.NOT_BOLD
                + ATTRIBUTE.NOT_ITALIC
                + ATTRIBUTE.UNDERLINE,
                "repr.uuid": FOREGROUND.YELLOW + ATTRIBUTE.NOT_BOLD,
                "reset": FOREGROUND.WHITE + BACKGROUND.BLACK + ATTRIBUTE.RESET,
                "reverse": ATTRIBUTE.REVERSE,
                "rule.line": FOREGROUND.GREEN,
                "rule.text": FOREGROUND.BLUE,
                "scope.border": FOREGROUND.BLUE,
                "scope.equals": FOREGROUND.RED,
                "scope.key.special": FOREGROUND.YELLOW
                + ATTRIBUTE.DIM
                + ATTRIBUTE.ITALIC,
                "scope.key": FOREGROUND.YELLOW + ATTRIBUTE.ITALIC,
                "status.spinner": FOREGROUND.GREEN,
                "strike": ATTRIBUTE.STRIKE,
                "strong": ATTRIBUTE.BOLD,
                "table.caption": ATTRIBUTE.DIM + ATTRIBUTE.ITALIC,
                "table.cell": "none",
                "table.footer": ATTRIBUTE.BOLD,
                "table.header": FOREGROUND.WHITE + ATTRIBUTE.BOLD,
                "table.title": ATTRIBUTE.ITALIC,
                "traceback.border.syntax_error": FOREGROUND.RED,
                "traceback.border": FOREGROUND.RED,
                "traceback.error_range": ATTRIBUTE.BOLD
                + ATTRIBUTE.NOT_DIM
                + ATTRIBUTE.UNDERLINE,
                "traceback.error": FOREGROUND.RED + ATTRIBUTE.ITALIC,
                "traceback.exc_type": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "traceback.exc_value": "none",
                "traceback.offset": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "traceback.text": "none",
                "traceback.title": FOREGROUND.RED + ATTRIBUTE.BOLD,
                "tree.line": "none",
                "tree": "none",
                "underline": ATTRIBUTE.UNDERLINE,
                "white": FOREGROUND.WHITE,
                "yellow": FOREGROUND.YELLOW,
            }
        )


class MonokaiConsole(DefaultConsole):

    def __init__(self, *args, **kwargs):
        new_kwargs = {"theme": MonokaiTheme()}
        super().__init__(*args, **new_kwargs)

    def PrintWithLabel(self, label, message, label_fg=FOREGROUND.WHITE):
        self.print(f"{label}:", style=label_fg + ATTRIBUTE.BOLD, end=" ")
        self.print(f"{message}", style=FOREGROUND.WHITE + ATTRIBUTE.NOT_BOLD, end="\n")

    def PrintException(self, ex):
        self.PrintFailure(ex.__class__.__name__, str(ex))

    def PrintFailure(self, label, message):
        self.PrintWithLabel(label, message, label_fg=FOREGROUND.RED)

    def PrintStatus(self, label, message):
        self.PrintWithLabel(label, message, label_fg=FOREGROUND.BLUE)

    def PrintSuccess(self, label, message):
        self.PrintWithLabel(label, message, label_fg=FOREGROUND.GREEN)

    def Status(self, message):
        style = FOREGROUND.ORANGE + ATTRIBUTE.BOLD
        return self.status(Text(message, style=style), spinner_style=style)
