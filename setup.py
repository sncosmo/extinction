#!/usr/bin/env python
import os
import re
import sys

import numpy
from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension

here = os.path.dirname(os.path.abspath(__file__))

# Everything except the version and the extension itself lives in
# pyproject.toml. Synchronize the version from code.
fname = os.path.join("src", "extinction", "_extinction.pyx")
version = re.findall(r"__version__ = \"(.*?)\"", open(fname).read())[0]

# Build Cython extension
source_files = [fname, os.path.join("extern", "bs.c")]
depends_files = [
    os.path.join("extern", "bs.h"),
    os.path.join("extern", "bsplines.pxi")
]
include_dirs = [numpy.get_include(), "extern"]

# MSVC does not understand -std=c11 and only warns about it.
extra_compile_args = [] if sys.platform == "win32" else ["-std=c11"]

extensions = [
    Extension(
        "extinction._extinction",
        source_files,
        include_dirs=include_dirs,
        depends=depends_files,
        extra_compile_args=extra_compile_args,
    )
]

setup(
    version=version,
    # `include "extern/bsplines.pxi"` in the .pyx resolves against the project
    # root, not the directory holding the .pyx.
    ext_modules=cythonize(extensions, language_level=3, include_path=[here]),
)
