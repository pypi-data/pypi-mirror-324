# PyPiUpdateCheck

**PyPiUpdateCheck** is a Python library that allows you to check if a PyPI package has a newer version available compared to the locally installed version. It compares the given version with the latest version on PyPI and returns the result.

## Features
- Supports Semantic Versioning
- Check the latest version of a PyPI package.
- Compare the online version with the locally installed version.
- Returns True/False wether online version is newer or not, and the latest online version.
- If not network aviable or other error, None will be returned with an error message.

## Installation

To install **PyPiUpdateCheck**, use `pip`:

```bash
pip install PyPiUpdateCheck
```

## Usage
```python
from PyPiUpdateCheck import PyPiUpdateCheck

ppl = PyPiUpdateCheck()
ppl.check_for_update("pypiPackagename", "x.y.z")
```
