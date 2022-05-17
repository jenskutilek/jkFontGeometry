# jkFontGeometry

Font-related geometry tools

## Installation

```bash
$ pip install --user .
```

There is a demo script for Glyphs.app in the `Scripts/Glyphs` folder.

## Type-Checking and Compilation

To run mypy:

```bash
MYPYPATH=stubs/ mypy Lib/jkFontGeometry
```

To build a wheel with binary code compiled by mypy:

```bash
MYPYPATH=stubs/ mypyc Lib/jkFontGeometry
```