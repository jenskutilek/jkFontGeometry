# jkFontGeometry

Font-related geometry tools

## Installation

```bash
$ pip2 install --user -e .
```

There is a demo script for Glyphs.app in the `Scripts/Glyphs` folder.

## Known bugs

* The c extension is not yet compatible with Python 3. Comment the `ext_modules` section in `setup.py` when building in Python 3.
