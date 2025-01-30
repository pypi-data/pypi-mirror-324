# Installation

```bash
pip install bitmask26
```

# Usage

`Bitmask26(word1) <= Bitmask(word2)` return `True` if all letters of `word1` is in `word2`.

```py
from bitmask26 import Bitmask26
Bitmask26('flee') <= Bitmask26('eefl') # True
Bitmask26('elf') <= Bitmask26('eefl')  # True
Bitmask26('left') <= Bitmask26('eefl') # False
Bitmask26('cap') <= Bitmask26('eefl')  # False
Bitmask26('fell') <= Bitmask26('eefl') # True
```

# Building
[py_bitmask26.py](https://github.com/adwaithhs/bitmask26/blob/master/py_bitmask26.py) has the same thing implemented in python.

```bash
pip install setuptools wheel twine pybind11
rm -rf build dist *.egg-info
python setup.py .
```