# spelling-tools

> Tools for working with spell-check dictionaries.

The intent is for this repository to eventually contain multiple tools (as a monorepo) related to managing personal word lists for spell checkers.

## dictsync merge

Synchronize (by merging) personal dictionaries for Firefox, Chrome, and Apple's system-wide spell checker (used by Safari on Mac).

Dictionaries can be found in several places depending on browser and operating system.

Firefox custom word lists are typically named `persdict.dat` and found in one of the follow locations:

* Firefox Linux: `~/.mozilla/firefox/<profile>/persdict.dat`
* Firefox Mac: `~/Library/Application Support/Firefox/Profiles/<profile>/persdict.dat`
* Firefox Windows: `%APPDATA%\Mozilla\Firefox\Profiles\<profile>\persdict.dat` (where `%APPDATA%` is usually `C:\Users\<username>\AppData\Roaming`)

Chrome custom word lists are generally named `Custom Dictionary.txt`:

* Chrome Linux: `~/.config/google-chrome/Default/Custom Dictionary.txt`
* Chrome Mac: `~/Library/Application Support/Google/Chrome/Default/Custom Dictionary.txt`
* Chrome Windows: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Custom Dictionary.txt`

Apple's Mac OS system-wide spell checker, used by Safari and other OS X applications, uses a dictionary file in a format very similar to Firefox, but stored separately:

* System-wide Mac: `~/Library/Spelling/LocalDictionary`

### Features

- Detects and reads Chrome (single-line, comma-delimited, `.txt` suffix) and Firefox (multi-line, LF-delimited, `.dat` suffix), and Apple (multi-line, LF-delimited, named `LocalDictionary`) formats
- Merges multiple dictionary files into one
- Writes merged dictionaries in either Chrome or Firefox/Apple format

### Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

It is recommended to install Poetry via the official installer script:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Then:

```sh
# Clone the repository
git clone https://github.com/yourusername/spelling-tools.git
cd spelling-tools

# Install virtual environment and dependencies
poetry install
```

### Usage

```sh
poetry run python -m dictsync.merge INPUT1 INPUT2 ... -o OUTPUT -f FORMAT
```

Note that while the tool attempts to detect input formats, the output format must be specified explicitly.
Breaking the command across multiple lines may make it easier to read:

```sh
poetry run python -m dictsync.merge \
~/Library/Spelling/LocalDictionary \
~/Library/Application Support/Google/Chrome/Default/Custom\ Dictionary.txt \
-o MERGED.dat -f firefox
```

