

import functools
import inspect
import logging
import os
import string
import sys
import tempfile
import unicodedata

s = lambda x: "" if x == 1 else "s"
s.__doc__ = "Returns 's' for quantities other than 1"


if __name__ == "__main__":
    import doctest
    doctest.testmod()