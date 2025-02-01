#!/usr/bin/env python3

import argparse
from spellchecker import SpellChecker

spell = SpellChecker()

asciimap = {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b", "z": "s"}


def leet(txt):
    """Convert normal text to leetspeak."""
    mapping = {ord(v): k for k, v in asciimap.items()}
    return txt.translate(mapping)


def unleet(txt):
    """Convert leetspeak text to normal text with spell correction."""
    mapping = {ord(k): v for k, v in asciimap.items()}
    output = []
    unleeted = txt.translate(mapping).split(" ")

    for word in unleeted:
        if word and word.isalpha():
            try:
                output.append(spell.correction(word.strip()) or word)
            except TypeError:
                output.append(word)
        else:
            output.append(word)

    return " ".join(output)


def main():
    parser = argparse.ArgumentParser(description="Convert text to leetspeak or back to normal.")
    parser.add_argument("text", type=str, help="The text to convert")
    parser.add_argument(
        "-u", "--unleet", action="store_true",
        help="Convert from leetspeak back to normal (default: convert to leetspeak)"
    )

    args = parser.parse_args()

    if args.unleet:
        print(unleet(args.text))
    else:
        print(leet(args.text))


if __name__ == "__main__":
    main()