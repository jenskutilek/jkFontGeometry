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

To build a wheel with binary code compiled by mypyc:

```bash
MYPYPATH=stubs/ python3 setup.py bdist_wheel
```

or compile in place:

```bash
MYPYPATH=stubs/ python3 setup.py build_ext --inplace
```
