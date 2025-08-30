# spelling-tools

> Tools for working with spell-check dictionaries.

The intent is for this repository to eventually contain multiple tools (as a monorepo) related to managing personal word lists for spell checkers.

## General Notes

This project uses [Poetry](https://python-poetry.org/) for dependency management.

It is recommended to install Poetry via the official installer script:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

## dictsync merge

Synchronize (by merging) personal dictionaries for Firefox, Chrome, and Apple's system-wide spell checker (used by Safari on Mac).

### Features

- Detects and reads Chrome (single-line, comma-delimited, `.txt` suffix) and Firefox (multi-line, LF-delimited, `.dat` suffix), and Apple (multi-line, LF-delimited, named `LocalDictionary`) formats
- Merges multiple dictionary files into one
- Writes merged dictionaries in either Chrome or Firefox/Apple format

### Installation

Provided you already have Poetry installed (see above):

```sh
# Clone the repository
git clone https://github.com/Jachimo/spelling-tools.git
cd spelling-tools

# Install virtual environment and dependencies
poetry install
```

### Usage

```sh
poetry run python -m dictsync.merge INPUT1 INPUT2 ... -o OUTPUT -f FORMAT
```

Note that while the tool will detect input formats, the output format must be specified explicitly.
Breaking the command across multiple lines may make it easier to read:

```sh
poetry run python -m dictsync.merge \
~/Library/Spelling/LocalDictionary \
~/Library/Application Support/Google/Chrome/Default/Custom\ Dictionary.txt \
-o MERGED.dat -f firefox
```

## dictsync automerge

Similar to the manual `merge` but automatically looks for input files in a number of common locations, and then merges them into a single file in the format (Chrome/Firefox) of your choice, at a specified location.

### Features

Automatically searches for personal dictionaries created by Chrome, Firefox, and Safari (on Mac OS only):

* Firefox Linux: `~/.mozilla/firefox/<profile>/persdict.dat`
* Firefox Mac: `~/Library/Application Support/Firefox/Profiles/<profile>/persdict.dat` (where `<profile>` is a randomized string, and one or more user profiles may exist)
* Firefox Windows: `%APPDATA%\Mozilla\Firefox\Profiles\<profile>\persdict.dat` (where `%APPDATA%` is usually `C:\Users\<username>\AppData\Roaming`, only the current user's files will be searched)

* Chrome Linux: `~/.config/google-chrome/Default/Custom Dictionary.txt`
* Chrome Mac: `~/Library/Application Support/Google/Chrome/Default/Custom Dictionary.txt`
* Chrome Windows: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Custom Dictionary.txt`

* System-wide Mac: `~/Library/Spelling/LocalDictionary` (system-wide, used by Safari and others)

Other spelling dictionaries and paths (e.g. for word processors) may be implemented in the future.
Pull requests are always welcome!

### Installation

Same as above.

### Usage

The following will merge all dictionaries that can be found into a single file, `merged.out`, in Firefox (one-word-per-line, no checksum) format:

```sh
poetry run python -m dictsync.automerge -o merged.out -f firefox
```
