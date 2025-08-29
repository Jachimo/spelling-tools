"""Utility functions for working with dictionary files."""

import os
import zlib
import hashlib

def detect_format(path):
    """Detects dictionary format by filename or content."""
    basename = os.path.basename(path)
    if basename.startswith('LocalDictionary'):
        return 'apple'  # Mac OS format is similar to Firefox
    if basename.lower().endswith('.dat'):
        return 'firefox'
    if basename.lower().endswith('.txt'):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) == 1 and ',' in lines[0]:  # single-line Chrome format, no checksum
                return 'chrome-old'
            if len(lines) == 2 and lines[1].strip().isdigit():  # single-line Chrome format w/ checksum
                return 'chrome-old'
            if lines[-1].strip().startswith('checksum'):  # multi-line Chrome format
                return 'chrome-new'
    raise ValueError(f"Cannot determine format of file: {path}")

def read_firefox_dict(path):
    """Reads Firefox personal dictionary file, returns set of words."""
    words = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                words.add(word)
    return words

def read_chrome_new_dict(path):
    """Reads Chrome new-format personal dictionary file, returns set of words."""
    words = set()
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for word in lines[:-1]:  # all but last line
            word = word.strip()
            if word:
                words.add(word)
    return words

def read_chrome_old_dict(path):
    """Reads Chrome old-style dictionary file, returns set of words."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            return set()
        # First line: comma-separated words
        words = set(lines[0].strip().split(',')) if lines[0].strip() else set()
        return words

def write_firefox_dict(words, output_path):
    """Writes word set to a Firefox-format dictionary file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for word in sorted(words, key=str.casefold):
            f.write(word + '\n')

def write_chrome_dict(words, output_path):
    """Writes word set to a Chrome-format dictionary file, with MD5 checksum."""
    word_str = '\n'.join(sorted(words, key=str.casefold)) + '\n'  # trailing LF is important
    checksum =  hashlib.md5(word_str.encode('utf-8')).hexdigest()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(word_str)
        f.write('checksum_v1 = ' + str(checksum))

def write_chrome_old_dict(words, output_path):
    """Writes word set to an old-style Chrome-format dictionary file, with CRC32 checksum."""
    word_line = ','.join(sorted(words, key=str.casefold))
    checksum = zlib.crc32(word_line.encode('utf-8'))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(word_line + '\n')
        f.write(checksum)
