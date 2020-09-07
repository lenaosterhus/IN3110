#!/usr/bin/env python3

import sys

file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = 0
    """A line is defined as a string of characters delimited
         by a <newline> character"""
    words = 0
    """A word is defined as a string of characters delimited by white space
         characters."""
    characters = 0
    """A character is the smallest unit of information that includes space, tab and newline."""

    for line in file:
        lines += 1
        words += len(line.split())
        characters += len(line)

    print(f"{lines}   {words}   {characters}   {file_name}")
