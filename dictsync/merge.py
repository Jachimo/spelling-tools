# dictsync/merge.py

import argparse
import sys

from .utils import *

def main():
    parser = argparse.ArgumentParser(
        description="Merge Chrome and Firefox spell checker dictionary files."
    )
    parser.add_argument(
        'inputs',
        metavar='INPUT',
        nargs='+',
        help='Input dictionary files (Chrome or Firefox format).'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output filename (e.g., merged.dat or merged.txt)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['apple', 'chrome', 'firefox'],
        required=True,
        help='Output format: "apple", "chrome" or "firefox"'
    )

    args = parser.parse_args()

    all_words = set()
    for input_file in args.inputs:
        fmt = detect_format(input_file)
        if fmt not in ['chrome-old', 'chrome-new', 'firefox', 'apple']:
            print(f"Unsupported format '{fmt}' for file: {input_file}", file=sys.stderr)
            return 1
        
        try:
            if fmt == 'chrome-old':
                words = read_chrome_old_dict(input_file)
            if fmt == 'chrome-new':
                words = read_chrome_new_dict(input_file)
            if fmt == 'firefox':
                words = read_firefox_dict(input_file)
            if fmt == 'apple':
                words = read_firefox_dict(input_file)  # same format as Firefox
            all_words.update(words)
        except Exception as e:
            print(f"Error while reading {input_file}: {e}", file=sys.stderr)
            return 1

    if args.format == 'apple':
        write_firefox_dict(all_words, args.output)
    if args.format == 'chrome':
        write_chrome_dict(all_words, args.output)
    if args.format == 'firefox':
        write_firefox_dict(all_words, args.output)

    print(f"Merged {len(args.inputs)} files into '{args.output}' ({len(all_words)} unique words, {args.format} format).")
    return 0  # no error

if __name__ == '__main__':
    sys.exit(main())
