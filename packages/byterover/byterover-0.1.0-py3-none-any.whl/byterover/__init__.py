import sys

if sys.version_info[:2] < (3, 11):
    raise RuntimeError("This version of Byterover requires at least Python 3.9")
if sys.version_info[:2] >= (3, 14):
    raise RuntimeError("This version of Byterover does not support Python 3.14+")