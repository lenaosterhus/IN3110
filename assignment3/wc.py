#!/usr/bin/env python3

import sys
import os

def word_count():
    """A Python implementation which counts the lines, words and character of files.

    When called with a file name as command line argument, the implementation prints
    the single line a b c fn where a is the number of lines in the file, b the
    number of words, c the number of characters, and fn the filename.

    A line is defined as a string of characters delimited by a <newline> character.
    A word is defined as a string of characters delimited by white space characters.
    A character is defined as the smallest unit of information that includes space,
    tab and newline.
    """

    total_lines = 0
    total_words = 0
    total_characters = 0

    for path in sys.argv[1:]:

        if os.path.isfile(path):

            with open(path, 'r') as file:
                lines = 0
                words = 0
                characters = 0

                for line in file:
                    lines += 1
                    words += len(line.split())
                    characters += len(line)

                print(f"{lines:>7} {words:>7} {characters:>7} {path}")

                total_lines += lines
                total_words += words
                total_characters += characters

    if len(sys.argv) > 2:
        # More than one file
        print(f"{total_lines:>7} {total_words:>7} {total_characters:>7} total")

word_count()
