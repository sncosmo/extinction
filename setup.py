#!/usr/bin/env python
import importlib.machinery
import os
import re
import sys
import sysconfig

import numpy
from Cython.Build import cythonize
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

here = os.path.dirname(os.path.abspath(__file__))

# Everything except the version and the extension itself lives in
# pyproject.toml. Synchronize the version from code.
fname = os.path.join("src", "extinction", "_extinction.pyx")
with open(fname, encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.*?)\"", f.read())[0]

# Build Cython extension
source_files = [fname, os.path.join("extern", "bs.c")]
depends_files = [os.path.join("extern", "bs.h"), os.path.join("extern", "bsplines.pxi")]
include_dirs = [numpy.get_include(), "extern"]

# MSVC does not understand -std=c11 and only warns about it.
extra_compile_args = [] if sys.platform == "win32" else ["-std=c11"]

# Pin the numpy C API level, so that a future numpy removing an already
# deprecated API is a compile error here rather than a surprise at runtime.
define_macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]

# From Python 3.11, build for the stable ABI (abi3), so that one wheel works
# on Python 3.11 and all later versions with the GIL. The typed memoryviews
# need the buffer protocol, which is in the limited API only from 3.11, so
# Python 3.10 gets its own wheel. The free-threaded builds also get their own
# wheels: their stable ABI (abi3t, from 3.15) needs support in Cython first.
# PyPy and GraalPy do not implement the whole limited API, and a module built
# for it there fails to import, so build for their own ABI.
limited_api = (
    sys.implementation.name == "cpython"
    and sys.version_info >= (3, 11)
    and not sysconfig.get_config_var("Py_GIL_DISABLED")
)
if limited_api:
    define_macros.append(("Py_LIMITED_API", "0x030B0000"))

extensions = [
    Extension(
        "extinction._extinction",
        source_files,
        include_dirs=include_dirs,
        depends=depends_files,
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
        py_limited_api=limited_api,
    )
]


class cythonize_build_ext(build_ext):
    """Generate the C when the extension is built.

    Cythonizing at the top level of setup.py would also run it for each call
    that only reads the metadata or makes the sdist.
    """

    def run(self):
        for ext in self.extensions:
            # `include "extern/bsplines.pxi"` in the .pyx resolves against the
            # project root, not the directory holding the .pyx. Always
            # regenerate the C, which depends on the numpy .pxd of the build
            # environment: uv links build environments from its cache with
            # old mtimes, so Cython's timestamp check can reuse a .c made for
            # another numpy, which then fails to compile.
            (cythonized,) = cythonize(
                [ext], language_level=3, include_path=[here], force=True
            )
            ext.sources = cythonized.sources
        super().run()
        if self.inplace and limited_api:
            # A build for this Python without the limited API leaves a module
            # with a version-specific suffix, which Python imports before the
            # new abi3 one, so remove it.
            for ext in self.extensions:
                stale = os.path.join(here, "src", *ext.name.split("."))
                stale += importlib.machinery.EXTENSION_SUFFIXES[0]
                if os.path.exists(stale):
                    os.remove(stale)


setup(
    version=version,
    ext_modules=extensions,
    cmdclass={"build_ext": cythonize_build_ext},
    # Tag the wheel cp311-abi3.
    options={"bdist_wheel": {"py_limited_api": "cp311"}} if limited_api else {},
)
