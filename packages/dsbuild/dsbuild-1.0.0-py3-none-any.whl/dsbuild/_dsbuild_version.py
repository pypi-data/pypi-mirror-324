"""
dsbuild version information.

This content is typically in the __init__.py file of the package but for this package
we use that information internally e.g. in __main__.py. This creates some confusion with
some of the tools used in our team and there is a risk of cirtcular imports since the
content of this file is also used internally by the package. So, we have moved the
version information to this separate module.
"""

import os
import warnings

try:
    with open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), '.version'), 'rt'
    ) as fid:
        __version__ = fid.readline().strip()
except FileNotFoundError:
    warnings.warn('.version file could not be found', stacklevel=1)
    __version__ = '0.0.0+dev'
