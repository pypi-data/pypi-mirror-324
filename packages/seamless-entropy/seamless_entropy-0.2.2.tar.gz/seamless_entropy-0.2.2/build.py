from __future__ import with_statement

import os
import sys
try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, \
    DistutilsPlatformError

# This script is borrowed and heavily adapted from the simplejson setup.py

IS_PYPY = hasattr(sys, 'pypy_translation_info')

ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)


class BuildFailed(Exception):
    pass


class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()


src_dir = "src/"
c_extension = Extension(
    "entropy_c",
    sources=[
        src_dir + "entropy.c",
        src_dir + "entropy_c_module.c",
    ],
    include_dirs=[src_dir],
)


def run_setup(setup_kwargs):
    new_kwargs = dict(
        setup_kwargs, 
        ext_modules=[c_extension],
        cmdclass=dict(build_ext=ve_build_ext)
    )

    setup(**new_kwargs)


DISABLE_SPEEDUPS = IS_PYPY or os.environ.get('DISABLE_SPEEDUPS') == '1'
CIBUILDWHEEL = os.environ.get('CIBUILDWHEEL') == '1'
REQUIRE_SPEEDUPS = CIBUILDWHEEL or os.environ.get('REQUIRE_SPEEDUPS') == '1'


def attempt_c_build(setup_kwargs):
    try:
        run_setup(setup_kwargs)
        return True
    except BuildFailed:
        return False


def build(setup_kwargs):
    if not DISABLE_SPEEDUPS:
        c_buildable = attempt_c_build(setup_kwargs)
        if c_buildable:
            setup_kwargs.update(
                {
                    "ext_modules": [c_extension],
                }
            )
        elif REQUIRE_SPEEDUPS:
                raise
        else:
            BUILD_EXT_WARNING = ("WARNING: The C extension could not be compiled, "
                                 "speedups are not enabled.")
    else:
        pass
        