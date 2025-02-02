# Copyright (c) 2021,2022,2023,2024,2025 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Packpage of different e-book formats."""

import argparse
from typing import Union

import txt2ebook.models.book
from txt2ebook.formats.epub import TEMPLATES as EPUB_TEMPLATES
from txt2ebook.formats.epub import EpubWriter
from txt2ebook.formats.gmi import GmiWriter
from txt2ebook.formats.md import MdWriter
from txt2ebook.formats.pdf import PdfWriter
from txt2ebook.formats.tex import TexWriter
from txt2ebook.formats.txt import TxtWriter
from txt2ebook.formats.typ import TypWriter
from txt2ebook.helpers import load_class, to_classname
from txt2ebook.models import Book

EBOOK_FORMATS = ["epub", "gmi", "md", "pdf", "tex", "txt", "typ"]
PAGE_SIZES = [
    "a0",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "b0",
    "b1",
    "b2",
    "b3",
    "b4",
    "b5",
    "b6",
    "elevenseventeen",
    "legal",
    "letter",
]


def create_format(
    book: txt2ebook.models.book.Book,
    ebook_format: str,
    config: argparse.Namespace,
) -> Union[TxtWriter, EpubWriter]:
    """Create ebook formatter by format using factory function.

    Args:
        book(txt2ebook.models.book.Book): The book model which contains
        metadata and table of contents of volumes and chapters.
        ebook_format(str): The ebook format.
        config(argparse.Namespace): The configs from the command-line.

    Returns:
        TxtWriter | EpubWriter
    """
    class_name = to_classname(ebook_format, "Writer")
    klass = load_class("txt2ebook.formats", class_name)
    formatter = klass(book, config)
    return formatter


__all__ = [
    "Book",
    "EBOOK_FORMATS",
    "EPUB_TEMPLATES",
    "EpubWriter",
    "GmiWriter",
    "MdWriter",
    "PAGE_SIZES",
    "PdfWriter",
    "TexWriter",
    "TxtWriter",
    "TypWriter",
]
