from __future__ import with_statement

import os
import sys

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, \
    DistutilsPlatformError


# This script is borrowed and heavily adapted from the simplejson setup.py
# https://github.com/simplejson/simplejson/blob/master/setup.py

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
        # This might be problematic. When we do this build, we end up with 
        # library files at eg build\lib.win-amd64-cpython-313\seamless_entropy
        # When we fallback to doing the Python only build, poetry will retrieve 
        # these built files, instead of the newly built output of the Python only
        # build at eg build\lib
        # The former *should* be the same as the latter but since the former are
        # the result of an abortive build, who knows what they will be?
        run_setup(setup_kwargs)
        return True
    except BuildFailed:
        return False


def build(setup_kwargs):
    print("Calling the build script")

    if DISABLE_SPEEDUPS:
        print("Building without C extension compilation")
        setup_kwargs.update(
            {
                'has_ext_modules': lambda : False
            }
        )
    else:
        c_buildable = attempt_c_build(setup_kwargs)
        if c_buildable:
            print("Building with C extensions compiled.")
            setup_kwargs.update(
                {
                    "ext_modules": [c_extension],
                }
            )
        elif REQUIRE_SPEEDUPS:
                raise
        else:
            print("WARNING: The C extension could not be compiled, speedups are not enabled.")
            setup_kwargs.update(
                {
                    # This override means that setuptools does the right thing
                    # (builds with a name tagged 'any' platform). However poetry
                    # does the wrong thing and gives the packaged wheel a platform-
                    # specific name. This is a poetry limitation:
                    # https://github.com/python-poetry/poetry/issues/3594
                    # We keep the correct setuptools behavior here, so that it's 
                    # easier to fix the whole thing if there is ever a poetry
                    # fix or workaround.
                    'has_ext_modules': lambda : False,
                }
            )
