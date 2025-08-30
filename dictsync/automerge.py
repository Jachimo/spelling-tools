# automerge.py - Automatically find and merge spell checker dictionaries from common locations.

import os
import sys
import argparse
import glob
from pathlib import Path

from .utils import *

def find_firefox_dicts():
    """Find Firefox personal dictionary files in common locations."""
    dicts = []
    home = str(Path.home())

    # Linux
    linux_profiles = os.path.join(home, ".mozilla/firefox")
    if os.path.isdir(linux_profiles):
        dicts += glob.glob(os.path.join(linux_profiles, "*/persdict.dat"))

    # macOS
    mac_profiles = os.path.join(home, "Library/Application Support/Firefox/Profiles")
    if os.path.isdir(mac_profiles):
        dicts += glob.glob(os.path.join(mac_profiles, "*/persdict.dat"))

    # Windows
    appdata = os.environ.get("APPDATA")
    if appdata:
        win_profiles = os.path.join(appdata, "Mozilla/Firefox/Profiles")
        if os.path.isdir(win_profiles):
            dicts += glob.glob(os.path.join(win_profiles, "*/persdict.dat"))

    return dicts

def find_chrome_dicts():
    """Find Chrome custom dictionary files in common locations."""
    dicts = []
    home = str(Path.home())

    # Linux
    linux_dict = os.path.join(home, ".config/google-chrome/Default/Custom Dictionary.txt")
    if os.path.isfile(linux_dict):
        dicts.append(linux_dict)

    # macOS
    mac_dict = os.path.join(home, "Library/Application Support/Google/Chrome/Default/Custom Dictionary.txt")
    if os.path.isfile(mac_dict):
        dicts.append(mac_dict)

    # Windows
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        win_dict = os.path.join(localappdata, "Google/Chrome/User Data/Default/Custom Dictionary.txt")
        if os.path.isfile(win_dict):
            dicts.append(win_dict)

    return dicts

def find_apple_dict():
    """Find Apple system-wide custom dictionary (macOS only)."""
    home = str(Path.home())
    apple_dict = os.path.join(home, "Library/Spelling/LocalDictionary")
    if os.path.isfile(apple_dict):
        return [apple_dict]
    return []

def find_all_dicts():
    """Find all known dictionary files on this system."""
    dicts = []
    dicts += find_firefox_dicts()
    dicts += find_chrome_dicts()
    dicts += find_apple_dict()
    return dicts

def read_dict_file(path):
    """Read a dictionary file and return its set of words."""
    fmt = detect_format(path)
    if fmt == 'chrome-old':
        return read_chrome_old_dict(path)
    if fmt == 'chrome-new':
        return read_chrome_new_dict(path)
    if fmt == 'firefox':
        return read_firefox_dict(path)
    if fmt == 'apple':
        return read_firefox_dict(path)  # Apple uses Firefox format
    raise ValueError(f"Unsupported dictionary format: {fmt}")

def main():
    parser = argparse.ArgumentParser(
        description="Automatically find and merge spell checker dictionaries from common locations."
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output filename (e.g., merged.dat or merged.txt)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['chrome', 'firefox'],
        required=True,
        help='Output format: "chrome" or "firefox"'
    )
    parser.add_argument(
        '--show-found',
        action='store_true',
        help='Show found dictionary files and exit'
    )

    args = parser.parse_args()

    dict_files = find_all_dicts()

    if args.show_found:
        print("Found dictionary files:")
        for f in dict_files:
            print(f)
        return 0

    if not dict_files:
        print("No dictionary files found in common locations.", file=sys.stderr)
        return 1

    all_words = set()
    for path in dict_files:
        try:
            words = read_dict_file(path)
            all_words.update(words)
        except Exception as e:
            print(f"Error reading {path}: {e}", file=sys.stderr)

    if args.format == 'chrome':
        write_chrome_dict(all_words, args.output)
    elif args.format == 'firefox':
        write_firefox_dict(all_words, args.output)

    print(f"Merged {len(dict_files)} files into '{args.output}' ({len(all_words)} unique words, {args.format} format).")
    return 0

if __name__ == '__main__':
    sys.exit(main())
